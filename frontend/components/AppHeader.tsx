import { View, TouchableOpacity, StyleSheet } from "react-native";
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from "react-native-safe-area-context";
import EatLogo from "../assets/EatLogo";

export default function AppHeader() {
  return (
    <SafeAreaView edges={["top"]} style={styles.safe}>
    <View style={styles.container}>
      {/* Left button */}
      <TouchableOpacity style={styles.left}>
        <Ionicons name="menu" size={28} color="white" />
      </TouchableOpacity>

      {/* Center logo */}
      <View style={styles.center}>
        <EatLogo width={100} height={38} />
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