---
url: https://docs.evidentlyai.com/docs/setup/cloud
source: Evidently Documentation
---

## [​](#1-create-an-account) 1. Create an Account

* If not yet, sign up for a [free Evidently Cloud account](https://app.evidently.cloud/signup).
* After logging in, create an **Organization** and name it.

## [​](#2-connect-from-python) 2. Connect from Python

You need this for programmatic tasks like tracing or logging local evals. Many other tasks can be done directly on the platform.

### [​](#get-a-token) Get a Token

Click the **Key** menu icon to open the [Token page](https://app.evidently.cloud/token). Generate and save token securely.

### [​](#install-evidently) Install Evidently

[Install](/docs/setup/installation) the Evidently Python library.

Copy

```python
pip install evidently ## or pip install evidently[llm]
```

### [​](#connect) Connect

Import the cloud workspace and pass your API token to connect:

Copy

```python
from evidently.ui.workspace import CloudWorkspace

ws = CloudWorkspace(
token="API_KEY",
url="https://app.evidently.cloud")
```

For Evidently 0.6.7 and Evidently Cloud v1, use `from evidently.ui.workspace.cloud import CloudWorkspace`. [Read more](/faq/cloud_v2).

You can also provide the API key by setting the environment variable `EVIDENTLY_API_KEY`.

You are all set! Create a Project and run your first [evaluation](/quickstart_llm).