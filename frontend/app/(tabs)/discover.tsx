import { View, Text, StyleSheet, ScrollView } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import AppHeader from "../../components/AppHeader";
import ItemCard from "../../components/ItemCard";


export default function Discover() {
  const insets = useSafeAreaInsets();

  const hues = [0, 130, 220, 30, 300]; 

  return (
    <View style={styles.container}>
      <AppHeader />
      <Text style={styles.title}>For You</Text>
      <ScrollView 
        contentContainerStyle={{
          paddingBottom: insets.bottom,
        }}
      >
    </ScrollView>
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