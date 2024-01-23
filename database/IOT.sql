CREATE TYPE "user_kind" AS ENUM (
  'normal',
  'privileged'
);

CREATE TABLE "Users" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" char(50) NOT NULL,
  "surname" char(50) NOT NULL,
  "kind" user_kind NOT NULL,
  "device_id" integer UNIQUE ,
  "last_location" integer,
  "last_read" timestamp
);

CREATE TABLE "Devices" (
  "id" SERIAL PRIMARY KEY,
  "mac_address" char(17) UNIQUE NOT NULL,
  "enabled" bool DEFAULT false
);

CREATE TABLE "Rooms" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" char(50) UNIQUE NOT NULL,
  "kind" user_kind NOT NULL,
  "num_employees" integer DEFAULT 0,
  "num_customers" integer DEFAULT 0
);

CREATE TABLE "Logs" (
  "id" SERIAL PRIMARY KEY NOT NULL ,
  "timestamp" timestamp NOT NULL,
  "action" integer NOT NULL,
  "room" integer NOT NULL,
  "user" integer
);

ALTER TABLE "Users" ADD FOREIGN KEY ("device_id") REFERENCES "Devices" ("id");

ALTER TABLE "Users" ADD FOREIGN KEY ("last_location") REFERENCES "Rooms" ("id");

ALTER TABLE "Logs" ADD FOREIGN KEY ("room") REFERENCES "Rooms" ("id");

ALTER TABLE "Logs" ADD FOREIGN KEY ("user") REFERENCES "Users" ("id");

INSERT INTO public."Rooms" (id, name, kind)
VALUES (default, 'Main Hall', 'normal');
INSERT INTO public."Rooms" (id, name, kind)
VALUES (default, 'Entrance Hall', 'normal');
INSERT INTO public."Rooms" (id, name, kind)
VALUES (default, 'Consulting Room', 'normal');
INSERT INTO public."Rooms" (id, name, kind)
VALUES (default, 'Vault', 'privileged');
INSERT INTO public."Users" (id,name,surname,kind)
VALUES (default,'Enzo','Rossi','normal');
INSERT INTO public."Users" (id,name,surname,kind)
VALUES (default,'Mario','Rossi','privileged')

