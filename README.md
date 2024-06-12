# Realtime Food Delivery Insights

This repository contains a real-time data analysis project for a food delivery service. It leverages AWS technologies for data ingestion, processing, storage, and visualization: Airflow, Kinesis Data Streams for real-time data ingestion, Redshift as a data warehouse, Spark Streaming on EMR for real-time data processing.

# Realtime Food Delivery Insights

## Table of Contents 

1. [Description](#description)
2. [Architecture](#architecture)
3. [Dataset](#dataset)
4. [Methodology](#methodology)
   - [Creating and Populating S3 Buckets](#creating-and-populating-s3-buckets)
   - [Data Ingestion with Kinesis](#data-ingestion-with-kinesis)
   - [Real-Time Processing with EMR and Spark Streaming](#real-time-processing-with-emr-and-spark-streaming)
   - [Data Storage in Redshift](#data-storage-in-redshift)
   - [Visualization with QuickSight](#visualization-with-quicksight)
5. [Modular Code Overview](#modular-code-overview)
   - [Python Simulation Script](#python-simulation-script)
   - [Airflow DAGs](#airflow-dags)

## Description

This project demonstrates a robust architecture for real-time data analysis in a food delivery service, utilizing various AWS services to simulate, ingest, process, store, and visualize data.

## Architecture

The architecture includes the following components:

- S3: Storage for input datasets and intermediate results.
- Python Simulation App: Generates simulated order data.
- Kinesis Data Streams: Captures real-time data streams.
- EMR with Spark Streaming: Processes data in real time.
- Redshift: Serves as the data warehouse.
- QuickSight: Provides data visualization and insights.

## Dataset

The dataset consists of several CSV files representing different entities in the food delivery service, such as customers, restaurants, and delivery riders.

## Methodology

### Creating and Populating S3 Buckets

To begin, you need to create S3 buckets and populate them with the necessary datasets. This can be done using AWS CLI commands.

1. **Download Data Files**:
    Download the CSV files from this repository to your local machine.
2. **Create S3 Buckets**:
   Open your terminal and run the following commands to create the buckets:
   ```bash
   aws s3api create-bucket --bucket airflow-managed-gds --region us-east-1
   aws s3api create-bucket --bucket food-delivery-data-analysis --region us-east-1
   ```
3. **Upload Data Files to S3**:
   ***Directory Structure***
   Assuming you have the following directory structure:
   ```scss
   .
   ├── dags
   │   └── (DAG files)
   ├── data_for_dims
   │   └── (Data files for dimensions)
   ├── scripts
   │   └── (PySpark scripts)
   └── jars
    └── (Redshift JAR files)
   ```
   ***Bash Script for Uploading Data***
   Save the following script in a file named `upload_data.sh`:
   ```bash
   #!/bin/bash
   # Subir archivos DAG a S3
   echo "Copying DAG files to S3..."
   aws s3 cp --recursive ./dags s3://airflow-managed-gds/dags/
   # Subir archivos de datos para dimensiones a S3
   echo "Copying dim data files to S3..."
   aws s3 cp --recursive ./data_for_dims s3://food-delivery-data-analysis/dims/
   # Subir scripts PySpark a S3
   echo "Copying pyspark scripts to S3..."
   aws s3 cp --recursive ./scripts s3://food-delivery-data-analysis/pyspark_script/
   # Subir archivo JAR de Redshift a S3
   echo "Copying redshift jar file to S3..."
   aws s3 cp --recursive ./jars s3://food-delivery-data-analysis/redshift-connector-jar/
   echo "Data upload complete!"
   ```
   ***Execute the Bash Script***
   ```sh
   chmod +x upload_data.sh
   ```
   ***Run the script from your terminal:***
   ```sh
   ./upload_data.sh
   ```
   ***Explanation of Commands***
   **Create Buckets:**
   - `aws s3api create-bucket --bucket airflow-managed-gds --region us-east-1`: Creates a bucket named airflow-managed-gds in the us-east-1 region.
   - `aws s3api create-bucket --bucket food-delivery-data-analysis --region us-east-1`: Creates a bucket named food-delivery-data-analysis in the us-east-1 region.
   **Upload Data:**
   - `aws s3 cp --recursive ./dags s3://airflow-managed-gds/dags/`: Copies all files and directories inside ./dags to the dags folder in the airflow-managed-gds bucket.
   - `aws s3 cp --recursive ./data_for_dims s3://food-delivery-data-analysis/dims/`: Copies all files and directories inside `./data_for_dims` to the dims folder in the food-delivery-data-analysis bucket.
   - `aws s3 cp --recursive ./scripts s3://food-delivery-data-analysis/pyspark_script/`: Copies all files and directories inside `./scripts` to the pyspark_script folder in the food-delivery-data-analysis bucket.
   - `aws s3 cp --recursive ./jars s3://food-delivery-data-analysis/redshift-connector-jar/`: Copies all files and directories inside `./jars` to the redshift-connector-jar folder in the food-delivery-data-analysis bucket.

### Data Ingestion with Kinesis

Set up Kinesis Data Streams to capture and manage real-time data streams from the Python simulation app.

1. **Create Kinesis Stream**:
    ```bash
    aws kinesis create-stream --stream-name incoming-food-order-data --shard-count 1
    ```

2. **Run Python Simulation Script**:
    Ensure your Python script is configured to send data to the Kinesis stream.

### Real-Time Processing with EMR and Spark Streaming

Use EMR with Spark Streaming to process the incoming data from Kinesis Data Streams in real time.

1. **Create EMR Cluster**:
    ```bash
    aws emr create-cluster --name "EMR Cluster for Streaming" --release-label emr-6.3.0 --applications Name=Spark --instance-type m5.xlarge --instance-count 3 --use-default-roles
    ```

2. **Add Steps to EMR Cluster**:
    ```bash
    aws emr add-steps --cluster-id <your-cluster-id> --steps Type=Spark,Name="Spark Streaming Step",Args=[--deploy-mode,cluster,--packages,com.qubole.spark:spark-sql-kinesis_2.12:1.2.0_spark-3.0,io.github.spark-redshift-community:spark-redshift_2.12:6.2.0-spark_3.5,--jars,s3://food-delivery-data-analysis/redshift-connector-jar/redshift-jdbc42-2.1.0.12.jar,s3://food-delivery-data-analysis/pyspark_script/pyspark_streaming.py,--redshift_user,<redshift_user>,--redshift_password,<redshift_password>,--aws_access_key,<aws_access_key>,--aws_secret_key,<aws_secret_key>]
    ```

### Data Storage in Redshift

Load the processed data into Redshift for further analysis and querying.

1. **Create Redshift Tables**:
    Use SQL scripts to create the necessary tables in Redshift.

    ```sql
    CREATE SCHEMA IF NOT EXISTS food_delivery_datamart;
    CREATE TABLE food_delivery_datamart.dimCustomers (
        CustomerID INT PRIMARY KEY,
        CustomerName VARCHAR(255),
        CustomerEmail VARCHAR(255),
        CustomerPhone VARCHAR(50),
        CustomerAddress VARCHAR(500),
        RegistrationDate DATE
    );
    CREATE TABLE food_delivery_datamart.dimRestaurants (
        RestaurantID INT PRIMARY KEY,
        RestaurantName VARCHAR(255),
        CuisineType VARCHAR(100),
        RestaurantAddress VARCHAR(500),
        RestaurantRating DECIMAL(3,1)
    );
    CREATE TABLE food_delivery_datamart.dimDeliveryRiders (
        RiderID INT PRIMARY KEY,
        RiderName VARCHAR(255),
        RiderPhone VARCHAR(50),
        RiderVehicleType VARCHAR(50),
        VehicleID VARCHAR(50),
        RiderRating DECIMAL(3,1)
    );
    CREATE TABLE food_delivery_datamart.factOrders (
        OrderID INT PRIMARY KEY,
        CustomerID INT REFERENCES food_delivery_datamart.dimCustomers(CustomerID),
        RestaurantID INT REFERENCES food_delivery_datamart.dimRestaurants(RestaurantID),
        RiderID INT REFERENCES food_delivery_datamart.dimDeliveryRiders(RiderID),
        OrderDate TIMESTAMP WITHOUT TIME ZONE,
        DeliveryTime INT,
        OrderValue DECIMAL(8,2),
        DeliveryFee DECIMAL(8,2),
        TipAmount DECIMAL(8,2),
        OrderStatus VARCHAR(50)
    );
    ```

2. **Load Data into Redshift**:
    Use `COPY` commands to load data from S3 to Redshift tables.

    ```sql
    COPY food_delivery_datamart.dimCustomers
    FROM 's3://food-delivery-data-analysis/dims/dimCustomers.csv'
    IAM_ROLE 'arn:aws:iam::<aws-account-id>:role/<redshift-role>'
    CSV
    IGNOREHEADER 1
    QUOTE '"';
    
    COPY food_delivery_datamart.dimRestaurants
    FROM 's3://food-delivery-data-analysis/dims/dimRestaurants.csv'
    IAM_ROLE 'arn:aws:iam::<aws-account-id>:role/<redshift-role>'
    CSV
    IGNOREHEADER 1
    QUOTE '"';
    
    COPY food_delivery_datamart.dimDeliveryRiders
    FROM 's3://food-delivery-data-analysis/dims/dimDeliveryRiders.csv'
    IAM_ROLE 'arn:aws:iam::<aws-account-id>:role/<redshift-role>'
    CSV
    IGNOREHEADER 1
    QUOTE '"';
    ```

### Visualization with QuickSight

Utilize QuickSight to create dashboards and visualizations for the data stored in Redshift.

1. **Create QuickSight Data Source**:
    Connect QuickSight to your Redshift cluster.

2. **Create QuickSight Dashboards**:
    Use the connected data source to create visualizations and dashboards.

