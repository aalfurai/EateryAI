import { createContext, useContext, useState } from "react";
import { User } from "../types/user";

type UserContextType = {
  user: User;
  setUser: (user: User) => void;
  updateConstraints: (patch: Partial<User["constraints"]>) => void;
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User>();

  const updateConstraints = (patch: Partial<User["constraints"]>) => {
    if (user) {
      setUser({
        ...user,
        constraints: {
          ...user.constraints,
          ...patch,
        },
      });
    }
  };

  return (
    <UserContext.Provider value={{ user: user as User, setUser, updateConstraints }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used within UserProvider");
  return context;
}