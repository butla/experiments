#!/bin/bash

#sets up an TPM emulator and tpm tools

TPM_DIR=tpm-emulator

# TODO setup gmp from source

# tools to make the emulator
sudo apt-get -y install cmake subversion #libgmp3c2 libgmp3-dev 

# get and build the emulator
svn checkout http://svn.berlios.de/svnroot/repos/tpm-emulator/trunk ${TPM_DIR}
cd ${TPM_DIR}
mkdir build
cd build
cmake ../
sudo make
sudo make install

# basic tools (trousers needs to be first, the tpmd_dev driver can't be loaded and tpmd can't be running or there will be errors)
sudo apt-get -y install trousers tpm-tools #libengine-tpm-openssl

#setup the kernel module
#TPM_KO_DIR=/lib/modules/$(uname -r)/kernel/drivers/char/tpm
#sudo cp tpmd_dev/linux/tpmd_dev.ko ${TPM_KO_DIR}
#cd ${TPM_KO_DIR}
#sudo insmod tpmd_dev/linux/tpmd_dev.ko
#sudo depmod
#modprobe -a tpm
#modprobe -a tpm_dev


