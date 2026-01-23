---
url: https://google.github.io/adk-docs/tools/google-cloud-tools/
source: Google ADK Documentation
---

[adk-python](https://github.com/google/adk-python "adk-python")

[adk-go](https://github.com/google/adk-go "adk-go")

[adk-java](https://github.com/google/adk-java "adk-java")

* [Home](../..)

  Home
* Build Agents




  Build Agents
  + [Get Started](../../get-started/)

    Get Started
    - [Python](../../get-started/python/)
    - [Go](../../get-started/go/)
    - [Java](../../get-started/java/)
  + [Build your Agent](../../tutorials/)

    Build your Agent
    - [Multi-tool agent](../../get-started/quickstart/)
    - [Agent team](../../tutorials/agent-team/)
    - [Streaming agent](../../get-started/streaming/)

      Streaming agent
      * [Python](../../get-started/streaming/quickstart-streaming/)
      * [Java](../../get-started/streaming/quickstart-streaming-java/)
    - [Visual Builder](../../visual-builder/)
    - [Advanced setup](../../get-started/installation/)
  + [Agents](../../agents/)

    Agents
    - [LLM agents](../../agents/llm-agents/)
    - [Workflow agents](../../agents/workflow-agents/)

      Workflow agents
      * [Sequential agents](../../agents/workflow-agents/sequential-agents/)
      * [Loop agents](../../agents/workflow-agents/loop-agents/)
      * [Parallel agents](../../agents/workflow-agents/parallel-agents/)
    - [Custom agents](../../agents/custom-agents/)
    - [Multi-agent systems](../../agents/multi-agents/)
    - [Agent Config](../../agents/config/)
    - [Models & Authentication](../../agents/models/)
  + [Tools for Agents](../)

    Tools for Agents
    - [Built-in tools](../built-in-tools/)
    - Gemini API tools




      Gemini API tools
      * [Computer use](../gemini-api/computer-use/)
    - Google Cloud tools




      Google Cloud tools
      * Overview

        [Overview](./)



        Table of contents
        + [Apigee API Hub Tools](#apigee-api-hub-tools)

          - [Create an API Hub Toolset](#create-an-api-hub-toolset)
        + [Application Integration Tools](#application-integration-tools)

          - [Prerequisites](#prerequisites)

            * [1. Install ADK](#1-install-adk)
            * [2. Install CLI](#2-install-cli)
            * [3. Provision Application Integration workflow and publish Connection Tool](#3-provision-application-integration-workflow-and-publish-connection-tool)
            * [4. Create project structure](#4-create-project-structure)
            * [5. Set roles and permissions](#5-set-roles-and-permissions)
          - [Use Integration Connectors](#use-integration-connectors)

            * [Before you begin](#before-you-begin)
            * [Create an Application Integration Toolset](#create-an-application-integration-toolset)
          - [Use Application Integration Workflows](#use-application-integration-workflows)

            * [1. Create a tool](#1-create-a-tool)
            * [2. Add the tool to your agent](#2-add-the-tool-to-your-agent)
            * [3. Expose your agent](#3-expose-your-agent)
            * [4. Use your agent](#4-use-your-agent)
      * [MCP Toolbox for Databases](../google-cloud/mcp-toolbox-for-databases/)
      * [BigQuery Agent Analytics](../google-cloud/bigquery-agent-analytics/)
      * [Code Execution with Agent Engine](../google-cloud/code-exec-agent-engine/)
    - [Third-party tools](../third-party/)

      Third-party tools
      * [AgentQL](../third-party/agentql/)
      * [Bright Data](../third-party/bright-data/)
      * [Browserbase](../third-party/browserbase/)
      * [Exa](../third-party/exa/)
      * [Firecrawl](../third-party/firecrawl/)
      * [GitHub](../third-party/github/)
      * [Hugging Face](../third-party/hugging-face/)
      * [Notion](../third-party/notion/)
      * [Tavily](../third-party/tavily/)
      * [Agentic UI (AG-UI)](../third-party/ag-ui/)
  + [Custom Tools](../../tools-custom/)

    Custom Tools
    - Function tools




      Function tools
      * [Overview](../../tools-custom/function-tools/)
      * [Tool performance](../../tools-custom/performance/)
      * [Action confirmations](../../tools-custom/confirmation/)
    - [MCP tools](../../tools-custom/mcp-tools/)
    - [OpenAPI tools](../../tools-custom/openapi-tools/)
    - [Authentication](../../tools-custom/authentication/)
* Run Agents




  Run Agents
  + [Agent Runtime](../../runtime/)

    Agent Runtime
    - [Runtime Config](../../runtime/runconfig/)
    - [API Server](../../runtime/api-server/)
    - [Resume Agents](../../runtime/resume/)
  + [Deployment](../../deploy/)

    Deployment
    - [Agent Engine](../../deploy/agent-engine/)
    - [Cloud Run](../../deploy/cloud-run/)
    - [GKE](../../deploy/gke/)
  + Observability




    Observability
    - [Logging](../../observability/logging/)
    - [Cloud Trace](../../observability/cloud-trace/)
    - [AgentOps](../../observability/agentops/)
    - [Arize AX](../../observability/arize-ax/)
    - [Freeplay](../../observability/freeplay/)
    - [Monocle](../../observability/monocle/)
    - [Phoenix](../../observability/phoenix/)
    - [W&B Weave](../../observability/weave/)
  + [Evaluation](../../evaluate/)

    Evaluation
    - [Criteria](../../evaluate/criteria/)
    - [User Simulation](../../evaluate/user-sim/)
  + [Safety and Security](../../safety/)

    Safety and Security
* Components




  Components
  + [Technical Overview](../../get-started/about/)
  + [Context](../../context/)

    Context
    - [Context caching](../../context/caching/)
    - [Context compression](../../context/compaction/)
  + [Sessions & Memory](../../sessions/)

    Sessions & Memory
    - [Session](../../sessions/session/)
    - [State](../../sessions/state/)
    - [Memory](../../sessions/memory/)
    - [Vertex AI Express Mode](../../sessions/express-mode/)
  + [Callbacks](../../callbacks/)

    Callbacks
    - [Types of callbacks](../../callbacks/types-of-callbacks/)
    - [Callback patterns](../../callbacks/design-patterns-and-best-practices/)
  + [Artifacts](../../artifacts/)

    Artifacts
  + [Events](../../events/)

    Events
  + [Apps](../../apps/)

    Apps
  + [Plugins](../../plugins/)

    Plugins
    - [Reflect and retry](../../plugins/reflect-and-retry/)
  + [MCP](../../mcp/)

    MCP
  + [A2A Protocol](../../a2a/)

    A2A Protocol
    - [Introduction to A2A](../../a2a/intro/)
    - A2A Quickstart (Exposing)




      A2A Quickstart (Exposing)
      * [Python](../../a2a/quickstart-exposing/)
      * [Go](../../a2a/quickstart-exposing-go/)
    - A2A Quickstart (Consuming)




      A2A Quickstart (Consuming)
      * [Python](../../a2a/quickstart-consuming/)
      * [Go](../../a2a/quickstart-consuming-go/)
  + [Bidi-streaming (live)](../../streaming/)

    Bidi-streaming (live)
    - [Custom Audio Bidi-streaming app sample (WebSockets)](../../streaming/custom-streaming-ws/)
    - [Bidi-streaming development guide series](../../streaming/dev-guide/part1/)
    - [Streaming Tools](../../streaming/streaming-tools/)
    - [Configurating Bidi-streaming behaviour](../../streaming/configuration/)
  + Grounding




    Grounding
    - [Understanding Google Search Grounding](../../grounding/google_search_grounding/)
    - [Understanding Vertex AI Search Grounding](../../grounding/vertex_ai_search_grounding/)
* Reference




  Reference
  + [API Reference](../../api-reference/)

    API Reference
    - [Python ADK](../../api-reference/python/)
    - [Go ADK](https://pkg.go.dev/google.golang.org/adk)
    - [Java ADK](../../api-reference/java/)
    - [CLI Reference](../../api-reference/cli/)
    - [Agent Config reference](../../api-reference/agentconfig/)
    - [REST API](../../api-reference/rest/)
  + [Community Resources](../../community/)
  + [Contributing Guide](../../contributing-guide/)

Table of contents

* [Apigee API Hub Tools](#apigee-api-hub-tools)

  + [Create an API Hub Toolset](#create-an-api-hub-toolset)
* [Application Integration Tools](#application-integration-tools)

  + [Prerequisites](#prerequisites)

    - [1. Install ADK](#1-install-adk)
    - [2. Install CLI](#2-install-cli)
    - [3. Provision Application Integration workflow and publish Connection Tool](#3-provision-application-integration-workflow-and-publish-connection-tool)
    - [4. Create project structure](#4-create-project-structure)
    - [5. Set roles and permissions](#5-set-roles-and-permissions)
  + [Use Integration Connectors](#use-integration-connectors)

    - [Before you begin](#before-you-begin)
    - [Create an Application Integration Toolset](#create-an-application-integration-toolset)
  + [Use Application Integration Workflows](#use-application-integration-workflows)

    - [1. Create a tool](#1-create-a-tool)
    - [2. Add the tool to your agent](#2-add-the-tool-to-your-agent)
    - [3. Expose your agent](#3-expose-your-agent)
    - [4. Use your agent](#4-use-your-agent)

# Google Cloud Tools[¶](#google-cloud-tools "Permanent link")

Google Cloud tools make it easier to connect your agents to Google Cloud’s
products and services. With just a few lines of code you can use these tools to
connect your agents with:

* **Any custom APIs** that developers host in Apigee.
* **100s** of **prebuilt connectors** to enterprise systems such as Salesforce,
  Workday, and SAP.
* **Automation workflows** built using application integration.
* **Databases** such as Spanner, AlloyDB, Postgres and more using the MCP Toolbox for
  databases.

![Google Cloud Tools](../../assets/google_cloud_tools.svg)

## Apigee API Hub Tools[¶](#apigee-api-hub-tools "Permanent link")

Supported in ADKPython v0.1.0

**ApiHubToolset** lets you turn any documented API from Apigee API hub into a
tool with a few lines of code. This section shows you the step by step
instructions including setting up authentication for a secure connection to your
APIs.

**Prerequisites**

1. [Install ADK](../../get-started/installation/)
2. Install the
   [Google Cloud CLI](https://cloud.google.com/sdk/docs/install?db=bigtable-docs#installation_instructions).
3. [Apigee API hub](https://cloud.google.com/apigee/docs/apihub/what-is-api-hub)
   instance with documented (i.e. OpenAPI spec) APIs
4. Set up your project structure and create required files

```python
project_root_folder
 |
 `-- my_agent
     |-- .env
     |-- __init__.py
     |-- agent.py
     `__ tool.py
```

### Create an API Hub Toolset[¶](#create-an-api-hub-toolset "Permanent link")

Note: This tutorial includes an agent creation. If you already have an agent,
you only need to follow a subset of these steps.

1. Get your access token, so that APIHubToolset can fetch spec from API Hub API.
   In your terminal run the following command

   ```python
   gcloud auth print-access-token
   # Prints your access token like 'ya29....'
   ```
2. Ensure that the account used has the required permissions. You can use the
   pre-defined role `roles/apihub.viewer` or assign the following permissions:

   1. **apihub.specs.get (required)**
   2. apihub.apis.get (optional)
   3. apihub.apis.list (optional)
   4. apihub.versions.get (optional)
   5. apihub.versions.list (optional)
   6. apihub.specs.list (optional)
3. Create a tool with `APIHubToolset`. Add the below to `tools.py`

   If your API requires authentication, you must configure authentication for
   the tool. The following code sample demonstrates how to configure an API
   key. ADK supports token based auth (API Key, Bearer token), service account,
   and OpenID Connect. We will soon add support for various OAuth2 flows.

   ```python
   from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
   from google.adk.tools.apihub_tool.apihub_toolset import APIHubToolset

   # Provide authentication for your APIs. Not required if your APIs don't required authentication.
   auth_scheme, auth_credential = token_to_scheme_credential(
       "apikey", "query", "apikey", apikey_credential_str
   )

   sample_toolset = APIHubToolset(
       name="apihub-sample-tool",
       description="Sample Tool",
       access_token="...",  # Copy your access token generated in step 1
       apihub_resource_name="...", # API Hub resource name
       auth_scheme=auth_scheme,
       auth_credential=auth_credential,
   )
   ```

   For production deployment we recommend using a service account instead of an
   access token. In the code snippet above, use
   `service_account_json=service_account_cred_json_str` and provide your
   security account credentials instead of the token.

   For apihub\_resource\_name, if you know the specific ID of the OpenAPI Spec
   being used for your API, use
   `` `projects/my-project-id/locations/us-west1/apis/my-api-id/versions/version-id/specs/spec-id` ``.
   If you would like the Toolset to automatically pull the first available spec
   from the API, use
   `` `projects/my-project-id/locations/us-west1/apis/my-api-id` ``
4. Create your agent file Agent.py and add the created tools to your agent
   definition:

   ```python
   from google.adk.agents.llm_agent import LlmAgent
   from .tools import sample_toolset

   root_agent = LlmAgent(
       model='gemini-2.0-flash',
       name='enterprise_assistant',
       instruction='Help user, leverage the tools you have access to',
       tools=sample_toolset.get_tools(),
   )
   ```
5. Configure your `__init__.py` to expose your agent

   ```python
   from . import agent
   ```
6. Start the Google ADK Web UI and try your agent:

   ```python
   # make sure to run `adk web` from your project_root_folder
   adk web
   ```

Then go to <http://localhost:8000> to try your agent from the Web UI.

---

## Application Integration Tools[¶](#application-integration-tools "Permanent link")

Supported in ADKPython v0.1.0Java v0.3.0

With **ApplicationIntegrationToolset**, you can seamlessly give your agents
secure and governed access to enterprise applications using Integration
Connectors' 100+ pre-built connectors for systems like Salesforce, ServiceNow,
JIRA, SAP, and more.

It supports both on-premise and SaaS applications. In addition, you can turn
your existing Application Integration process automations into agentic workflows
by providing application integration workflows as tools to your ADK agents.

Federated search within Application Integration lets you use ADK agents to query
multiple enterprise applications and data sources simultaneously.

[See how ADK Federated Search in Application Integration works in this video walkthrough](https://www.youtube.com/watch?v=JdlWOQe5RgU)

### Prerequisites[¶](#prerequisites "Permanent link")

#### 1. Install ADK[¶](#1-install-adk "Permanent link")

Install Agent Development Kit following the steps in the
[installation guide](../../get-started/installation/).

#### 2. Install CLI[¶](#2-install-cli "Permanent link")

Install the
[Google Cloud CLI](https://cloud.google.com/sdk/docs/install#installation_instructions).
To use the tool with default credentials, run the following commands:

```python
gcloud config set project <project-id>
gcloud auth application-default login
gcloud auth application-default set-quota-project <project-id>
```

Replace `<project-id>` with the unique ID of your Google Cloud project.

#### 3. Provision Application Integration workflow and publish Connection Tool[¶](#3-provision-application-integration-workflow-and-publish-connection-tool "Permanent link")

Use an existing
[Application Integration](https://cloud.google.com/application-integration/docs/overview)
workflow or
[Integrations Connector](https://cloud.google.com/integration-connectors/docs/overview)
connection you want to use with your agent. You can also create a new
[Application Integration workflow](https://cloud.google.com/application-integration/docs/setup-application-integration)
or a
[connection](https://cloud.google.com/integration-connectors/docs/connectors/neo4j/configure#configure-the-connector).

Import and publish the
[Connection Tool](https://console.cloud.google.com/integrations/templates/connection-tool/locations/global)
from the template library.

**Note**: To use a connector from Integration Connectors, you need to provision
the Application Integration in the same region as your connection.

#### 4. Create project structure[¶](#4-create-project-structure "Permanent link")

PythonJava

Set up your project structure and create the required files:

```python
project_root_folder
├── .env
└── my_agent
    ├── __init__.py
    ├── agent.py
    └── tools.py
```

When running the agent, make sure to run `adk web` from the `project_root_folder`.

Set up your project structure and create the required files:

```python
  project_root_folder
  └── my_agent
      ├── agent.java
      └── pom.xml
```

When running the agent, make sure to run the commands from the `project_root_folder`.

#### 5. Set roles and permissions[¶](#5-set-roles-and-permissions "Permanent link")

To get the permissions that you need to set up
**ApplicationIntegrationToolset**, you must have the following IAM roles on the
project (common to both Integration Connectors and Application Integration
Workflows):

```python
- roles/integrations.integrationEditor
- roles/connectors.invoker
- roles/secretmanager.secretAccessor
```

**Note:** When using Agent Engine (AE) for deployment, don't use
`roles/integrations.integrationInvoker`, as it can result in 403 errors. Use
`roles/integrations.integrationEditor` instead.

### Use Integration Connectors[¶](#use-integration-connectors "Permanent link")

Connect your agent to enterprise applications using
[Integration Connectors](https://cloud.google.com/integration-connectors/docs/overview).

#### Before you begin[¶](#before-you-begin "Permanent link")

**Note:** The *ExecuteConnection* integration is typically created automatically when you provision Application Integration in a given region. If the *ExecuteConnection* doesn't exist in the [list of integrations](https://console.cloud.google.com/integrations/list), you must follow these steps to create it:

1. To use a connector from Integration Connectors, click **QUICK SETUP** and [provision](https://console.cloud.google.com/integrations)
   Application Integration in the same region as your connection.

![Google Cloud Tools](../../assets/application-integration-overview.png)

1. Go to the [Connection Tool](https://console.cloud.google.com/integrations/templates/connection-tool/locations/us-central1)
   template in the template library and click **USE TEMPLATE**.

   ![Google Cloud Tools](../../assets/use-connection-tool-template.png)
2. Enter the Integration Name as *ExecuteConnection* (it is mandatory to use this exact integration name only).
   Then, select the region to match your connection region and click **CREATE**.
3. Click **PUBLISH** to publish the integration in the *Application Integration* editor.

   ![Google Cloud Tools](../../assets/publish-integration.png)

#### Create an Application Integration Toolset[¶](#create-an-application-integration-toolset "Permanent link")

To create an Application Integration Toolset for Integration Connectors, follow these steps:

1. Create a tool with `ApplicationIntegrationToolset` in the `tools.py` file:

   ```python
   from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset

   connector_tool = ApplicationIntegrationToolset(
       project="test-project", # TODO: replace with GCP project of the connection
       location="us-central1", #TODO: replace with location of the connection
       connection="test-connection", #TODO: replace with connection name
       entity_operations={"Entity_One": ["LIST","CREATE"], "Entity_Two": []},#empty list for actions means all operations on the entity are supported.
       actions=["action1"], #TODO: replace with actions
       service_account_json='{...}', # optional. Stringified json for service account key
       tool_name_prefix="tool_prefix2",
       tool_instructions="..."
   )
   ```

   **Note:**

   * You can provide a service account to be used instead of default credentials by generating a [Service Account Key](https://cloud.google.com/iam/docs/keys-create-delete#creating), and providing the right [Application Integration and Integration Connector IAM roles](#prerequisites) to the service account.
   * To find the list of supported entities and actions for a connection, use the Connectors APIs: [listActions](https://cloud.google.com/integration-connectors/docs/reference/rest/v1/projects.locations.connections.connectionSchemaMetadata/listActions) or [listEntityTypes](https://cloud.google.com/integration-connectors/docs/reference/rest/v1/projects.locations.connections.connectionSchemaMetadata/listEntityTypes).

   `ApplicationIntegrationToolset` supports `auth_scheme` and `auth_credential` for **dynamic OAuth2 authentication** for Integration Connectors. To use it, create a tool similar to this in the `tools.py` file:

   ```python
   from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset
   from google.adk.tools.openapi_tool.auth.auth_helpers import dict_to_auth_scheme
   from google.adk.auth import AuthCredential
   from google.adk.auth import AuthCredentialTypes
   from google.adk.auth import OAuth2Auth

   oauth2_data_google_cloud = {
     "type": "oauth2",
     "flows": {
         "authorizationCode": {
             "authorizationUrl": "https://accounts.google.com/o/oauth2/auth",
             "tokenUrl": "https://oauth2.googleapis.com/token",
             "scopes": {
                 "https://www.googleapis.com/auth/cloud-platform": (
                     "View and manage your data across Google Cloud Platform"
                     " services"
                 ),
                 "https://www.googleapis.com/auth/calendar.readonly": "View your calendars"
             },
         }
     },
   }

   oauth_scheme = dict_to_auth_scheme(oauth2_data_google_cloud)

   auth_credential = AuthCredential(
     auth_type=AuthCredentialTypes.OAUTH2,
     oauth2=OAuth2Auth(
         client_id="...", #TODO: replace with client_id
         client_secret="...", #TODO: replace with client_secret
     ),
   )

   connector_tool = ApplicationIntegrationToolset(
       project="test-project", # TODO: replace with GCP project of the connection
       location="us-central1", #TODO: replace with location of the connection
       connection="test-connection", #TODO: replace with connection name
       entity_operations={"Entity_One": ["LIST","CREATE"], "Entity_Two": []},#empty list for actions means all operations on the entity are supported.
       actions=["GET_calendars/%7BcalendarId%7D/events"], #TODO: replace with actions. this one is for list events
       service_account_json='{...}', # optional. Stringified json for service account key
       tool_name_prefix="tool_prefix2",
       tool_instructions="...",
       auth_scheme=oauth_scheme,
       auth_credential=auth_credential
   )
   ```
2. Update the `agent.py` file and add tool to your agent:

   ```python
   from google.adk.agents.llm_agent import LlmAgent
   from .tools import connector_tool

   root_agent = LlmAgent(
       model='gemini-2.0-flash',
       name='connector_agent',
       instruction="Help user, leverage the tools you have access to",
       tools=[connector_tool],
   )
   ```
3. Configure `__init__.py` to expose your agent:

   ```python
   from . import agent
   ```
4. Start the Google ADK Web UI and use your agent:

   ```python
   # make sure to run `adk web` from your project_root_folder
   adk web
   ```

After completing the above steps, go to <http://localhost:8000>, and choose
`my\_agent` agent (which is the same as the agent folder name).

### Use Application Integration Workflows[¶](#use-application-integration-workflows "Permanent link")

Use an existing
[Application Integration](https://cloud.google.com/application-integration/docs/overview)
workflow as a tool for your agent or create a new one.

#### 1. Create a tool[¶](#1-create-a-tool "Permanent link")

PythonJava

To create a tool with `ApplicationIntegrationToolset` in the `tools.py` file, use the following code:

```python
    integration_tool = ApplicationIntegrationToolset(
        project="test-project", # TODO: replace with GCP project of the connection
        location="us-central1", #TODO: replace with location of the connection
        integration="test-integration", #TODO: replace with integration name
        triggers=["api_trigger/test_trigger"],#TODO: replace with trigger id(s). Empty list would mean all api triggers in the integration to be considered.
        service_account_json='{...}', #optional. Stringified json for service account key
        tool_name_prefix="tool_prefix1",
        tool_instructions="..."
    )
```

**Note:** You can provide a service account to be used instead of using default credentials. To do this, generate a [Service Account Key](https://cloud.google.com/iam/docs/keys-create-delete#creating) and provide the correct
[Application Integration and Integration Connector IAM roles](#prerequisites) to the service account. For more details about the IAM roles, refer to the [Prerequisites](#prerequisites) section.

To create a tool with `ApplicationIntegrationToolset` in the `tools.java` file, use the following code:

```python
    import com.google.adk.tools.applicationintegrationtoolset.ApplicationIntegrationToolset;
    import com.google.common.collect.ImmutableList;
    import com.google.common.collect.ImmutableMap;

    public class Tools {
        private static ApplicationIntegrationToolset integrationTool;
        private static ApplicationIntegrationToolset connectionsTool;

        static {
            integrationTool = new ApplicationIntegrationToolset(
                    "test-project",
                    "us-central1",
                    "test-integration",
                    ImmutableList.of("api_trigger/test-api"),
                    null,
                    null,
                    null,
                    "{...}",
                    "tool_prefix1",
                    "...");

            connectionsTool = new ApplicationIntegrationToolset(
                    "test-project",
                    "us-central1",
                    null,
                    null,
                    "test-connection",
                    ImmutableMap.of("Issue", ImmutableList.of("GET")),
                    ImmutableList.of("ExecuteCustomQuery"),
                    "{...}",
                    "tool_prefix",
                    "...");
        }
    }
```

**Note:** You can provide a service account to be used instead of using default credentials. To do this, generate a [Service Account Key](https://cloud.google.com/iam/docs/keys-create-delete#creating) and provide the correct [Application Integration and Integration Connector IAM roles](#prerequisites) to the service account. For more details about the IAM roles, refer to the [Prerequisites](#prerequisites) section.

#### 2. Add the tool to your agent[¶](#2-add-the-tool-to-your-agent "Permanent link")

PythonJava

To update the `agent.py` file and add the tool to your agent, use the following code:

```python
    from google.adk.agents.llm_agent import LlmAgent
    from .tools import integration_tool, connector_tool

    root_agent = LlmAgent(
        model='gemini-2.0-flash',
        name='integration_agent',
        instruction="Help user, leverage the tools you have access to",
        tools=[integration_tool],
    )
```

To update the `agent.java` file and add the tool to your agent, use the following code:

```java
import com.google.adk.agent.LlmAgent;
import com.google.adk.tools.BaseTool;
import com.google.common.collect.ImmutableList;

```python
    public class MyAgent {
        public static void main(String[] args) {
            // Assuming Tools class is defined as in the previous step
            ImmutableList<BaseTool> tools = ImmutableList.<BaseTool>builder()
                    .add(Tools.integrationTool)
                    .add(Tools.connectionsTool)
                    .build();

            // Finally, create your agent with the tools generated automatically.
            LlmAgent rootAgent = LlmAgent.builder()
                    .name("science-teacher")
                    .description("Science teacher agent")
                    .model("gemini-2.0-flash")
                    .instruction(
                            "Help user, leverage the tools you have access to."
                    )
                    .tools(tools)
                    .build();

            // You can now use rootAgent to interact with the LLM
            // For example, you can start a conversation with the agent.
        }
    }
```
```

**Note:** To find the list of supported entities and actions for a
connection, use these Connector APIs: `listActions`, `listEntityTypes`.

#### 3. Expose your agent[¶](#3-expose-your-agent "Permanent link")

Python

To configure `__init__.py` to expose your agent, use the following code:

```python
    from . import agent
```

#### 4. Use your agent[¶](#4-use-your-agent "Permanent link")

PythonJava

To start the Google ADK Web UI and use your agent, use the following commands:

```python
    # make sure to run `adk web` from your project_root_folder
    adk web
```

After completing the above steps, go to <http://localhost:8000>, and choose the `my_agent` agent (which is the same as the agent folder name).

To start the Google ADK Web UI and use your agent, use the following commands:

```python
    mvn install

    mvn exec:java \
        -Dexec.mainClass="com.google.adk.web.AdkWebServer" \
        -Dexec.args="--adk.agents.source-dir=src/main/java" \
        -Dexec.classpathScope="compile"
```

After completing the above steps, go to <http://localhost:8000>, and choose the `my_agent` agent (which is the same as the agent folder name).

Back to top