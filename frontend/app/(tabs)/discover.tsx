import { View, Text, StyleSheet } from "react-native";
import AppHeader from "../../components/AppHeader";

export default function Placeholder() {
  return (
    <View style={styles.container}>
      <AppHeader />
      <Text style={styles.title}>For You</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#010000",
  },
  title: {
    fontSize: 22,
    fontWeight: "700",
    textAlign: "center",
    color: "white",
    marginHorizontal: 16,
    marginTop: 8,
    marginBottom: 8,
  },
})