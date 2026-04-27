import { View, TouchableOpacity, StyleSheet, Text } from "react-native";
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import EatLogo from "../assets/EatLogo";

export default function ProfileHeader({ username="User" }) {
  const router = useRouter();

  return (
    <SafeAreaView edges={["top"]}>
      <View style={styles.container}>
        <View style={styles.topRow}>
          <View style={styles.logoContainer}>
            <EatLogo width={100} height={38} />
          </View>

          <TouchableOpacity
            style={styles.logoutButton}
            onPress={() => router.replace("/(auth)/login")}
          >
            <Ionicons name="log-out-outline" size={26} color="white" />
          </TouchableOpacity>
        </View>

        <View style={styles.userContainer}>
          <Ionicons name="at" size={30} color="white" />
          <Text style={styles.username}>{username}</Text>  
        </View>
        
        <Text style={styles.subtitle}>Saved Meals</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 16,
    paddingBottom: 20,
  },
  topRow: {
    height: 80,
    justifyContent: "center",
  },
  logoContainer: {
    position: "absolute",
    left: 0,
    right: 0,
    alignItems: "center",
  },
  logoutButton: {
    position: "absolute",
    right: 0,
    padding: 4,
  },
  userContainer: {
    flexDirection: "row",
    marginTop: 70,
  },
  username: {
    fontSize: 22,
    fontWeight: "700",
    color: "white",
    marginBottom: 120,
  },
  subtitle: {
    fontSize: 16,
    fontWeight: 500,
    color: "white",
  },
});