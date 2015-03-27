#!/usr/bin/env bash

remote_dir=/home/coordt/backups/databases/calloway/hourly
dst=callowayproject.com
if [ -z $1 ]
then
    backup_filename=`ssh $dst ls -1td $remote_dir/\* | head -1`
else
    backup_filename=$1
fi
dst_filename=$(basename $backup_filename)
USER=postgres
DB=calloway

if [ ! -e $dst_filename ]
    then echo "File doesn't exist, retrieving."; scp $dst:$backup_filename .
fi

#dropdb $DB -U $USER -h localhost
createdb $DB -E UTF8 -U $USER -h localhost
psql -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"' $DB -U $USER -h localhost
gunzip -c $dst_filename | psql -U $USER $DB -h localhost
#rm $dst_filename
