import { View, Text, ScrollView, StyleSheet, TouchableOpacity, Image, ActivityIndicator } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useSafeAreaInsets, SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";
import EatAILogo from "../../../assets/EatAILogo";
import { useItem } from "../../../hooks/useItem";
import { getRestaurantImageURL } from "../../../utils/imageURLs";


export default function ItemDetail() {
  const params = useLocalSearchParams();

  const restaurant = decodeURIComponent(
    Array.isArray(params.restaurant)
      ? params.restaurant[0]
      : params.restaurant ?? ""
  );

  const id = decodeURIComponent(
    Array.isArray(params.id)
      ? params.id[0]
      : params.id ?? ""
  );

  const source = Array.isArray(params.source)
    ? params.source[0]
    : params.source;

  const fromEatAI = source === "eatai";

  const router = useRouter();
  const insets = useSafeAreaInsets();

  const { item, loading, error } = useItem(restaurant, id);
  console.log("item:", item);

  const imageURL = item?.image_url || getRestaurantImageURL(restaurant);

  if (loading) return <ActivityIndicator />;
  if (error) return <Text style={{ color: "white", }}>Failed to load item.</Text>;

  return (
    <View style={styles.container}>
      
      <View style={styles.restaurantHeader}>
        <View style={styles.restaurantHeaderTag}>
          <Text style={styles.restaurantHeaderText}>{restaurant}</Text>
        </View>
      </View>

      <TouchableOpacity
        style={[
          styles.closeButton,
          { top: insets.top },
        ]}
        onPress={() => router.back()}
      >
        <Ionicons name="close" size={18} color="white" />
      </TouchableOpacity>
      
      <ScrollView
        style={styles.sheet}
        contentContainerStyle={{ paddingBottom: insets.bottom + 200 }}
        showsVerticalScrollIndicator={false}
      >
        {/* Image area */}
        <View style={styles.imageArea}>
          <Image
            source={{ uri: item?.image_url || imageURL }}
            style={styles.image}
            resizeMode="cover"
          />
          <LinearGradient
            colors={["transparent", "rgba(0,0,0,0.6)"]}
            style={styles.imageOverlay}
          />
        </View>
        
        {/* Content sheet */}
        <View style={styles.content}>
          <Text style={styles.itemName}>{item?.menu_item_name}</Text>
          <Text style={styles.restaurantLabel}>{restaurant}</Text>
          <Text style={styles.quickStats}>
            {item?.price !== undefined ? `$${item.price.toFixed(2)}` : ""}  ·  {item?.calories} cal  ·  {item?.protein}g protein
       
          </Text>

          <Text style={styles.sectionTitle}>Meal Information</Text>
          <View style={styles.mealInfoRow}>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 10, paddingRight: 10 }}>
              <View style={styles.tag}>
                <Text style={styles.tagText}>{item?.category}</Text>
              </View>
              <View style={styles.tag}>
                <Text style={styles.tagText}>{item?.serving_size}</Text>
              </View>
              {!fromEatAI && (
                <TouchableOpacity
                  style={styles.eatAIButton}
                  onPress={() => router.push(`/eatai/${encodeURIComponent(restaurant)}?seed=${encodeURIComponent(id)}`)}
                  activeOpacity={0.8}
                >
                  <EatAILogo width={35} height={16} />
                </TouchableOpacity>
            )}
            </ScrollView>
          </View>

          <Text style={styles.sectionTitle}>Meal Description</Text>
          <Text style={styles.description}>{item?.ai_description}</Text>

          <Text style={styles.sectionTitle}>Nutrition Information</Text>
          <View style={styles.nutritionRow}>
            <NutritionCell label="Carbs" value={`${item?.total_carbohydrates}g`} />
            <View style={styles.divider} />
            <NutritionCell label="Fats" value={`${item?.total_fat}g`} />
            <View style={styles.divider} />
            <NutritionCell label="Sugar" value={`${item?.sugars}g`} />
            <View style={styles.divider} />
            <NutritionCell label="Sodium" value={`${item?.sodium}mg`} />
            <View style={styles.divider} />
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

function NutritionCell({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.nutritionCell}>
      <Text style={styles.nutritionValue}>{value}</Text>
      <Text style={styles.nutritionLabel}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#010000",
  },
  imageArea: {
    height: 220,
    backgroundColor: "#1a1a1a",
    justifyContent: "center",
    alignItems: "center",
    overflow: "hidden",
    marginTop: 105,
  },
  image: {
    width: "100%",
    height: "100%",
  },
  imageOverlay: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    height: 80,
  },
  closeButton: {
    position: "absolute",
    left: 16,
    zIndex: 10,
    elevation: 10,
    width: 34,
    height: 34,
    borderRadius: 17,
    backgroundColor: "rgba(0,0,0,0.5)",
    borderColor: "rgba(161, 161, 161, 0.17)",
    borderWidth: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  sheet: {
    flex: 1,
    backgroundColor: "#010000",
  },
  content: {
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  itemName: {
    color: "white",
    fontSize: 26,
    fontWeight: "700",
    marginBottom: 4,
  },
  restaurantLabel: {
    color: "#898989",
    fontSize: 14,
    marginBottom: 6,
  },
  quickStats: {
    color: "#ccc",
    fontSize: 14,
    marginBottom: 24,
  },
  sectionTitle: {
    color: "white",
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 12,
  },
  mealInfoRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    marginBottom: 24,
  },
  tag: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: "#1e1e1e",
    borderWidth: 1,
    borderColor: "#333",
  },
  tagText: {
    color: "#aaa",
    fontSize: 13,
  },
  eatAIButton: {
    paddingHorizontal: 18,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "white",
  },
  eatAIText: {
    color: "white",
    fontSize: 13,
    fontWeight: "600",
  },
  description: {
    color: "#aaa",
    fontSize: 14,
    lineHeight: 21,
    marginBottom: 24,
  },
  nutritionRow: {
    flexDirection: "row",
    backgroundColor: "#111",
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "#1e1e1e",
    overflow: "hidden",
  },
  nutritionCell: {
    flex: 1,
    alignItems: "center",
    paddingVertical: 16,
  },
  nutritionValue: {
    color: "white",
    fontSize: 16,
    fontWeight: "700",
  },
  nutritionLabel: {
    color: "#898989",
    fontSize: 11,
    marginTop: 4,
  },
  divider: {
    width: 1,
    backgroundColor: "#1e1e1e",
    marginVertical: 12,
  },
  restaurantHeader : {
    position: "absolute",
    top: 60,
    left: 0,
    right: 0,
    alignItems: "center",
    zIndex: 10,
  },
  restaurantHeaderTag: {
    position: "absolute",
    zIndex: 10,
    elevation: 10,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 18,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: "white",
    shadowColor: "#000",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
  },
  restaurantHeaderText: {
    color: "#1e1e1e",
    fontSize: 14,
    fontWeight: 600,
  },
});
