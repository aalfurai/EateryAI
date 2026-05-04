import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import ItemCard from "../../components/ItemCard";

// replace with api call to GET /menu/{restaurant}
const PLACEHOLDER_ITEMS = [
  { item_id: "1", name: "Spicy Deluxe Sandwich", category: "Entree", price: 5.75, calories: 450, protein: 36 },
  { item_id: "2", name: "Grilled Chicken Sandwich", category: "Entree", price: 5.29, calories: 320, protein: 32 },
  { item_id: "3", name: "Chicken Nuggets (8ct)", category: "Entree", price: 4.45, calories: 260, protein: 26 },
  { item_id: "4", name: "Waffle Potato Fries", category: "Side", price: 2.89, calories: 420, protein: 5 },
  { item_id: "5", name: "Mac & Cheese", category: "Side", price: 3.29, calories: 440, protein: 12 },
  { item_id: "6", name: "Side Salad", category: "Side", price: 2.69, calories: 80, protein: 5 },
  { item_id: "7", name: "Lemonade", category: "Drink", price: 2.49, calories: 170, protein: 0 },
  { item_id: "8", name: "Sweet Tea", category: "Drink", price: 2.19, calories: 120, protein: 0 },
  { item_id: "9", name: "Chocolate Milkshake", category: "Drink", price: 3.89, calories: 580, protein: 13 },
];

const CATEGORIES = ["Entree", "Side", "Drink"];

export default function RestaurantMenu() {
  const { name } = useLocalSearchParams<{ name: string }>();
  const router = useRouter();
  const insets = useSafeAreaInsets();

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
          const items = PLACEHOLDER_ITEMS.filter((i) => i.category === category);
          return (
            <View key={category}>
              <Text style={styles.categoryHeader}>{category}</Text>
              {items.map((item) => (
                <ItemCard
                  key={item.item_id}
                  name={item.name}
                  category={item.category}
                  price={item.price}
                  calories={item.calories}
                  protein={item.protein}
                  onPress={() => router.push(`/item/${item.item_id}`)}
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
