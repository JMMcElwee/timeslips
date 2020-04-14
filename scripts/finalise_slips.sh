echo -e "\e[34;1m[INFO]\e[0m Converting time slips to ChannelID format."
python TimeSlipConverter.py
echo -e "\e[34;1m[INFO]\e[0m Producing upload tables."
mkdir tables
python ProduceTables.py final_timeslips_converted.txt
echo -e "\e[34;1m[INFO]\e[0m Creating upload script."
source gen_upload_script.sh
echo -e "\e[34;1m[INFO]\e[0m Complete!"
echo -e "\e[34;1m[INFO]\e[0m To upload tables run:"
echo -e "\e[34;1m[INFO]\e[0m $ cd tables && source UploadScript.sh"
