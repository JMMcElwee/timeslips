#!/bin/bash

cd tables

if [[ ! -z $ND280SYS ]]
then
    echo -e "\e[34;1m[INFO]\e[0m \$ND280SYS set to" $ND280SYS
    # Find the upload script. Saves on hardcoding the position
    UPLOADER=$(find $ND280SYS/oaOfflineDatabase/*/Linux* -name "database_updater.py")
else 
    echo -e "\e[31;1m[ERROR]\e[0m Please set \$ND280SYS to point at your ND280 build."
    return;
fi

cat > UploadFiles.sh <<EOF
#!/bin/bash
source $CMTPATH/oaOfflineDatabase/v*r*/cmt/setup.sh
EOF

for f in ./*.dat; do
cat >> UploadFiles.sh <<EOF
python $UPLOADER --convert_unsigned apply_local_update $f
EOF
done

cd -
