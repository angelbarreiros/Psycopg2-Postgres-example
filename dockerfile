FROM postgres:latest
COPY CreateTables.sql docker-entrypoint-initdb.d/a.sql
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=vicon