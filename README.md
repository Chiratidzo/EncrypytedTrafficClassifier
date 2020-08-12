<br>
<img src="logo.png" alt="DLOGs" width="400"/>

# DLOGs Honours Project 
## A Comparative Evaluation of Deep Learning Approaches to Online Network Traffic Classification for Community Networks

### Overview

The goal of the project is to build Deep Learning network traffic packet classifiers for the purposes of Quality of Service (QoS) and traffic engineering in community networks. PCAP files collected from the Ocean View community network will be used for training and testing of the models. 

The first stage of the project involves preprocessing the raw PCAP files into a suitable format for training and testing - the output of this stage are `train.csv` and `test.csv` files with rows being the 1480 bytes of each packet's IP payload and the corresponding ground-truth label. The second stage involves building classification models - these include SVM and MLP models as baselines, and then more sophisticated 1D-CNN, 2D-CNN and LSTM RNN deep learning models.

### Project stages

#### 1) Preprocessing

1. Use *pkt2flow* to split raw PCAP files into flows

    1. Install [pkt2flow](https://github.com/caesar0301/pkt2flow).

        ```bash
        cd preprocessing/flow-extraction
        git clone https://github.com/caesar0301/pkt2flow
        ```

    2.  Run the `extract-packets` script.
        ```bash
        bash extract-packets.sh
        ```
        

2. Label the packets in each flow by running *nDPI* on each flow.

    1. Install [ndpi](https://github.com/ntop/nDPI), and follow the instructions for compilation.

        ```bash
        cd preprocessing/labelling/
        git clone https://github.com/ntop/nDPI.git
        ```
        To compile nDPI:
        ```bash
        cd ndpi/
        ./autogen.sh
        ./configure
        make
        ```

    2. Run the `labelling` script.
        ```bash
        cd labelling/
        bash labelling.sh
        ```

3. Extract the label and 1480 bytes of the IP payload for each packet, into `data.csv`.
    
    ```bash
    cd preprocessing/packet-byte-extraction
    python3 packet_byte_extractor.py
    ```
4. Create `train.csv` and `test.csv` files each containing packet-label pairs.

    ```bash
    cd preprocessing/train-test-data-construction
    python3 train_test_splitter.py
    ```

#### 2) Models

- Baseline models:
    -   Support Vector Machine (SVM)
    -   Multi-layer Perceptron (MLP)

- Deep learning models:
    -   LSTM RNN
    -   1D-CNN
    -   2D-CNN