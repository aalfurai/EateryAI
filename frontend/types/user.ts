import { Weights } from "./weights";
import { Constraints } from "./constraints";

export type User = {
  user_id: string;
  name: string;
  constraints: Constraints;
  weights: Weights;
};