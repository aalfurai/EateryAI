import { Stack } from "expo-router";

export default function Layout() {
  return (
    <Stack 
      screenOptions={{
        contentStyle: { backgroundColor: '#010000' },
        headerShown: false,
    }}>
    </Stack>
  );
}