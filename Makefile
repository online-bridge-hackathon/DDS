DOCKER_REPO ?= gcr.io/online-bridge-hackathon-2020
VERSION ?= $(shell cat VERSION)
DOCKER_TAG=${DOCKER_REPO}/dds-api:${VERSION}

EXTERNAL_ADDRES ?= dds.hackathon.globalbridge.app

DDS_K8S_NS ?= dds-api
GCP_PROJECT ?= online-bridge-hackathon-2020
GKE_CLUSTER_NAME ?= hackathon-cluster
GKE_ZONE ?= europe-west3-b

LIBDDS_REMOTE ?= libdds_for_cachebust
LIBDDS_REPO ?= https://github.com/suokko/dds

release: build push

.git/refs/remotes/${LIBDDS_REMOTE}/master:
	git remote add ${LIBDDS_REMOTE} ${LIBDDS_REPO}
	git fetch --no-tags ${LIBDDS_REMOTE}

build: .git/refs/remotes/${LIBDDS_REMOTE}/master
	git fetch --no-tags ${LIBDDS_REMOTE}
	docker build -t ${DOCKER_TAG} \
		--build-arg CACHEBUST=$(shell git describe --always ${LIBDDS_REMOTE}/master) \
		.

push:
	docker push ${DOCKER_TAG}

deploy: set_gcp_context ensure_ns
	helm upgrade --install dds-api ./chart \
		--set image="${DOCKER_TAG}" \
		--set externalHostname="${EXTERNAL_ADDRES}" \
		--namespace ${DDS_K8S_NS} \
		--history-max=10

uninstall: set_gcp_context
	helm del dds-api --namespace ${DDS_K8S_NS}

set_gcp_context:
	gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${GKE_ZONE} --project ${GCP_PROJECT}

ensure_ns:
	kubectl create ns ${DDS_K8S_NS} || :

run_local_tests:
	python3 -m unittest discover
