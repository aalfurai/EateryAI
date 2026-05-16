import { View, ScrollView, StyleSheet, Text, ActivityIndicator, TouchableOpacity} from "react-native";
import { useState } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import { useRestaurants } from "../../hooks/useRestaurants";
import { useRestaurantSearch } from "../../hooks/useRestaurantSearch";
import RestaurantCard from "../../components/RestaurantCard";
import AppHeader from "../../components/AppHeader";
import TargetModal from "../../components/TargetModal";
import SearchModal from "../../components/SearchModal";

export default function Home() {
  const insets = useSafeAreaInsets();
  const router = useRouter();

  const [filtersVisible, setFiltersVisible] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const [searchVisible, setSearchVisible] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  const { restaurants, loading, error } = useRestaurants();
  const {
    results: searchResults,
    loading: searchLoading,
    error: searchError,
  } = useRestaurantSearch(searchQuery);

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

  const isSearching = searchQuery.trim().length > 0;
  const displayedRestaurants = isSearching
    ? searchResults
    : showAll
      ? restaurants
      : featuredRestaurants;
  
  const hues = [0, 130, 220, 30, 300]; 
  
  if (loading) return <ActivityIndicator />;
  if (error) return <Text style={styles.emptyText}>Failed to load restaurants.</Text>;
  
  return (
    <View style={styles.container}>
      <AppHeader 
        onPressFilters={() => setFiltersVisible(true)}
        onPressSearch={() => setSearchVisible(true)}
      />
      <TargetModal
        visible={filtersVisible}
        onClose={() => setFiltersVisible(false)}
      />
      <SearchModal
        visible={searchVisible}
        onClose={() => setSearchVisible(false)}
        value={searchInput}
        onChange={setSearchInput}
        onSubmit={() => {
          setSearchQuery(searchInput);
          setSearchVisible(false);
        }}
      />

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
          {searchLoading && (
            <ActivityIndicator style={{ marginTop: 20 }} />
          )}
          {isSearching && displayedRestaurants.length === 0 && !searchLoading && (
            <Text style={styles.emptyText}>No restaurants found.</Text>
          )}
          {isSearching ? (
            <View style={styles.centerButtonContainer}>
              <TouchableOpacity
                style={styles.button}
                onPress={() => {
                  setSearchInput("");
                  setSearchQuery("");
                  setShowAll(false);
                }}
              >
                <Text style={styles.buttonText}>Back to Featured</Text>
              </TouchableOpacity>
            </View>

          ) : !showAll ? (

            <View style={styles.centerButtonContainer}>
              <TouchableOpacity
                style={styles.button}
                onPress={() => setShowAll(true)}
              >
                <Text style={styles.buttonText}>View All Restaurants</Text>
              </TouchableOpacity>
            </View>

          ) : (

            <View style={styles.centerButtonContainer}>
              <TouchableOpacity
                onPress={() => {
                setSearchInput("");
                setSearchQuery("");
                setShowAll(false);
              }}
              >
                <Text style={styles.buttonText}>Back to Featured</Text>
              </TouchableOpacity>
            </View>

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
  centerButtonContainer: { 
    alignItems: "center", 
    marginTop: 16,
  },
  button: {
    borderColor: "#7C7C7C",
    borderWidth: 1,
    borderRadius: 25,
    alignItems: "center",
    justifyContent: "center",
    width: 200,
    height: 50,
  },
  buttonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "500",
  },
  emptyText: {
    color: "white",
    fontSize: 16,
    textAlign: "center",
  },
});