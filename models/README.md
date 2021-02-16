# DLOGs Honours Project – Shane Weisz
## Network Traffic Classification using Two-Dimensional Convolutional Neural Networks for Community Networks

### Overview

In this component of the project, we explore the effectiveness of **two-dimensional convolutional neural networks (2D-CNNs)** for the traffic classification task within the context of community networks. 2D-CNNs have been shown to demonstrate success in the packet-based classification task, as a result of their ability to learn spatial patterns in the packet data. Additionally, their characteristics of sparse interactions and parameter sharing enhance their ability to meet computational resource-usage constraints and hence their suitability to the needs of community networks. The above factors guided the choice to investigate 2D-CNNs for our use case. 

In order to evaluate the suitability of 2D-CNNs for this classification task, we compare its performance to baseline models in the form of the simpler **multi-layer perceptron (MLP)** neural network, as well as the **support vector machine (SVM)** traditional machine learning algorithm. We aim to investigate whether 2D-CNNs offer superior classification accuracy to the baseline models, as well as identify which of the models would be fast enough for real-time classification. Additionally, we will explore the tradeoff between improving prediction speed at the expense of decreasing accuracy due to reducing the proportion of a packet's payload used as input for the models. The network traffic data to be used for training and evaluating these models has been provided in the format of raw PCAP files by the Ocean View community network in Cape Town.

### Experiment 1

Experiment 1 involves comparing the models' accuracy and prediction speed across a varying number of parameters.

The five models considered are:

1.  Deep 2D-CNN (4 convolutional layers)
2.  Shallow 2D-CNN (1 convolution layer)
3.  Deep MLP (3 hidden layers)
4.  Shallow MLP (1 hidden layer)
5.  SVM (with a linear kernel)

For each model, for each number of parameters, we conduct a grid search over the hyperparameter space to select the model that attains the highest validation accuracy for that architecture and number of parameters -- by running the corresponding notebook stored in the `training-notebooks` folder. The validation results and model description for each of these trained models are stored in respective CSVs in the `training-results` folder.

Thereafter, the `experiment2_script.py` script is run to compute the test accuracy and average prediction speed for each model for each number of parameters, with the results saved to `Exp1_Results.csv` in the `experiment-results` folder. Finally, run `experiment2_plots.py` to create summary plots of the results, stored as PNGs in the `experiment-results` folder.

### Experiment 2

Experiment 2 varies the number of bytes of each packet's payload used as model input, and evaluates the effect on the deep 2D-CNN's accuracy and prediction speeds.

The folder structure and order of running the notebooks and scripts follows in the same way as for Experiment 1.