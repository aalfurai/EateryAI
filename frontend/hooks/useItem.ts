import { useEffect, useState } from "react";
import { getItem } from "../api/item";
import { MenuItem } from "../api/menu";

export function useItem(restaurant: string, item_id: string) {
  const [item, setItem] = useState<MenuItem>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    getItem(restaurant, item_id)
      .then(setItem)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [restaurant, item_id]);

  return { item, loading, error };
}
