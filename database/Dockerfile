FROM postgres:latest
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_USER=username
ENV POSTGRES_DB=IOT
COPY IOT.sql /docker-entrypoint-initdb.d/IOT.sql
