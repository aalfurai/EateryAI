import { View, Text, StyleSheet } from "react-native";
import { Meal } from "../types/Meal";
import { MenuItem } from "../api/menu";

const CATEGORY_COLORS: Record<string, string> = {
  Entree:   "#39ff14",
  Side:     "#ffd600",
  Drink:    "#ff2975",
  "Add-On": "#00eaff",
  Dessert:  "#d500f9",
};

type Section = { label: string; ids: number[]; color: string };

type Props = {
  meal: Meal;
  menuItems: MenuItem[];
  rank: number;
};

function resolveItems(ids: number[], menuItems: MenuItem[]): MenuItem[] {
  return ids.flatMap((id) => {
    const item = menuItems.find((m) => m.index === id || Number(m.item_id) === id);
    return item ? [item] : [];
  });
}

export default function MealCard({ meal, menuItems, rank }: Props) {
  const sections: Section[] = [
    { label: "Entree",   ids: meal.Entree_ids,  color: CATEGORY_COLORS.Entree   },
    { label: "Side",     ids: meal.Side_ids,    color: CATEGORY_COLORS.Side     },
    { label: "Drink",    ids: meal.Drink_ids,   color: CATEGORY_COLORS.Drink    },
    { label: "Add-On",   ids: meal.Addon_ids,   color: CATEGORY_COLORS["Add-On"]},
    { label: "Dessert",  ids: meal.Dessert_ids, color: CATEGORY_COLORS.Dessert  },
  ].filter((s) => s.ids.length > 0);

  const score = Math.round(meal.golden_ratio * 100);

  return (
    <View style={styles.card}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.rankLabel}>
          {rank === 1 ? "Best Match" : `#${rank} Option`}
        </Text>
        <View style={styles.scoreBadge}>
          <Text style={styles.scoreText}>{score}</Text>
          <Text style={styles.scoreUnit}>score</Text>
        </View>
      </View>

      {/* Items */}
      <View style={styles.itemsContainer}>
        {sections.map((section) => {
          const resolved = resolveItems(section.ids, menuItems);
          if (resolved.length > 0) {
            return resolved.map((item) => (
              <View key={item.item_id} style={styles.itemRow}>
                <View style={[styles.dot, { backgroundColor: section.color }]} />
                <Text style={styles.itemName} numberOfLines={1}>{item.menu_item_name}</Text>
                <Text style={styles.itemCal}>{item.calories} cal</Text>
              </View>
            ));
          }
          return (
            <View key={section.label} style={styles.itemRow}>
              <View style={[styles.dot, { backgroundColor: section.color }]} />
              <Text style={[styles.itemName, styles.unknownItem]}>{section.label}</Text>
            </View>
          );
        })}
      </View>

      <View style={styles.divider} />

      {/* Totals */}
      <View style={styles.totals}>
        <View style={styles.totalItem}>
          <Text style={styles.totalValue}>${meal.total_price.toFixed(2)}</Text>
          <Text style={styles.totalLabel}>price</Text>
        </View>
        <View style={styles.totalDivider} />
        <View style={styles.totalItem}>
          <Text style={styles.totalValue}>{meal.total_cal}</Text>
          <Text style={styles.totalLabel}>cal</Text>
        </View>
        <View style={styles.totalDivider} />
        <View style={styles.totalItem}>
          <Text style={styles.totalValue}>{meal.total_protein}g</Text>
          <Text style={styles.totalLabel}>protein</Text>
        </View>
        <View style={styles.totalDivider} />
        <View style={styles.totalItem}>
          <Text style={styles.totalValue}>{meal.total_carbohydrates}g</Text>
          <Text style={styles.totalLabel}>carbs</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#0d1117",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#1e2530",
    marginHorizontal: 16,
    marginVertical: 8,
    padding: 18,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 16,
  },
  rankLabel: {
    color: "white",
    fontSize: 16,
    fontWeight: "700",
  },
  scoreBadge: {
    alignItems: "center",
    backgroundColor: "rgba(255,214,0,0.08)",
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderWidth: 1,
    borderColor: "rgba(255,214,0,0.25)",
  },
  scoreText: {
    color: "#ffd600",
    fontSize: 15,
    fontWeight: "700",
  },
  scoreUnit: {
    color: "#ffd600",
    fontSize: 10,
    opacity: 0.7,
  },
  itemsContainer: {
    gap: 10,
    marginBottom: 16,
  },
  itemRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    flexShrink: 0,
  },
  itemName: {
    flex: 1,
    color: "white",
    fontSize: 14,
    fontWeight: "500",
  },
  unknownItem: {
    color: "#3a3a3a",
  },
  itemCal: {
    color: "#555",
    fontSize: 13,
  },
  divider: {
    height: 1,
    backgroundColor: "#1e2530",
    marginBottom: 14,
  },
  totals: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  totalItem: {
    flex: 1,
    alignItems: "center",
  },
  totalValue: {
    color: "white",
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 2,
  },
  totalLabel: {
    color: "#555",
    fontSize: 11,
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
  totalDivider: {
    width: 1,
    height: 28,
    backgroundColor: "#1e2530",
  },
});
