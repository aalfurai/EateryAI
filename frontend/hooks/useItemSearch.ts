import { useEffect, useState } from "react";
import { searchItems, SearchItem, ItemSearchParams } from "../api/item";

export function useItemSearch(params?: ItemSearchParams | null) {
  const [results, setResults] = useState<SearchItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // do nothing if params missing
    if (!params) return;

    const hasSearch =
      params.q?.trim() ||
      params.price_min != null ||
      params.price_max != null ||
      params.calories_min != null ||
      params.calories_max != null ||
      params.protein_min != null ||
      params.protein_max != null;

    // do nothing if no valid search params
    if (!hasSearch) return;

    setLoading(true);
    setError(null);

    searchItems(params)
      .then((data) => {
        setResults(Array.isArray(data) ? data : []);
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => {
        setLoading(false);
      });

  }, [params]);

  return { results, loading, error };
}