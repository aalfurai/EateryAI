import { useEffect, useState } from "react";
import { searchRestaurants, Restaurant } from "../api/restaurant";

export function useRestaurantSearch(query: string) {
  const [results, setResults] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    setLoading(true);

    searchRestaurants(query)
      .then((data) => {
        setResults(Array.isArray(data) ? data : []);
      })
      .catch(setError)
      .finally(() => setLoading(false));
  }, [query]);

  return { results, loading, error };
}