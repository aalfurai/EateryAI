import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useRouter } from "expo-router";
import { useUser } from "../../context/UserContext";
import { User } from "../../types/user";
import EatLogo from "../../assets/EatLogo";

// replace with api call to user database
const dummyUser: User = {
  user_id: "1",
  name: "dummyUser",
  constraints: {
    price: 14,
    calories: 800,
    protein: 20,
    price_tol_pct: 0.2,
    calories_tol_pct: 0.1,
    protein_tol_pct: 0.3,
  },
  weights: {
    price: 0.2,
    calories: 0.4,
    protein: 0.4,
    fiber: 0,
    sugar: 0,
    sodium: 0,
    drink_cal: 0,
    addon_cal: 0,
  },
};

export default function Login() {
  const router = useRouter();
  const { setUser } = useUser();

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
          onPress={() => {
            router.replace("/(tabs)");
            setUser(dummyUser); // replace with actual user
          }}
        >
          <Text style={styles.buttonText}>Bodybuilder</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.button}
          onPress={() => {
            router.replace("/(tabs)");
            setUser(dummyUser); // replace with actual user
          }}
        >
          <Text style={styles.buttonText}>Budgeter</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.button}
          onPress={() => {
            router.replace("/(tabs)");
            setUser(dummyUser); // replace with actual user
          }}
        >
          <Text style={styles.buttonText}>Dieting</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.button}
          onPress={() => {
            router.replace("/(tabs)");
            setUser(dummyUser); // replace with actual user
          }}
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