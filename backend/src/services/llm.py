import os
from google import genai
from dotenv import load_dotenv
from schemas.user import User
from schemas.restaurant import Restaurant

load_dotenv()

_client = None

def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set in environment")
        _client = genai.Client(api_key=api_key)
    return _client


def _build_index_map(restaurant: Restaurant) -> dict[int, str]:
    index_to_name = {}
    for items in restaurant.menu.values():
        for item in items:
            index_to_name[item["index"]] = item["menu_item_name"]
    return index_to_name


def _resolve_by_category(meal: dict, index_to_name: dict[int, str]) -> dict[str, list[str]]:
    result = {}
    for field, label in [("Entree_ids", "Entree"), ("Side_ids", "Side"), ("Drink_ids", "Drink"), ("Addon_ids", "Add-On"), ("Dessert_ids", "Dessert")]:
        names = [index_to_name[idx] for idx in meal.get(field, []) if idx in index_to_name]
        if names:
            result[label] = names
    return result


def _get_seed_context(seed_id: str | None, restaurant: Restaurant) -> tuple[str | None, str | None]:
    """Returns (seed_item_name, seed_category) if a seed was provided, else (None, None)."""
    if not seed_id:
        return None, None
    items = restaurant.menu.get(seed_id, [])
    if not items:
        return None, None
    item = items[0]
    return item["menu_item_name"], item["category"]


def generate_meal_summary(user: User, meals: list[dict], restaurant: Restaurant, seed_id: str | None = None) -> str:
    if not meals:
        return ""

    try:
        index_to_name = _build_index_map(restaurant)
        c = user.constraints

        top = meals[0]
        by_cat = _resolve_by_category(top, index_to_name)

        category_lines = "\n".join(
            f"  {label}: {', '.join(names)}" for label, names in by_cat.items()
        )

        lines = [
            f"Restaurant: {restaurant.name}",
            f"User targets: {c.calories} cal, {c.protein}g protein, ${c.price:.2f} budget",
            f"Top meal breakdown:\n{category_lines}",
            f"Total: {top['total_cal']} cal · {top['total_protein']}g protein · ${top['total_price']:.2f}",
        ]
        if len(meals) > 1:
            lines.append(f"Alternative options available: {len(meals) - 1}")

        seed_name, seed_category = _get_seed_context(seed_id, restaurant)

        if seed_name is None:
            framing = (
                "The AI built this entire meal from scratch — the user didn't pick any specific item. "
                "Write as 'we put together a [adj] meal for you at [restaurant]: [items]'. "
                "Highlight how it fits their targets."
            )
        elif seed_category == "Entree":
            framing = (
                f"The user chose the {seed_name} (entree). The AI added the sides and drinks. "
                "Frame it as 'we paired your [entree] with [side/drink]' to make clear the AI chose the additions."
            )
        else:
            framing = (
                f"The user chose the {seed_name} ({seed_category.lower()}). The AI filled in the rest of the meal. "
                f"Frame it as 'we built a meal around your {seed_name} with [rest of items]'."
            )

        prompt = (
            "You are a friendly meal assistant for EatAI. "
            f"{framing} "
            "Write a short 2-3 sentence response. "
            "Mention how the totals compare to the user's targets. "
            "If alternatives are available, end with one brief sentence about them. "
            "Plain text only — no markdown, no bullet points.\n\n"
            + "\n".join(lines)
        )

        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        return response.text.strip()

    except Exception as e:
        print(f"LLM summary error: {e}")
        return ""
