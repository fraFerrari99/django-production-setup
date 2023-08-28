#!This is the Dockerfile related to the django project

# This is the official base Python Docker image 
FROM python:3.11-slim-bullseye 

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

#Set the working directory of the image
WORKDIR /code

# Upgrade pip package and install all the libraries needed that are inside requirements.txt
RUN pip install --upgrade pip

# Run these commands to install a C compiler neded to use uwsgi
RUN apt-get update && apt-get install -y build-essential

#copy the requirements.txt file into the code directory of the image
COPY requirements.txt /code/
RUN pip install -r requirements.txt


#Copy the local directory inside the code directory of the image
COPY . /code/

