import { View, TouchableOpacity, StyleSheet } from "react-native";
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import EatLogo from "../assets/EatLogo";
import Octicons from '@expo/vector-icons/Octicons';

type Props = {
  onPressFilters?: () => void;
  onPressSearch?: () => void;
};

export default function AppHeader({ onPressFilters, onPressSearch }:Props) {
  const router = useRouter();

  return (
    <SafeAreaView edges={["top"]} style={styles.safe}>
    <View style={styles.container}>
      {/* Left side */}
      <View style={styles.leftContainer}>
        <TouchableOpacity onPress={() => router.replace("/(auth)/login")}>
          <Octicons name="goal" size={24} color="white" />
        </TouchableOpacity>
      </View>

      {/* Center logo */}
      <View style={styles.center}>
        <EatLogo width={100} height={38} />
      </View>

      {/* Right side */}
      <View style={styles.rightContainer}>
        <TouchableOpacity 
          style={styles.iconButton}
          onPress={onPressFilters}
        >
          <Ionicons name="options-outline" size={28} color="white" />
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.iconButton}
          onPress={onPressSearch}
        >
          <Ionicons name="search-outline" size={28} color="white" />
        </TouchableOpacity>
      </View>
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
  leftContainer: {
    width: 80,
    justifyContent: "center",
    alignItems: "flex-start",
  },
  center: {
    position: "absolute",
    left: 0,
    right: 0,
    alignItems: "center",
  },
  rightContainer: {
    width: 80,
    flexDirection: "row",
    justifyContent: "flex-end",
    alignItems: "center",
    gap: 12,
  },
  iconButton: {
    justifyContent: "center",
    alignItems: "center",
  },
});