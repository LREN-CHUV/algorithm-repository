#!/bin/sh
# This script will be executed when Postgres starts
echo "host all all fe80::/10 md5" >> /var/lib/postgresql/data/pg_hba.conf
