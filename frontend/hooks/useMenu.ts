import { useEffect, useState } from "react";
import { getMenu, MenuItem } from "../api/menu";

export function useMenu(restaurant: string) {
  const [items, setItems] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    getMenu(restaurant)
      .then((data) => {
        setItems(data.items.map((item, index) => ({ ...item, index })));
      })
      .catch(setError)
      .finally(() => setLoading(false));
  }, [restaurant]);

  return { items, loading, error };
}
