--
-- PostgreSQL database dump
--

\restrict TXrdv1dfPZFSEtWNdFfjrJnh7h7bXO3ikJopQwQ7zvwC6yov0Be4yC1M5Zty6vp

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: EateryAI Test1; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "EateryAI Test1";


ALTER SCHEMA "EateryAI Test1" OWNER TO postgres;

--
-- Name: SCHEMA "EateryAI Test1"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA "EateryAI Test1" IS 'first test schema for EateryAI data';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: allergen_metadata; Type: TABLE; Schema: EateryAI Test1; Owner: postgres
--

CREATE TABLE "EateryAI Test1".allergen_metadata (
    item_id text NOT NULL,
    allergy_info text,
    disclaimer text,
    dietary_info jsonb
);


ALTER TABLE "EateryAI Test1".allergen_metadata OWNER TO postgres;

--
-- Name: allergens; Type: TABLE; Schema: EateryAI Test1; Owner: postgres
--

CREATE TABLE "EateryAI Test1".allergens (
    allergen_id integer NOT NULL,
    allergen_name text NOT NULL
);


ALTER TABLE "EateryAI Test1".allergens OWNER TO postgres;

--
-- Name: menu_item_allergens; Type: TABLE; Schema: EateryAI Test1; Owner: postgres
--

CREATE TABLE "EateryAI Test1".menu_item_allergens (
    id integer NOT NULL,
    item_id text,
    allergen_id integer,
    allergen_status text
);


ALTER TABLE "EateryAI Test1".menu_item_allergens OWNER TO postgres;

--
-- Name: menu_item_cuisines; Type: TABLE; Schema: EateryAI Test1; Owner: postgres
--

CREATE TABLE "EateryAI Test1".menu_item_cuisines (
    id integer NOT NULL,
    cuisine_type text NOT NULL,
    item_id text NOT NULL
);


ALTER TABLE "EateryAI Test1".menu_item_cuisines OWNER TO postgres;

--
-- Name: menu_item_macronutrients; Type: TABLE; Schema: EateryAI Test1; Owner: postgres
--

CREATE TABLE "EateryAI Test1".menu_item_macronutrients (
    id integer NOT NULL,
    macronutrient_tag text NOT NULL,
    item_id text NOT NULL
);


ALTER TABLE "EateryAI Test1".menu_item_macronutrients OWNER TO postgres;

--
-- Name: menu_items; Type: TABLE; Schema: EateryAI Test1; Owner: postgres
--

CREATE TABLE "EateryAI Test1".menu_items (
    item_id text NOT NULL,
    menu_item_id uuid NOT NULL,
    restaurant_id uuid NOT NULL,
    menu_item_name text NOT NULL,
    category text NOT NULL,
    price numeric NOT NULL,
    golden_ratio numeric NOT NULL,
    ai_description text NOT NULL
);


ALTER TABLE "EateryAI Test1".menu_items OWNER TO postgres;

--
-- Name: nutrition_info; Type: TABLE; Schema: EateryAI Test1; Owner: postgres
--

CREATE TABLE "EateryAI Test1".nutrition_info (
    item_id text NOT NULL,
    serving_size text,
    calories integer NOT NULL,
    sodium integer,
    total_carbohydrates integer,
    dietary_fiber integer,
    sugars integer,
    protein integer NOT NULL,
    potassium integer,
    total_fat integer
);


ALTER TABLE "EateryAI Test1".nutrition_info OWNER TO postgres;

--
-- Name: restaurants; Type: TABLE; Schema: EateryAI Test1; Owner: postgres
--

CREATE TABLE "EateryAI Test1".restaurants (
    restaurant_id uuid NOT NULL,
    restaurant_name text NOT NULL,
    menu_card_image text
);


ALTER TABLE "EateryAI Test1".restaurants OWNER TO postgres;

--
-- Data for Name: allergen_metadata; Type: TABLE DATA; Schema: EateryAI Test1; Owner: postgres
--

COPY "EateryAI Test1".allergen_metadata (item_id, allergy_info, disclaimer, dietary_info) FROM stdin;
\.


--
-- Data for Name: allergens; Type: TABLE DATA; Schema: EateryAI Test1; Owner: postgres
--

COPY "EateryAI Test1".allergens (allergen_id, allergen_name) FROM stdin;
\.


--
-- Data for Name: menu_item_allergens; Type: TABLE DATA; Schema: EateryAI Test1; Owner: postgres
--

COPY "EateryAI Test1".menu_item_allergens (id, item_id, allergen_id, allergen_status) FROM stdin;
\.


--
-- Data for Name: menu_item_cuisines; Type: TABLE DATA; Schema: EateryAI Test1; Owner: postgres
--

COPY "EateryAI Test1".menu_item_cuisines (id, cuisine_type, item_id) FROM stdin;
\.


--
-- Data for Name: menu_item_macronutrients; Type: TABLE DATA; Schema: EateryAI Test1; Owner: postgres
--

COPY "EateryAI Test1".menu_item_macronutrients (id, macronutrient_tag, item_id) FROM stdin;
\.


--
-- Data for Name: menu_items; Type: TABLE DATA; Schema: EateryAI Test1; Owner: postgres
--

COPY "EateryAI Test1".menu_items (item_id, menu_item_id, restaurant_id, menu_item_name, category, price, golden_ratio, ai_description) FROM stdin;
\.


--
-- Data for Name: nutrition_info; Type: TABLE DATA; Schema: EateryAI Test1; Owner: postgres
--

COPY "EateryAI Test1".nutrition_info (item_id, serving_size, calories, sodium, total_carbohydrates, dietary_fiber, sugars, protein, potassium, total_fat) FROM stdin;
\.


--
-- Data for Name: restaurants; Type: TABLE DATA; Schema: EateryAI Test1; Owner: postgres
--

COPY "EateryAI Test1".restaurants (restaurant_id, restaurant_name, menu_card_image) FROM stdin;
\.


--
-- Name: allergen_metadata allergen_metadata_pkey; Type: CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".allergen_metadata
    ADD CONSTRAINT allergen_metadata_pkey PRIMARY KEY (item_id);


--
-- Name: allergens allergens_pkey; Type: CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".allergens
    ADD CONSTRAINT allergens_pkey PRIMARY KEY (allergen_id);


--
-- Name: menu_item_allergens menu_item_allergens_pkey; Type: CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".menu_item_allergens
    ADD CONSTRAINT menu_item_allergens_pkey PRIMARY KEY (id);


--
-- Name: menu_item_cuisines menu_item_cuisines_pkey; Type: CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".menu_item_cuisines
    ADD CONSTRAINT menu_item_cuisines_pkey PRIMARY KEY (id);


--
-- Name: menu_item_macronutrients menu_item_macronutrients_pkey; Type: CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".menu_item_macronutrients
    ADD CONSTRAINT menu_item_macronutrients_pkey PRIMARY KEY (id);


--
-- Name: menu_items menu_items_pkey; Type: CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".menu_items
    ADD CONSTRAINT menu_items_pkey PRIMARY KEY (item_id);


--
-- Name: nutrition_info nutrition_info_pkey; Type: CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".nutrition_info
    ADD CONSTRAINT nutrition_info_pkey PRIMARY KEY (item_id);


--
-- Name: restaurants restaurants_pkey; Type: CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".restaurants
    ADD CONSTRAINT restaurants_pkey PRIMARY KEY (restaurant_id);


--
-- Name: fki_item; Type: INDEX; Schema: EateryAI Test1; Owner: postgres
--

CREATE INDEX fki_item ON "EateryAI Test1".menu_item_macronutrients USING btree (item_id);


--
-- Name: fki_item_id; Type: INDEX; Schema: EateryAI Test1; Owner: postgres
--

CREATE INDEX fki_item_id ON "EateryAI Test1".menu_item_cuisines USING btree (item_id);


--
-- Name: menu_item_macronutrients_item_id_index; Type: INDEX; Schema: EateryAI Test1; Owner: postgres
--

CREATE INDEX menu_item_macronutrients_item_id_index ON "EateryAI Test1".menu_item_macronutrients USING btree (item_id);


--
-- Name: allergen_metadata allergen_metadata_item_id_fkey; Type: FK CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".allergen_metadata
    ADD CONSTRAINT allergen_metadata_item_id_fkey FOREIGN KEY (item_id) REFERENCES "EateryAI Test1".menu_items(item_id) NOT VALID;


--
-- Name: menu_item_allergens menu_item_allergens_allergen_id_fkey; Type: FK CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".menu_item_allergens
    ADD CONSTRAINT menu_item_allergens_allergen_id_fkey FOREIGN KEY (allergen_id) REFERENCES "EateryAI Test1".allergens(allergen_id) NOT VALID;


--
-- Name: menu_item_cuisines menu_item_cuisines_item_id_fkey; Type: FK CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".menu_item_cuisines
    ADD CONSTRAINT menu_item_cuisines_item_id_fkey FOREIGN KEY (item_id) REFERENCES "EateryAI Test1".menu_items(item_id) NOT VALID;


--
-- Name: menu_item_macronutrients menu_item_macronutrients_item_id_fkey; Type: FK CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".menu_item_macronutrients
    ADD CONSTRAINT menu_item_macronutrients_item_id_fkey FOREIGN KEY (item_id) REFERENCES "EateryAI Test1".menu_items(item_id) NOT VALID;


--
-- Name: menu_items menu_items_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".menu_items
    ADD CONSTRAINT menu_items_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES "EateryAI Test1".restaurants(restaurant_id) NOT VALID;


--
-- Name: nutrition_info nutrition_info_item_id_fkey; Type: FK CONSTRAINT; Schema: EateryAI Test1; Owner: postgres
--

ALTER TABLE ONLY "EateryAI Test1".nutrition_info
    ADD CONSTRAINT nutrition_info_item_id_fkey FOREIGN KEY (item_id) REFERENCES "EateryAI Test1".menu_items(item_id) NOT VALID;


--
-- PostgreSQL database dump complete
--

\unrestrict TXrdv1dfPZFSEtWNdFfjrJnh7h7bXO3ikJopQwQ7zvwC6yov0Be4yC1M5Zty6vp

