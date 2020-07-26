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

LOGDIR := logs

# TODO: Add LIBDDS_BUILD_DIR
TMPDIRS := \
	${LOGDIR} \
# end of TMPDIRS

${TMPDIRS}:
	mkdir -p $@

release: build push

# Make sure submodules have been initialized and libdds has latest code
libdds/.git libdds-update:
	git submodule update --init --recursive

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

# TODO: Consider a more straightforward approach than $@.
curl_local_URL := http://localhost:5000/api/dds-table/
curl_prod_URL  := https://dds.prod.globalbridge.app/api/dds-table/
CURL_URL       ?= ${$@_URL}

# NOTE: We might need to switch to http or to add --insecure or --cacert when we add more targets.
curl_local curl_prod:
	curl \
	--header "Content-Type: application/json" \
	--data "@./data/sample_deal.json" \
	${CURL_URL}

logfile := ${LOGDIR}/src.api.$(shell date +%FT%T).log
pidfile := ${LOGDIR}/server.PID

start_local_server: libdds-build stop_local_server ${LOGDIR}
	@echo
	@echo Starting a local test service as a background process. You can stop it with \`make stop_local_server\`
	@echo The server log will be written to \'${logfile}\'.
	@echo
	python3 -m src.api > ${logfile} 2>&1 & echo $$! > ${pidfile}

stop_local_server:
	[ ! -e ${pidfile} ] || (kill $$(cat ${pidfile}) ; rm ${pidfile})
