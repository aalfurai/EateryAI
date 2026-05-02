import { View, Text, StyleSheet, ScrollView } from "react-native";
import { MenuItem } from "../../types/menuItem";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import AppHeader from "../../components/AppHeader";
import ItemCard from "../../components/ItemCard";

// placeholder item
const mockItems: MenuItem[] = [
  {
    index: 0,
    item_id: 1,
    menu_item_name: "Chicken Sandwich",
    category: "Entree",
    price: 6.99,
    calories: 450,
    protein: 28,
    dietary_fiber: 2,
    sugars: 5,
    sodium: 900,
    cholesterol: 60,
    total_carbohydrates: 40,
    potassium: 300,
    total_fat: 20,
    serving_size: "1 sandwich",
    image_url: "https://fastfoodnutrition.org/item-photos/400x226/3415_s.jpg",
    restaurant_name: "Chick-fil-A",
  },
  {
    index: 2,
    item_id: 1,
    menu_item_name: "Crunchwrap Supreme",
    category: "Entree",
    price: 6.79,
    calories: 530,
    protein: 16,
    dietary_fiber: 6,
    sugars: 6,
    sodium: 1200,
    cholesterol: 25,
    total_carbohydrates: 71,
    potassium: 300,
    total_fat: 21,
    serving_size: "1 crunchwrap",
    image_url: "https://fastfoodnutrition.org/item-photos/400x406/2318.jpg",
    restaurant_name: "Taco Bell",
  },
];

export default function Discover() {
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
        <ItemCard 
          key={item.item_id} 
          item={item} 
          hue={hues[i % hues.length]} />
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