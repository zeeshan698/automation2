#!/usr/bin/ksh
export ORACLE_HOME=/usr/lib/oracle/18.5/client64
export PATH=$ORACLE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$ORACLE_HOME/lib
export PATH=$LD_LIBRARY_PATH:$PATH
emails='syed.ahmed5@verizon.com','suresh.k.raman@verizon.com','akhila.sivakoti@verizon.com','sriram.krshna@verizon.com','deepakkumar.patnala@verizon.com','snehal.kulkarni@verizon.com'
start_time=`date '+%D %I:%M%p'`
subject_date=`date '+%m/%d/%Y'`
subject_time=`date '+%I:%M %p'`
Load_time=`date '+%m/%d/%Y %I:%M %p'`
echo "Started at $start_time"


echo "Extraction of PIMS and WFM Tables to Postgres tables for PIMS Snapshot started."
cd /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin
python pims_snapshot.py > log/pims_snapshot.txt
echo "Finished inserting PIMS and WFM Tables to Postgres tables for PIMS Snapshot"


end_time=`date '+%m/%d/%Y %I:%M %p'`
echo "Completed at $end_time"
echo "________________(Process of Extracting from PIMS and insertions into Postgres tables completed )________________________________"
(echo "Hi All,
Attached are logs of Extraction of PIMS and WFM Tables to Postgres tables for PIMS Snapshot
Load start time :  $Load_time
Load End time : $end_time"  ; uuencode /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/pims_snapshot.txt pims_snapshot.txt) | mailx -s "Status of Extraction of PIMS and WFM Tables into Postgres tables for PIMS Snapshot  at $subject_time  on $subject_date" $emails
echo "Sent mail."
echo "----------Thank you. ALL FINISHED---------------------"

