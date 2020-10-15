# Importing Base Image:

 FROM python:3.6

# Adding Root Privileges:

 USER root

# Creating Working Directory:

 WORKDIR /project

# Copying Source Code into Container:

 ADD . /project

# Docker Installation:

 RUN apt-get update
 RUN apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common
 RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
 RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
 RUN apt-get update
 RUN apt-get -y install docker-ce

# Source to Image Installation:

 RUN wget https://github.com/openshift/source-to-image/releases/download/v1.3.0/source-to-image-v1.3.0-eed2850f-linux-amd64.tar.gz
 RUN tar -xvf source-to-image-v1.3.0-eed2850f-linux-amd64.tar.gz
 RUN  mv s2i /bin

# OC Client Installation:

 RUN wget https://github.com/openshift/origin/releases/download/v3.6.0-alpha.2/openshift-origin-client-tools-v3.6.0-alpha.2-3c221d5-linux-64bit.tar.gz
 RUN tar -xvf openshift-origin-client-tools-v3.6.0-alpha.2-3c221d5-linux-64bit.tar.gz
 RUN mv openshift-origin-client-tools-v3.6.0-alpha.2-3c221d5-linux-64bit/oc /usr/bin

# Application Requirements Installation:
 
 RUN pip install --upgrade pip
 RUN pip install -r requirements.txt

# Exposing port 5000 to world outside container:

EXPOSE 5000

# Start Application:

 CMD ["python","app.py"]
