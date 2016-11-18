#include <stdio.h>
#include <openssl/md5.h>

int main() {
    const unsigned char to_hash[4] = {0x70, 0x70, 0x70, 0};
    printf("%x %x %x %x\n", to_hash[0], to_hash[1], to_hash[2], to_hash[3]);
    
    unsigned char *hash = MD5(to_hash, 4, NULL);
    printf("MD5 hash of the above:\n");
    for(int i=0; i<16; i++){
        printf("%x ", hash[i]);
    }
    printf("\n");
    return 0;
}
