echo "=== Converting Timeslips to ChannelID Format ==="
python TimeSlipConverter.py
echo "=== Producing upload tables ==="
mkdir tables
python ProduceTables.py final_timeslips_converted.txt
echo "=== Creating Upload Script ==="
source gen_upload_script.sh
echo "=== Complete ==="
echo "To upload tables run : "
echo "$ cd tables && source UploadScript.sh"

