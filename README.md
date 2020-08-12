<br>
<img src="logo.png" alt="DLOGs" width="400"/>

# DLOGs Honours Project 
## A Comparative Evaluation of Deep Learning Approaches to Online Network Traffic Classification for Community Networks

### Overview

The goal of the project is to 

### Pipeline

#### 1) Preprocessing

1. Use *pkt2flow* to split raw PCAP files into flows

    1. Install [pkt2flow](https://github.com/caesar0301/pkt2flow).

        ```bash
        cd preprocessing/
        git clone https://github.com/caesar0301/pkt2flow
        ```

    2.  Run the `extract-packets` script.
        ```bash
        bash extract-packets.sh
        ```
        

2. Label the packets in each flow by running *nDPI* on each flow.

    1. Install [ndpi](https://github.com/ntop/nDPI), and follow the instructions for compilation.

        ```bash
        cd preprocessing/
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
    cd packet-byte-extraction
    python3 packet_byte_extractor.py
    ```
4. Create `train.csv` and `test.csv` files each containing packet-label pairs.

    ```bash
    cd train-test-data-construction
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