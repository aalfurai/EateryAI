import { View, TouchableOpacity, StyleSheet } from "react-native";
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import EatAILogo from "../assets/EatAILogo";

export default function EatAIHeader() {
  const router = useRouter();

  return (
    <SafeAreaView edges={["top"]} style={styles.safe}>
    <View style={styles.container}>
      {/* Back button */}
      <TouchableOpacity 
        style={styles.left}
        onPress={() => router.back()}
      >
        <Ionicons name="arrow-back-outline" size={24} color="white" />
      </TouchableOpacity>

      {/* Center logo */}
      <View style={styles.center}>
        <EatAILogo width={80} height={30} />
      </View>

      {/* Right spacer (keeps logo centered) */}
      <View style={styles.right} />
    </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    backgroundColor: "#010000",
  },
  container: {
    height: 80,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    backgroundColor: "#010000",
  },
  left: {
    width: 40,
    alignItems: "flex-start",
  },
  center: {
    position: "absolute",
    left: 0,
    right: 0,
    alignItems: "center",
  },
  right: {
    width: 40,
  },
});