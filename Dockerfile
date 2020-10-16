# Importing Base Image:

FROM python:3.6

# Adding Root Privileges:

USER root

# Creating Working Directory:

WORKDIR /project

# Copying Source Code into Container:

ADD . /project
RUN chmod -R 777 /project/

# Docker Installation:

RUN apt-get update
RUN apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN apt-get update
RUN apt-get -y install docker-ce

# OC Client Installation:

RUN wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz
RUN tar xvf openshift-client-linux.tar.gz
RUN mv oc kubectl /usr/bin
RUN oc login --token=eyJhbGciOiJSUzI1NiIsImtpZCI6InRncmJWeUYwZ1A4MktfOEhtTDFoemt6MUNSYmJEa3ZQakdxeHBLYm9fM0UifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJvZGgiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoic2VsZG9uLXdlYi1hcGktdG9rZW4tMmJzZ3MiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoic2VsZG9uLXdlYi1hcGkiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI2ZDZiNTEyZC0xNDZkLTRlMzctOGZjMC1hNmQxZWM2ZjllZDIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6b2RoOnNlbGRvbi13ZWItYXBpIn0.hT_VWGsCz76tEIq42vbvzClc1qRzyp8JEPu91Eb2WiQEGWU89zS-LyW6zyeLA355gGLtaNEqLrlEVgRU4Ou5S8UXPMrYUd_mxY3xf-9Pp6lzEsSShIaaHEFoT8X_zWsX9Qh-voGdgIDrzTVkc1ANLYlsQSaQAllX_eXHdeFsol2FbjKQwnj7pmtussqV-fKmhg5QSOH6YNoKd_E1_9Cu7vjZjvljb6VNVZ9ml_fL6orNMDduhXmjxj-T3Pe6FQDdVZFOHVkiCcJXi-JkicXKf2n1mFXtx6nxrGo5PcLvCDFEAOVgaYJ2YyXyQbwA2t1DF5ZBvv4kfv4XfDb5HB1Agg --insecure-skip-tls-verify --server=https://api.ai.innerdata.ml:6443

# Source to Image Installation:

RUN wget https://github.com/openshift/source-to-image/releases/download/v1.3.0/source-to-image-v1.3.0-eed2850f-linux-amd64.tar.gz
RUN tar -xvf source-to-image-v1.3.0-eed2850f-linux-amd64.tar.gz
RUN  mv s2i sti /usr/bin

RUN chmod -R 777 /project/

# Application Requirements Installation:
 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposing port 5000 to world outside container:

EXPOSE 8080

# Start Application:

 CMD ["python","app.py"]
