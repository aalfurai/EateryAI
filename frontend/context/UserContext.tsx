import { createContext, useContext, useState } from "react";
import { User } from "../types/user";
import { updateUserConstraints } from "../api/user";

type UserContextType = {
  user: User;
  setUser: (user: User) => void;
  updateConstraints: (patch: Partial<User["constraints"]>) => void;
  token: string | null;
  setToken: (token: string | null) => void;
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User>();
  const [token, setToken] = useState<string | null>(null);

  const updateConstraints = async (
    patch: Partial<User["constraints"]>
  ) => {
    if (!user || !token) return;

    const updatedConstraints = {
      ...user.constraints,
      ...patch,
    };

    setUser({
      ...user,
      constraints: updatedConstraints,
    });

    try {
      const response = await updateUserConstraints(
        token,
        updatedConstraints
      );

      setUser({
        ...user,
        constraints: response.constraints,
      });
    } catch (err) {
      console.error("Failed to update constraints", err);
    }
  };

  return (
    <UserContext.Provider value={{ user: user as User, setUser, updateConstraints, token, setToken }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used within UserProvider");
  return context;
}
