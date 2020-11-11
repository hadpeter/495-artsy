# 495-artsy

## About
Artsy is a drawing game that gives patients a fun way to use an incentive spirometer and improve their recovery through art. By using the spirometer, users unlock paints, stensils and brushes to express their creativity on a limitless iPad canvas. Artsy will lead to improved usage of the spirometer across young patients and provide long term spirometer data for clinitian analysis. It's the app for your hospital! 

## Database Library
The dbLib folder contains the files for our database library. This library is used to query the DynamoDB instance in order to gather information requested. 

## Cloud Infrastructure
Our REST API will be deployed on an AWS API Gateway instance, making our backend serverless. The logic for our API endpoints will be deployed in AWS Lambda functions that will be called by the API Gateway. The Lambda Functions will host the majority of our software as it will execute the logic for evaluating incoming requests, our database library, and constructing responses with the necessary data.

## Creating the S3 Bucket
1. In the AWS console under services select S3
2. Select Create bucket
3. Do not enable versioning, do not enable logging
4. Do not enable encryption at rest - not necessary for the contents of this bucket
5. Under configure options select block all public access
6. Review and create bucket

## Uploading a file to the S3 Bucket
1. In the AWS console under services select S3
2. Select the artsy-backend bucket
3. Under Overview select the upload bucket
4. Select the file(s) and click upload

## Required installations
1. pip install requests

## Creating the deployment package
1. Install dependencies 'pip3 install --target ./package requests'
2. Create the deployment package by moving into the package directory. Be sure to have the lambda_function.py file in this directory. Run the command 'zip -r package.zip ./*'
3. In the lambda console select upload zip and select the zip file from your local file tree
