import { View, Text, StyleSheet, ScrollView } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import { MenuItem } from "../../types/MenuItem";
import AppHeader from "../../components/AppHeader";
import DiscoverItemCard from "../../components/DiscoverItemCard";

const mockItems: MenuItem[] = [
  {
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
  },
  {
    item_id: "2",
    menu_item_name: "Chicken Sandwich",
    category: "Entree",
    price: 6.99,
    golden_ratio: 0.82,
    ai_description: "",
    restaurant_name: "Chick-fil-A",
    calories: 450,
    protein: 28,
    total_fat: 20,
    total_carbohydrates: 40,
    dietary_fiber: 2,
    sugars: 5,
    sodium: 900,
    cholesterol: 60,
    potassium: 300,
    serving_size: "1 sandwich",
    image_url: "https://fastfoodnutrition.org/item-photos/400x226/3415_s.jpg",
  },
  {
    item_id: "3",
    menu_item_name: "Crunchwrap Supreme",
    category: "Entree",
    price: 6.79,
    golden_ratio: 0.82,
    ai_description: "",
    restaurant_name: "Taco Bell",
    calories: 530,
    protein: 16,
    total_fat: 21,
    total_carbohydrates: 71,
    dietary_fiber: 6,
    sugars: 6,
    sodium: 1200,
    cholesterol: 25,
    potassium: 300,
    serving_size: "1 crunchwrap",
    image_url: "https://fastfoodnutrition.org/item-photos/400x406/2318.jpg",
  },
];

export default function Discover() {
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const hues = [0, 130, 220, 30, 300]; 

  return (
    <View style={styles.container}>
      <AppHeader />
      <Text style={styles.title}>For You</Text>
      <ScrollView 
        contentContainerStyle={{
          paddingBottom: insets.bottom,
        }}
      >
        {mockItems.map((item, i) => (
        <DiscoverItemCard 
          key={item.item_id}
          item={item}
          hue={hues[i % hues.length]}
          onPress={() => router.push(`/item/${item.item_id}`)}
        />
      ))}
    </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#010000",
  },
  title: {
    fontSize: 22,
    fontWeight: "700",
    textAlign: "center",
    color: "white",
    marginHorizontal: 16,
    marginTop: 8,
    marginBottom: 8,
  },
})