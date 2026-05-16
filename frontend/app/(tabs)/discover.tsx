import { View, Text, StyleSheet, ScrollView, ActivityIndicator, TouchableOpacity } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useState, useMemo } from "react";
import { useRouter, } from "expo-router";
import { useUser } from "../../context/UserContext";
import { getRangesForDiscover } from "../../types/user";
import { useItemSearch } from "../../hooks/useItemSearch";
import AppHeader from "../../components/AppHeader";
import DiscoverItemCard from "../../components/DiscoverItemCard";
import TargetModal from "../../components/TargetModal";
import SearchModal from "../../components/SearchModal";

export default function Discover() {
  const { user } = useUser();
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const [filtersVisible, setFiltersVisible] = useState(false);
  const [searchVisible, setSearchVisible] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  /* Load items based on user constraints */
  const ranges = useMemo(() => {
    return user ? getRangesForDiscover(user) : null;
  }, [user]);
  const recommendationParams = useMemo(() => {
    if (!ranges) return null;

    return {
      price_min: ranges.minPrice,
      price_max: ranges.maxPrice,

      calories_min: ranges.minCalories,
      calories_max: ranges.maxCalories,

      protein_min: ranges.minProtein,
      protein_max: ranges.maxProtein,
    };
  }, [ranges]);

  const {
    results: recommendedItems,
    loading: recommendationsLoading,
    error: recommendationsError,
  } = useItemSearch(recommendationParams);

  /* Search items based on user input */
  const searchParams = useMemo(() => {
    if (!searchQuery.trim()) return null;

    return {
      q: searchQuery,
    };
  }, [searchQuery]);
  const {
    results: searchResults,
    loading: searchLoading,
    error: searchError,
  } = useItemSearch(searchParams);

  /* Display first 20 items or search results */
  const isSearching = searchQuery.trim().length > 0;

  const displayedItems = isSearching
    ? searchResults.slice(0,30)
    : recommendedItems.slice(0, 20);

  const hues = [0, 130, 220, 30, 300]; 

  if (recommendationsError) return <Text style={styles.emptyText}>Failed to load items.</Text>;

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
        
      <Text style={styles.title}>For You</Text>
      <ScrollView 
        contentContainerStyle={{
          paddingBottom: insets.bottom,
        }}
      >
        {recommendationsLoading && (
          <ActivityIndicator style={{ marginTop: 20 }} />
        )}
        {displayedItems.map((item, i) => (
          <DiscoverItemCard 
            key={item.item_id}
            item={item}
            hue={hues[i % hues.length]}
            onPress={() =>
              router.push(
                `/item/${encodeURIComponent(item.restaurant_name)}/${encodeURIComponent(item.item_id)}`
              )
            }
          />
        ))}
        {searchLoading && (
          <ActivityIndicator style={{ marginTop: 20 }} />
        )}
        {isSearching && displayedItems.length === 0 && !searchLoading && (
          <Text style={styles.emptyText}>No items found.</Text>
        )}
        {!isSearching && recommendedItems.length === 0 && !recommendationsLoading && (
          <Text style={styles.emptyText}>No recommendations found. Try adjusting your constraints.</Text>
        )}
        {isSearching && (
          <View style={styles.centerButtonContainer}>
            <TouchableOpacity
              style={styles.button}
              onPress={() => {
                setSearchInput("");
                setSearchQuery("");
              }}
            >
              <Text style={styles.buttonText}>Clear Search Results</Text>
            </TouchableOpacity>
          </View>
        )}
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
})