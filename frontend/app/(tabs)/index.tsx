import { View, ScrollView, StyleSheet, Text, } from "react-native";
import { useState } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import RestaurantCard from "../../components/RestaurantCard";
import AppHeader from "../../components/AppHeader";
import FilterModal from "../../components/FilterModal";

export default function Home() {
  const insets = useSafeAreaInsets();
  const router = useRouter();

  // replace this with api call later
  const restaurants = [
    "Chick-Fil-A",
    "Taco Bell",
    "Subway",
    "Chipotle",
    "McDonald's",
    "Arby's",
  ];

  const [filtersVisible, setFiltersVisible] = useState(false);

  const hues = [0, 130, 220, 30, 300]; 

  return (
    <View style={styles.container}>
      <AppHeader onPressFilters={() => setFiltersVisible(true)}/>
      <FilterModal
        visible={filtersVisible}
        onClose={() => setFiltersVisible(false)}/>

      <ScrollView
        contentContainerStyle={{
          paddingBottom: insets.bottom,
        }}
      >
        <Text style={styles.title}>Build Meal By Restaurant</Text>

        <View>
          {restaurants.map((name, i) => (
            <RestaurantCard
              key={name}
              name={name}
              hue={hues[i % hues.length]}
              onPress={() => router.push(`/restaurant/${name}`)}
            />
          ))}
        </View>
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
    color: "white",
    marginHorizontal: 16,
    marginTop: 8,
    marginBottom: 8,
  },
});