# core-api
## Final Project Data Expert G2Academy | author : azwar8597@gmail.com

## Core API
This project describes how to build a REST API from a machine learning model that has been created.

## The process steps are as follows:
### 1. API to get latest ml model
  - connect to AWS S3 Resource
  - read list folder model in AWS S3
  - get last model from folder model
  - get model name
  - print result to JSON file
  
### 2. API for loan approval prediction
  - connect to AWS S3 Resource
  - read list folder model in AWS S3
  - get last model from folder model
  - connect to AWS S3 Client
  - Download model file and save to local directory
  - get last model from local directory
  - initiation parameter
  - run model for prediction
  - print result prediciton to JSON file
