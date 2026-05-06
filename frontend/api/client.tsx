import { Platform } from "react-native";

declare const process: { env: Record<string, string | undefined> };

/** Android emulator → your PC is 10.0.2.2, not 127.0.0.1. iOS simulator / Expo web → 127.0.0.1. Physical phone → set EXPO_PUBLIC_API_URL to http://YOUR_PC_IP:8000 */
const DEV_HOST = Platform.OS === "android" ? "http://10.0.2.2:8000" : "http://127.0.0.1:8000";
const BASE_URL = (process.env.EXPO_PUBLIC_API_URL ?? DEV_HOST).replace(/\/$/, "");

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  return res.json() as Promise<T>;
}
