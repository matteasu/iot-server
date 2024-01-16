CREATE TYPE "user_kind" AS ENUM (
  'normal',
  'privileged'
);

CREATE TABLE "Users" (
  "id" integer PRIMARY KEY NOT NULL,
  "name" char(50) NOT NULL,
  "surname" char(50) NOT NULL,
  "kind" user_kind NOT NULL,
  "device_id" integer,
  "last_location" integer,
  "last_read" timestamp
);

CREATE TABLE "Devices" (
  "id" integer PRIMARY KEY,
  "mac_address" char(17) UNIQUE NOT NULL,
  "enabled" bool DEFAULT false
);

CREATE TABLE "Rooms" (
  "id" integer PRIMARY KEY NOT NULL,
  "name" char(50) UNIQUE NOT NULL,
  "kind" user_kind NOT NULL
);

CREATE TABLE "Logs" (
  "id" integer PRIMARY KEY NOT NULL,
  "timestamp" timestamp NOT NULL,
  "action" integer NOT NULL,
  "room" integer NOT NULL,
  "user" intege NOT NULL
);

ALTER TABLE "Users" ADD FOREIGN KEY ("device_id") REFERENCES "Devices" ("id");

ALTER TABLE "Users" ADD FOREIGN KEY ("last_location") REFERENCES "Rooms" ("id");

ALTER TABLE "Logs" ADD FOREIGN KEY ("room") REFERENCES "Rooms" ("id");

ALTER TABLE "Logs" ADD FOREIGN KEY ("user") REFERENCES "Users" ("id");
