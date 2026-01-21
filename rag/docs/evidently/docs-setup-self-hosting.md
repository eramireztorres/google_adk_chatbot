---
url: https://docs.evidentlyai.com/docs/setup/self-hosting
source: Evidently Documentation
---

This page explains how to self-host the lightweight open-source platform. [Contact us](https://www.evidentlyai.com/get-demo) for Enterprise version with extra features and support. Compare [OSS vs. Enterprise/Cloud](/faq/oss_vs_cloud).

In addition to using Evidently Python library, you can self-host the UI Service to get a monitoring Dashboard and organize the results of your evaluations. This is optional: you can also view evaluation results in Python or export to JSON or HTML.
To get a self-hostable Dashboard, you must:

* Create a Workspace (local or remote) to store your data.
* Launch the UI service.

## [​](#1-create-a-workspace) 1. Create a Workspace

Sign up for a free [Evidently Cloud](cloud) account to get a managed version instantly.

Once you [install Evidently](/docs/setup/installation), you will need to create a `workspace`. This designates a remote or local directory where you will store the evaluation results (JSON Reports called `snapshots`). The UI Service will read the data from this source.
There are three scenarios, based on where you run the UI Service and store data.

* **Local Workspace**. Both the UI Service and data storage are local.
* **Remote Workspace**. Both the UI Service and data storage are remote.
* **Workspace with remote data storage**. Run the UI Service and store data on different servers.

### [​](#local-workspace) Local Workspace

Here, you generate, store the snapshots and run the monitoring UI on the same machine.
Imports:

Copy

```python
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase
```

To create a local Workspace and assign a name:

Copy

```python
ws = Workspace.create("evidently_ui_workspace")
```

You can pass a `path` parameter to specify the path to a local directory.

### [​](#remote-workspace) Remote Workspace

**Code example (Docker)**. See the [remote service example](https://github.com/evidentlyai/evidently/tree/main/examples/service).

In this scenario, you send the snapshots to a remote server. You must run the Monitoring UI on the same remote server. It will directly interface with the filesystem where the snapshots are stored.
Imports:

Copy

```python
from evidently.ui.remote import RemoteWorkspace
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase
```

To create a remote Workspace (UI should be running at this address):

Copy

```python
workspace = RemoteWorkspace("http://localhost:8000")
```

You can pass the following parameters:

| Parameter | Description |
| --- | --- |
| `self.base_url = base_url` | URL for the remote UI service. |
| `self.secret = secret` | String with secret, None by default. Use it if access to the URL is protected by a password. |

### [​](#remote-snapshot-storage) Remote snapshot storage

In the examples above, you store the snapshots and run the UI on the same server. Alternatively, you can store snapshots in a remote data store (such as an S3 bucket). The Monitoring UI service will interface with the designated data store to read the snapshot data.
To connect to data stores Evidently uses `fsspec` that allows accessing data on remote file systems via a standard Python interface.
You can verify supported data stores in the Fsspec documentation ([built-in implementations](https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations) and [other implementations](https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations)).
For example, to read snapshots from an S3 bucket (with MinIO running on localhost:9000), you must specify environment variables:

Copy

```python
FSSPEC_S3_ENDPOINT_URL=http://localhost:9000/
FSSPEC_S3_KEY=my_key FSSPEC_S3_SECRET=my_secret
evidently ui --workspace s3://my_bucket/workspace
```

### [​](#[danger]-delete-workspace) [DANGER] Delete Workspace

To delete a Workspace, run the command from the Terminal:

Copy

```python
cd src/evidently/ui/
rm -r workspace
```

**You are deleting all the data**. This command will delete all the data stored in the workspace folder. To maintain access to the generated Reports, you must store them elsewhere.

## [​](#2-launch-the-ui-service) 2. Launch the UI service

To launch the Evidently UI service, you must run a command in the Terminal.
**Option 1**. If you log snapshots to a local Workspace directory, you run Evidently UI over it. Run the following command from the directory where the Workspace folder is located.

Copy

```python
evidently ui
```

**Option 2**. If you have your Project in a different Workspace, specify the path:

Copy

```python
evidently ui --workspace . /workspace
```

**Option 3**. If you have your Project in a specified Workspace and run the UI service at the specific port (if the default port 8000 is occupied).

Copy

```python
evidently ui --workspace ./workspace --port 8080
```

To view the Evidently interface, go to URL <http://localhost:8000> or a specified port in your web browser.

### [​](#demo-projects) Demo projects

To launch the Evidently service with the demo projects, run:

Copy

```python
evidently ui --demo-projects all
```

## [​](#tutorial) Tutorial

Check this tutorial for an end-to-end example:
[## Evidently UI tutorial

How to create a workspace, project and run Reports.](https://github.com/evidentlyai/evidently/blob/main/examples/service/workspace_tutorial.ipynb)