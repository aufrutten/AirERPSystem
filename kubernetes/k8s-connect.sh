#!/bin/sh

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
KUBECONFIG_PATH="${SCRIPT_DIR}/kubeconfig.yml"


if [ -f "$KUBECONFIG_PATH" ]; then
  echo "Applying kubeconfig to access to k8s cluster"
  export KUBECONFIG="$KUBECONFIG_PATH"
  kubectl get nodes -o wide
  /bin/sh
else
  echo "File ${KUBECONFIG_PATH} isn't exist" && exit 1
fi