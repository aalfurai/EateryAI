import { Tabs } from "expo-router";

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        sceneStyle: { backgroundColor: "#1C1C1E" },
        headerStyle: { backgroundColor: "#1C1C1E" },
        headerTintColor: 'white',
        tabBarStyle: { backgroundColor: '#1C1C1E', },
        tabBarActiveTintColor: '#ffffff',
        tabBarInactiveTintColor: '#898989',
      }}
    >
      <Tabs.Screen name="index" options={{ title: "Home" }} />
      <Tabs.Screen name="discover" />
      <Tabs.Screen name="profile" />
    </Tabs>
  );
}