---
url: https://google.github.io/adk-docs/grounding/google_search_grounding/
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
  + [Tools for Agents](../../tools/)

    Tools for Agents
    - [Built-in tools](../../tools/built-in-tools/)
    - Gemini API tools




      Gemini API tools
      * [Computer use](../../tools/gemini-api/computer-use/)
    - Google Cloud tools




      Google Cloud tools
      * [Overview](../../tools/google-cloud-tools/)
      * [MCP Toolbox for Databases](../../tools/google-cloud/mcp-toolbox-for-databases/)
      * [BigQuery Agent Analytics](../../tools/google-cloud/bigquery-agent-analytics/)
      * [Code Execution with Agent Engine](../../tools/google-cloud/code-exec-agent-engine/)
    - [Third-party tools](../../tools/third-party/)

      Third-party tools
      * [AgentQL](../../tools/third-party/agentql/)
      * [Bright Data](../../tools/third-party/bright-data/)
      * [Browserbase](../../tools/third-party/browserbase/)
      * [Exa](../../tools/third-party/exa/)
      * [Firecrawl](../../tools/third-party/firecrawl/)
      * [GitHub](../../tools/third-party/github/)
      * [Hugging Face](../../tools/third-party/hugging-face/)
      * [Notion](../../tools/third-party/notion/)
      * [Tavily](../../tools/third-party/tavily/)
      * [Agentic UI (AG-UI)](../../tools/third-party/ag-ui/)
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
    - Understanding Google Search Grounding

      [Understanding Google Search Grounding](./)



      Table of contents
      * [What You'll Learn](#what-youll-learn)

        + [Additional resource](#additional-resource)
      * [Google Search Grounding Quickstart](#google-search-grounding-quickstart)

        + [1. Set up Environment & Install ADK](#set-up-environment-install-adk)
        + [2. Create Agent Project](#create-agent-project)

          - [Edit agent.py](#edit-agentpy)
        + [3. Choose a platform](#choose-a-platform)
        + [4. Run Your Agent](#run-your-agent)
        + [📝 Example prompts to try](#example-prompts-to-try)
      * [How grounding with Google Search works](#how-grounding-with-google-search-works)

        + [Data Flow Diagram](#data-flow-diagram)
        + [Detailed Description](#detailed-description)
        + [Understanding grounding with Google Search response](#understanding-grounding-with-google-search-response)

          - [Example of a Grounded Response](#example-of-a-grounded-response)
          - [How to Interpret the Response](#how-to-interpret-the-response)
        + [How to display grounding responses with Google Search](#how-to-display-grounding-responses-with-google-search)

          - [Displaying Search Suggestions](#displaying-search-suggestions)
      * [Summary](#summary)
    - [Understanding Vertex AI Search Grounding](../vertex_ai_search_grounding/)
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

* [What You'll Learn](#what-youll-learn)

  + [Additional resource](#additional-resource)
* [Google Search Grounding Quickstart](#google-search-grounding-quickstart)

  + [1. Set up Environment & Install ADK](#set-up-environment-install-adk)
  + [2. Create Agent Project](#create-agent-project)

    - [Edit agent.py](#edit-agentpy)
  + [3. Choose a platform](#choose-a-platform)
  + [4. Run Your Agent](#run-your-agent)
  + [📝 Example prompts to try](#example-prompts-to-try)
* [How grounding with Google Search works](#how-grounding-with-google-search-works)

  + [Data Flow Diagram](#data-flow-diagram)
  + [Detailed Description](#detailed-description)
  + [Understanding grounding with Google Search response](#understanding-grounding-with-google-search-response)

    - [Example of a Grounded Response](#example-of-a-grounded-response)
    - [How to Interpret the Response](#how-to-interpret-the-response)
  + [How to display grounding responses with Google Search](#how-to-display-grounding-responses-with-google-search)

    - [Displaying Search Suggestions](#displaying-search-suggestions)
* [Summary](#summary)

# Understanding Google Search Grounding[¶](#understanding-google-search-grounding "Permanent link")

[Google Search Grounding tool](../../tools/built-in-tools/#google-search) is a powerful feature in the Agent Development Kit (ADK) that enables AI agents to access real-time, authoritative information from the web. By connecting your agents to Google Search, you can provide users with up-to-date answers backed by reliable sources.

This feature is particularly valuable for queries requiring current information like weather updates, news events, stock prices, or any facts that may have changed since the model's training data cutoff. When your agent determines that external information is needed, it automatically performs web searches and incorporates the results into its response with proper attribution.

## What You'll Learn[¶](#what-youll-learn "Permanent link")

In this guide, you'll discover:

* **Quick Setup**: How to create and run a Google Search-enabled agent from scratch
* **Grounding Architecture**: The data flow and technical process behind web grounding
* **Response Structure**: How to interpret grounded responses and their metadata
* **Best Practices**: Guidelines for displaying search results and citations to users

### Additional resource[¶](#additional-resource "Permanent link")

As an additional resource, [Gemini Fullstack Agent Development Kit (ADK) Quickstart](https://github.com/google/adk-samples/tree/main/python/agents/gemini-fullstack) has [a great practical use of the Google Search grounding](https://github.com/google/adk-samples/blob/main/python/agents/gemini-fullstack/app/agent.py) as a full stack application example.

## Google Search Grounding Quickstart[¶](#google-search-grounding-quickstart "Permanent link")

This quickstart guides you through creating an ADK agent with Google Search grounding feature. This quickstart assumes a local IDE (VS Code or PyCharm, etc.) with Python 3.9+ and terminal access.

### 1. Set up Environment & Install ADK[¶](#set-up-environment-install-adk "Permanent link")

Create & Activate Virtual Environment:

```python
# Create
python -m venv .venv

# Activate (each new terminal)
# macOS/Linux: source .venv/bin/activate
# Windows CMD: .venv\Scripts\activate.bat
# Windows PowerShell: .venv\Scripts\Activate.ps1
```

Install ADK:

```python
pip install google-adk==1.4.2
```

### 2. Create Agent Project[¶](#create-agent-project "Permanent link")

Under a project directory, run the following commands:

OS X & LinuxWindows

```python
# Step 1: Create a new directory for your agent
mkdir google_search_agent

# Step 2: Create __init__.py for the agent
echo "from . import agent" > google_search_agent/__init__.py

# Step 3: Create an agent.py (the agent definition) and .env (Gemini authentication config)
touch google_search_agent/agent.py .env
```

```python
# Step 1: Create a new directory for your agent
mkdir google_search_agent

# Step 2: Create __init__.py for the agent
echo "from . import agent" > google_search_agent/__init__.py

# Step 3: Create an agent.py (the agent definition) and .env (Gemini authentication config)
type nul > google_search_agent\agent.py 
type nul > google_search_agent\.env
```

#### Edit `agent.py`[¶](#edit-agentpy "Permanent link")

Copy and paste the following code into `agent.py`:

google\_search\_agent/agent.py

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="google_search_agent",
    model="gemini-2.5-flash",
    instruction="Answer questions using Google Search when needed. Always cite sources.",
    description="Professional search assistant with Google Search capabilities",
    tools=[google_search]
)
```

Now you would have the following directory structure:

```python
my_project/
    google_search_agent/
        __init__.py
        agent.py
    .env
```

### 3. Choose a platform[¶](#choose-a-platform "Permanent link")

To run the agent, you need to select a platform that the agent will use for calling the Gemini model. Choose one from Google AI Studio or Vertex AI:

Gemini - Google AI StudioGemini - Google Cloud Vertex AI

1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).
2. When using Python, open the **`.env`** file and copy-paste the following code.

   .env

   ```python
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
   ```
3. Replace `PASTE_YOUR_ACTUAL_API_KEY_HERE` with your actual `API KEY`.

1. You need an existing
   [Google Cloud](https://cloud.google.com/?e=48754805&hl=en) account and a
   project.
   * Set up a
     [Google Cloud project](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal#setup-gcp)
   * Set up the
     [gcloud CLI](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal#setup-local)
   * Authenticate to Google Cloud, from the terminal by running
     `gcloud auth login`.
   * [Enable the Vertex AI API](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com).
2. When using Python, open the **`.env`** file and copy-paste the following code and update the project ID and location.

   .env

   ```python
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
   GOOGLE_CLOUD_LOCATION=LOCATION
   ```

### 4. Run Your Agent[¶](#run-your-agent "Permanent link")

There are multiple ways to interact with your agent:

Dev UI (adk web)Terminal (adk run)

Run the following command to launch the **dev UI**.

```python
adk web
```

Note for Windows users

When hitting the `_make_subprocess_transport NotImplementedError`, consider using `adk web --no-reload` instead.

**Step 1:** Open the URL provided (usually `http://localhost:8000` or
`http://127.0.0.1:8000`) directly in your browser.

**Step 2.** In the top-left corner of the UI, you can select your agent in
the dropdown. Select "google\_search\_agent".

Troubleshooting

If you do not see "google\_search\_agent" in the dropdown menu, make sure you
are running `adk web` in the **parent folder** of your agent folder
(i.e. the parent folder of google\_search\_agent).

**Step 3.** Now you can chat with your agent using the textbox.

Run the following command, to chat with your Weather agent.

```python
adk run google_search_agent
```

To exit, use Cmd/Ctrl+C.

### 📝 Example prompts to try[¶](#example-prompts-to-try "Permanent link")

With those questions, you can confirm that the agent is actually calling Google Search
to get the latest weather and time.

* What is the weather in New York?
* What is the time in New York?
* What is the weather in Paris?
* What is the time in Paris?

![Try the agent with adk web](../../assets/google_search_grd_adk_web.png)

You've successfully created and interacted with your Google Search agent using ADK!

## How grounding with Google Search works[¶](#how-grounding-with-google-search-works "Permanent link")

Grounding is the process that connects your agent to real-time information from the web, allowing it to generate more accurate and current responses. When a user's prompt requires information that the model was not trained on, or that is time-sensitive, the agent's underlying Large Language Model intelligently decides to invoke the google\_search tool to find the relevant facts

### **Data Flow Diagram**[¶](#data-flow-diagram "Permanent link")

This diagram illustrates the step-by-step process of how a user query results in a grounded response.

![](../../assets/google_search_grd_dataflow.png)

### **Detailed Description**[¶](#detailed-description "Permanent link")

The grounding agent uses the data flow described in the diagram to retrieve, process, and incorporate external information into the final answer presented to the user.

1. **User Query**: An end-user interacts with your agent by asking a question or giving a command.
2. **ADK Orchestration** : The Agent Development Kit orchestrates the agent's behavior and passes the user's message to the core of your agent.
3. **LLM Analysis and Tool-Calling** : The agent's LLM (e.g., a Gemini model) analyzes the prompt. If it determines that external, up-to-date information is required, it triggers the grounding mechanism by calling the  
   google\_search tool. This is ideal for answering queries about recent news, weather, or facts not present in the model's training data.
4. **Grounding Service Interaction** : The google\_search tool interacts with an internal grounding service that formulates and sends one or more queries to the Google Search Index.
5. **Context Injection**: The grounding service retrieves the relevant web pages and snippets. It then integrates these search results into the model's context  
   before the final response is generated. This crucial step allows the model to "reason" over factual, real-time data.
6. **Grounded Response Generation**: The LLM, now informed by the fresh search results, generates a response that incorporates the retrieved information.
7. **Response Presentation with Sources** : The ADK receives the final grounded response, which includes the necessary source URLs and   
   groundingMetadata, and presents it to the user with attribution. This allows end-users to verify the information and builds trust in the agent's answers.

### Understanding grounding with Google Search response[¶](#understanding-grounding-with-google-search-response "Permanent link")

When the agent uses Google Search to ground a response, it returns a detailed set of information that includes not only the final text answer but also the sources it used to generate that answer. This metadata is crucial for verifying the response and for providing attribution to the original sources.

#### **Example of a Grounded Response**[¶](#example-of-a-grounded-response "Permanent link")

The following is an example of the content object returned by the model after a grounded query.

**Final Answer Text:**

```python
"Yes, Inter Miami won their last game in the FIFA Club World Cup. They defeated FC Porto 2-1 in their second group stage match. Their first game in the tournament was a 0-0 draw against Al Ahly FC. Inter Miami is scheduled to play their third group stage match against Palmeiras on Monday, June 23, 2025."
```

**Grounding Metadata Snippet:**

```python
"groundingMetadata": {
  "groundingChunks": [
    { "web": { "title": "mlssoccer.com", "uri": "..." } },
    { "web": { "title": "intermiamicf.com", "uri": "..." } },
    { "web": { "title": "mlssoccer.com", "uri": "..." } }
  ],
  "groundingSupports": [
    {
      "groundingChunkIndices": [0, 1],
      "segment": {
        "startIndex": 65,
        "endIndex": 126,
        "text": "They defeated FC Porto 2-1 in their second group stage match."
      }
    },
    {
      "groundingChunkIndices": [1],
      "segment": {
        "startIndex": 127,
        "endIndex": 196,
        "text": "Their first game in the tournament was a 0-0 draw against Al Ahly FC."
      }
    },
    {
      "groundingChunkIndices": [0, 2],
      "segment": {
        "startIndex": 197,
        "endIndex": 303,
        "text": "Inter Miami is scheduled to play their third group stage match against Palmeiras on Monday, June 23, 2025."
      }
    }
  ],
  "searchEntryPoint": { ... }
}
```

#### **How to Interpret the Response**[¶](#how-to-interpret-the-response "Permanent link")

The metadata provides a link between the text generated by the model and the sources that support it. Here is a step-by-step breakdown:

1. **groundingChunks**: This is a list of the web pages the model consulted. Each chunk contains the title of the webpage and a uri that links to the source.
2. **groundingSupports**: This list connects specific sentences in the final answer back to the groundingChunks.
3. **segment**: This object identifies a specific portion of the final text answer, defined by its startIndex, endIndex, and the text itself.
4. **groundingChunkIndices**: This array contains the index numbers that correspond to the sources listed in the groundingChunks. For example, the sentence "They defeated FC Porto 2-1..." is supported by information from groundingChunks at index 0 and 1 (both from mlssoccer.com and intermiamicf.com).

### How to display grounding responses with Google Search[¶](#how-to-display-grounding-responses-with-google-search "Permanent link")

A critical part of using grounding is to correctly display the information, including citations and search suggestions, to the end-user. This builds trust and allows users to verify the information.

![Responnses from Google Search](../../assets/google_search_grd_resp.png)

#### **Displaying Search Suggestions**[¶](#displaying-search-suggestions "Permanent link")

The `searchEntryPoint` object in the `groundingMetadata` contains pre-formatted HTML for displaying search query suggestions. As seen in the example image, these are typically rendered as clickable chips that allow the user to explore related topics.

**Rendered HTML from searchEntryPoint:** The metadata provides the necessary HTML and CSS to render the search suggestions bar, which includes the Google logo and chips for related queries like "When is the next FIFA Club World Cup" and "Inter Miami FIFA Club World Cup history". Integrating this HTML directly into your application's front end will display the suggestions as intended.

For more information, consult [using Google Search Suggestions](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/grounding-search-suggestions) in Vertex AI documentation.

## Summary[¶](#summary "Permanent link")

Google Search Grounding transforms AI agents from static knowledge repositories into dynamic, web-connected assistants capable of providing real-time, accurate information. By integrating this feature into your ADK agents, you enable them to:

* Access current information beyond their training data
* Provide source attribution for transparency and trust
* Deliver comprehensive answers with verifiable facts
* Enhance user experience with relevant search suggestions

The grounding process seamlessly connects user queries to Google's vast search index, enriching responses with up-to-date context while maintaining the conversational flow. With proper implementation and display of grounded responses, your agents become powerful tools for information discovery and decision-making.

Back to top