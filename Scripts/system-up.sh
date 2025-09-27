#! /bin/bash

set -e

cd ../Terraform
terraform init && terraform validate && terraform plan && terraform apply -auto-approve

cd ../Helm
helm repo add aws-ebs-csi-driver https://kubernetes-sigs.github.io/aws-ebs-csi-driver
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add jenkinsci https://charts.jenkins.io
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install aws-ebs-csi-driver aws-ebs-csi-driver/aws-ebs-csi-driver --version 2.15.0 --namespace kube-system -f csi-driver.yaml 

cd ../Manifests
kubectl apply -f namespaces.yaml
kubectl apply -f volumes.yaml

sleep 5

cd ../Helm
helm upgrade --install ingress ingress-nginx/ingress-nginx --version 4.13.2 --namespace ingress --create-namespace -f ingress.yaml
helm upgrade --install jenkins jenkinsci/jenkins --version 5.8.90 --namespace jenkins --create-namespace -f jenkins.yaml
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack --version 77.10.0 --namespace monitoring --create-namespace -f monitoring.yaml 

kubectl apply -f ../Manifests

kubectl create secret generic dockerhub-secret \
  --from-file=.dockerconfigjson=../dockerhub.json \
  --type=kubernetes.io/dockerconfigjson \
  -n jenkins

echo "================================================"
echo "***************** All done! ********************"
echo "================================================"