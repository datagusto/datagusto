--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.2 (Debian 16.2-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country (
    country_id integer PRIMARY KEY,
    country character varying(50),
    last_update timestamp without time zone
);
ALTER TABLE public.country OWNER TO postgres;


--
-- Name: city; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.city (
    city_id integer PRIMARY KEY,
    city character varying(50),
    country_id integer REFERENCES public.country(country_id),
    last_update timestamp without time zone
);
ALTER TABLE public.city OWNER TO postgres;

--
-- Data for Name: country; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.country (country_id, country, last_update) FROM stdin;
20	Canada	2006-02-15 04:44:00
50	Japan	2006-02-15 04:44:00
102	United Kingdom	2006-02-15 04:44:00
\.


--
-- Data for Name: city; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.city (city_id, city, country_id, last_update) FROM stdin;
312	London	102	2006-02-15 04:45:25
313	London	20	2006-02-15 04:45:25
376	Okayama	50	2006-02-15 04:45:25
377	Okinawa	50	2006-02-15 04:45:25
\.


--
-- PostgreSQL database dump complete
--
