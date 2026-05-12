import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useState } from "react";
import { useRouter, } from "expo-router";
import { useMenu } from "../../hooks/useMenu";
import AppHeader from "../../components/AppHeader";
import DiscoverItemCard from "../../components/DiscoverItemCard";
import FilterModal from "../../components/TargetModal";

export default function Discover() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const [filtersVisible, setFiltersVisible] = useState(false);

  // load just one restaurant for now
  const [restaurant] = useState("Chick-fil-A");
  const { items } = useMenu(restaurant);

  const hues = [0, 130, 220, 30, 300]; 

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
        {items.map((item, i) => (
        <DiscoverItemCard 
          key={item.item_id}
          item={item}
          hue={hues[i % hues.length]}
          onPress={() =>
            router.push({
              pathname: "/item/[restaurant]/[id]",
              params: {
                restaurant,
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