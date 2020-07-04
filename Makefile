DOCKER_REPO ?= gcr.io/online-bridge-hackathon-2020
VERSION ?= $(shell cat VERSION)
DOCKER_TAG=${DOCKER_REPO}/dds-api:${VERSION}

EXTERNAL_ADDRES ?= dds.hackathon.globalbridge.app

ifeq (${SILENT},1)
	VERBOSE_TEST :=
else
	VERBOSE_TEST := -v
endif


DDS_K8S_NS ?= dds-api
GCP_PROJECT ?= online-bridge-hackathon-2020
GKE_CLUSTER_NAME ?= hackathon-cluster
GKE_ZONE ?= europe-west3-b

LIBDDS_BUILD_DIR := libdds/.build

release: build push

# Make sure submodules have been initialized and libdds has latest code
libdds/.git libdds-update:
	git submodule update --init --rebase

# Configure libdds build
# Dependency makes sure submodules have been initialized
${LIBDDS_BUILD_DIR}/CMakeCache.txt: libdds/.git
	mkdir -p ${LIBDDS_BUILD_DIR}
	cd ${LIBDDS_BUILD_DIR} && cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ..

# Build libdds
# Dependencies makes sure that configure has been run and code is the latest one
libdds-build: ${LIBDDS_BUILD_DIR}/CMakeCache.txt libdds-update
	+make -C ${LIBDDS_BUILD_DIR}

build: libdds-update
	docker build -t ${DOCKER_TAG} \
		--build-arg CACHEBUST=$(shell git --git-dir=libdds/.git describe) \
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

run_local_tests: libdds-build
	python3 -m unittest discover ${VERBOSE_TEST}
