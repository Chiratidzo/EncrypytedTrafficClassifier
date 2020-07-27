from ndpi import get_labels
import os

FILE_DIR = 'SampleFlows'

for file in os.listdir(FILE_DIR + "/tcp_syn"):
    path = FILE_DIR + "/" + "tcp_syn" + "/" + file
    print(get_labels(path))

# print(get_labels("SampleFlows/tcp_syn/10.2.83.121_41957_5.62.53.224_80_1558374588.pcap")) # HTTP


# print(get_labels("SampleFlows/tcp_syn/10.2.10.130_48239_216.58.223.74_443_1551913927.pcap")) # Google
