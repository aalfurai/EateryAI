import { Stack } from "expo-router";

export default function Layout() {
  return (
    <Stack 
      screenOptions={{
      contentStyle: { backgroundColor: '#1C1C1E' },
      headerStyle: { backgroundColor: '#1C1C1E' },
      headerTintColor: 'white',
    }}/>
  );
}