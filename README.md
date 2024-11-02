
# YOLO Detection with IPFS and AWS Lambda Integration

This repository provides a setup to run YOLO-based object detection, integrated with IPFS for decentralized file storage, and an AWS Lambda function for managing detections via API Gateway. Follow the steps below to set up and run the project.
---
- [Clone the Repository](#clone-the-repository)
- [Set Up Virtual Environment](#set-up-virtual-environment)
- [Install Dependencies](#install-dependencies)
- [Prepare YOLO Models](#prepare-yolo-models)
- [Install IPFS](#install-ipfs)
- [Set Up DynamoDB and CLI](#set-up-dynamodb-and-cli)
- [Create AWS Lambda Function](#create-aws-lambda-function)
- [Run Detection and Control Station](#run-detection-and-control-station)
---

### Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/wepandas4/Crime-Detection.git
cd Crime-Detection
```

### Set Up Virtual Environment
Make sure you have Python 3.11 installed on your system. Then, create a virtual environment:

```bash
python3.11 -m venv venv
venv\Scripts\activate  # On Linux, use `source venv/bin/activate`
```

### Install Dependencies
With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### Prepare YOLO Models
1. Create a directory to store your YOLO models:

    ```bash
    mkdir models
    ```

2. Place your YOLO model files in the `models` directory. Ensure they are correctly named and compatible with the code.

### Install IPFS
Install IPFS Desktop and IPFS CLI (also known as IPFS Kubo) as follows:

1. **Download IPFS Desktop** from [IPFS Desktop Downloads](https://docs.ipfs.io/install/ipfs-desktop/).

2. **Install IPFS Kubo (CLI):**
   - Follow the official instructions for installing Kubo from [IPFS Kubo](https://docs.ipfs.io/how-to/command-line-quick-start/).
   - Once installed, you can initialize IPFS with the following command:
     ```bash
     ipfs init
     ```
   - To start the IPFS daemon:
     ```bash
     ipfs daemon
     ```

### Set Up DynamoDB and CLI
1. **Create a DynamoDB Table:**
   - Go to the [AWS DynamoDB Console](https://console.aws.amazon.com/dynamodb).
   - Create a new table with the desired primary key and attributes according to your project requirements.

2. **Install AWS CLI:**
   - Follow the instructions on [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
   - Configure the AWS CLI with your credentials:
     ```bash
     aws configure
     ```
   - You can now manage DynamoDB and other AWS services from the command line.

### Create AWS Lambda Function
1. **Create a Lambda Function:**
   - In the [AWS Lambda Console](https://console.aws.amazon.com/lambda/), create a new Lambda function.
   - Upload `lambda_function.py` as the function code for processing.
   - Set up an API Gateway trigger for the function, which will allow it to be called via HTTP requests.

2. **Integrate Lambda in Control Station**:
   - Use the API Gateway endpoint in `Control Station/app.py` to connect the Lambda function for API calls from the application.

### Run Detection and Control Station
1. Start the main detection script:
    ```bash
    python main.py
    ```

2. Run the Control Station (Flask app):
    ```bash
    cd Control\ Station
    flask run
    ```

3. After detection completes, stop `main.py` by terminating the process.

---

Your setup is complete! You can now start detecting objects with YOLO and manage results through the Control Station interface.
```

Just replace `<your-repo-url>` and `<your-repo-name>` with the appropriate values for your project. This file should cover all the necessary steps for setup and usage.
