CREATE TABLE IF NOT EXISTS eye_tracker_data
(
    id serial NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    event_time double precision NOT NULL,
    unix_timestamp double precision NOT NULL,
    lsl_timestamp double precision NOT NULL,
    round_id text COLLATE pg_catalog."default" NOT NULL,
    player_id text COLLATE pg_catalog."default" NOT NULL,
    eye_tracker_data json,
    CONSTRAINT eye_tracker_data_pkey PRIMARY KEY (id)
);
END;