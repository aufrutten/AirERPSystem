#!/bin/sh

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
KUBECONFIG_PATH="${SCRIPT_DIR}/kubeconfig.yml"


if [ -f "$KUBECONFIG_PATH" ]; then
  echo "Applying kubeconfig to access to k8s cluster"
  export KUBECONFIG="$KUBECONFIG_PATH"
  kubectl delete --all pods,deployments,services,configmaps --namespace=production
  kubectl delete --all persistentvolumeclaims,secrets,persistentvolumes --namespace=production
  kubectl delete namespace production
  kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
  kubectl delete -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml
  echo "Done. production is uninstalled"
else
  echo "File ${KUBECONFIG_PATH} isn't exist" && exit 1
fi