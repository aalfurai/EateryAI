import { View, Text, Image, StyleSheet, TouchableOpacity } from "react-native";

type Props = {
  name: string;
  onPress?: () => void;
};

function formatNameForUrl(name: string) {
  const reformattedString = name.toLowerCase().replace(/\s+/g, "-");
  const removedBadChars = reformattedString.replace("'", "");
  return removedBadChars;
}

export default function RestaurantCard({ name, onPress }: Props) {
  const formatted = formatNameForUrl(name);
  const imageUrl = `https://fastfoodnutrition.org/logos/${formatted}.jpg`;

  return (
    <TouchableOpacity onPress={onPress} style={styles.card}>
      <Text style={styles.name}>{name}</Text>

      <View style={styles.logoContainer}>
        <Image
          source={{ uri: imageUrl }}
          style={styles.logo}
          resizeMode="contain"
        />
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    marginVertical: 8,
    marginHorizontal: 16,
    backgroundColor: "#f2f2f2",
    borderRadius: 12,
  },
  name: {
    fontSize: 18,
    fontWeight: "600",
  },
  logoContainer: {
    width: 50,
    height: 50,
    backgroundColor: "white",
    borderRadius: 8,
    justifyContent: "center",
    alignItems: "center",
  },
  logo: {
    width: 40,
    height: 40,
  },
});