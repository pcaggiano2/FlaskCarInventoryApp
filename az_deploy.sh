#!/bin/bash

# Build the images of the services
docker build --platform linux/amd64 -t pax7898/car_inventory car_inventory/.
docker build --platform linux/amd64 -f pax7898/vin_decoder vin_decoder/.

# Push the images to DockerHub
docker push pax7898/car_inventory
docker push pax7898/vin_decoder

# Login to Azure
az login

# Variables
resourceGroupName="devops"
clusterName="car-inventory-cluster"

# Create the resource group
az group create --name $resourceGroupName --location italynorth

# Create the AKS cluster
az aks create --resource-group $resourceGroupName --name $clusterName --enable-managed-identity --node-count 1 --generate-ssh-keys

# Autheticate with the AKS cluster
az aks get-credentials --resource-group $resourceGroupName --name $clusterName

# Switch to AKS context
kubectl config get-contexts

kubectl config use-context car-inventory-cluster

# Deploy
kubectl apply -f car_inventory/car_inventory.yaml -f vin_decoder/vin_decoder.yaml