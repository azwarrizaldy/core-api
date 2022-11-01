"""
    author  : azwar8597@gmail.com
    project : API 
"""


from fastapi import APIRouter #type: ignore
from datetime import datetime as dt
import pandas as pd #type: ignore
from dotenv import load_dotenv #type: ignore
import os, numpy as np, pandas as pd #type: ignore
import boto3 #type:ignore
import pickle, json

router: APIRouter = APIRouter()

def load_model(model_path):
    with open(model_path, 'rb') as f:
        return pickle.load(f)

@router.get("/get-latest-ml-model")
def model_ml():

    #load function dotenv
    load_dotenv()

    #define env aws access key id
    KEY_ID      = os.environ['key']

    #define env aws secret access key
    ACCESS_KEY  = os.environ['acc']

    #define env region name
    REGION      = os.environ['reg']

    #path working directory
    directory = os.getcwd()

    #initiation connect to S3 resource
    s3 = boto3.resource(
                    's3',
                    aws_access_key_id = '{}'.format(KEY_ID),
                    aws_secret_access_key = '{}'.format(ACCESS_KEY),
                    region_name = '{}'.format(REGION)
                    )

    #read list folder model in S3
    model_list = list(s3.Bucket({bucket_name}).objects.filter(Prefix={bucket_path}).all())
    
    #get last model
    last_model = model_list[-1]

    #model key name in S3 Bucket
    model_key_s3 = '{}'.format(last_model.key)
    
    #output result
    return {"json_data": model_key_s3}

@router.post("/approval-loan-predictive")
def approval_loan_predictive(gender: str,
                        married: str,
                        dependents: int,
                        education: str,
                        self_employed: str,
                        credit_history: float,
                        applicant_income: float,
                        coapplicant_income: float,
                        loan_amount_in_thousand: float,
                        loan_amount_term: int,
                        property_area: str
                        ):

    #load function dotenv
    load_dotenv()

    #define env aws access key id
    KEY_ID      = os.environ['key']

    #define env aws secret access key
    ACCESS_KEY  = os.environ['acc']

    #define env region name
    REGION      = os.environ['reg']

    #path working directory
    directory = os.getcwd()

    #initiation connect to S3 resource
    s3 = boto3.resource(
                    's3',
                    aws_access_key_id = '{}'.format(KEY_ID),
                    aws_secret_access_key = '{}'.format(ACCESS_KEY),
                    region_name = '{}'.format(REGION)
                    )

    #read list folder model in S3
    model_list = list(s3.Bucket({bucket_name}).objects.filter(Prefix={bucket_path}).all())
    
    #get last model
    last_model = model_list[-1]

    #model key name in S3
    model_key_s3 = '{}'.format(last_model.key)

    #model name
    model_name = model_key_s3.replace({bucket_path}, '')

    #model path in local directory
    model_path = directory + '/api_analytic/model/' + model_name

    #initiation connect to S3 client
    endpoint = boto3.client(
                    's3',
                    aws_access_key_id = '{}'.format(KEY_ID),
                    aws_secret_access_key = '{}'.format(ACCESS_KEY),
                    region_name = '{}'.format(REGION)
                    )
    
    #download model file to local directory
    endpoint.download_file({bucket_name}, model_key_s3, model_path)

    #path model in local directory
    ModelDir = './api_analytic/model/{}.clf'

    try:
        #initiation variable for sort model file in directory
        models = [
            dt.strptime(model.replace('.clf', ''), '%Y%m%d%H%M%S%f')
            for model in os.listdir("./api_analytic/model/")
            if model.endswith('.clf')
        ]
    except:
        print("error")
    else:
        if not models:
            print("model not found")
        else:
            #sort model file in directory
            models.sort()

            #model path for the lastest model in directory 
            model_path = ModelDir.format(
                models[-1].strftime('%Y%m%d%H%M%S%f')
            )

    #read model classifier
    model_clf       =  load_model(model_path)

    #initiation for value gender
    gen = '{}'.format(gender)
    if gen == 'male':
        gen = 1
    elif gen == 'female':
        gen = 0

    #initiation for value married
    mar = '{}'.format(married)
    if mar == 'yes':
        mar = 1
    elif mar == 'no':
        mar = 0
    
    #initiation for value dependents
    if dependents == 0:
        dep = 0
    elif dependents == 1:
        dep = 1
    elif dependents == 2:
        dep = 2
    else:
        dep = 3
    
    #initiation for value education
    edu = '{}'.format(education)
    if edu == 'not graduate':
        edu = 1
    elif edu == 'graduate':
        edu = 0
    
    #initiation for value self employed
    sel = '{}'.format(self_employed)
    if sel == 'yes':
        sel = 1
    elif sel == 'no':
        sel = 0
    
    #initiation for value property area
    pro = '{}'.format(property_area)
    if pro == 'semiurban':
        pro = 1
    elif pro == 'urban':
        pro = 2
    elif pro == 'rural':
        pro = 0

    #input parameters
    input_values    = (gen, mar, dep, edu, sel, credit_history, applicant_income,
                    coapplicant_income, loan_amount_in_thousand, loan_amount_term, pro)

    #prediction 
    y_preds = model_clf.predict([input_values])


    #with assumption '1' loan approved 
    if y_preds == 1:
        
        details = {
                    'Result' : 'Loan Approved'
                }
        predict = pd.DataFrame(details, index = ['1'])

        out_var = predict.to_json(orient='records')

        datajsonreturn = json.loads(out_var)

    else:
        
        details = {
                    'Result' : 'Loan Not Approved'
                }
        predict = pd.DataFrame(details, index = ['1'])

        out_var = predict.to_json(orient='records')

        datajsonreturn = json.loads(out_var)
    
    return {"msg": datajsonreturn}