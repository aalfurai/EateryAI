import { View, Text, StyleSheet } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useRouter } from "expo-router";
import EatAIHeader from "../../components/EatAIHeader";

export default function EatAI() {
  const router = useRouter()

  return (
    <View style={{ flex: 1 }}>
      <EatAIHeader />
      <LinearGradient
        colors={["#010000", "#181f2a"]}
        start={{ x: 1, y: 0 }}
        end={{ x: 0, y: 1 }}
        style={{ flex: 1 }}
      >
      </LinearGradient>
    </View>
  );
}