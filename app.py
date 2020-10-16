from flask import Flask, render_template, jsonify, request
import os
import json
import boto3
import requests
import subprocess
from kubernetes import client, config
from openshift.dynamic import DynamicClient, exceptions


app = Flask(__name__)


k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)


def checkNamespace(namespace_name):
    v1_projects = dyn_client.resources.get(api_version='project.openshift.io/v1', kind='Project')
    projects_list = v1_projects.get()
    for project in projects_list.items:
        if namespace_name == project.metadata.name:
            return True
    return False


def checkSeldonInstance(seldon_operator_instance_name, namespace):
    try:
        v1_seldon_operator_instance = dyn_client.resources.get(api_version='machinelearning.seldon.io/v1', kind='SeldonDeployment')
        resp = v1_seldon_operator_instance.get(name=seldon_operator_instance_name, namespace=namespace)
        return True
    except:
        return False

def checkDeployment(model_deploment_name, namespace):
    try:
      v1_deployment = dyn_client.resources.get(api_version='v1', kind='Deployment')
      dep = v1_deployment.get(name=model_deploment_name, namespace=namespace)
    except exceptions.NotFoundError:
      return 1
    else:
      return 0

def modelRouteCreate(model_route_name, namespace):
    v1_route = dyn_client.resources.get(api_version='route.openshift.io/v1', kind='Route')
    resp = v1_route.get(name=model_route_name, namespace=namespace)
    return resp.spec.host


@app.route("/", methods = ['GET'])
def index():
    if request.method=='GET':
        return render_template("index.html")


@app.route("/tensorflow", methods = ['GET', 'POST'])
def tensorflow_deploy():
    if request.method == 'GET':
        return render_template("tensorflow.html")
    else:
        # post_data = request.get_json()
        # print(request.data)
        # print(request.args.get('key1'))
        email = request.form.get('email')
        username = email.split('@')[0].replace('.', '-')
        namespace = request.form.get('namespace')
        aws_access_key_id = request.form.get('aws_access_key_id')
        aws_secret_access_key = request.form.get('aws_secret_access_key')
        s3_bucket_name = request.form.get('s3_bucket_name')
        model_name = request.form.get('model_name').replace('_','-')
        s3_model_path = request.form.get('s3_model_path')
        seldon_instance_name = username+"-"+model_name+"-model"
        model_service_name = username + "-" + model_name + "-model-model"
        
        namespace_exists = checkNamespace(namespace_name=namespace)
        if not namespace_exists:
            return render_template('error.html', Error="The namespace you provided does not exist. Enter a valid namespace.")
        
        seldon_instance_exists = checkSeldonInstance(seldon_operator_instance_name=seldon_instance_name, namespace=namespace)
        if seldon_instance_exists:
            # return jsonify({"Error": "The name provided for the model already exists. Try deploying again with a new name for your model."})
            return render_template('error.html', Error="The name provided for the tensorflow model already exists. Try deploying again with a new name for your model.")
        
        else:
            sh_cmd="sh tensorflow_deploy.sh "+username+" "+namespace+" "+aws_access_key_id+" "+aws_secret_access_key+" "+s3_bucket_name+" "+model_name+" "+s3_model_path+" "+model_service_name
            os.system(sh_cmd)
            model_route_url = modelRouteCreate(model_route_name=model_service_name, namespace=namespace)
            
            # return jsonify({'Model Endpoint:': "http://"+model_route_url+"/v1/models/"+model_name+"-model/:predict"})
        return render_template('success.html', Route="http://"+model_route_url+"/v1/models/"+model_name+"-model/:predict")


@app.route("/xgboost", methods = ['GET', 'POST'])
def xgboost_deploy():
    if request.method == 'GET':
        return render_template("xgboost.html")
    else:
        email = request.form.get('email')
        username = email.split('@')[0].replace('.', '-')
        namespace = request.form.get('namespace')
        aws_access_key_id = request.form.get('aws_access_key_id')
        aws_secret_access_key = request.form.get('aws_secret_access_key')
        s3_bucket_name = request.form.get('s3_bucket_name')
        model_name = request.form.get('model_name').replace('_','-')
        s3_model_path = request.form.get('s3_model_path')
        seldon_instance_name = username + "-" + model_name + "-model"
        model_service_name = username + "-" + model_name + "-model-default"
        
        namespace_exists = checkNamespace(namespace_name=namespace)
        if not namespace_exists:
            return render_template('error.html', Error="The namespace you provided does not exist. Enter a valid namespace.")

        seldon_instance_exists = checkSeldonInstance(seldon_operator_instance_name=seldon_instance_name, namespace=namespace)
        if seldon_instance_exists:
            return render_template('error.html', Error="The name provided for the xgboost model already exists. Try deploying again with a new name for your model.")
        
        else:
            sh_cmd = "sh xgboost_deploy.sh "+username+" "+namespace+" "+aws_access_key_id+" "+aws_secret_access_key+" "+s3_bucket_name+" "+model_name+" "+s3_model_path+" "+model_service_name
            os.system(sh_cmd)
            model_route_url = modelRouteCreate(model_route_name=model_service_name, namespace=namespace)
            return render_template('success.html', Route="http://"+model_route_url+"/api/v1.0/predictions")


@app.route("/sklearn", methods = ['GET', 'POST'])
def sklearn_deploy():
    if request.method == 'GET':
        return render_template("sklearn.html")
    else:
        email = request.form.get('email')
        username = email.split('@')[0].replace('.', '-')
        namespace = request.form.get('namespace')
        aws_access_key_id = request.form.get('aws_access_key_id')
        aws_secret_access_key = request.form.get('aws_secret_access_key')
        s3_bucket_name = request.form.get('s3_bucket_name')
        model_name = request.form.get('model_name').replace('_','-')
        s3_model_path = request.form.get('s3_model_path')
        prediction_method = request.form.get('prediction_method')
        seldon_instance_name = username + "-" + model_name + "-model"
        model_service_name = username + "-" + model_name + "-model-default"
        
        namespace_exists = checkNamespace(namespace_name=namespace)
        if not namespace_exists:
            return render_template('error.html', Error="The namespace you provided does not exist. Enter a valid namespace.")
        
        seldon_instance_exists = checkSeldonInstance(seldon_operator_instance_name=seldon_instance_name, namespace=namespace)
        if seldon_instance_exists:
            return render_template('error.html', Error="The name provided for the sklearn model already exists. Try deploying again with a new name for your model.")
        
        else:
            sh_cmd = "sh sklearn_deploy.sh "+username+" "+namespace+" "+aws_access_key_id+" "+aws_secret_access_key+" "+s3_bucket_name+" "+model_name+" "+s3_model_path+" "+prediction_method+" "+model_service_name
            os.system(sh_cmd)
            model_route_url = modelRouteCreate(model_route_name=model_service_name, namespace=namespace)
            return render_template('success.html', Route="http://"+model_route_url+"/api/v1.0/predictions")


@app.route("/h2o", methods=['GET', 'POST'])
def h2o_deploy():
    if request.method == 'GET':
        return render_template("h2o.html")
    else:
        email = request.form.get('email')
        username = email.split('@')[0].replace('.', '-')
        namespace = request.form.get('namespace')
        aws_access_key_id = request.form.get('aws_access_key_id')
        aws_secret_access_key = request.form.get('aws_secret_access_key')
        s3_bucket_name = request.form.get('s3_bucket_name')
        model_name = request.form.get('model_name').replace('_','-')
        s3_model_path = request.form.get('s3_model_path')
        model_to_be_saved = username+"-"+model_name+".zip"
        s3_region = ''
        
        namespace_exists = checkNamespace(namespace_name=namespace)
        if not namespace_exists:
            return render_template('error.html', Error="The namespace you provided does not exist. Enter a valid namespace.")

        s3_endpoint_url = 'https://s3-rook-ceph.apps.ai.innerdata.ml'
        if checkDeployment(username+"-"+model_name, namespace)==0:
            return render_template('error.html', Error="The name provided for the h2o model already exists. Try deploying again with a new name for your model.")
        
        else:
            s3 = boto3.client('s3', s3_region, endpoint_url=s3_endpoint_url, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
            s3.download_file(s3_bucket_name,s3_model_path, model_to_be_saved)
            sh_cmd = "sh h2o_deploy.sh "+model_name+" "+username+" "+namespace+" "+model_to_be_saved
            os.system(sh_cmd)
            model_route_url = modelRouteCreate(model_route_name=username+"-"+model_name, namespace=namespace)
            return render_template('success.html', Route="http://"+model_route_url+"/predict")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, use_reloader=True, debug=True)
