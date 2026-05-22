/* Weight presets for different user preferences */
import { Weights } from "../types/weights";

export const weightPresets: Record<string, Weights> = {
  bodybuilder: {
    price: 0.10,
    calories: 0.15,
    protein: 0.55,

    fiber: 0.07,
    sugar: 0.05,
    sodium: 0.03,

    drink_cal: 0.03,
    addon_cal: 0.02,
  },

  budgeter: {
    price: 0.50,
    calories: 0.20,
    protein: 0.15,

    fiber: 0.05,
    sugar: 0.04,
    sodium: 0.03,

    drink_cal: 0.02,
    addon_cal: 0.01,
  },

  dieting: {
    price: 0.15,
    calories: 0.40,
    protein: 0.25,

    fiber: 0.08,
    sugar: 0.07,
    sodium: 0.03,

    drink_cal: 0.015,
    addon_cal: 0.015,
  },

  balanced: {
    price: 0.20,
    calories: 0.25,
    protein: 0.25,

    fiber: 0.10,
    sugar: 0.08,
    sodium: 0.05,
    
    drink_cal: 0.04,
    addon_cal: 0.03,
  },
};