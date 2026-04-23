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

  const hues = [0, 130, 220, 30, 300]; 

  return (
    <ScrollView>
      <View>
        {restaurants.map((name, i) => (
          <RestaurantCard
            key={name}
            name={name}
            hue={hues[i % hues.length]}
          />
        ))}
      </View>
    </ScrollView>
  );
}