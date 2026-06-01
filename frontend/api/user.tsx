import { apiFetch } from "./client";
import { User } from "../types/user";

type ConstraintPatch = Partial<User["constraints"]>;

type ConstraintResponse = {
  message: string;
  constraints: User["constraints"];
};

export const updateUserConstraints = (
  token: string,
  constraints: ConstraintPatch
) =>
  apiFetch<ConstraintResponse>("/user/constraints", {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(constraints),
  });