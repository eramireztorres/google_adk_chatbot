---
url: https://google.github.io/adk-docs/api-reference/cli/cli.html
source: Google ADK Documentation
---

# CLI Reference[¶](#cli-reference "Link to this heading")

This page contains the auto-generated command-line reference for the adk tool.

## adk[¶](#adk "Link to this heading")

Agent Development Kit CLI tools.

```python
adk [OPTIONS] COMMAND [ARGS]...
```

Options

--version[¶](#cmdoption-adk-version "Link to this definition")
:   Show the version and exit.

### api\_server[¶](#adk-api-server "Link to this heading")

Starts a FastAPI server for agents.

AGENTS\_DIR: The directory of agents, where each sub-directory is a single
agent, containing at least \_\_init\_\_.py and agent.py files.

Example:

> adk api\_server –port=[port] path/to/agents\_dir

```python
adk api_server [OPTIONS] [AGENTS_DIR]
```

Options

--host <host>[¶](#cmdoption-adk-api_server-host "Link to this definition")
:   Optional. The binding host of the server

    Default:
    :   `'127.0.0.1'`

--port <port>[¶](#cmdoption-adk-api_server-port "Link to this definition")
:   Optional. The port of the server

--allow\_origins <allow\_origins>[¶](#cmdoption-adk-api_server-allow_origins "Link to this definition")
:   Optional. Any additional origins to allow for CORS.

--log\_level <log\_level>[¶](#cmdoption-adk-api_server-log_level "Link to this definition")
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

--trace\_to\_cloud[¶](#cmdoption-adk-api_server-trace_to_cloud "Link to this definition")
:   Optional. Whether to enable cloud trace for telemetry.

    Default:
    :   `False`

--reload, --no-reload[¶](#cmdoption-adk-api_server-reload "Link to this definition")
:   Optional. Whether to enable auto reload for server. Not supported for Cloud Run.

--a2a[¶](#cmdoption-adk-api_server-a2a "Link to this definition")
:   Optional. Whether to enable A2A endpoint.

    Default:
    :   `False`

--reload\_agents[¶](#cmdoption-adk-api_server-reload_agents "Link to this definition")
:   Optional. Whether to enable live reload for agents changes.

    Default:
    :   `False`

--session\_service\_uri <session\_service\_uri>[¶](#cmdoption-adk-api_server-session_service_uri "Link to this definition")
:   Optional. The URI of the session service.
    - Use ‘agentengine://<agent\_engine\_resource\_id>’ to connect to Agent Engine sessions.
    - Use ‘sqlite://<path\_to\_sqlite\_file>’ to connect to a SQLite DB.
    - See https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls for more details on supported database URIs.

--artifact\_service\_uri <artifact\_service\_uri>[¶](#cmdoption-adk-api_server-artifact_service_uri "Link to this definition")
:   Optional. The URI of the artifact service, supported URIs: gs://<bucket name> for GCS artifact service.

--eval\_storage\_uri <eval\_storage\_uri>[¶](#cmdoption-adk-api_server-eval_storage_uri "Link to this definition")
:   Optional. The evals storage URI to store agent evals, supported URIs: gs://<bucket name>.

--memory\_service\_uri <memory\_service\_uri>[¶](#cmdoption-adk-api_server-memory_service_uri "Link to this definition")
:   Optional. The URI of the memory service.
    - Use ‘rag://<rag\_corpus\_id>’ to connect to Vertex AI Rag Memory Service.
    - Use ‘agentengine://<agent\_engine\_resource\_id>’ to connect to Vertex AI Memory Bank Service. e.g. agentengine://12345

--session\_db\_url <session\_db\_url>[¶](#cmdoption-adk-api_server-session_db_url "Link to this definition")
:   Deprecated. Use –session\_service\_uri instead.

--artifact\_storage\_uri <artifact\_storage\_uri>[¶](#cmdoption-adk-api_server-artifact_storage_uri "Link to this definition")
:   Deprecated. Use –artifact\_service\_uri instead.

Arguments

AGENTS\_DIR[¶](#cmdoption-adk-api_server-arg-AGENTS_DIR "Link to this definition")
:   Optional argument

### create[¶](#adk-create "Link to this heading")

Creates a new app in the current folder with prepopulated agent template.

APP\_NAME: required, the folder of the agent source code.

Example:

> adk create path/to/my\_app

```python
adk create [OPTIONS] APP_NAME
```

Options

--model <model>[¶](#cmdoption-adk-create-model "Link to this definition")
:   Optional. The model used for the root agent.

--api\_key <api\_key>[¶](#cmdoption-adk-create-api_key "Link to this definition")
:   Optional. The API Key needed to access the model, e.g. Google AI API Key.

--project <project>[¶](#cmdoption-adk-create-project "Link to this definition")
:   Optional. The Google Cloud Project for using VertexAI as backend.

--region <region>[¶](#cmdoption-adk-create-region "Link to this definition")
:   Optional. The Google Cloud Region for using VertexAI as backend.

Arguments

APP\_NAME[¶](#cmdoption-adk-create-arg-APP_NAME "Link to this definition")
:   Required argument

### deploy[¶](#adk-deploy "Link to this heading")

Deploys agent to hosted environments.

```python
adk deploy [OPTIONS] COMMAND [ARGS]...
```

#### agent\_engine[¶](#adk-deploy-agent-engine "Link to this heading")

Deploys an agent to Agent Engine.

AGENT: The path to the agent source code folder.

Example:

> adk deploy agent\_engine –project=[project] –region=[region]
> :   –staging\_bucket=[staging\_bucket] –display\_name=[app\_name] path/to/my\_agent

```python
adk deploy agent_engine [OPTIONS] AGENT
```

Options

--project <project>[¶](#cmdoption-adk-deploy-agent_engine-project "Link to this definition")
:   Required. Google Cloud project to deploy the agent. It will override GOOGLE\_CLOUD\_PROJECT in the .env file (if it exists).

--region <region>[¶](#cmdoption-adk-deploy-agent_engine-region "Link to this definition")
:   Required. Google Cloud region to deploy the agent. It will override GOOGLE\_CLOUD\_LOCATION in the .env file (if it exists).

--staging\_bucket <staging\_bucket>[¶](#cmdoption-adk-deploy-agent_engine-staging_bucket "Link to this definition")
:   Required. GCS bucket for staging the deployment artifacts.

--trace\_to\_cloud[¶](#cmdoption-adk-deploy-agent_engine-trace_to_cloud "Link to this definition")
:   Optional. Whether to enable Cloud Trace for Agent Engine.

    Default:
    :   `False`

--display\_name <display\_name>[¶](#cmdoption-adk-deploy-agent_engine-display_name "Link to this definition")
:   Optional. Display name of the agent in Agent Engine.

    Default:
    :   `''`

--description <description>[¶](#cmdoption-adk-deploy-agent_engine-description "Link to this definition")
:   Optional. Description of the agent in Agent Engine.

    Default:
    :   `''`

--adk\_app <adk\_app>[¶](#cmdoption-adk-deploy-agent_engine-adk_app "Link to this definition")
:   Optional. Python file for defining the ADK application (default: a file named agent\_engine\_app.py)

--temp\_folder <temp\_folder>[¶](#cmdoption-adk-deploy-agent_engine-temp_folder "Link to this definition")
:   Optional. Temp folder for the generated Agent Engine source files. If the folder already exists, its contents will be removed. (default: a timestamped folder in the system temp directory).

--env\_file <env\_file>[¶](#cmdoption-adk-deploy-agent_engine-env_file "Link to this definition")
:   Optional. The filepath to the .env file for environment variables. (default: the .env file in the agent directory, if any.)

--requirements\_file <requirements\_file>[¶](#cmdoption-adk-deploy-agent_engine-requirements_file "Link to this definition")
:   Optional. The filepath to the requirements.txt file to use. (default: the requirements.txt file in the agent directory, if any.)

Arguments

AGENT[¶](#cmdoption-adk-deploy-agent_engine-arg-AGENT "Link to this definition")
:   Required argument

#### cloud\_run[¶](#adk-deploy-cloud-run "Link to this heading")

Deploys an agent to Cloud Run.

AGENT: The path to the agent source code folder.

Example:

> adk deploy cloud\_run –project=[project] –region=[region] path/to/my\_agent

```python
adk deploy cloud_run [OPTIONS] AGENT
```

Options

--project <project>[¶](#cmdoption-adk-deploy-cloud_run-project "Link to this definition")
:   Required. Google Cloud project to deploy the agent. When absent, default project from gcloud config is used.

--region <region>[¶](#cmdoption-adk-deploy-cloud_run-region "Link to this definition")
:   Required. Google Cloud region to deploy the agent. When absent, gcloud run deploy will prompt later.

--service\_name <service\_name>[¶](#cmdoption-adk-deploy-cloud_run-service_name "Link to this definition")
:   Optional. The service name to use in Cloud Run (default: ‘adk-default-service-name’).

--app\_name <app\_name>[¶](#cmdoption-adk-deploy-cloud_run-app_name "Link to this definition")
:   Optional. App name of the ADK API server (default: the folder name of the AGENT source code).

--port <port>[¶](#cmdoption-adk-deploy-cloud_run-port "Link to this definition")
:   Optional. The port of the server

--allow\_origins <allow\_origins>[¶](#cmdoption-adk-deploy-cloud_run-allow_origins "Link to this definition")
:   Optional. Any additional origins to allow for CORS.

--log\_level <log\_level>[¶](#cmdoption-adk-deploy-cloud_run-log_level "Link to this definition")
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

--trace\_to\_cloud[¶](#cmdoption-adk-deploy-cloud_run-trace_to_cloud "Link to this definition")
:   Optional. Whether to enable cloud trace for telemetry.

    Default:
    :   `False`

--reload, --no-reload[¶](#cmdoption-adk-deploy-cloud_run-reload "Link to this definition")
:   Optional. Whether to enable auto reload for server. Not supported for Cloud Run.

--a2a[¶](#cmdoption-adk-deploy-cloud_run-a2a "Link to this definition")
:   Optional. Whether to enable A2A endpoint.

    Default:
    :   `False`

--reload\_agents[¶](#cmdoption-adk-deploy-cloud_run-reload_agents "Link to this definition")
:   Optional. Whether to enable live reload for agents changes.

    Default:
    :   `False`

--with\_ui[¶](#cmdoption-adk-deploy-cloud_run-with_ui "Link to this definition")
:   Optional. Deploy ADK Web UI if set. (default: deploy ADK API server only)

    Default:
    :   `False`

--verbosity <verbosity>[¶](#cmdoption-adk-deploy-cloud_run-verbosity "Link to this definition")
:   Deprecated. Use –log\_level instead.

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

--temp\_folder <temp\_folder>[¶](#cmdoption-adk-deploy-cloud_run-temp_folder "Link to this definition")
:   Optional. Temp folder for the generated Cloud Run source files (default: a timestamped folder in the system temp directory).

--adk\_version <adk\_version>[¶](#cmdoption-adk-deploy-cloud_run-adk_version "Link to this definition")
:   Optional. The ADK version used in Cloud Run deployment. (default: the version in the dev environment)

    Default:
    :   `'1.7.0'`

--session\_service\_uri <session\_service\_uri>[¶](#cmdoption-adk-deploy-cloud_run-session_service_uri "Link to this definition")
:   Optional. The URI of the session service.
    - Use ‘agentengine://<agent\_engine\_resource\_id>’ to connect to Agent Engine sessions.
    - Use ‘sqlite://<path\_to\_sqlite\_file>’ to connect to a SQLite DB.
    - See https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls for more details on supported database URIs.

--artifact\_service\_uri <artifact\_service\_uri>[¶](#cmdoption-adk-deploy-cloud_run-artifact_service_uri "Link to this definition")
:   Optional. The URI of the artifact service, supported URIs: gs://<bucket name> for GCS artifact service.

--eval\_storage\_uri <eval\_storage\_uri>[¶](#cmdoption-adk-deploy-cloud_run-eval_storage_uri "Link to this definition")
:   Optional. The evals storage URI to store agent evals, supported URIs: gs://<bucket name>.

--memory\_service\_uri <memory\_service\_uri>[¶](#cmdoption-adk-deploy-cloud_run-memory_service_uri "Link to this definition")
:   Optional. The URI of the memory service.
    - Use ‘rag://<rag\_corpus\_id>’ to connect to Vertex AI Rag Memory Service.
    - Use ‘agentengine://<agent\_engine\_resource\_id>’ to connect to Vertex AI Memory Bank Service. e.g. agentengine://12345

--session\_db\_url <session\_db\_url>[¶](#cmdoption-adk-deploy-cloud_run-session_db_url "Link to this definition")
:   Deprecated. Use –session\_service\_uri instead.

--artifact\_storage\_uri <artifact\_storage\_uri>[¶](#cmdoption-adk-deploy-cloud_run-artifact_storage_uri "Link to this definition")
:   Deprecated. Use –artifact\_service\_uri instead.

Arguments

AGENT[¶](#cmdoption-adk-deploy-cloud_run-arg-AGENT "Link to this definition")
:   Required argument

### eval[¶](#adk-eval "Link to this heading")

Evaluates an agent given the eval sets.

AGENT\_MODULE\_FILE\_PATH: The path to the \_\_init\_\_.py file that contains a
module by the name “agent”. “agent” module contains a root\_agent.

EVAL\_SET\_FILE\_PATH: You can specify one or more eval set file paths.

For each file, all evals will be run by default.

If you want to run only specific evals from a eval set, first create a comma
separated list of eval names and then add that as a suffix to the eval set
file name, demarcated by a :.

For example,

sample\_eval\_set\_file.json:eval\_1,eval\_2,eval\_3

This will only run eval\_1, eval\_2 and eval\_3 from sample\_eval\_set\_file.json.

CONFIG\_FILE\_PATH: The path to config file.

PRINT\_DETAILED\_RESULTS: Prints detailed results on the console.

```python
adk eval [OPTIONS] AGENT_MODULE_FILE_PATH [EVAL_SET_FILE_PATH]...
```

Options

--config\_file\_path <config\_file\_path>[¶](#cmdoption-adk-eval-config_file_path "Link to this definition")
:   Optional. The path to config file.

--print\_detailed\_results[¶](#cmdoption-adk-eval-print_detailed_results "Link to this definition")
:   Optional. Whether to print detailed results on console or not.

    Default:
    :   `False`

--eval\_storage\_uri <eval\_storage\_uri>[¶](#cmdoption-adk-eval-eval_storage_uri "Link to this definition")
:   Optional. The evals storage URI to store agent evals, supported URIs: gs://<bucket name>.

Arguments

AGENT\_MODULE\_FILE\_PATH[¶](#cmdoption-adk-eval-arg-AGENT_MODULE_FILE_PATH "Link to this definition")
:   Required argument

EVAL\_SET\_FILE\_PATH[¶](#cmdoption-adk-eval-arg-EVAL_SET_FILE_PATH "Link to this definition")
:   Optional argument(s)

### run[¶](#adk-run "Link to this heading")

Runs an interactive CLI for a certain agent.

AGENT: The path to the agent source code folder.

Example:

> adk run path/to/my\_agent

```python
adk run [OPTIONS] AGENT
```

Options

--save\_session[¶](#cmdoption-adk-run-save_session "Link to this definition")
:   Optional. Whether to save the session to a json file on exit.

    Default:
    :   `False`

--session\_id <session\_id>[¶](#cmdoption-adk-run-session_id "Link to this definition")
:   Optional. The session ID to save the session to on exit when –save\_session is set to true. User will be prompted to enter a session ID if not set.

--replay <replay>[¶](#cmdoption-adk-run-replay "Link to this definition")
:   The json file that contains the initial state of the session and user queries. A new session will be created using this state. And user queries are run againt the newly created session. Users cannot continue to interact with the agent.

--resume <resume>[¶](#cmdoption-adk-run-resume "Link to this definition")
:   The json file that contains a previously saved session (by–save\_session option). The previous session will be re-displayed. And user can continue to interact with the agent.

Arguments

AGENT[¶](#cmdoption-adk-run-arg-AGENT "Link to this definition")
:   Required argument

### web[¶](#adk-web "Link to this heading")

Starts a FastAPI server with Web UI for agents.

AGENTS\_DIR: The directory of agents, where each sub-directory is a single
agent, containing at least \_\_init\_\_.py and agent.py files.

Example:

> adk web –port=[port] path/to/agents\_dir

```python
adk web [OPTIONS] [AGENTS_DIR]
```

Options

--host <host>[¶](#cmdoption-adk-web-host "Link to this definition")
:   Optional. The binding host of the server

    Default:
    :   `'127.0.0.1'`

--port <port>[¶](#cmdoption-adk-web-port "Link to this definition")
:   Optional. The port of the server

--allow\_origins <allow\_origins>[¶](#cmdoption-adk-web-allow_origins "Link to this definition")
:   Optional. Any additional origins to allow for CORS.

--log\_level <log\_level>[¶](#cmdoption-adk-web-log_level "Link to this definition")
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

--trace\_to\_cloud[¶](#cmdoption-adk-web-trace_to_cloud "Link to this definition")
:   Optional. Whether to enable cloud trace for telemetry.

    Default:
    :   `False`

--reload, --no-reload[¶](#cmdoption-adk-web-reload "Link to this definition")
:   Optional. Whether to enable auto reload for server. Not supported for Cloud Run.

--a2a[¶](#cmdoption-adk-web-a2a "Link to this definition")
:   Optional. Whether to enable A2A endpoint.

    Default:
    :   `False`

--reload\_agents[¶](#cmdoption-adk-web-reload_agents "Link to this definition")
:   Optional. Whether to enable live reload for agents changes.

    Default:
    :   `False`

--session\_service\_uri <session\_service\_uri>[¶](#cmdoption-adk-web-session_service_uri "Link to this definition")
:   Optional. The URI of the session service.
    - Use ‘agentengine://<agent\_engine\_resource\_id>’ to connect to Agent Engine sessions.
    - Use ‘sqlite://<path\_to\_sqlite\_file>’ to connect to a SQLite DB.
    - See https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls for more details on supported database URIs.

--artifact\_service\_uri <artifact\_service\_uri>[¶](#cmdoption-adk-web-artifact_service_uri "Link to this definition")
:   Optional. The URI of the artifact service, supported URIs: gs://<bucket name> for GCS artifact service.

--eval\_storage\_uri <eval\_storage\_uri>[¶](#cmdoption-adk-web-eval_storage_uri "Link to this definition")
:   Optional. The evals storage URI to store agent evals, supported URIs: gs://<bucket name>.

--memory\_service\_uri <memory\_service\_uri>[¶](#cmdoption-adk-web-memory_service_uri "Link to this definition")
:   Optional. The URI of the memory service.
    - Use ‘rag://<rag\_corpus\_id>’ to connect to Vertex AI Rag Memory Service.
    - Use ‘agentengine://<agent\_engine\_resource\_id>’ to connect to Vertex AI Memory Bank Service. e.g. agentengine://12345

--session\_db\_url <session\_db\_url>[¶](#cmdoption-adk-web-session_db_url "Link to this definition")
:   Deprecated. Use –session\_service\_uri instead.

--artifact\_storage\_uri <artifact\_storage\_uri>[¶](#cmdoption-adk-web-artifact_storage_uri "Link to this definition")
:   Deprecated. Use –artifact\_service\_uri instead.

Arguments

AGENTS\_DIR[¶](#cmdoption-adk-web-arg-AGENTS_DIR "Link to this definition")
:   Optional argument

# [adk cli](index.html)



### Navigation

Contents:

* [CLI Reference](#)
  + [adk](#adk)

### Related Topics

* [Documentation overview](index.html)
  + Previous: [adk cli documentation](index.html "previous chapter")

©2025, Google.
|
Powered by [Sphinx 8.2.3](https://www.sphinx-doc.org/)
& [Alabaster 1.0.0](https://alabaster.readthedocs.io)
|
[Page source](_sources/cli.rst.txt)