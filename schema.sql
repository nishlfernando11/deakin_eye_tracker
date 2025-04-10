
CREATE TABLE IF NOT EXISTS eye_tracker_data
(
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT timezone('UTC', NOW()),
    event_time double precision NOT NULL,
    unix_timestamp double precision NOT NULL,
    lsl_timestamp double precision NOT NULL,
    round_id text COLLATE pg_catalog."default" NOT NULL,
    player_id text COLLATE pg_catalog."default" NOT NULL,
    uid TEXT NOT NULL,
    eye_tracker_data json,
    CONSTRAINT fk_round_ecg FOREIGN KEY (id) REFERENCES rounds (id)
);
END;