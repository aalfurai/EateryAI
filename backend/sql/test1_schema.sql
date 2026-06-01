-- 1. Wipe everything existing in that schema
DROP SCHEMA IF EXISTS eateryai_test1 CASCADE;

-- 2. Recreate the schema
CREATE SCHEMA eateryai_test1;
COMMENT ON SCHEMA eateryai_test1 IS 'First test schema for EateryAI data';

-- =========================
-- Restaurants
-- =========================
CREATE TABLE eateryai_test1.restaurants (
    restaurant_id uuid PRIMARY KEY,
    restaurant_name text NOT NULL UNIQUE,
    menu_card_image text
);

-- =========================
-- Menu Items
-- =========================
CREATE TABLE eateryai_test1.menu_items (
    item_id text PRIMARY KEY,
    menu_item_id text UNIQUE NOT NULL,
    restaurant_id uuid NOT NULL,
    menu_item_name text NOT NULL,
    category text NOT NULL,
    price numeric NOT NULL,
    golden_ratio numeric NOT NULL,
    ai_description text NOT NULL,
    CONSTRAINT menu_items_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES eateryai_test1.restaurants (restaurant_id)
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
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id text NOT NULL,
    allergen_id integer NOT NULL,
    allergen_status text,
    CONSTRAINT menu_item_allergens_item_id_fkey FOREIGN KEY (item_id) REFERENCES eateryai_test1.menu_items (item_id),
    CONSTRAINT menu_item_allergens_allergen_id_fkey FOREIGN KEY (allergen_id) REFERENCES eateryai_test1.allergens (allergen_id)
);

-- =========================
-- Menu Item Cuisines
-- =========================
CREATE TABLE eateryai_test1.menu_item_cuisines (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cuisine_type text NOT NULL,
    item_id text NOT NULL,
    CONSTRAINT menu_item_cuisines_item_id_fkey FOREIGN KEY (item_id) REFERENCES eateryai_test1.menu_items (item_id)
);

-- =========================
-- Menu Item Macronutrients
-- =========================
CREATE TABLE eateryai_test1.menu_item_macronutrients (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    macronutrient_tag text NOT NULL,
    item_id text NOT NULL,
    CONSTRAINT menu_item_macronutrients_item_id_fkey FOREIGN KEY (item_id) REFERENCES eateryai_test1.menu_items (item_id)
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
    CONSTRAINT nutrition_info_item_id_fkey FOREIGN KEY (item_id) REFERENCES eateryai_test1.menu_items (item_id)
);

-- =========================
-- Allergen Metadata (1–to–1)
-- =========================
CREATE TABLE eateryai_test1.allergen_metadata (
    item_id text PRIMARY KEY,
    allergy_info text,
    disclaimer text,
    dietary_info jsonb,
    CONSTRAINT allergen_metadata_item_id_fkey FOREIGN KEY (item_id) REFERENCES eateryai_test1.menu_items (item_id)
);

-- =========================
-- User Management
-- =========================
CREATE TABLE eateryai_test1.user_information (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE -- Added this so the index below works
);

CREATE TABLE eateryai_test1.user_preferences (
    user_id INT PRIMARY KEY,
    price_tol FLOAT NOT NULL DEFAULT 0.00,
    cal_def_tol FLOAT NOT NULL DEFAULT 0.00,
    cal_sur_tol FLOAT NOT NULL DEFAULT 0.00,
    protein_tol FLOAT NOT NULL DEFAULT 0.00,
    price_w FLOAT NOT NULL DEFAULT 0.00,
    cal_w FLOAT NOT NULL DEFAULT 0.00,
    protein_w FLOAT NOT NULL DEFAULT 0.00,
    CONSTRAINT user_prefs_user_id_fkey FOREIGN KEY (user_id) REFERENCES eateryai_test1.user_information(user_id) ON DELETE CASCADE
);

CREATE TABLE eateryai_test1.carts (
    cart_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT carts_user_id_fkey FOREIGN KEY (user_id) REFERENCES eateryai_test1.user_information(user_id) ON DELETE CASCADE
);

CREATE TABLE eateryai_test1.cart_items (
    cart_item_id SERIAL PRIMARY KEY,
    cart_id INT NOT NULL,
    item_id text NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cart_items_cart_id_fkey FOREIGN KEY (cart_id) REFERENCES eateryai_test1.carts(cart_id) ON DELETE CASCADE,
    CONSTRAINT cart_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES eateryai_test1.menu_items(item_id) ON DELETE CASCADE
);

-- =========================
-- Indexes
-- =========================
CREATE INDEX idx_username ON eateryai_test1.user_information (username);
CREATE INDEX idx_email ON eateryai_test1.user_information (email);
CREATE INDEX menu_item_cuisines_item_id_idx ON eateryai_test1.menu_item_cuisines (item_id);
CREATE INDEX menu_item_macronutrients_item_id_idx ON eateryai_test1.menu_item_macronutrients (item_id);