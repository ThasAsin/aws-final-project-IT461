# Directory Layout

**diagrams** - Contains an image of the overall architecture of the system with colored pathing

**screenshots** - Snapshots of various resources for examples of data or processes

**lambda_code** - Files for the code ran in Lambda functions

-------------------------------------

# Overview

The system is a backend for a serverless web application that allows users to upload images, automatically analyze them, and search for them later using descriptions and metadata.


All requests from the web application pass through AWS WAF and Amazon API Gateway before being handled by AWS Lambda functions. From there, the application follows one of two main workflows:

* Querying existing metadata (QM)
* Uploading and processing pictures (UPP)

-------------------------------------

## White path: Core Request Flow

Every action initiated from the web application follows this path:

User → Internet → AWS WAF → Amazon API Gateway → AWS Lambda

* AWS WAF filters unwanted traffic.
* Amazon API Gateway serves as the secure entry point for all requests.
* AWS Lambda executes backend logic.

-------------------------------------

## Orange Path: 3Query Metadata (QM)

This workflow handles searches for previously analyzed images.

### Process Flow

Main → DynamoDB → Lambda → API Gateway → Web App


### Steps

1. The user queries for characteristics of an image.
2. The request passes through WAF and API Gateway.
3. A Lambda function queries DynamoDB table.
4. Matching metadata is returned.
5. Displays the results.

#### High-Level Path

Main → QM → Main

-------------------------------------

## Red path: Upload and Process Picture (UPP)

This workflow handles image uploads and automated analysis.

### Process Flow

Main → User → S3 Raw → SQS → Lambda → Rekognition → DynamoDB → S3 Valid

### Steps
1. The user initiates an upload of an image.
2. A Lambda function generates a pre-signed URL.
3. The user uploads the image directly to the Raw S3 bucket.
4. The upload event sends a message to Amazon SQS.
6. A Lambda function processes the queued message.
7. The image is validated for inappropriate content.
8. Amazon Rekognition analyzes the image and gathers labels.
9. Metadata is stored in DynamoDB.
10. The validated image is moved to the Valid S3 bucket.

### High-Level Path

User → Main → User → UPP

-------------------------------------

## AWS Services Used

### WAF
Filters malicious or unwanted traffic before requests reach the API.

### API Gateway
Provides secure REST API endpoints for the web application.

### Lambda
Runs serverless backend functions for uploads, processing, and search.

### S3

**Raw Bucket** - Temporary upload location for newly submitted images. Unvalidated files are stored here briefly before processing.

**Valid Bucket** - Permanent storage for images that have passed validation and analysis.

### SQS
Queues image processing jobs for asynchronous execution.

### DynamoDB
Stores image metadata.

### Rekognition
Uses machine learning to detect labels and objects in images.
### VPC
Provides network isolation and organization for backend resources.
