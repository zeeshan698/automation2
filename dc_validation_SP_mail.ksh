#!/usr/bin/ksh
emails='syed.ahmed5@verizon.com','suresh.k.raman@verizon.com','akhila.sivakoti@verizon.com','sriram.krshna@verizon.com','deepakkumar.patnala@verizon.com','snehal.kulkarni@verizon.com'
start_time=`date '+%D %I:%M%p'`
subject_date=`date '+%m/%d/%Y'`
subject_time=`date '+%I:%M %p'`
Load_time=`date '+%m/%d/%Y %I:%M %p'`
echo "Started at $start_time"


echo "log files."
#Include posgtres configurations
. ./config/postgres_config.ksh
psql -h $pg_hostname  -p $pg_port -U $pg_username -d $pg_database <<EOF
\o log/dctrack_validation_logs.txt
SELECT * FROM stg.conv_activity_n_stats_log where program_name = 'validation_dc_track';
\o
\q
EOF

end_time=`date '+%m/%d/%Y %I:%M %p'`
(echo "Hi All,
Attached are logs of dc track validation
Load start time :  $Load_time
Load End time : $end_time"  ; uuencode /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/dctrack_validation_logs.txt dctrack_validation_logs.txt ; uuencode /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/data/validation_evidence.csv validation_evidence.csv ) | mailx -s "Status of Dc Track validation  at $subject_time  on $subject_date" $emails
echo "Sent mail."
echo "----------Thank you. ALL FINISHED---------------------"

