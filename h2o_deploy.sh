#!/bin/bash
echo "Hello World!"
model=$1
user=$2
namespace=$3
modelToChange=$4
image='img-registry-openshift-image-registry.apps.ai.innerdata.ml/'$namespace'/'$user'-'$model':0.1'
regimage='image-registry.openshift-image-registry.svc:5000/'$namespace'/'$user'-'$model':0.1'
servicename='svc/'$user'-'$model

sudo mkdir $user
sudo chmod 777 $user
sudo mv $modelToChange $user'/model.zip'
cd ./$user
git clone https://github.com/SeldonIO/seldon-core.git
sudo chmod 777 seldon-core
sudo mv model.zip seldon-core/examples/models/h2o_mojo/src/main/resources/
sudo s2i build seldon-core/examples/models/h2o_mojo/ seldonio/seldon-core-s2i-java-build:0.1 $image --runtime-image seldonio/seldon-core-s2i-java-runtime:0.1
echo $image
sudo docker images | tail -n +2 | awk '{print $1":"$2}'
cd ..
sudo rm -r $user
sudo docker push $image
oc new-app $regimage
oc expose $servicename
sudo docker rmi $image





