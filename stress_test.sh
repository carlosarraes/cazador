#!/bin/bash

if ! command -v hey &>/dev/null; then
	echo "O comando 'hey' não foi encontrado. Por favor, instale o hey para continuar."
	exit 1
fi

if ! command -v minikube &>/dev/null; then
	echo "O comando 'minikube' não foi encontrado. Por favor, instale o minikube para continuar."
	exit 1
fi

MINIKUBE_IP=$(minikube ip)
if [ -z "$MINIKUBE_IP" ]; then
	echo "Não foi possível obter o IP do Minikube. Certifique-se de que o Minikube esteja rodando."
	exit 1
fi

ENDPOINT_URL="http://${MINIKUBE_IP}:30007"
TOTAL_REQUESTS="${1:-10000}"

echo "Iniciando teste de estresse com hey para o endpoint: $ENDPOINT_URL"
echo "Este teste pode demorar alguns minutos..."
hey -n "$TOTAL_REQUESTS" "$ENDPOINT_URL"
