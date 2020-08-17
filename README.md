<br>
<img src="logo.png" alt="DLOGs" width="400"/>

# DLOGs Honours Project 
## A Comparative Evaluation of Deep Learning Approaches to Online Network Traffic Classification for Community Networks

### Overview

The goal of the project is to build Deep Learning network traffic packet classifiers for the purposes of Quality of Service (QoS) and traffic engineering in community networks. PCAP files collected from the Ocean View community network will be used for training and testing of the models. 

The first stage of the project involves preprocessing the raw PCAP files into a suitable format for training and testing - with the outputs of this stage being `train.csv`, `val.csv` and `test.csv` files with each row consisting of the 1480 bytes of a packet's IP payload and the packet's corresponding ground-truth label (payloads are zero-padded if they are less than 1480 bytes). The second stage involves building classification models - these include SVM and MLP models as baselines, and then more sophisticated 1D-CNN, 2D-CNN and LSTM RNN deep learning models.

### Project stages

#### 1) Preprocessing

##### Summary:

1. Use *pkt2flow* to split the packets contained in raw PCAP files into flows (each flow will be saved in an individual PCAP file).
2. Label the packets in each flow by running *nDPI* on each flow.
3. Extract the label and 1480 bytes of the IP payload for each packet into `data.csv`.
4. Create `train.csv`, `val.csv` and `test.csv` files each containing packet-label pairs.

If the necessary prerequisites are met (*pkt2flow* installed and compiled inside the `flow-splitting` folder, *nDPI* installed and compiled inside the `labelling` folder, and a set of raw PCAP files stored in the folder `data/raw_pcaps`), then the following script can be run to conduct the entire preprocessing pipeline:

```bash
bash preprocessor.sh
```

##### Step-by-step details for the preprocessing process:

1. Use *pkt2flow* to split raw PCAP files into flows

    1. Prerequisite installs:

        - The `libpcap` library:
        
        ```bash
        sudo apt install -y libpcap-dev
        ```

        - The SCons sofware construction tool:

        ```bash
        sudo apt install -y scons
        ```

        Assumption:

        The data to be used (PCAP files) is stored in the `preprocessing/data/raw_pcaps` directory.

    2. Install [pkt2flow](https://github.com/caesar0301/pkt2flow) in the `flow-splitting` directory.

        ```bash
        cd preprocessing/flow-splitting
        git clone https://github.com/caesar0301/pkt2flow
        ```

        To compile pkt2flow:
        ```bash
        cd pkt2flow
        scons
        ```

    3.  Run the `flow-splitter.sh` script from within the `preprocessing` directory.
        ```bash
        bash flow-splitting/flow-splitter.sh
        ```
        

2. Label the packets in each flow by running *nDPI* on each flow.

    1. Prerequisites:

        - GNU tools (autogen, automake, autoconf, libtool)
        - GNU C compiler (gcc)

    2. Install [ndpi](https://github.com/ntop/nDPI) in the `labelling` directory, and follow the instructions for compilation.

        ```bash
        cd preprocessing/labelling/
        git clone https://github.com/ntop/nDPI.git
        ```
        To compile nDPI:
        ```bash
        cd nDPI/
        ./autogen.sh
        ./configure
        make
        ```

    2. Run the `labelling` script from within the `preprocessing` directory.
        ```bash
        bash labelling/labelling.sh
        ```

3. Extract the label and 1480 bytes of the IP payload for each packet into `data.csv` (run from within the `preprocessing` directory).
    
    ```bash
    python3 packet-byte-extraction/packet_byte_extractor.py
    ```

4. Create `train.csv`, `val.csv` and `test.csv` files each containing packet-label pairs (run from within the `preprocessing` directory).

    ```python3
    python3 train-val-test-data-construction/train-val-test-splitter.py
    ```

    Note that the labels to use (e.g Facebook, WhatsApp etc.), and the number of packets per label to sample, are defined at the top of the `train-val-test-splitter.py` script.

*Please note: each step requires the previous step to have been completed first, i.e., each stage in the preprocessing process requires the output of the previous stage as its input*.

#### 2) Models

- Baseline models:
    -   Support Vector Machine (SVM)
    -   Multi-layer Perceptron (MLP)

- Deep learning models:
    -   LSTM RNN
    -   1D-CNN
    -   2D-CNN