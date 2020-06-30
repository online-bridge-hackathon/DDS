# Build, test, and deploy the Double Dummy Solver (DDS) webservice using the Google Cloud Platform (GCP)

For overall project info please see [README.md](https://github.com/online-bridge-hackathon/DDS/blob/master/README.md)

# Connect to the cloud shell

Using your favorite web browser, open a cloud shell terminal at <https://ssh.cloud.google.com/cloudshell>.
You'll need a free Google account. These days, most people have one already.

# Build and install the C++ library

This repository contains the hackathon's fork of Bo Haglund's double-dummy solver code.

```
gcloud config set project online-bridge-hackathon-2020
mkdir ~/bridge-hackathon/
cd ~/bridge-hackathon/
git clone https://github.com/online-bridge-hackathon/libdds.git
cd libdds/
mkdir .build
cd .build/
# Build with debugging symbols. Inexpensive and sometimes useful.
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
make
```

Optional, to be sure the library built correctly.
It will take about six minutes to complete.
```
make check
```

Install the library where Python can find it:
```
sudo cmake -DCMAKE_INSTALL_COMPONENT=Runtime -DCMAKE_INSTALL_PREFIX=/usr -P cmake_install.cmake
```

The cloud shell clears out /usr/lib/ every so often, so add the install command to your *.bashrc* file:
```
cd $HOME/bridge-hackathon/dds/.build/ && sudo cmake -DCMAKE_INSTALL_COMPONENT=Runtime -DCMAKE_INSTALL_PREFIX=/usr -P cmake_install.cmake
```

# Build and test the DDS webservice wrapper for the double-dummy solver library

Note that the C++ project is named **dds** and the webservice project is named **DDS**. Yes, this could be confusing - we plan to rename one or both.

```
cd ~/bridge-hackathon/
git clone https://github.com/online-bridge-hackathon/DDS.git
cd DDS/
make run_local_tests
```

# Install and run the DDS webservice in a local server


```
pip3 install -r requirements.txt
cd ~/bridge-hackathon/DDS/src
python3 api.py
```

# Test your local service manually

Open a new terminal tab by pressing the "+" button in the cloud shell menu bar.

```
curl --header "Content-Type: application/json" --data '{"hands":{"S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],"W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK","H8"],"N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],"E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]}}'   http://localhost:5000/api/dds-table/
```

# Create a docker image and deploy it to the GCP


Build the application stack using:
```
cd ~/bridge-hackathon/DDS/
make build
```

Push to the remote registry:
```
make push
```

Remove the old namespace. In the future we plan to have *make deploy* do this for us.
Note that this will make the service unavailable until the deploy finishes successfully.
```
kubectl delete ns dds-api
```

Deploy to GCP:
```
make deploy
```

Now check your deployment on the GCP console.

Visit <https://console.cloud.google.com/kubernetes/list?project=online-bridge-hackathon-2020>

Navigate to Kubernetes Engine / Workloads:

Select the *dds-api-deployment* in namespace *dds-api*. Or this will take you there directly:

<https://console.cloud.google.com/kubernetes/deployment/europe-west3-b/hackathon-cluster/dds-api/dds-api-deployment?project=online-bridge-hackathon-2020&tab=overview&deployment_overview_active_revisions_tablesize=50&duration=PT1H&pod_summary_list_tablesize=20&service_list_datatablesize=20>

The **Created on** timestamp should be a few minutes old, roughy matching the time your ran *make deploy*.

Now view the logs:
1. Click on the link under Managed pods. It will look something like **dds-api-deployment-58dbc7fcd8-zlzkc**.
2. Switch to the LOGS tab.

Now send your service a POST request, either from the cloud shell or your local machine:

```
curl --header "Content-Type: application/json" --data '{"hands":{"S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],"W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK","H8"],"N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],"E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]}}'   https://dds.hackathon.globalbridge.app/api/dds-table/ 
```

When you refresh the logs page you should see a line showing your POST.

# What if I encounter problems?

No worries! Please post to the *p-dds* channel of the bridge-hackathon Discord. You can find it here:

<https://discord.com/channels/710156643970842754/712639195986002021>
