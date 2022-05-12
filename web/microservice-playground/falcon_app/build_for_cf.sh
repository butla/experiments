MB_VERSION=mountebank-v1.2.122-linux-x64
MB_TAR=${MB_VERSION}.tar.gz
TOOLS_DIR=tools

if [ ! -d ${TOOLS_DIR}/${MB_VERSION} ]; then
    mkdir -p ${TOOLS_DIR}
    wget https://s3.amazonaws.com/mountebank/v1.2/${MB_TAR}
    tar -xf ${MB_TAR} -C ${TOOLS_DIR}
    rm ${MB_TAR}
fi;

tox

exit $?
