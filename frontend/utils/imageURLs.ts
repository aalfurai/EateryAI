// since we don't have image URLs, use restaurant URL instead
export function getRestaurantImageURL(name: string) {
  const noApostrophes = name.replace(/'/g, "");
  const formattedName = noApostrophes.toLowerCase().replace(/\s+/g, "-");
  return `https://fastfoodnutrition.org/logos/${formattedName}.jpg`;
}