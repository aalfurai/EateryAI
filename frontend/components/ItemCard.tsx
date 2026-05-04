import { View, Text, StyleSheet, TouchableOpacity } from "react-native";

type Props = {
  name: string;
  category: string;
  price: number;
  calories: number;
  protein: number;
  onPress?: () => void;
};

export default function ItemCard({ name, category, price, calories, protein, onPress }: Props) {
  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.7}>
      <View style={styles.info}>
        <Text style={styles.category}>{category}</Text>
        <Text style={styles.name} numberOfLines={2}>{name}</Text>
        <Text style={styles.stats}>
          ${price.toFixed(2)}  ·  {calories} cal  ·  {protein}g protein
        </Text>
      </View>
      <View style={styles.imagePlaceholder} />
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#111",
    borderRadius: 14,
    marginHorizontal: 16,
    marginVertical: 6,
    padding: 16,
    borderWidth: 1,
    borderColor: "#1e1e1e",
  },
  info: {
    flex: 1,
    marginRight: 14,
  },
  category: {
    color: "#7ddf7d",
    fontSize: 11,
    fontWeight: "600",
    textTransform: "uppercase",
    letterSpacing: 0.5,
    marginBottom: 5,
  },
  name: {
    color: "white",
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 6,
  },
  stats: {
    color: "#898989",
    fontSize: 13,
  },
  imagePlaceholder: {
    width: 72,
    height: 72,
    backgroundColor: "#222",
    borderRadius: 10,
  },
});
