#!/usr/bin/ksh
emails='syed.ahmed5@verizon.com','suresh.k.raman@verizon.com','akhila.sivakoti@verizon.com','sriram.krshna@verizon.com','deepakkumar.patnala@verizon.com','snehal.kulkarni@verizon.com'
start_time=`date '+%Y%m%d-%H%M'`
end_time=`date '+%Y%m%d_%H%M'`
Load_time=`date '+%m/%d/%Y %I:%M %p'`
load_end_time=`date '+%m/%d/%Y %I:%M %p'`
email_date=`date '+%m/%d/%Y'`
email_time=`date '+%I:%M %p'`


echo "Started at $start_time"
echo "started loading  Error files to postgres"
cd /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin
python postgres_import_errorfile.py > log/postgres_import_errorfile.txt
echo "Finished laoding Error files to postgres"

(echo "Hi All,
loading Error Files started  at $Load_time
loding  Error Files ended at $load_end_time
Error files stages to the tables can be found in reporting schema
Attached are logs of the Error files loaded to Postgres tables"  ; uuencode /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/postgres_import_errorfile.txt postgres_import_errorfile.txt) | mailx -s "Status of loading Error files to postgres table at $email_time on $email_date" $emails
echo "All Error files are loaded into postgres tables."
echo "Sent mail."
echo "----------Thank you. ALL FINISHED---------------------"

