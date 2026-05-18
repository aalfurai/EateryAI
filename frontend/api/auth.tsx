import { apiFetch } from "./client";
import { User } from "../types/user";

type LoginRequest = {
  user_id: string;
  name: string;
};

type RegisterRequest = {
  user_id: string;
  name: string;
  // no options to set contraints or weights in demo
  constraints?: User["constraints"];
  weights?: User["weights"];
}

type SessionResponse = {
  token: string;
  user: User;
};

const registerUser = (req: RegisterRequest) =>
  apiFetch<SessionResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(req),
  });

const loginUser = (req: LoginRequest) =>
  apiFetch<SessionResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(req),
  });

export const login = async (req: LoginRequest): Promise<SessionResponse> => {
  try {
    console.log("Attempting login for:", req.user_id);
    return await loginUser(req);
  } catch {
    console.log("Login failed, registering:", req.user_id);
    return await registerUser(req);
  }
};