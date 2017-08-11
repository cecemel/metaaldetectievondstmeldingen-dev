FROM postgres:9.6
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

ENV POSTGIS_MAJOR 2.3
ENV POSTGIS_VERSION 2.3.3+dfsg-1.pgdg80+1

RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
           postgis=$POSTGIS_VERSION \
      && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./scripts/ /docker-entrypoint-initdb.d/

