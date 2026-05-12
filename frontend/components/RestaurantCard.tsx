import { View, Text, Image, StyleSheet, TouchableOpacity } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { Restaurant } from "../api/restaurant";

type Props = {
  restaurant: Restaurant;
  hue: number;
  onPress?: () => void;
};

function formatNameForUrl(name: string) {
  const reformattedString = name.toLowerCase().replace(/\s+/g, "-");
  const removedBadChars = reformattedString.replace("'", "");
  return removedBadChars;
}

function getCardColors(hue: number) {
  return {
    bgStart: `hsl(${hue}, 20%, 25%)`,
    bgEnd: `hsl(${hue}, 20%, 10%)`,
    borderTop: `hsl(${hue}, 20%, 40%)`,
    borderBottom: `hsl(${hue}, 30%, 25%)`,
  };
}

export default function RestaurantCard({ restaurant, hue, onPress }: Props) {
  const { restaurant_name, menu_card_image } = restaurant;

  const colors = getCardColors(hue);

  return (
    <TouchableOpacity onPress={onPress} style={styles.wrapper}>
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
          <Text style={styles.name}>{restaurant_name}</Text>

          <View style={styles.logoContainer}>
            <Image
              source={{ uri: menu_card_image }}
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
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    borderRadius: 12,
  },
  name: {
    color: 'white',
    fontSize: 18,
    fontWeight: "600",
  },
  logoContainer: {
    width: 100,
    height: 100,
    backgroundColor: "white",
    borderRadius: 8,
    justifyContent: "center",
    alignItems: "center",
  },
  logo: {
    width: 60,
    height: 60,
  },
});