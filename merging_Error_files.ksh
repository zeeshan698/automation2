#!/usr/bin/ksh
emails='syed.ahmed5@verizon.com','suresh.k.raman@verizon.com','akhila.sivakoti@verizon.com','sriram.krshna@verizon.com','deepakkumar.patnala@verizon.com','snehal.kulkarni@verizon.com'
start_time=`date '+%Y%m%d-%H%M'`
end_time=`date '+%Y%m%d_%H%M'`
Load_time=`date '+%m/%d/%Y %I:%M %p'`
load_end_time=`date '+%m/%d/%Y %I:%M %p'`
email_date=`date '+%m/%d/%Y'`
email_time=`date '+%I:%M %p'`


echo "Started at $start_time"
echo "started merging Error files from Dc track"
cd /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin
python merging_Error_files.py > log/merging_Error_files.txt
echo "Finished merging Error files from Dc track"

(echo "Hi All,
Error Files merging started  at $Load_time
Error Files merging finished at $load_end_time
Merged Error files can be found in /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/Error_file
Attached are logs of the Merged Error Files"  ; uuencode /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/merging_Error_files.txt merging_Error_files.txt) | mailx -s "Status of Merging Error files into one file at $email_time on $email_date" $emails
echo "All  files are Merged and  saved in Error_file folder."
echo "Sent mail."
echo "----------Thank you. ALL FINISHED---------------------"

