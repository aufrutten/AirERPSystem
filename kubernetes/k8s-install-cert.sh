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

TMP_PATH="/var/tmp/k8s"
mkdir -p "${TMP_PATH}"

envsubst < "./nginx-ingress.yml" > "${TMP_PATH}/nginx-ingress.yml"
envsubst < "./nginx-cert-issuer.yml" > "${TMP_PATH}/nginx-cert-issuer.yml"

kubectl create namespace production

echo " "
echo " "
echo "BEFORE THIS, YOU MUST CONFIGURE YOUR DOMAIN SETTINGS!!!"
echo " "
echo " "

visual_sleep 110
kubectl create -f "${TMP_PATH}/nginx-cert-issuer.yml"
visual_sleep 110
kubectl apply -f "${TMP_PATH}/nginx-ingress.yml"
visual_sleep 300

kubectl get certificates -n production
kubectl rollout restart deployment cert-manager --namespace cert-manager
kubectl rollout restart deployment ingress-nginx-controller --namespace ingress-nginx

echo "Done"
rm -rf "${TMP_PATH}"
