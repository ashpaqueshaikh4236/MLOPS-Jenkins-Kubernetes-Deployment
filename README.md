# MLOPS-Jenkins-Kubernetes-Deployment

## Project Setup Guide

### 1. Create and Activate the Virtual Environment

Create environment with Python 3.8
```bash
conda create -n visa python=3.8 -y
```

Activate the environment
```bash
conda activate visa
```


### 2. Install Dependencies

Install required packages
```bash
pip install -r requirements.txt
```

### 3. .gitignore File

Go to the `.gitignore` file and at the end, you will find the `artifact/*` entry. Simply comment it out by adding `#` before it, right before running `dvc init`.  

```bash
artifact/*
#artifact/*
```
