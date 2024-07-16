#!/usr/bin/ksh
emails='syed.ahmed5@verizon.com','suresh.k.raman@verizon.com','akhila.sivakoti@verizon.com','sriram.krshna@verizon.com','deepakkumar.patnala@verizon.com','snehal.kulkarni@verizon.com'
start_time=`date '+%Y%m%d-%H%M'`
end_time=`date '+%Y%m%d_%H%M'`
Load_time=`date '+%m/%d/%Y %I:%M %p'`
load_end_time=`date '+%m/%d/%Y %I:%M %p'`
email_date=`date '+%m/%d/%Y'`
email_time=`date '+%I:%M %p'`

cd /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/data_split
rm -f *.csv

echo "Started at $start_time"
echo "started breaking PIMS Extracted csv files into smaller chunks"
cd /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin
python split_csv_file.py > log/split_csv_file.txt
echo "Finished breaking PIMS Extracted csv files into smaller chunks"

(echo "Hi All,
Files breaking started  at $Load_time
Files breaking finished at $load_end_time
Broken files can be found in /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/data_split
Attached are logs of the Extracted PIMS csv files into smaller chunks"  ; uuencode /apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin/log/split_csv_file.txt split_csv_file.txt) | mailx -s "Status of breaking PIMS Extracted csv files into smaller chunks at $email_time on $email_date" $emails
echo "All  files are splitted and found in data_split folder."
echo "Sent mail."
echo "----------Thank you. ALL FINISHED---------------------"

