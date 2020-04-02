#!/bin/bash

cd tables/

cat > UploadFiles.sh <<EOF
#!/bin/bash
source $CMTPATH/oaOfflineDatabase/v*r*/cmt/setup.sh
EOF

for f in ./*.dat; do
cat >> UploadFiles.sh <<EOF
python $CMTPATH/oaOfflineDatabase/v*r*/Linux-x86_64/database_updater.py --convert_unsigned apply_local_update $f
EOF
done

cd -
