import { View, Text, StyleSheet } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useUser } from "../../context/UserContext";
import ProfileHeader from "../../components/ProfileHeader";

export default function Placeholder() {
  const { user } = useUser();
  return (
    <LinearGradient
      colors={["#010000", "#19192C"]}
      style={styles.container}
    >
      <ProfileHeader username={user?.name}/>
      <View>
        <Text>Coming soon</Text>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#010000",
  },
})