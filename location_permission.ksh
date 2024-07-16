#!/usr/bin/ksh
emails='syed.ahmed5@verizon.com','suresh.k.raman@verizon.com','akhila.sivakoti@verizon.com','sriram.krshna@verizon.com','deepakkumar.patnala@verizon.com','snehal.kulkarni@verizon.com'
start_time=`date '+%D %I:%M%p'`
subject_date=`date '+%m/%d/%Y'`
subject_time=`date '+%I:%M %p'`
Load_time=`date '+%m/%d/%Y %I:%M %p'`
echo "Started at $start_time"


echo "Logging of location Permission started."
cd /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin
python api_permission.py > log/api_permission.txt

echo "Logging of location Permission ended."

end_time=`date '+%m/%d/%Y %I:%M %p'`
echo "________________Process#1(Postgres)________________________________"
(echo "Hi All,
Attached are logs of the Location Permission
Load start time :  $Load_time
Load End time : $end_time"  ; uuencode /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/api_permission.txt api_permission.txt) | mailx -s "Status of Location Permission post migration  at $subject_time  on $subject_date" $emails
echo "Sent mail."
echo "----------Thank you. ALL FINISHED---------------------"

