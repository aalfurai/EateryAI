import { View, Text, ScrollView, StyleSheet, TouchableOpacity, ActivityIndicator } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import ItemCard from "../../components/ItemCard";
import { useMenu } from "../../hooks/useMenu";


const CATEGORIES = ["Entree", "Side", "Drink", "Add-On", "Dessert"];

export default function RestaurantMenu() {
  const { name } = useLocalSearchParams<{ name: string }>();
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const { items, loading, error } = useMenu(name);

  if (loading) return <ActivityIndicator />;
  if (error) return <Text style={{ color: "white", }}>Failed to load menu.</Text>;

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="chevron-back" size={26} color="white" />
        </TouchableOpacity>
        <Text style={styles.restaurantName}>{name}</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: insets.bottom + 24 }}
      >
        <TouchableOpacity
          style={styles.eatAIBanner}
          onPress={() => router.push(`/eatai/${encodeURIComponent(name)}`)}
          activeOpacity={0.8}
        >
          <View>
            <Text style={styles.eatAIBannerTitle}>Build a Meal</Text>
            <Text style={styles.eatAIBannerSub}>Let eatAI pick the best combo for you</Text>
          </View>
          <Ionicons name="chevron-forward" size={20} color="white" />
        </TouchableOpacity>

        {CATEGORIES.map((category) => {
          const restaurant_items = items.filter((i) => i.category === category);
          return (
            <View key={category}>
              <Text style={styles.categoryHeader}>{category}</Text>
              {restaurant_items.map((item) => (
                <ItemCard
                  key={item.item_id}
                  name={item.menu_item_name}
                  category={item.category}
                  price={item.price}
                  calories={item.calories}
                  protein={item.protein}
                  onPress={() => router.push(`/item/${name}/${item.index}`)}
                />
              ))}
            </View>
          );
        })}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#010000",
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  backButton: {
    width: 40,
  },
  restaurantName: {
    color: "white",
    fontSize: 17,
    fontWeight: "700",
  },
  eatAIBanner: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginHorizontal: 16,
    marginTop: 8,
    marginBottom: 4,
    padding: 18,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "white",
  },
  eatAIBannerTitle: {
    color: "white",
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 2,
  },
  eatAIBannerSub: {
    color: "#898989",
    fontSize: 13,
  },
  categoryHeader: {
    color: "#898989",
    fontSize: 12,
    fontWeight: "600",
    textTransform: "uppercase",
    letterSpacing: 0.8,
    marginHorizontal: 20,
    marginTop: 24,
    marginBottom: 4,
  },
});
