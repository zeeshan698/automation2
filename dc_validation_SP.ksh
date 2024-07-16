#!/usr/bin/ksh
#Include posgtres configurations
. ./config/postgres_config.ksh

psql -h $pg_hostname  -p $pg_port -U $pg_username -d $pg_database <<EOF
DO
\$\$DECLARE
BEGIN
   CALL migr.validation_dc_track();
END;\$\$
EOF

