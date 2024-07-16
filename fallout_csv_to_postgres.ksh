#!/usr/bin/ksh
emails='syed.ahmed5@verizon.com'
start_time=`date '+%D %I:%M%p'`
subject_date=`date '+%m/%d/%Y'`
subject_time=`date '+%I:%M %p'`
Load_time=`date '+%m/%d/%Y %I:%M %p'`
echo "Started at $start_time"


echo "Loading fallout CSV into Postgres."
cd /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin
python fallout_csv_to_postgres.py > log/fallout_csv_to_postgres.txt

echo "Loading fallout CSV into Postgres finished."


echo "_________________Process#1(Postgres)_______________________________"
#Include posgtres configurations
. ./config/postgres_config.ksh
echo "Started loading CSV logging counts into stat summary table."
psql -h $pg_hostname  -p $pg_port -U $pg_username -d $pg_database -c "\COPY stg.conv_stat_summary_log FROM '/apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/csv_fallout_import_to_postgres.csv' delimiter ',' csv header;"
echo "Finished loading CSV logging counts into stat summary table. Please review."

end_time=`date '+%m/%d/%Y %I:%M %p'`
echo "________________Process#2(Postgres)________________________________"
(echo "Hi All,
Attached are logs of the data load to Staging DB from the fallout CSV'S
Load start time :  $Load_time
Load End time : $end_time"  ; uuencode /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/fallout_csv_to_postgres.txt fallout_csv_to_postgres.txt) | mailx -s "Status of fallout data  load to Staging DB  at $subject_time  on $subject_date" $emails
echo "Sent mail."
echo "----------Thank you. ALL FINISHED---------------------"
