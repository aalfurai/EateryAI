import { Stack } from "expo-router";
import { UserProvider } from "../context/UserContext";

export default function Layout() {
  return (
    <UserProvider>
      <Stack 
        screenOptions={{
          contentStyle: { backgroundColor: '#010000' },
          headerShown: false,
      }}>
      </Stack>
    </UserProvider>
  );
}