import { View, Text, StyleSheet, TextInput, TouchableOpacity } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
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

        {/* Username input */}
        <View style={styles.inputContainer}>
          <Ionicons name="at" size={20} color="white" style={styles.icon} />
          <TextInput
            placeholder="Username"
            placeholderTextColor="#ccc"
            style={styles.input}
          />
        </View>

        {/* Login button */}
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.replace("/(tabs)")}
        >
          <Text style={styles.buttonText}>Log In</Text>
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
    top: 160,
    alignItems: "center",
  },
  centerContent: {
    position: "absolute",
    top: 330,
    alignItems: "center",
  },
  title: {
    fontSize: 36,
    fontWeight: "700",
    color: "white",
    marginBottom: 40,
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    borderRadius: 15,
    paddingHorizontal: 12,
    paddingVertical: 10,
    height: 65,
    width: 340,
    marginBottom: 16,
    backgroundColor: "rgba(255, 255, 255, 0.20)",
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
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: "white",
    paddingVertical: 12,
    paddingHorizontal: 40,
    borderRadius: 50,
    height: 65,
    width: 340,
  },
  buttonText: {
    color: "#333",
    fontWeight: "700",
    fontSize: 18,
  },
});