import os
from scapy.all import *
import time

def main():

    # dictionary with the number of packets per label
    packets_per_label = {}

    # getting a list with the labels already used
    labels_used = []

    # setting the labels that we want to exclude
    excluded_labels = ['HTTP', 'SSDP', 'Unknown', 'TLS', 'HTTP_Proxy']

    # set the file path
    cwd = os.getcwd()
    directory_path = 'data/flows/'

    start_time = time.time()

    # get the path to the labels.csv
    labels_file_path = 'data/labels.csv'

    # open the file for writing
    f_write = open('data/data.csv', 'w')

    # write the headers
    header = ['label']
    for i in range(1, 1481):
        header.append('byte'+str(i))
    f_write.write(','.join(header)+'\n')

    # get the number of flows for display purposes
    if os.path.exists(labels_file_path):
        with open(labels_file_path) as f_read:
            num_flows = sum(1 for row in f_read)
    else:
        print('Could not find labels.csv')

    count = 0
    if os.path.exists(labels_file_path):
        with open(labels_file_path) as f_read:

            for line in f_read:
                if count == 0:  # skip header row
                    count += 1
                    continue

                split_line = line.split(',')

                # get the file path, labels and num packets from csv
                file_path = split_line[0]
                label = split_line[1]

                # if the label has not been used yet initialize
                if label not in labels_used:
                    packets_per_label[label] = 1
                    labels_used.append(label)

                num_packets = split_line[2]
                file_path = directory_path + file_path

                # process the pcap file
                if label not in excluded_labels:
                    packets_per_label = label_packets(
                        file_path, label, f_write, packets_per_label)
                else:
                    print('({}/{}) - {} ({}) has been skipped'.format(count,
                                                                      num_flows,
                                                                      file_path,
                                                                      label))
                    count += 1
                    continue

                print('({}/{}) - {} ({}) has been processed'.format(count,
                                                                    num_flows,
                                                                    file_path,
                                                                    label))
                count += 1
    else:
        print('Could not find labels.csv')

    end_time = time.time()
    print('Total time to run: {}'.format(end_time-start_time))

    # close file for reading
    f_read.close()

    # close file for writing
    f_write.close()


def label_packets(file_path, label, f_write, packets_per_label):
    '''
    param file_path (String): Path to the pcap file
    param label(String): Label for each packet in the flow 
    '''
    # packets per label = 100 000
    maximum_packets = 100000

    # This value will determine how many packets per flow(with payload) to sample
    # set to ALL to sample all packets in a flow
    if packets_per_label[label] < maximum_packets:
        packets = 0
        packets_per_flow = 10000
        count_packets_per_flow = 0
        if os.path.exists(file_path):
            data = sniff(offline=file_path)
            #print('Read {}'.format(file_path))
            for pkt in data:
                if count_packets_per_flow <= packets_per_flow:
                    if pkt.haslayer(IP) and pkt.haslayer(Raw):
                        hex_data = linehexdump(
                            pkt[IP].payload, onlyhex=1, dump=True).split(" ")
                        decimal_data = list(map(hex_to_dec, hex_data))
                        # print(decimal_data)
                        f_write.write(label+','+','.join(decimal_data))
                        f_write.write('\n')

                        packets_per_label[label] += 1
                    else:
                        continue
                else:
                    break
                count_packets_per_flow += 1

        else:
            print('Could not find {}'.format(file_path))

    return packets_per_label


def hex_to_dec(hex):
    return str(int(hex, base=16))


if __name__ == '__main__':
    main()
