# Building Trust in Automotive Intrusion Detection Systems Through XAI Methods

This repository contains the implementation for my bachelor thesis project on **Explainable AI (XAI) for automotive intrusion detection systems (IDS)**.

The project investigates how explainability techniques can improve trust in AI-based IDS deployment for modern in-vehicle networks. The main idea is to build a baseline IDS model for automotive network traffic, then apply both **local** and **global** XAI methods to better understand and evaluate the model’s decisions.

## Research Question

**How can explainable AI techniques, including general methods such as LIME and SHAP, as well as IDS-specific explainability frameworks like Trustee, enhance trust in the deployment of automotive intrusion detection systems?**

## Background

Modern vehicles rely on increasingly complex in-vehicle communication networks. While traditional automotive communication was dominated by **CAN (Controller Area Network)**, modern vehicles also include **Automotive Ethernet (AE)**, which increases connectivity but also expands the attack surface.

As a result, automotive **Intrusion Detection Systems (IDS)** are becoming increasingly important. Traditional signature-based IDS approaches are limited when facing unknown or evolving attacks, so this project focuses on **AI-based IDS**. However, AI models are often difficult to interpret, which can reduce trust in their outputs. This is where **Explainable AI (XAI)** becomes important.

## Project Overview

This project consists of four main parts:

1. **Data inspection and preprocessing**
   - Process raw vehicular network traffic
   - Extract packet/message-level features
   - Convert message sequences into structured model input

2. **Baseline IDS model**
   - Train a **Temporal Convolutional Network (TCN)** for intrusion detection on automotive network traffic

3. **Explainability analysis**
   - Apply **SHAP** as a local explanation method
   - Apply **Trustee** as a global explanation framework

4. **Trust evaluation**
   - Evaluate the quality of explanations using established XAI criteria such as:
     - **Fidelity**
     - **Stability**

## Methodology

### 1. Data Representation

The model uses input sequences derived from **raw bytes of vehicular network traffic**.

Extracted features include:

- **CAN ID** (4 bytes)
- **Payload bytes** (up to 64 bytes)
- **Interface** (which CAN line the packet belongs to)
- **Protocol type** (Classical CAN vs CAN FD)
- **Message length** (before padding)
- **Timestamp differences**
  - Difference from the previous message on the same interface
  - Difference from the previous message with the same ID on the same interface

Following prior work, CAN messages can be arranged into **M × N images**, where:
- **M** = number of features
- **N** = number of messages in the sequence

### 2. Baseline Model: Temporal Convolutional Network (TCN)

A **Temporal Convolutional Network (TCN)** is used as the baseline IDS model.

Why TCN?

- Vehicular network traffic is naturally a **time series**
- TCN is effective at modelling **temporal patterns**
- It helps distinguish **real intrusions** from normal temporal variation
- It is generally **faster than RNN/LSTM** due to parallel 1D convolutions
- It is more intuitive for this task than reshaping data for a 2D CNN

### 3. Explainability Methods

#### Local XAI: SHAP
SHAP is used to explain the contribution of individual input features to a specific prediction.

It helps answer questions such as:

- Why was this particular sequence flagged as malicious?
- Which features contributed positively or negatively to the IDS decision?

#### Global XAI: Trustee
Trustee is used as a global explainability framework to reveal overall model behaviour across the dataset.

It helps answer questions such as:

- What decision patterns does the IDS learn overall?
- Which features or behaviours are generally treated as malicious?

### 4. Trust Evaluation

To assess whether the explanations are actually useful for building trust, this project evaluates explanation quality using established XAI criteria:

- **Fidelity**  
  Measures how well the explanation reflects the real behaviour of the model.

- **Stability**  
  Measures whether similar inputs produce similar explanations.

High-quality explanations should be both faithful to the model and robust to small input changes.

## Repository Structure

```text
.
├── data/                  # Raw or processed dataset files (not included if restricted)
├── src/
│   ├── preprocessing/     # Feature extraction and sequence construction
│   ├── models/            # TCN model implementation
│   ├── explainability/    # SHAP / Trustee related code
│   ├── evaluation/        # Fidelity and stability evaluation
│   └── utils/             # Helper functions
├── results/               # Figures, explanation outputs, and evaluation results
├── README.md
└── requirements.txt
