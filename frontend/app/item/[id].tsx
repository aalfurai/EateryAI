import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { MenuItem } from "../../types/MenuItem";

// replace with api call to GET /menu/{restaurant}/{item_id}
const PLACEHOLDER_ITEM: MenuItem = {
  item_id: "1",
  menu_item_name: "Spicy Deluxe Sandwich",
  category: "Entree",
  price: 5.75,
  golden_ratio: 0.82,
  ai_description:
    "A perfectly seasoned spicy chicken breast nestled between a toasted brioche bun with crisp pickles and creamy coleslaw. High protein with a moderate calorie count makes this a solid choice for your macros.",
  restaurant_name: "Chick-Fil-A",
  calories: 450,
  protein: 36,
  total_fat: 17,
  total_carbohydrates: 41,
  dietary_fiber: 2,
  sugars: 8,
  sodium: 1220,
  cholesterol: 90,
  potassium: 430,
  serving_size: "231g",
  image_url: "https://fastfoodnutrition.org/item-photos/400x270/5038.jpg",
};

export default function ItemDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const item = PLACEHOLDER_ITEM;

  return (
    <View style={styles.container}>
      {/* Image area */}
      <View style={styles.imageArea}>
        <TouchableOpacity
          style={[styles.closeButton, { top: insets.top + 12 }]}
          onPress={() => router.back()}
        >
          <Ionicons name="close" size={18} color="white" />
        </TouchableOpacity>
        <Text style={styles.imagePlaceholderText}>picture</Text>
      </View>

      {/* Content sheet */}
      <ScrollView
        style={styles.sheet}
        contentContainerStyle={{ paddingBottom: insets.bottom + 32 }}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.itemName}>{item.menu_item_name}</Text>
        <Text style={styles.restaurantLabel}>{item.restaurant_name}</Text>
        <Text style={styles.quickStats}>
          ${item.price.toFixed(2)}  ·  {item.calories} cal  ·  {item.protein}g protein
        </Text>

        <Text style={styles.sectionTitle}>Meal Information</Text>
        <View style={styles.mealInfoRow}>
          <View style={styles.tag}>
            <Text style={styles.tagText}>{item.category}</Text>
          </View>
          <View style={styles.tag}>
            <Text style={styles.tagText}>{item.serving_size}</Text>
          </View>
          <TouchableOpacity
            style={styles.eatAIButton}
            onPress={() => router.push(`/eatai/${encodeURIComponent(item.restaurant_name)}`)}
            activeOpacity={0.8}
          >
            <Text style={styles.eatAIText}>eatAI</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.sectionTitle}>Meal Description</Text>
        <Text style={styles.description}>{item.ai_description}</Text>

        <Text style={styles.sectionTitle}>Nutrition Information</Text>
        <View style={styles.nutritionRow}>
          <NutritionCell label="Carbs" value={`${item.total_carbohydrates}g`} />
          <View style={styles.divider} />
          <NutritionCell label="Fats" value={`${item.total_fat}g`} />
          <View style={styles.divider} />
          <NutritionCell label="Sugar" value={`${item.sugars}g`} />
          <View style={styles.divider} />
          <NutritionCell label="Sodium" value={`${item.sodium}mg`} />
        </View>
      </ScrollView>
    </View>
  );
}

function NutritionCell({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.nutritionCell}>
      <Text style={styles.nutritionValue}>{value}</Text>
      <Text style={styles.nutritionLabel}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#010000",
  },
  imageArea: {
    height: 240,
    backgroundColor: "#1a1a1a",
    justifyContent: "center",
    alignItems: "center",
  },
  closeButton: {
    position: "absolute",
    left: 16,
    width: 34,
    height: 34,
    borderRadius: 17,
    backgroundColor: "rgba(0,0,0,0.5)",
    justifyContent: "center",
    alignItems: "center",
  },
  imagePlaceholderText: {
    color: "#555",
    fontSize: 14,
  },
  sheet: {
    flex: 1,
    backgroundColor: "#010000",
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  itemName: {
    color: "white",
    fontSize: 26,
    fontWeight: "700",
    marginBottom: 4,
  },
  restaurantLabel: {
    color: "#898989",
    fontSize: 14,
    marginBottom: 6,
  },
  quickStats: {
    color: "#ccc",
    fontSize: 14,
    marginBottom: 24,
  },
  sectionTitle: {
    color: "white",
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 12,
  },
  mealInfoRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    marginBottom: 24,
  },
  tag: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: "#1e1e1e",
    borderWidth: 1,
    borderColor: "#333",
  },
  tagText: {
    color: "#aaa",
    fontSize: 13,
  },
  eatAIButton: {
    paddingHorizontal: 18,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "white",
  },
  eatAIText: {
    color: "white",
    fontSize: 13,
    fontWeight: "600",
  },
  description: {
    color: "#aaa",
    fontSize: 14,
    lineHeight: 21,
    marginBottom: 24,
  },
  nutritionRow: {
    flexDirection: "row",
    backgroundColor: "#111",
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "#1e1e1e",
    overflow: "hidden",
  },
  nutritionCell: {
    flex: 1,
    alignItems: "center",
    paddingVertical: 16,
  },
  nutritionValue: {
    color: "white",
    fontSize: 16,
    fontWeight: "700",
  },
  nutritionLabel: {
    color: "#898989",
    fontSize: 11,
    marginTop: 4,
  },
  divider: {
    width: 1,
    backgroundColor: "#1e1e1e",
    marginVertical: 12,
  },
});
