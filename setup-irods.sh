#!/bin/bash

# Changed the iRods directory as currently the cluster has died
export iRODS_directory=/data/perry/t2k-software/iRODS
export PATH=${iRODS_directory}/clients/icommands/bin:${PATH}   
export irodsEnvFile=/data/perry/t2k-software/.irods/.irodsEnv

irodsConfigDir=${HOME}/.irods

if [[ ! -e ${irodsConfigDir} ]]
then
    echo -e "\e[34;1m[INFO]\e[0m Making irods configuration directory $irodsConfigDir"
    mkdir -p ${irodsConfigDir}
    echo -e "\e[34;1m[INFO]\e[0m Initialising client."
    iinit
fi

export irodsAuthFileName=${irodsConfigDir}/.irodsA


