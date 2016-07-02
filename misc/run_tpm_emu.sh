TPM_EMU_DIR=/home/butla/development/tpm-emulator
cd ${TPM_EMU_DIR}

sudo insmod build/tpmd_dev/linux/tpmd_dev.ko
sudo tpmd
sudo tcsd