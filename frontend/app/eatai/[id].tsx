import {
  View, Text, ScrollView, StyleSheet, TouchableOpacity,
  TextInput, KeyboardAvoidingView, Platform, ActivityIndicator, 
  Image, FlatList, Dimensions,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useState, useEffect } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import EatAIHeader from "../../components/EatAIHeader";
import ItemCard from "../../components/ItemCard";
import TargetModal from "../../components/TargetModal";
import { useMenu } from "../../hooks/useMenu";
import { useUser } from "../../context/UserContext";
import { getRecommendations } from "../../api/recommend";
import { saveMeal, unsaveMeal } from "../../api/meals";
import { getItem } from "../../api/item";
import { Meal } from "../../types/Meal";
import { MenuItem } from "../../api/menu";
import { getRestaurantImageURL } from "../../utils/imageURLs";
import NutritionCard from "../../components/NutritionCard";

type Pill = {
  id: string;
  label: string;
  icon: keyof typeof Ionicons.glyphMap;
  color: string;
  bg: string;
};

const WELCOME_PILLS: Pill[] = [
  { id: "full",    label: "Build full meal", icon: "restaurant-outline", color: "#39ff14", bg: "rgba(57,255,20,0.12)"  },
  { id: "protein", label: "Add Protein",     icon: "barbell-outline",    color: "#ffd600", bg: "rgba(255,214,0,0.12)" },
  { id: "side",    label: "Add Side",        icon: "nutrition-outline",  color: "#ffd600", bg: "rgba(255,214,0,0.12)" },
];

const FOLLOW_UP_PILLS: Pill[] = [
  { id: "alt",       label: "Alternative Meals",     icon: "swap-horizontal-outline", color: "#00eaff", bg: "rgba(0,234,255,0.12)"  },
  { id: "nutrition", label: "Nutritional Breakdown", icon: "bar-chart-outline",       color: "#00eaff", bg: "rgba(0,234,255,0.12)"  },
  { id: "protein",   label: "Add Protein",           icon: "barbell-outline",         color: "#ffd600", bg: "rgba(255,214,0,0.12)"  },
];

const PILL_CATEGORIES: Record<string, string[]> = {
  full:    ["Entree", "Side", "Drink"],
  protein: ["Entree"],
  side:    ["Side"],
  alt:     ["Entree", "Side", "Drink"],
};

function resolveItems(ids: string[], menuItems: MenuItem[]): MenuItem[] {
  return ids.flatMap((id) => {
    const item = menuItems.find((m) => String(m.index) === String(id));
    return item ? [item] : [];
  });
}

function getMealItems(meal: Meal, menuItems: MenuItem[]): MenuItem[] {
  return [
    ...resolveItems(meal.Entree_ids  ?? [], menuItems),
    ...resolveItems(meal.Side_ids    ?? [], menuItems),
    ...resolveItems(meal.Drink_ids   ?? [], menuItems),
    ...resolveItems(meal.Addon_ids   ?? [], menuItems),
    ...resolveItems(meal.Dessert_ids ?? [], menuItems),
  ];
}

function buildSummary(meal: Meal, constraints?: { calories: number; protein: number; price: number }): string {
  const { total_protein: protein, total_cal: cal, total_price: price } = meal;
  const targetCal   = constraints?.calories ?? 800;
  const targetPrice = constraints?.price    ?? 14;

  const calPart = cal > targetCal
    ? `exceeds your target of ${targetCal} calories with a total of ${cal} calories`
    : `stays within your ${targetCal} calorie target at ${cal} calories`;

  const pricePart = price <= targetPrice
    ? `it is under $${targetPrice}!`
    : `it goes slightly over your $${targetPrice.toFixed(2)} budget.`;

  return `This meal hits ${protein}g of protein but ${calPart}. However, ${pricePart}`;
}

function PillRow({ pills, onPress }: { pills: Pill[]; onPress: (p: Pill) => void }) {
  return (
    <View style={pillStyles.container}>
      {pills.map((pill) => (
        <TouchableOpacity
          key={pill.id}
          style={[pillStyles.pill, { backgroundColor: pill.bg }]}
          onPress={() => onPress(pill)}
          activeOpacity={0.7}
        >
          <Ionicons name={pill.icon} size={15} color={pill.color} />
          <Text style={[pillStyles.text, { color: pill.color }]}>{pill.label}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const pillStyles = StyleSheet.create({
  container: { gap: 8, alignItems: "flex-start" },
  pill: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 10,
  },
  text: { fontSize: 13, fontWeight: "600" },
});

export default function EatAI() {
  const { id, seed } = useLocalSearchParams<{ id: string; seed?: string }>();
  const restaurantName = decodeURIComponent(id);
  const imageURL = getRestaurantImageURL(restaurantName);
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { token, user } = useUser();
  const { items: menuItems } = useMenu(restaurantName);

  const [seedItem, setSeedItem]             = useState<MenuItem | null>(null);
  const [prompt, setPrompt]                 = useState("");
  const [loading, setLoading]               = useState(false);
  const [meals, setMeals]                   = useState<Meal[]>([]);
  const [summary, setSummary]               = useState("");
  const [roundIdx, setRoundIdx]             = useState(0);  // which group of 3 (0,1,2)
  const [mealIdx, setMealIdx]               = useState(0);  // which meal within the round
  const [savedKeys, setSavedKeys]           = useState<Map<string, number>>(new Map());
  const [filtersVisible, setFiltersVisible] = useState(false);
  const [hasGenerated, setHasGenerated]     = useState(false);
  const [showNutrition, setShowNutrition]   = useState(false);
  const [nutritionIdx, setNutritionIdx] = useState(0);

  useEffect(() => {
    if (!seed) return;
    getItem(restaurantName, decodeURIComponent(seed))
      .then(setSeedItem)
      .catch(() => {});
  }, [seed, restaurantName]);

  const ROUND_SIZE = 3;
  // How many full-or-partial rounds of 3 we have, capped at 3
  const numRounds = Math.min(3, Math.ceil((meals ?? []).length / ROUND_SIZE)) || 1;
  // The 3 meals for the current round (may be fewer if not enough meals)
  const currentRoundMeals = (meals ?? []).slice(roundIdx * ROUND_SIZE, (roundIdx + 1) * ROUND_SIZE);
  const currentMeal = currentRoundMeals[mealIdx] ?? null;
  const currentItems = currentMeal?.items ?? [];
  const SCREEN_WIDTH = Dimensions.get("window").width;

  const handleGenerate = async (categories = ["Entree", "Side", "Drink"]) => {
    if (!token) return;
    setShowNutrition(false);
    setLoading(true);
    setHasGenerated(true);
    try {
      const { recommendations, summary: llmSummary } = await getRecommendations(
        { restaurant_name: restaurantName, categories, seed_id: seed ? decodeURIComponent(seed) : undefined, calories: seedItem?.calories },
        token,
      );
      setMeals(recommendations ?? []);
      setSummary(llmSummary ?? "");
      setRoundIdx(0);
      setMealIdx(0);
    } catch {
      setMeals([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePill = (pill: Pill) => {
    // toggle nutritional information
    if (pill.id === "nutrition") {
      setShowNutrition(prev => !prev);
      return;
    }
    else {
      setShowNutrition(false);
    }

    if (pill.id === "alt") {
      // Cycle to the next round of 3 meals, wrapping back to round 0 after the last
      setRoundIdx((prev) => (prev + 1) % numRounds);
      setMealIdx(0);
      return;
    }

    // handle add side template: categories need to include current item/meal categories + side
    if (pill.id === "side" && currentMeal) {
      const currentCategories = new Set(currentMeal.items?.map((i) => i.category));
      currentCategories.add("Side");
      handleGenerate(Array.from(currentCategories));
      return;
    }
    if (pill.id === "side" && !currentMeal && seedItem) {
      const currentCategories = new Set<string>([seedItem.category, "Side"]);
      handleGenerate(Array.from(currentCategories));
      return;
    }

    handleGenerate(PILL_CATEGORIES[pill.id] ?? ["Entree", "Side", "Drink"]);
  };

  const handleSaveMeal = async () => {
    if (!token || !currentMeal) return;
    const key = currentMeal.item_ids.join(",");
    try {
      if (savedKeys.has(key)) {
        const savedIndex = savedKeys.get(key)!;
        await unsaveMeal(savedIndex, token);
        setSavedKeys((prev) => { const next = new Map(prev); next.delete(key); return next; });
      } else {
        const { saved_count } = await saveMeal(currentMeal, token);
        setSavedKeys((prev) => new Map(prev).set(key, saved_count - 1));
      }
    } catch {}
  };

  const handleSend = () => { if (prompt.trim()) handleGenerate(); };

  return (
    <KeyboardAvoidingView
      style={styles.root}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      <EatAIHeader />

      <LinearGradient
        colors={["#010000", "#181f2a"]}
        start={{ x: 1, y: 0 }}
        end={{ x: 0, y: 1 }}
        style={styles.gradient}
      >
        <TargetModal visible={filtersVisible} onClose={() => setFiltersVisible(false)} />

        <TouchableOpacity
          onPress={() => setFiltersVisible(true)}
          style={[
            styles.floatingFiltersButton,
            { bottom: insets.bottom + 80 }
          ]}
        >
          <Ionicons name="options-outline" size={26} color="white" />
        </TouchableOpacity>

        {/* ── SCROLL CONTENT ── */}
        <ScrollView
          contentContainerStyle={styles.scroll}
          showsVerticalScrollIndicator={false}
        >
          {!hasGenerated ? (
            <View style={styles.welcomeContainer}>
              {/* Seed item */}
              {seedItem && (
                <View style={styles.seedSection}>
                  <Text style={styles.seedLabel}>Your Item:</Text>
                  <LinearGradient
                    colors={["#66718A", "#272C45"]}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 1 }}
                    style={styles.seedCard}
                  >
                    <View style={styles.seedInfo}>
                      <Text style={styles.seedName}>{seedItem.menu_item_name}</Text>
                      <Text style={styles.seedStats}>
                        ${seedItem.price.toFixed(2)}  ·  {seedItem.calories} cal  ·  {seedItem.protein}g protein
                      </Text>
                    </View>
                    <View style={styles.seedImagePlaceholder}>
                      <Image
                        source={{ uri: imageURL}}
                        style={styles.image}
                        resizeMode="cover"
                      />
                    </View>
                  </LinearGradient>
                </View>
              )}

              {/* Welcome text */}
              <Text style={styles.welcomeLine1}>Welcome to EatAI!</Text>
              <Text style={styles.welcomeLine2}>How should we begin?</Text>

              {/* Pills right below */}
              <View style={styles.welcomePills}>
                <PillRow pills={WELCOME_PILLS} onPress={handlePill} />
              </View>
            </View>
          ) : loading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator color="white" size="large" />
              <Text style={styles.loadingText}>Building your meal…</Text>
            </View>
          ) : currentMeal ? (
            <View>
              <FlatList
                data={currentRoundMeals}
                horizontal
                pagingEnabled
                showsHorizontalScrollIndicator={false}
                keyExtractor={(_, index) => index.toString()}
                onMomentumScrollEnd={(event) => {
                  const index = Math.round(
                    event.nativeEvent.contentOffset.x / SCREEN_WIDTH
                  );
                  setMealIdx(index);
                }}
                renderItem={({ item: meal }) => {
                  const mealItems = meal.items ?? [];

                  return (
                    <View style={{ width: SCREEN_WIDTH }}>
                      <Text style={styles.summaryText}>
                        {summary || buildSummary(meal, user?.constraints)}
                      </Text>

                      {/* Heart / save button */}
                      {(() => {
                        const isSaved = savedKeys.has(meal.item_ids.join(","));

                        return (
                          <TouchableOpacity
                            style={styles.heartButton}
                            onPress={handleSaveMeal}
                            activeOpacity={0.7}
                          >
                            <Ionicons
                              name={isSaved ? "heart" : "heart-outline"}
                              size={22}
                              color={isSaved ? "#ff2975" : "#555"}
                            />

                            <Text
                              style={[
                                styles.heartLabel,
                                isSaved && styles.heartLabelSaved,
                              ]}
                            >
                              {isSaved ? "Saved" : "Save meal"}
                            </Text>
                          </TouchableOpacity>
                        );
                      })()}

                      {mealItems.map((item) => (
                        <ItemCard
                          key={item.item_id}
                          name={item.menu_item_name}
                          category={item.category}
                          price={item.price}
                          calories={item.calories}
                          protein={item.protein}
                          image_url={imageURL}
                          onPress={() =>
                            router.push(
                              `/item/${encodeURIComponent(
                                restaurantName
                              )}/${encodeURIComponent(item.item_id)}?source=eatai`
                            )
                          }
                        />
                      ))}
                    </View>
                  );
                }}
              />

              {currentRoundMeals.length > 1 && (
                <View style={styles.dotsRow}>
                  {currentRoundMeals.map((_, i) => (
                    <TouchableOpacity key={i} onPress={() => setMealIdx(i)}>
                      <View style={[styles.dot, i === mealIdx && styles.dotActive]} />
                    </TouchableOpacity>
                  ))}
                </View>
              )}

              {/* Nutrition breakdown section */}
              {showNutrition && (
                <View style={styles.nutritionalBreakdown}>
                  <FlatList
                    data={currentRoundMeals}
                    horizontal
                    pagingEnabled
                    showsHorizontalScrollIndicator={false}
                    keyExtractor={(_, index) => `nutrition-${index}`}
                    onMomentumScrollEnd={(event) => {
                      const index = Math.round(
                        event.nativeEvent.contentOffset.x / SCREEN_WIDTH
                      );
                      setNutritionIdx(index);
                    }}
                    renderItem={({ item: meal, index }) => (
                      <View style={{ width: SCREEN_WIDTH }}>
                        <Text style={styles.mealLabel}>
                          Recommendation #{index + 1}
                        </Text>

                        <NutritionCard meal={meal} />
                      </View>
                    )}
                  />

                  {currentRoundMeals.length > 1 && (
                    <View style={styles.dotsRow}>
                      {currentRoundMeals.map((_, i) => (
                        <TouchableOpacity
                          key={i}
                          onPress={() => setNutritionIdx(i)}
                        >
                          <View
                            style={[
                              styles.dot,
                              i === nutritionIdx && styles.dotActive,
                            ]}
                          />
                        </TouchableOpacity>
                      ))}
                    </View>
                  )}
                </View>
              )}
            </View>
          ) : (
            <View style={styles.loadingContainer}>
              <Text style={styles.loadingText}>No meals found. Try a different option.</Text>
            </View>
          )}

          {/* Follow-up pills + hamburger (results state only) */}
          <View style={styles.bottomArea}>
            {hasGenerated && !loading && (
              <View style={styles.followUpRow}>
                <PillRow
                  pills={FOLLOW_UP_PILLS.filter((p) => p.id !== "alt" || numRounds > 1)}
                  onPress={handlePill}
                />
              </View>
            )}
          </View>
        </ScrollView>

        {/* ── BOTTOM BAR ── */}
        <View style={[styles.bottomArea, { paddingBottom: insets.bottom + 8 }]}>
          {/* Prompt bar */}
          <View style={styles.promptBar}>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                placeholder="Enter a prompt"
                placeholderTextColor="#444"
                value={prompt}
                onChangeText={setPrompt}
                onSubmitEditing={handleSend}
                returnKeyType="send"
              />
            </View>
            <TouchableOpacity style={styles.sendButton} onPress={handleSend}>
              <Ionicons name="arrow-up" size={18} color="black" />
            </TouchableOpacity>
          </View>
        </View>
      </LinearGradient>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: "#010000",
  },
  gradient: {
    flex: 1,
  },
  scroll: {
    paddingBottom: 16,
  },

  /* Welcome */
  welcomeContainer: {
    paddingTop: 16,
    paddingHorizontal: 20,
  },
  seedSection: {
    marginBottom: 24,
  },
  seedLabel: {
    color: "#555",
    fontSize: 11,
    fontWeight: "600",
    textTransform: "uppercase",
    letterSpacing: 0.8,
    marginBottom: 10,
  },
  seedCard: {
    flexDirection: "row",
    alignItems: "center",
    borderRadius: 14,
    padding: 16,
  },
  seedInfo: {
    flex: 1,
    marginRight: 12,
  },
  seedName: {
    color: "white",
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 6,
  },
  seedStats: {
    color: "rgba(255,255,255,0.6)",
    fontSize: 13,
  },
  seedImagePlaceholder: {
    width: 72,
    height: 72,
    backgroundColor: "rgba(255,255,255,0.1)",
    borderRadius: 10,
    overflow: "hidden",
  },
  image: {
    width: "100%",
    height: "100%",
  },
  welcomeLine1: {
    color: "#FFFFFF",
    fontSize: 20,
    fontWeight: "400",
    letterSpacing: -0.5,
    lineHeight: 40,
  },
  welcomeLine2: {
    color: "#FFFFFF",
    fontSize: 36,
    fontWeight: "400",
    letterSpacing: -0.5,
    lineHeight: 40,
    marginBottom: 24,
  },
  welcomePills: {
    // pills sit right under the heading
  },

  /* Loading */
  loadingContainer: {
    padding: 40,
    alignItems: "center",
    gap: 14,
  },
  loadingText: {
    color: "#555",
    fontSize: 14,
  },

  /* Save button */
  heartButton: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    paddingHorizontal: 20,
    marginBottom: 12,
  },
  heartLabel: {
    color: "#555",
    fontSize: 13,
    fontWeight: "600",
  },
  heartLabelSaved: {
    color: "#ff2975",
  },

  /* Result */
  summaryText: {
    color: "white",
    fontSize: 15,
    lineHeight: 23,
    paddingHorizontal: 20,
    marginBottom: 12,
    marginTop: 8,
  },
  dotsRow: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 6,
    marginVertical: 14,
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: "#2a2a2a",
  },
  dotActive: {
    backgroundColor: "white",
  },

  /* Bottom */
  bottomArea: {
    paddingTop: 12,
    paddingHorizontal: 16,
    gap: 10,
    // transparent — gradient shows through
  },
  followUpRow: {
    flexDirection: "row",
    alignItems: "flex-end",
    gap: 10,
  },
  hamburger: {
    position: "absolute",
    right: 16,
    bottom: 100,
  },
  hamburgerRight: {
    alignSelf: "flex-end",
  },
  floatingFiltersButton: {
    position: "absolute",
    right: 16,
    zIndex: 1000,

    width: 40,
    height: 40,
    borderRadius: 10,

    backgroundColor: "rgba(40, 40, 40, 0.67)",
    justifyContent: "center",
    alignItems: "center",
  },
  promptBar: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
  },
  inputContainer: {
    flex: 1,
    backgroundColor: "rgba(255,255,255,0.05)",
    borderRadius: 22,
    paddingHorizontal: 16,
    paddingVertical: 11,
    borderWidth: 1,
    borderColor: "#1a1a1a",
  },
  input: {
    color: "white",
    fontSize: 15,
  },
  sendButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: "white",
    justifyContent: "center",
    alignItems: "center",
  },
  nutritionalBreakdown: {
    flex: 1,
    alignItems: 'center',
  },
  mealLabel : {
    color: "white",
    fontSize: 14,
    fontWeight: 600,
    marginLeft: 16,
    marginBottom: 10,
  },
});
