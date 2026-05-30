import { View, Text, StyleSheet } from "react-native";
import { Meal } from "../types/Meal";

type Props = {
  meal: Meal;
}

export default function NutritionCard({ meal }: Props) {
  const mealItems = meal.items ?? [];

  const nutrients = [
    { label: "Calories", value: meal.total_cal },
    { label: "Protein", value: `${meal.total_protein}g` },
    { label: "Carbs", value: `${meal.total_carbohydrates}g` },
    { label: "Fat", value: `${meal.total_fat}g` },
    { label: "Fiber", value: `${meal.total_fiber}g` },
    { label: "Sugar", value: `${meal.total_sugars}g` },
    { label: "Sodium", value: `${meal.total_sodium}mg` },
    { label: "Cholesterol", value: `${meal.total_cholesterol}mg` },
    { label: "Potassium", value: `${meal.total_potassium}mg` },
    { label: "Golden Ratio", value: `${meal.golden_ratio.toFixed(2)}`}
  ];

  return(
    <View style={styles.card}>
      <Text style={styles.title}>Items</Text>
      {mealItems.map((item, idx) => (
        <Text 
          key={`${item.index}-${idx}`}
          style={styles.items}
        >
          {`${item.menu_item_name}`}
        </Text>
      ))}

      <View style={styles.nutritionTable}>
        {nutrients.map((n) => (
          <View key={n.label} style={styles.row}>
            <Text style={styles.label}>{n.label}</Text>
            <Text style={styles.value}>{n.value}</Text>
          </View>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card : {
    flex: 1,
    justifyContent: 'center',
    backgroundColor: '#00000000',
    borderRadius: 14,
    borderColor: '#0c1728b1',
    borderWidth: 1,
    width: 360,
    alignSelf: "center",
  },

  title: {
    color: "white",
    fontSize: 16,
    fontWeight: 700,
    marginLeft: 16,
    marginTop: 16,
    marginBottom: 8,
  },

  items: {
    color: "white",
    fontSize: 14,
    fontWeight: 400,
    fontStyle: 'italic',
    marginLeft: 26,
    marginBottom: 6,
  },

  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#22222277",
    width: '90%'
  },

  label: {
    color: "#dbdbdb",
    fontSize: 16,
  },

  value: {
    color: "white",
    fontSize: 16,
    fontWeight: "500",
  },

  nutritionTable : {
    alignItems: 'center',
    marginBottom: 16,
  },
});