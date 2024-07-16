#!/usr/bin/ksh
export ORACLE_HOME=/usr/lib/oracle/18.5/client64
export PATH=$ORACLE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$ORACLE_HOME/lib
export PATH=$LD_LIBRARY_PATH:$PATH

emails='syed.ahmed5@verizon.com','suresh.k.raman@verizon.com','akhila.sivakoti@verizon.com','sriram.krshna@verizon.com','deepakkumar.patnala@verizon.com','snehal.kulkarni@verizon.com'
start_time=`date '+%Y%m%d_%H%M'`
end_time=`date '+%Y%m%d_%H%M'`
email_date=`date '+%m/%d/%Y'`
email_time=`date '+%I:%M %p'`
Load_time=`date '+%m/%d/%Y %I:%M %p'`
echo "Started at $start_time"

cd /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/dctrack_csv
rm -f *.csv

echo "start generating CSV from DC track API."
cd /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin
python dc_track_api_to_csv.py > log/dc_track_csv_extraction.txt

echo "CSV generation from DC track API finished."


echo "_________________Process#3_______________________________"
#Include posgtres configurations
. ./config/postgres_config.ksh

echo "Started loading API extracted CSV logs into postgres DB."
psql -h $pg_hostname  -p $pg_port -U $pg_username -d $pg_database -c "\COPY stg.conv_activity_n_stats_log FROM '/apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/csv_logging_json.csv' delimiter ',' csv header;"
echo "Finished loading API Extracted CSV logs into postgres DB. Please review."

echo "________________Process#4________________________________"
echo "Loading DC track extracted CSV data into postgres DB."
. ./DC_track_extracted_CSV_to_postgres.ksh
echo "Finished Loading DC track extracted CSV data into postgres DB. Please review."

echo "________________Process#5________________________________"
end_time=`date '+%m/%d/%Y %I:%M %p'`
(echo "Hi All,
API Extrcation Data Extraction started  at $Load_time
API Extrcation Data Extraction  completed at $end_time
Attached are logs of the file"  ; uuencode /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/dc_track_csv_extraction.txt dc_track_csv_extraction.txt) | mailx  -s "status of dc track extracted csv to postgres DB import logs at $email_time on $email_date" $emails
echo "Sent mail."
echo "----------Thank you. ALL FINISHED---------------------"

