import { useEffect, useState } from "react";
import { searchItems, SearchItem, ItemSearchParams } from "../api/item";

export function useItemSearch(params: ItemSearchParams) {
  const [results, setResults] = useState<SearchItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const hasSearch =
      params.q?.trim() ||
      params.price_min != null ||
      params.price_max != null ||
      params.calories_min != null ||
      params.calories_max != null ||
      params.protein_min != null ||
      params.protein_max != null;

    if (!hasSearch) {
      setResults([]);
      return;
    }

    setLoading(true);

    searchItems(params)
      .then((data) => {
        setResults(Array.isArray(data) ? data : []);
      })
      .catch(setError)
      .finally(() => setLoading(false));
  }, [JSON.stringify(params)]);

  return { results, loading, error };
}