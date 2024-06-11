# Realtime Food Delivery Insights

This repository contains a real-time data analysis project for a food delivery service. It leverages AWS technologies for data ingestion, processing, storage, and visualization: Airflow, Kinesis Data Streams for real-time data ingestion, Redshift as a data warehouse, Spark Streaming on EMR for real-time data processing.

## Table of Contents  

- [Description](#description) 
- [Architecture](#architecture)
- [Dataset](#Dataset)
- [Methodology](#Methodology)
- [Modular Code Overview](#modular-code-overview)
- [Contribution](#contribution)
- [Contact](#contact)

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

## Methodology

### Creating and Populating S3 Buckets

To begin, you need to create S3 buckets and populate them with the necessary datasets. This can be done using AWS CLI commands.

1. **Create S3 Buckets**:
    ```bash
    aws s3 mb s3://food-delivery-data-analysis
    aws s3 mb s3://food-delivery-data-analysis/dims
    ```

2. **Download Data Files**:
    Download the CSV files from this repository to your local machine.

3. **Upload Data Files to S3**:
    ```bash
    aws s3 cp path/to/dimCustomers.csv s3://food-delivery-data-analysis/dims/
    aws s3 cp path/to/dimRestaurants.csv s3://food-delivery-data-analysis/dims/
    aws s3 cp path/to/dimDeliveryRiders.csv s3://food-delivery-data-analysis/dims/
    ```

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

