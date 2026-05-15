import { View, Text, TouchableOpacity, StyleSheet, Image } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { SearchItem } from "../api/item";
import { getRestaurantImageURL } from "../utils/imageURLs";

type Props = {
  item: SearchItem;
  hue: number;
  onPress?: () => void;
};

function getCardColors(hue: number) {
  return {
    bgStart: `hsl(${hue}, 20%, 25%)`,
    bgEnd: `hsl(${hue}, 20%, 10%)`,
    borderTop: `hsl(${hue}, 20%, 40%)`,
    borderBottom: `hsl(${hue}, 30%, 25%)`,
  };
}

export default function ItemCard({ item, hue, onPress }: Props) {
  const colors = getCardColors(hue);

  const itemRestaurantURL = getRestaurantImageURL(item.restaurant_name);

  return (
    <TouchableOpacity
      style={styles.wrapper}
      onPress={onPress}
    >
      {/* Border gradient */}
      <LinearGradient
        colors={[colors.borderTop, colors.borderBottom]}
        start={{ x: 0.5, y: 0 }}   // top center
        end={{ x: 0.5, y: 1 }}     // bottom
        style={styles.border}
      >
        {/* Inner card gradient */}
        <LinearGradient
          colors={[colors.bgStart, colors.bgEnd]}
          start={{ x: 0, y: 0.5 }}  // left
          end={{ x: 1, y: 0.5 }}    // right
          style={styles.card}
        >
          <View style={styles.text}>
            {/* Restaurant */}
            <Text style={styles.restaurant}>
              {item.restaurant_name}
            </Text>

            {/* Item name */}
            <Text style={styles.name}>{item.menu_item_name}</Text>

            {/* Basic stats */}
            <View style={styles.row}>
              <Text style={styles.stat}>
                ${item.price.toFixed(2)}  ·  {item.calories} cal  ·  {item.protein}g protein
              </Text>
            </View>
          </View>

          {/* Item image */}
          <View style={styles.logoContainer}>
            <Image
              source={{ uri: itemRestaurantURL }}
              style={styles.logo}
              resizeMode="contain"
            />
          </View>
        </LinearGradient>
      </LinearGradient>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    marginVertical: 8,
    marginHorizontal: 16,
  },
  border: {
    borderRadius: 14,
    padding: 1,
  },
  card: {
    flexDirection: "row",
    padding: 16,
    borderRadius: 12,
  },
  text: {
    flex: 1,
    marginRight: 12,  
  },
  restaurant: {
    color: "#aaa",
    fontSize: 12,
    marginBottom: 4,
  },
  name: {
    color: "white",
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 8,
  },
  row: {
    flexDirection: "row",
  },
  stat: {
    color: "#ddd",
    fontSize: 13,
  },
  logoContainer: {
    width: 100,
    height: 100,
    backgroundColor: "white",
    borderRadius: 8,
    justifyContent: "center",
    alignItems: "center",
    overflow: "hidden",
  },
  logo: {
    width: "100%",
    height: "100%",
  },
});