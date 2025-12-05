#!/bin/bash
# Script de inicialización para el servidor primario de PostgreSQL

set -e

# Crear usuario de replicación
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
    CREATE DATABASE ecomarket;
EOSQL

echo "Usuario de replicación creado exitosamente"
