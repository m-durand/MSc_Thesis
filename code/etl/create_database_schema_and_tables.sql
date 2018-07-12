-- Create the necessary user - best to keep things neat and tidy!
-- password to be provided separately
-- CREATE ROLE experiments WITH LOGIN PASSWORD '';
-- ALTER ROLE experiments CREATEDB;

-- Database: reinforcement_learning

-- DROP DATABASE reinforcement_learning;

CREATE DATABASE reinforcement_learning
    WITH 
    OWNER = experiments
    ENCODING = 'UTF8'
    -- LC_COLLATE = 'English_United States.1252'
    -- LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- SCHEMA: policy_iteration

-- DROP SCHEMA policy_iteration ;

CREATE SCHEMA policy_iteration
    AUTHORIZATION experiments;

-- Table: policy_iteration.agent_parameters

DROP TABLE policy_iteration.agent_parameters;

CREATE TABLE policy_iteration.agent_parameters
(
    experiment_id character(56) COLLATE pg_catalog."default" NOT NULL,
    agent character(20) COLLATE pg_catalog."default" NOT NULL,
    initial_inventory integer NOT NULL,
    buying_price integer NOT NULL,
    selling_price integer NOT NULL,
    CONSTRAINT agent_parameters_pkey PRIMARY KEY (experiment_id, agent)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE policy_iteration.agent_parameters
    OWNER to experiments;

-- Table: policy_iteration.experiment_results

DROP TABLE policy_iteration.experiment_results;

CREATE TABLE policy_iteration.experiment_results
(
    experiment_id character(56) COLLATE pg_catalog."default" NOT NULL,
    agent character(20) COLLATE pg_catalog."default" NOT NULL,
    best_payout character varying COLLATE pg_catalog."default" NOT NULL,
    best_policy character varying COLLATE pg_catalog."default" NOT NULL,
    historic_payout character varying COLLATE pg_catalog."default" NOT NULL,
    policy_inventory character varying COLLATE pg_catalog."default" NOT NULL,
    total_money double precision NOT NULL,
    CONSTRAINT experiment_results_pkey PRIMARY KEY (experiment_id, agent)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE policy_iteration.experiment_results
    OWNER to experiments;

-- Table: policy_iteration.experiments

DROP TABLE policy_iteration.experiments;

CREATE TABLE policy_iteration.experiments
(
    experiment_id character(56) COLLATE pg_catalog."default" NOT NULL,
    datetime timestamp without time zone NOT NULL,
    total_epochs integer NOT NULL,
    warmstart_proportion double precision NOT NULL,
    epsilon_greedy_converges_to double precision NOT NULL,
    elapsed_time double precision NOT NULL,
    CONSTRAINT experiments_pkey PRIMARY KEY (experiment_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE policy_iteration.experiments
    OWNER to experiments;

-- Table: policy_iteration.world_parameters

DROP TABLE policy_iteration.world_parameters;

CREATE TABLE policy_iteration.world_parameters
    (
        experiment_id character(56) COLLATE pg_catalog."default" NOT NULL,
        max_demand integer NOT NULL,
        customer_demand character varying COLLATE pg_catalog."default" NOT NULL,
        fields_supply character varying COLLATE pg_catalog."default" NOT NULL,
        warehouse_price integer NOT NULL,
        CONSTRAINT world_parameters_pkey PRIMARY KEY (experiment_id)
    )
    WITH (
        OIDS = FALSE
    )
    TABLESPACE pg_default;

ALTER TABLE policy_iteration.world_parameters
    OWNER to experiments;

-- This is needed manually to insert from python with psycopg2
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA policy_iteration TO experiments;

-- Which is equivalent to
-- GRANT ALL PRIVILEGES ON TABLE policy_iteration.agent_parameters TO experiments;
-- GRANT ALL PRIVILEGES ON TABLE policy_iteration.experiment_results TO experiments;
-- GRANT ALL PRIVILEGES ON TABLE policy_iteration.experiments TO experiments;
-- GRANT ALL PRIVILEGES ON TABLE policy_iteration.world_parameters TO experiments;
