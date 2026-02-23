-- =========================
-- Schema
-- =========================
CREATE SCHEMA IF NOT EXISTS eateryai_test1;
COMMENT ON SCHEMA eateryai_test1 IS 'first test schema for EateryAI data';

-- =========================
-- Restaurants
-- =========================
CREATE TABLE eateryai_test1.restaurants (
    restaurant_id uuid PRIMARY KEY,
    restaurant_name text NOT NULL,
    menu_card_image text
);

-- =========================
-- Menu Items
-- =========================
CREATE TABLE eateryai_test1.menu_items (
    item_id text PRIMARY KEY,
    menu_item_id uuid UNIQUE NOT NULL,
    restaurant_id uuid NOT NULL,
    menu_item_name text NOT NULL,
    category text NOT NULL,
    price numeric NOT NULL,
    golden_ratio numeric NOT NULL,
    ai_description text NOT NULL,
    CONSTRAINT menu_items_restaurant_id_fkey
        FOREIGN KEY (restaurant_id)
        REFERENCES eateryai_test1.restaurants (restaurant_id)
);

-- =========================
-- Allergens (lookup)
-- =========================
CREATE TABLE eateryai_test1.allergens (
    allergen_id integer PRIMARY KEY,
    allergen_name text UNIQUE NOT NULL
);

-- =========================
-- Menu Item ↔ Allergens (join)
-- =========================
CREATE TABLE eateryai_test1.menu_item_allergens (
    id integer PRIMARY KEY,
    item_id text NOT NULL,
    allergen_id integer NOT NULL,
    allergen_status text,
    CONSTRAINT menu_item_allergens_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES eateryai_test1.menu_items (item_id),
    CONSTRAINT menu_item_allergens_allergen_id_fkey
        FOREIGN KEY (allergen_id)
        REFERENCES eateryai_test1.allergens (allergen_id)
);

-- =========================
-- Menu Item Cuisines
-- =========================
CREATE TABLE eateryai_test1.menu_item_cuisines (
    id integer PRIMARY KEY,
    cuisine_type text NOT NULL,
    item_id text NOT NULL,
    CONSTRAINT menu_item_cuisines_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES eateryai_test1.menu_items (item_id)
);

-- =========================
-- Menu Item Macronutrients
-- =========================
CREATE TABLE eateryai_test1.menu_item_macronutrients (
    id integer PRIMARY KEY,
    macronutrient_tag text NOT NULL,
    item_id text NOT NULL,
    CONSTRAINT menu_item_macronutrients_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES eateryai_test1.menu_items (item_id)
);

-- =========================
-- Nutrition Info (1–to–1)
-- =========================
CREATE TABLE eateryai_test1.nutrition_info (
    item_id text PRIMARY KEY,
    serving_size text,
    calories integer,
    cholesterol integer,
    sodium integer,
    total_carbohydrates integer,
    dietary_fiber integer,
    sugars integer,
    protein integer,
    potassium integer,
    total_fat integer,
    CONSTRAINT nutrition_info_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES eateryai_test1.menu_items (item_id)
);

-- =========================
-- Allergen Metadata (1–to–1)
-- =========================
CREATE TABLE eateryai_test1.allergen_metadata (
    item_id text PRIMARY KEY,
    allergy_info text,
    disclaimer text,
    dietary_info jsonb,
    CONSTRAINT allergen_metadata_item_id_fkey
        FOREIGN KEY (item_id)
        REFERENCES eateryai_test1.menu_items (item_id)
);

-- =========================
-- Indexes
-- =========================
CREATE INDEX menu_item_cuisines_item_id_idx
    ON eateryai_test1.menu_item_cuisines (item_id);

CREATE INDEX menu_item_macronutrients_item_id_idx
    ON eateryai_test1.menu_item_macronutrients (item_id);