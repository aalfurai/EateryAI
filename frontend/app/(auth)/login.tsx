import { View, Text, StyleSheet, TextInput, TouchableOpacity } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useRouter } from "expo-router";
import EatLogo from "../../assets/EatLogo";

export default function Login() {
  const router = useRouter();

  return (
    <LinearGradient
      colors={["#AB94CB", "#CC6567", "#C94371", "#B2B194"]}
      start={{ x:0, y:0 }}
      end={{ x:1, y:1 }}
      style={styles.container}
    >
      {/* Logo */}
      <View style={styles.logoContainer}>
        <EatLogo width={140} height={60} />
      </View>

      <View style={styles.centerContent}>
        {/* Welcome text */}
        <Text style={styles.title}>Welcome</Text>
        <Text style={styles.subtitle}>Select a demo user:</Text>

        {/* Demo Users */}
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.replace("/(tabs)")}
        >
          <Text style={styles.buttonText}>Bodybuilder</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.replace("/(tabs)")}
        >
          <Text style={styles.buttonText}>Budgeter</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.replace("/(tabs)")}
        >
          <Text style={styles.buttonText}>Dieting</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.replace("/(tabs)")}
        >
          <Text style={styles.buttonText}>Balanced</Text>
        </TouchableOpacity>

      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoContainer: {
    position: "absolute",
    top: 130,
    alignItems: "center",
  },
  centerContent: {
    position: "absolute",
    top: 260,
    alignItems: "flex-start",
  },
  title: {
    fontSize: 32,
    fontWeight: "700",
    color: "white",
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 20,
    fontWeight: "600",
    color: "white",
    marginBottom: 30,
  },
  icon: {
    marginRight: 8,
  },
  input: {
    flex: 1,
    color: "white",
    fontSize: 16,
  },
  button: {
    flexDirection: "row",
    alignItems: "center",
    borderRadius: 15,
    paddingHorizontal: 25,
    paddingVertical: 10,
    height: 80,
    width: 340,
    marginBottom: 16,
    backgroundColor: "rgba(255, 255, 255, 0.20)",
  },
  buttonText: {
    color: "white",
    fontWeight: "600",
    fontSize: 18,
  },
});