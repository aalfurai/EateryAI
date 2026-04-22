import { View, ScrollView } from "react-native";
import RestaurantCard from "../../components/RestaurantCard";

export default function Home() {
  // replace this with api call later
  const restaurants = [
    "Chick-Fil-A",
    "Taco Bell",
    "Subway",
    "Chipotle",
    "McDonald's",
  ];

  return (
    <ScrollView>
      <View>
        {restaurants.map((name) => (
          <RestaurantCard
            key={name}
            name={name}
            onPress={() => {
              console.log("Pressed", name);
            }}
          />
        ))}
      </View>
    </ScrollView>
  );
}