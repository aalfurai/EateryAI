import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useState } from "react";
import { useRouter, } from "expo-router";
import { useUser } from "../../context/UserContext";
import { getMinAndMaxValues } from "../../types/user";
import { useItemSearch } from "../../hooks/useItemSearch";
import AppHeader from "../../components/AppHeader";
import DiscoverItemCard from "../../components/DiscoverItemCard";
import FilterModal from "../../components/TargetModal";

export default function Discover() {
  const { user } = useUser();
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const [filtersVisible, setFiltersVisible] = useState(false);

  /* Load items based on user constraints */
  const ranges = user ? getMinAndMaxValues(user) : null;
  const {
    results: items,
    loading,
    error,
  } = useItemSearch(
    ranges
      ? {
          price_min: ranges.minPrice,
          price_max: ranges.maxPrice,

          calories_min: ranges.minCalories,
          calories_max: ranges.maxCalories,

          protein_min: ranges.minProtein,
          protein_max: ranges.maxProtein,
        }
      : {}
  );

  // display first 20
  const displayedItems = items.slice(0, 20);

  const hues = [0, 130, 220, 30, 300]; 

  if (loading) return <ActivityIndicator />;
  if (error) return <Text>Failed to load items.</Text>;

  return (
    <View style={styles.container}>
      <AppHeader onPressFilters={() => setFiltersVisible(true)}/>
      <FilterModal
        visible={filtersVisible}
        onClose={() => setFiltersVisible(false)}/>
        
      <Text style={styles.title}>For You</Text>
      <ScrollView 
        contentContainerStyle={{
          paddingBottom: insets.bottom,
        }}
      >
        {displayedItems.map((item, i) => (
        <DiscoverItemCard 
          key={item.item_id}
          item={item}
          hue={hues[i % hues.length]}
          onPress={() =>
            router.push({
              pathname: "/item/[restaurant]/[id]",
              params: {
                restaurant: item.restaurant_name,
                id: item.item_id,
              },
            })
          }
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