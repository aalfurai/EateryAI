import { View, ScrollView, StyleSheet, Text, ActivityIndicator, TouchableOpacity} from "react-native";
import { useState } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import { useRestaurants } from "../../hooks/useRestaurants";
import RestaurantCard from "../../components/RestaurantCard";
import AppHeader from "../../components/AppHeader";
import FilterModal from "../../components/TargetModal";

export default function Home() {
  const { restaurants, loading, error } = useRestaurants();

  const insets = useSafeAreaInsets();
  const router = useRouter();
  const [filtersVisible, setFiltersVisible] = useState(false);
  const [showAll, setShowAll] = useState(false);

  const defaultRestaurants = [
    "Chick-fil-A",
    "Taco Bell",
    "Subway",
    "Chipotle",
    "McDonald's",
    "Arby's",
  ];
  const featuredRestaurants = restaurants.filter((restaurant) =>
    defaultRestaurants.includes(restaurant.restaurant_name)
  );
  const displayedRestaurants = showAll
    ? restaurants
    : featuredRestaurants;
  
  const hues = [0, 130, 220, 30, 300]; 
  
  if (loading) return <ActivityIndicator />;
  if (error) return <Text style={{ color: "white", }}>Failed to load restaurants.</Text>;
  
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
          {displayedRestaurants.map((restaurant, i) => (
            <RestaurantCard
              key={restaurant.restaurant_id}
              restaurant={restaurant}
              hue={hues[i % hues.length]}
              onPress={() =>
                router.push({
                  pathname: "/restaurant/[restaurant]",
                  params: { restaurant: restaurant.restaurant_name,},
              })}
            />
          ))}
          {!showAll && (
          <TouchableOpacity
            style={styles.loadMoreButton}
            onPress={() => setShowAll(true)}
          >
            <Text style={styles.loadMoreText}>View All Restaurants</Text>
          </TouchableOpacity>
        )}
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
  loadMoreButton: {
    backgroundColor: "#303030",
    borderColor: "#7C7C7C",
    borderWidth: 1,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    width: 180,
    height: 40,
    marginTop: 16,
    marginLeft: 16,
  },
  loadMoreText: {
    color: "white",
    fontSize: 14,
    fontWeight: "400",
  },
});