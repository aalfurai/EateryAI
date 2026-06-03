import { View, Text, StyleSheet, ScrollView, ActivityIndicator, TouchableOpacity } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useFocusEffect } from "expo-router";
import { useCallback, useRef, useState } from "react";
import { useUser } from "../../context/UserContext";
import ProfileHeader from "../../components/ProfileHeader";
import { getSavedMeals, unsaveMeal } from "../../api/meals";
import { Meal } from "../../types/Meal";
import { Ionicons } from "@expo/vector-icons";

const GRACE_MS = 3000;

const CATEGORY_COLORS: Record<string, string> = {
  Entree:   "#39ff14",
  Side:     "#ffd600",
  Drink:    "#ff2975",
  "Add-On": "#00eaff",
  Dessert:  "#d500f9",
};

type CardProps = {
  meal: Meal;
  index: number;
  isPending: boolean;
  onToggle: (meal: Meal, index: number) => void;
};

function SavedMealCard({ meal, index, isPending, onToggle }: CardProps) {
  return (
    <View style={[styles.card, isPending && styles.cardPending]}>
      <View style={styles.cardHeader}>
        <Text style={styles.cardRestaurant}>{meal.restaurant_name || "Unknown Restaurant"}</Text>
        <TouchableOpacity onPress={() => onToggle(meal, index)} activeOpacity={0.7} hitSlop={12}>
          <Ionicons
            name={isPending ? "heart-outline" : "heart"}
            size={22}
            color={isPending ? "#555" : "#ff2975"}
          />
        </TouchableOpacity>
      </View>

      {isPending && (
        <Text style={styles.undoHint}>Tap heart again to undo</Text>
      )}

      <View style={styles.itemList}>
        {(meal.items ?? []).map((item, idx) => (
          <View key={`${item.item_id}-${idx}`} style={styles.itemRow}>
            <View style={[styles.dot, { backgroundColor: CATEGORY_COLORS[item.category] ?? "#555" }]} />
            <Text style={styles.itemName} numberOfLines={1}>{item.menu_item_name}</Text>
            <Text style={styles.itemCal}>{item.calories} cal</Text>
          </View>
        ))}
      </View>

      <View style={styles.divider} />

      <View style={styles.totals}>
        <View style={styles.totalItem}>
          <Text style={styles.totalValue}>${meal.total_price?.toFixed(2)}</Text>
          <Text style={styles.totalLabel}>price</Text>
        </View>
        <View style={styles.totalDivider} />
        <View style={styles.totalItem}>
          <Text style={styles.totalValue}>{meal.total_cal}</Text>
          <Text style={styles.totalLabel}>cal</Text>
        </View>
        <View style={styles.totalDivider} />
        <View style={styles.totalItem}>
          <Text style={styles.totalValue}>{meal.total_protein}g</Text>
          <Text style={styles.totalLabel}>protein</Text>
        </View>
        <View style={styles.totalDivider} />
        <View style={styles.totalItem}>
          <Text style={styles.totalValue}>{meal.total_carbohydrates}g</Text>
          <Text style={styles.totalLabel}>carbs</Text>
        </View>
      </View>
    </View>
  );
}

export default function Profile() {
  const { user, token } = useUser();
  const [savedMeals, setSavedMeals] = useState<Meal[]>([]);
  const [loading, setLoading]       = useState(false);
  // Keys of meals pending removal (item_ids joined)
  const [pendingKeys, setPendingKeys] = useState<Set<string>>(new Set());
  // Refs store the actual timers and the array index at the time of scheduling
  const timers = useRef<Map<string, ReturnType<typeof setTimeout>>>(new Map());
  const indexAtSchedule = useRef<Map<string, number>>(new Map());

  const getMealKey = (meal: Meal) => (meal.item_ids ?? []).join(",");

  useFocusEffect(
    useCallback(() => {
      if (!token) return;
      setLoading(true);
      getSavedMeals(token)
        .then((data) => setSavedMeals(data.saved_meals ?? []))
        .catch(() => setSavedMeals([]))
        .finally(() => setLoading(false));
    }, [token])
  );

  const handleToggle = (meal: Meal, arrayIndex: number) => {
    const key = getMealKey(meal);

    if (pendingKeys.has(key)) {
      // Cancel the pending delete — restore heart to red
      clearTimeout(timers.current.get(key));
      timers.current.delete(key);
      indexAtSchedule.current.delete(key);
      setPendingKeys((prev) => { const next = new Set(prev); next.delete(key); return next; });
    } else {
      // Start grace period — heart goes grey
      setPendingKeys((prev) => new Set(prev).add(key));
      indexAtSchedule.current.set(key, arrayIndex);

      const timer = setTimeout(async () => {
        const backendIndex = indexAtSchedule.current.get(key) ?? arrayIndex;
        try {
          await unsaveMeal(backendIndex, token!);
          setSavedMeals((prev) => prev.filter((_, i) => i !== backendIndex));
        } catch {}
        timers.current.delete(key);
        indexAtSchedule.current.delete(key);
        setPendingKeys((prev) => { const next = new Set(prev); next.delete(key); return next; });
      }, GRACE_MS);

      timers.current.set(key, timer);
    }
  };

  return (
    <LinearGradient colors={["#010000", "#19192C"]} style={styles.container}>
      <ProfileHeader username={user?.name} />
      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>
        {loading ? (
          <ActivityIndicator color="white" style={{ marginTop: 40 }} />
        ) : savedMeals.length === 0 ? (
          <View style={styles.empty}>
            <Ionicons name="heart-outline" size={36} color="#a6a6a6" />
            <Text style={styles.emptyText}>No saved meals yet</Text>
            <Text style={styles.emptySubtext}>Heart a meal on the EatAI page to save it here</Text>
          </View>
        ) : (
          savedMeals.map((meal, i) => (
            <SavedMealCard
              key={`${getMealKey(meal)}-${i}`}
              meal={meal}
              index={i}
              isPending={pendingKeys.has(getMealKey(meal))}
              onToggle={handleToggle}
            />
          ))
        )}
      </ScrollView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  scroll: { paddingBottom: 40 },

  empty: {
    alignItems: "center",
    marginTop: 60,
    gap: 10,
  },
  emptyText: {
    color: "#cdcdcd",
    fontSize: 16,
    fontWeight: "600",
  },
  emptySubtext: {
    color: "#a6a6a6",
    fontSize: 13,
    textAlign: "center",
    paddingHorizontal: 40,
  },

  card: {
    backgroundColor: "#0d1117",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#1e2530",
    marginHorizontal: 16,
    marginVertical: 8,
    padding: 18,
  },
  cardPending: {
    opacity: 0.5,
  },
  cardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 14,
  },
  cardRestaurant: {
    color: "white",
    fontSize: 15,
    fontWeight: "700",
    flex: 1,
  },
  undoHint: {
    color: "#555",
    fontSize: 12,
    marginBottom: 10,
    marginTop: -6,
  },
  itemList: {
    gap: 10,
    marginBottom: 14,
  },
  itemRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    flexShrink: 0,
  },
  itemName: {
    flex: 1,
    color: "white",
    fontSize: 14,
    fontWeight: "500",
  },
  itemCal: {
    color: "#555",
    fontSize: 13,
  },
  divider: {
    height: 1,
    backgroundColor: "#1e2530",
    marginBottom: 14,
  },
  totals: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  totalItem: {
    flex: 1,
    alignItems: "center",
  },
  totalValue: {
    color: "white",
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 2,
  },
  totalLabel: {
    color: "#555",
    fontSize: 11,
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
  totalDivider: {
    width: 1,
    height: 28,
    backgroundColor: "#1e2530",
  },
});
