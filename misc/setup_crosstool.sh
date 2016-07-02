#!/bin/bash

# configuration
CROSSTOOL_VERSION="1.19.0"
TOOLCHAIN_NAME="armv6-rpi-linux-gnueabi"
TOOLCHAIN_CFG_LOCATION="/home/$(whoami)/${TOOLCHAIN_NAME}-config"

# install necessaary software
sudo apt-get -y install libssl-dev openssh-server pkg-config build-essential curl gcc g++
sudo apt-get -y install bison flex gperf libtool texinfo gawk automake
sudo apt-get -y install subversion git-core
sudo apt-get -y install autoconf autotools-dev libncurses-dev

# get crosstool-ng
wget "http://crosstool-ng.org/download/crosstool-ng/crosstool-ng-${CROSSTOOL_VERSION}.tar.bz2"
tar xjf "crosstool-ng-${CROSSTOOL_VERSION}.tar.bz2"
rm "crosstool-ng-${CROSSTOOL_VERSION}.tar.bz2"
cd "crosstool-ng-${CROSSTOOL_VERSION}"

# configure and make crosstool
./configure
make
sudo make install

# create predefined toolchain for raspberry
mkdir -p ${TOOLCHAIN_CFG_LOCATION}
cd ${TOOLCHAIN_CFG_LOCATION}
ct-ng ${TOOLCHAIN_NAME}
ct-ng ${CT_NG_COMMAND} build

# remove directory with configuration for creating the toolchain
cd ..
rm -rf ${TOOLCHAIN_CFG_LOCATION}
