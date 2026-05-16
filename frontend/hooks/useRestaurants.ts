import { useEffect, useState } from "react";
import { getRestaurants, Restaurant } from "../api/restaurant";

export function useRestaurants() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    getRestaurants()
      .then((data) => {
        setRestaurants(data);
      })
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return { restaurants, loading, error };
}