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

## Spirmeter Scoring System
There are two main factors we consider when scoring patients spirometer breaths: length and flow. Both of these numbers come from the flow array that is recorded by the spirometer and then sent to backend. The spirometer records flow rates of 0, 1, 2, and 3. It records the flow every 0.5 seconds.

# Length
This is the main component of the score, and is graphed here on desmos: https://www.desmos.com/calculator/z5qwylid3u. We use the length of the flow array for the input to this function.

# Flow
We take flow data and come up with a modifier. Our aim is to classify the flows as 'good' or 'bad'. To do this, we want to make a modifier which rewards the user on having lower flow (1 being the best, 3 the worst) and on being consistent (consecutive numbers are better than vasilating flow values).
Specifically, there is a value associated with starting on one value and moving to the next value. Since there are 4 possible starting and ending values (0-3) there are 16 values (4 starting values * 4 ending values = 16). In the file apiLib.py, there is a function called compute score. In it is a hard coded array called values. This array has 16 values corresponding to the 16 possible starting and ending values. The first 4 represent starting at 0, the second 4 are for starting at 1, the third 4 are for starting at 2, and the last 4 represent starting with 3. In each set of 4, the first number corresonds to ending with 0, and then the next three correspond to ending with 1, 2, and 3 respectively. There is also a vector for weights for each of these values, but almost all the weights are 1 so that everything is weighted equall.

The final score comes from the output of the desmos curve multiplied by the modifier and then rounded down. Hopefully this helps you understand the scoring system if any small adjustments need to be made.