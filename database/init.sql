-- public.medications_info definition
CREATE TABLE public.medications_info (
	medication_id serial4 PRIMARY KEY,
	name text NOT NULL,
	dosage text NULL
);

-- public.user_medications_info definition
CREATE TABLE public.user_medications_info (
	user_email text,
	medication_name text,
	exp_date text,
	created_at timestamptz DEFAULT current_timestamp
);

-- public.users definition
CREATE TABLE public.users (
	user_id serial4 PRIMARY KEY,
	email text UNIQUE NOT NULL,
	password text NOT NULL,
	created_at timestamptz DEFAULT current_timestamp
);

-- Function to add user medication info
CREATE OR REPLACE FUNCTION public.add_user_medication_info(user_email text, medication_name text, exp_date text)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Check if the user_email and medication_name are not null
    IF user_email IS NULL OR medication_name IS NULL THEN
        RAISE EXCEPTION 'User email and medication name cannot be null.';
    END IF;

    INSERT INTO user_medications_info (user_email, medication_name, exp_date)
    VALUES (user_email, medication_name, exp_date);
END;
$function$;

-- Function to check password
CREATE OR REPLACE FUNCTION public.check_password(user_email text, provided_password text)
 RETURNS boolean
 LANGUAGE plpgsql
AS $function$
DECLARE
    stored_password text;
BEGIN
    -- Check if the user_email and provided_password are not null
    IF user_email IS NULL OR provided_password IS NULL THEN
        RAISE EXCEPTION 'User email and provided password cannot be null.';
    END IF;

    SELECT password INTO stored_password FROM users WHERE email = user_email;

    -- Check if the password matches
    RETURN stored_password = provided_password;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN FALSE; -- User not found
END;
$function$;

-- Function to get all medications info
CREATE OR REPLACE FUNCTION public.get_all_medications_info()
 RETURNS TABLE(user_email text, medication_name text, exp_date text, created_at timestamptz)
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT * FROM public.user_medications_info;
END;
$function$;

-- Function to get all users
CREATE OR REPLACE FUNCTION public.get_all_users()
 RETURNS SETOF text
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY SELECT email FROM public.users;
END;
$function$;

-- Function to get user medications info
CREATE OR REPLACE FUNCTION public.get_user_medications_info(p_user_email text)
 RETURNS TABLE(user_email text, medication_name text, exp_date text, created_at timestamptz)
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Check if the user_email is not null
    IF p_user_email IS NULL THEN
        RAISE EXCEPTION 'User email cannot be null.';
    END IF;

    RETURN QUERY
    SELECT
        umi.user_email,
        umi.medication_name,
        umi.exp_date,
        umi.created_at
    FROM
        public.user_medications_info umi
    WHERE
        umi.user_email = p_user_email;
END;
$function$;

-- Function to insert user
CREATE OR REPLACE FUNCTION public.insert_user(user_email text, user_password text)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    existing_user_count INTEGER;
BEGIN
    -- Check if the user_email and user_password are not null
    IF user_email IS NULL OR user_password IS NULL THEN
        RAISE EXCEPTION 'User email and password cannot be null.';
    END IF;

    -- Check if the user already exists
    SELECT COUNT(*) INTO existing_user_count
    FROM users
    WHERE email = user_email;

    IF existing_user_count = 0 THEN
        INSERT INTO users (email, password)
        VALUES (user_email, user_password);

        RETURN 'New user created successfully.';
    ELSE
        RETURN 'Error: Email already exists.';
    END IF;
END;
$function$;

-- Function to remove user medication info
CREATE OR REPLACE FUNCTION public.remove_user_medication_info(p_user_email text, p_medication_name text, p_exp_date text)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Check if the user_email, medication_name, and exp_date are not null
    IF p_user_email IS NULL OR p_medication_name IS NULL OR p_exp_date IS NULL THEN
        RAISE EXCEPTION 'User email, medication name, and expiration date cannot be null.';
    END IF;

    DELETE FROM user_medications_info
    WHERE user_email = p_user_email AND medication_name = p_medication_name AND exp_date = p_exp_date;
END;
$function$;
