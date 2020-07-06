# Project / Org
GCP_PROJECT ?= globalbridge-app
GKE_ZONE ?= europe-west4-b

# Service / App
GKE_CLUSTER_NAME ?= prod-cluster
RELEASE_NAME ?= dds
K8S_NS ?= prod-${RELEASE_NAME}
EXTERNAL_ADDRESS ?= ${RELEASE_NAME}.prod.globalbridge.app

# Docker Config
DOCKER_REPO ?= gcr.io/${GCP_PROJECT}
VERSION ?= $(shell cat VERSION)
DOCKER_TAG = ${DOCKER_REPO}/${RELEASE_NAME}:${VERSION}


ifeq (${SILENT},1)
	VERBOSE_TEST :=
else
	VERBOSE_TEST := -v
endif

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
	helm upgrade --install ${RELEASE_NAME} ./chart \
		--set image="${DOCKER_TAG}" \
		--set externalHostname="${EXTERNAL_ADDRESS}" \
		--namespace ${K8S_NS} \
#		--history-max=10

uninstall: set_gcp_context
	helm del ${RELEASE_NAME} --namespace ${K8S_NS}

set_gcp_context:
	gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${GKE_ZONE} --project ${GCP_PROJECT}

ensure_ns:
	kubectl create ns ${K8S_NS} || :

run_local_tests: libdds-build
	python3 -m unittest discover ${VERBOSE_TEST}

curl_local:
	curl \
	--header "Content-Type: application/json" \
	--data \
	'{"hands": { \
		"S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],    \
		"W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK", "H8"],    \
		"N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],    \
		"E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"] }}' \
	http://localhost:5000/api/dds-table/

