#!/bin/bash

username=$1
namespace=$2
aws_access_key_id=$3
aws_secret_access_key=$4
s3_bucket_name=$5
modelname=$6
s3_model_path=$7
model_service_name=$8

oc project openshift
oc process seldon-tensorflow-template-chain -p=USERNAME=$username -p=NAMESPACE=$namespace -p=AWS_ACCESS_KEY_ID=$aws_access_key_id -p=AWS_SECRET_ACCESS_KEY=$aws_secret_access_key -p=S3_BUCKET_NAME=$s3_bucket_name -p=MODELNAME=$modelname -p=S3_MODEL_PATH=$s3_model_path | oc create -f -
oc project $namespace
sleep 40
oc expose svc/$model_service_name
# oc get route/$username-$modelname-model-model -o custom-columns=NAME:.spec.host | tail -n 1
