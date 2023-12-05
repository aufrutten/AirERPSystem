#!/bin/sh


# That is setup sh script file to configure and launch the project in production
# Notice what before you must to configure the env files and have the kubeconfig file

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
KUBECONFIG_PATH="${SCRIPT_DIR}/kubeconfig.yml"

visual_sleep() {
    local seconds=$1
    local delay=1

    for ((i = 0; i <= 100; i++)); do
        printf "\r[%d%%] " $i
        sleep $((seconds * delay / 100))
    done

    printf "\r[100%%]\n"
}

# Connecting to k8s
if [ -f "$KUBECONFIG_PATH" ]; then
  echo "Applying kubeconfig to access to k8s cluster"
  export KUBECONFIG="$KUBECONFIG_PATH"
  kubectl get nodes -o wide
else
  echo "File ${KUBECONFIG_PATH} do not exist" && exit 1
fi


# Applying app configurations
if [ -f "$(dirname "$SCRIPT_DIR")/public.env" ] && [ -f "$(dirname "$SCRIPT_DIR")/private.env" ]; then
  set -o allexport
  source "$(dirname "$SCRIPT_DIR")/public.env"
  source "$(dirname "$SCRIPT_DIR")/private.env"
  set +o allexport

else
  echo "ENV file $(dirname "$SCRIPT_DIR")/public.env or $(dirname "$SCRIPT_DIR")/private.env do not exist"
  echo "Or not configured."
  exit 1
fi

# shellcheck disable=SC2155
# shellcheck disable=SC2046
export DOCKER_IMAGE=$(basename $(git remote get-url origin) | sed 's/\.git$//' | tr '[:upper:]' '[:lower:]')
echo "your docker username is - $DOCKER_USERNAME"
echo "your docker image is - $DOCKER_IMAGE"

TMP_PATH="/var/tmp/k8s"
mkdir -p "${TMP_PATH}"

PRIVATE_TMP_FILE="${TMP_PATH}/private.env"
PUBLIC_TMP_FILE="${TMP_PATH}/public.env"

envsubst < "$(dirname "$SCRIPT_DIR")/public.env" > "${PUBLIC_TMP_FILE}"
envsubst < "$(dirname "$SCRIPT_DIR")/private.env" > "${PRIVATE_TMP_FILE}"

envsubst < "./celery/worker/deploy.yml" > "${TMP_PATH}/celery-worker-deploy.yml"
envsubst < "./celery/beat/deploy.yml" > "${TMP_PATH}/celery-beat-deploy.yml"
envsubst < "./frontend/deploy.yml" > "${TMP_PATH}/frontend-deploy.yml"
envsubst < "./backend/deploy.yml" > "${TMP_PATH}/backend-deploy.yml"

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml

kubectl create namespace production

kubectl create configmap app-public-config --from-env-file="${PUBLIC_TMP_FILE}" --namespace=production
kubectl create secret generic app-secret-config --from-env-file="${PRIVATE_TMP_FILE}" --namespace=production

kubectl apply -f redis/deploy.yml
kubectl apply -f redis/service.yml

kubectl apply -f database/volume.yml
kubectl apply -f database/deploy.yml
kubectl apply -f database/service.yml

kubectl apply -f "${TMP_PATH}/backend-deploy.yml"
kubectl apply -f backend/service.yml

kubectl apply -f "${TMP_PATH}/frontend-deploy.yml"
kubectl apply -f frontend/service.yml

kubectl apply -f "${TMP_PATH}/celery-beat-deploy.yml"
kubectl apply -f "${TMP_PATH}/celery-worker-deploy.yml"

rm -rf "${TMP_PATH}"
visual_sleep 350

IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')
clear
echo "==================================================================================================="
echo "You must to configure your dns in this ip"
echo "IP of LoadBalancer: $IP"

echo "$BACKEND_HOST - $IP"
echo "$FRONTEND_HOST - $IP"
echo "==================================================================================================="
echo "After configure the DNS, launch the k8s-install-cert.sh, this is for HTTPS and Ingress in app"


