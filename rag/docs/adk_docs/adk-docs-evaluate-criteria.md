---
url: https://google.github.io/adk-docs/evaluate/criteria/
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
  + [Evaluation](../)

    Evaluation
    - Criteria

      [Criteria](./)



      Table of contents
      * [tool\_trajectory\_avg\_score](#tool_trajectory_avg_score)

        + [When To Use This Criterion?](#when-to-use-this-criterion)
        + [Details](#details)
        + [How To Use This Criterion?](#how-to-use-this-criterion)
        + [Output And How To Interpret](#output-and-how-to-interpret)
      * [response\_match\_score](#response_match_score)

        + [When To Use This Criterion?](#when-to-use-this-criterion_1)
        + [Details](#details_1)
        + [How To Use This Criterion?](#how-to-use-this-criterion_1)
        + [Output And How To Interpret](#output-and-how-to-interpret_1)
      * [final\_response\_match\_v2](#final_response_match_v2)

        + [When To Use This Criterion?](#when-to-use-this-criterion_2)
        + [Details](#details_2)
        + [How To Use This Criterion?](#how-to-use-this-criterion_2)
        + [Output And How To Interpret](#output-and-how-to-interpret_2)
      * [rubric\_based\_final\_response\_quality\_v1](#rubric_based_final_response_quality_v1)

        + [When To Use This Criterion?](#when-to-use-this-criterion_3)
        + [Details](#details_3)
        + [How To Use This Criterion?](#how-to-use-this-criterion_3)
        + [Output And How To Interpret](#output-and-how-to-interpret_3)
      * [rubric\_based\_tool\_use\_quality\_v1](#rubric_based_tool_use_quality_v1)

        + [When To Use This Criterion?](#when-to-use-this-criterion_4)
        + [Details](#details_4)
        + [How To Use This Criterion?](#how-to-use-this-criterion_4)
        + [Output And How To Interpret](#output-and-how-to-interpret_4)
      * [hallucinations\_v1](#hallucinations_v1)

        + [When To Use This Criterion?](#when-to-use-this-criterion_5)
        + [Details](#details_5)
        + [How To Use This Criterion?](#how-to-use-this-criterion_5)
        + [Output And How To Interpret](#output-and-how-to-interpret_5)
      * [safety\_v1](#safety_v1)

        + [When To Use This Criterion?](#when-to-use-this-criterion_6)
        + [Details](#details_6)
        + [How To Use This Criterion?](#how-to-use-this-criterion_6)
        + [Output And How To Interpret](#output-and-how-to-interpret_6)
    - [User Simulation](../user-sim/)
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

* [tool\_trajectory\_avg\_score](#tool_trajectory_avg_score)

  + [When To Use This Criterion?](#when-to-use-this-criterion)
  + [Details](#details)
  + [How To Use This Criterion?](#how-to-use-this-criterion)
  + [Output And How To Interpret](#output-and-how-to-interpret)
* [response\_match\_score](#response_match_score)

  + [When To Use This Criterion?](#when-to-use-this-criterion_1)
  + [Details](#details_1)
  + [How To Use This Criterion?](#how-to-use-this-criterion_1)
  + [Output And How To Interpret](#output-and-how-to-interpret_1)
* [final\_response\_match\_v2](#final_response_match_v2)

  + [When To Use This Criterion?](#when-to-use-this-criterion_2)
  + [Details](#details_2)
  + [How To Use This Criterion?](#how-to-use-this-criterion_2)
  + [Output And How To Interpret](#output-and-how-to-interpret_2)
* [rubric\_based\_final\_response\_quality\_v1](#rubric_based_final_response_quality_v1)

  + [When To Use This Criterion?](#when-to-use-this-criterion_3)
  + [Details](#details_3)
  + [How To Use This Criterion?](#how-to-use-this-criterion_3)
  + [Output And How To Interpret](#output-and-how-to-interpret_3)
* [rubric\_based\_tool\_use\_quality\_v1](#rubric_based_tool_use_quality_v1)

  + [When To Use This Criterion?](#when-to-use-this-criterion_4)
  + [Details](#details_4)
  + [How To Use This Criterion?](#how-to-use-this-criterion_4)
  + [Output And How To Interpret](#output-and-how-to-interpret_4)
* [hallucinations\_v1](#hallucinations_v1)

  + [When To Use This Criterion?](#when-to-use-this-criterion_5)
  + [Details](#details_5)
  + [How To Use This Criterion?](#how-to-use-this-criterion_5)
  + [Output And How To Interpret](#output-and-how-to-interpret_5)
* [safety\_v1](#safety_v1)

  + [When To Use This Criterion?](#when-to-use-this-criterion_6)
  + [Details](#details_6)
  + [How To Use This Criterion?](#how-to-use-this-criterion_6)
  + [Output And How To Interpret](#output-and-how-to-interpret_6)

# Evaluation Criteria[¶](#evaluation-criteria "Permanent link")

Supported in ADKPython

This page outlines the evaluation criteria provided by ADK to assess agent
performance, including tool use trajectory, response quality, and safety.

| Criterion | Description | Reference-Based | Requires Rubrics | LLM-as-a-Judge | Supports [User Simulation](../user-sim/) |
| --- | --- | --- | --- | --- | --- |
| `tool_trajectory_avg_score` | Exact match of tool call trajectory | Yes | No | No | No |
| `response_match_score` | ROUGE-1 similarity to reference response | Yes | No | No | No |
| `final_response_match_v2` | LLM-judged semantic match to reference response | Yes | No | Yes | No |
| `rubric_based_final_response_quality_v1` | LLM-judged final response quality based on custom rubrics | No | Yes | Yes | No |
| `rubric_based_tool_use_quality_v1` | LLM-judged tool usage quality based on custom rubrics | No | Yes | Yes | No |
| `hallucinations_v1` | LLM-judged groundedness of agent response against context | No | No | Yes | Yes |
| `safety_v1` | Safety/harmlessness of agent response | No | No | Yes | Yes |

## tool\_trajectory\_avg\_score[¶](#tool_trajectory_avg_score "Permanent link")

This criterion compares the sequence of tools called by the agent against a list
of expected calls and computes an average score based on one of the match types:
`EXACT`, `IN_ORDER`, or `ANY_ORDER`.

#### When To Use This Criterion?[¶](#when-to-use-this-criterion "Permanent link")

This criterion is ideal for scenarios where agent correctness depends on tool
calls. Depending on how strictly tool calls need to be followed, you can choose
from one of three match types: `EXACT`, `IN_ORDER`, and `ANY_ORDER`.

This metric is particularly valuable for:

* **Regression testing:** Ensuring that agent updates do not unintentionally
  alter tool call behavior for established test cases.
* **Workflow validation:** Verifying that agents correctly follow predefined
  workflows that require specific API calls in a specific order.
* **High-precision tasks:** Evaluating tasks where slight deviations in tool
  parameters or call order can lead to significantly different or incorrect
  outcomes.

Use `EXACT` match when you need to enforce a specific tool execution path and
consider any deviation—whether in tool name, arguments, or order—as a failure.

Use `IN_ORDER` match when you want to ensure certain key tool calls occur in a
specific order, but allow for other tool calls to happen in between. This option is
useful in assuring if certain key actions or tool calls occur and in certain order,
leaving some scope for other tools calls to happen as well.

Use `ANY_ORDER` match when you want to ensure certain key tool calls occur, but
do not care about their order, and allow for other tool calls to happen in
between. This criteria is helpful for cases where multiple tool calls about the
same concept occur, like your agent issues 5 search queries. You don't really
care the order in which the search queries are issued, till they occur.

#### Details[¶](#details "Permanent link")

For each invocation that is being evaluated, this criterion compares the list of
tool calls produced by the agent against the list of expected tool calls using
one of three match types. If the tool calls match based on the selected match
type, a score of 1.0 is awarded for that invocation, otherwise the score is 0.0.
The final value is the average of these scores across all invocations in the
eval case.

The comparison can be done using one of following match types:

* **`EXACT`**: Requires a perfect match between the actual and expected tool
  calls, with no extra or missing tool calls.
* **`IN_ORDER`**: Requires all tool calls from the expected list to be present
  in the actual list, in the same order, but allows for other tool calls to
  appear in between.
* **`ANY_ORDER`**: Requires all tool calls from the expected list to be
  present in the actual list, in any order, and allows for other tool calls to
  appear in between.

#### How To Use This Criterion?[¶](#how-to-use-this-criterion "Permanent link")

By default, `tool_trajectory_avg_score` uses `EXACT` match type. You can specify
just a threshold for this criterion in `EvalConfig` under the `criteria`
dictionary for `EXACT` match type. The value should be a float between 0.0 and
1.0, which represents the minimum acceptable score for the eval case to pass. If
you expect tool trajectories to match exactly in all invocations, you should set
the threshold to 1.0.

Example `EvalConfig` entry for `EXACT` match:

```python
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0
  }
}
```

Or you could specify the `match_type` explicitly:

```python
{
  "criteria": {
    "tool_trajectory_avg_score": {
      "threshold": 1.0,
      "match_type": "EXACT"
    }
  }
}
```

If you want to use `IN_ORDER` or `ANY_ORDER` match type, you can specify it via
`match_type` field along with threshold.

Example `EvalConfig` entry for `IN_ORDER` match:

```python
{
  "criteria": {
    "tool_trajectory_avg_score": {
      "threshold": 1.0,
      "match_type": "IN_ORDER"
    }
  }
}
```

Example `EvalConfig` entry for `ANY_ORDER` match:

```python
{
  "criteria": {
    "tool_trajectory_avg_score": {
      "threshold": 1.0,
      "match_type": "ANY_ORDER"
    }
  }
}
```

#### Output And How To Interpret[¶](#output-and-how-to-interpret "Permanent link")

The output is a score between 0.0 and 1.0, where 1.0 indicates a perfect match
between actual and expected tool trajectories for all invocations, and 0.0
indicates a complete mismatch for all invocations. Higher scores are better. A
score below 1.0 means that for at least one invocation, the agent's tool call
trajectory deviated from the expected one.

## response\_match\_score[¶](#response_match_score "Permanent link")

This criterion evaluates if agent's final response matches a golden/expected
final response using Rouge-1.

### When To Use This Criterion?[¶](#when-to-use-this-criterion_1 "Permanent link")

Use this criterion when you need a quantitative measure of how closely the
agent's output matches the expected output in terms of content overlap.

### Details[¶](#details_1 "Permanent link")

ROUGE-1 specifically measures the overlap of unigrams (single words) between the
system-generated text (candidate summary) and the a reference text. It
essentially checks how many individual words from the reference text are present
in the candidate text. To learn more, see details on
[ROUGE-1](https://github.com/google-research/google-research/tree/master/rouge).

### How To Use This Criterion?[¶](#how-to-use-this-criterion_1 "Permanent link")

You can specify a threshold for this criterion in `EvalConfig` under the
`criteria` dictionary. The value should be a float between 0.0 and 1.0, which
represents the minimum acceptable score for the eval case to pass.

Example `EvalConfig` entry:

```python
{
  "criteria": {
    "response_match_score": 0.8
  }
}
```

### Output And How To Interpret[¶](#output-and-how-to-interpret_1 "Permanent link")

Value range for this criterion is [0,1], with values closer to 1 more desirable.

## final\_response\_match\_v2[¶](#final_response_match_v2 "Permanent link")

This criterion evaluates if the agent's final response matches a golden/expected
final response using LLM as a judge.

### When To Use This Criterion?[¶](#when-to-use-this-criterion_2 "Permanent link")

Use this criterion when you need to evaluate the correctness of an agent's final
response against a reference, but require flexibility in how the answer is
presented. It is suitable for cases where different phrasings or formats are
acceptable, as long as the core meaning and information match the reference.
This criterion is a good choice for evaluating question-answering,
summarization, or other generative tasks where semantic equivalence is more
important than exact lexical overlap, making it a more sophisticated alternative
to `response_match_score`.

### Details[¶](#details_2 "Permanent link")

This criterion uses a Large Language Model (LLM) as a judge to determine if the
agent's final response is semantically equivalent to the provided reference
response. It is designed to be more flexible than lexical matching metrics (like
`response_match_score`), as it focuses on whether the agent's response contains
the correct information, while tolerating differences in formatting, phrasing,
or the inclusion of additional correct details.

For each invocation, the criterion prompts a judge LLM to rate the agent's
response as "valid" or "invalid" compared to the reference. This is repeated
multiple times for robustness (configurable via `num_samples`), and a majority
vote determines if the invocation receives a score of 1.0 (valid) or 0.0
(invalid). The final criterion score is the fraction of invocations deemed valid
across the entire eval case.

### How To Use This Criterion?[¶](#how-to-use-this-criterion_2 "Permanent link")

This criterion uses `LlmAsAJudgeCriterion`, allowing you to configure the
evaluation threshold, the judge model, and the number of samples per invocation.

Example `EvalConfig` entry:

```python
{
  "criteria": {
    "final_response_match_v2": {
      "threshold": 0.8,
      "judge_model_options": {
            "judge_model": "gemini-2.5-flash",
            "num_samples": 5
          }
        }
    }
  }
}
```

### Output And How To Interpret[¶](#output-and-how-to-interpret_2 "Permanent link")

The criterion returns a score between 0.0 and 1.0. A score of 1.0 means the LLM
judge considered the agent's final response to be valid for all invocations,
while a score closer to 0.0 indicates that many responses were judged as invalid
when compared to the reference responses. Higher values are better.

## rubric\_based\_final\_response\_quality\_v1[¶](#rubric_based_final_response_quality_v1 "Permanent link")

This criterion assesses the quality of an agent's final response against a
user-defined set of rubrics using LLM as a judge.

### When To Use This Criterion?[¶](#when-to-use-this-criterion_3 "Permanent link")

Use this criterion when you need to evaluate aspects of response quality that go
beyond simple correctness or semantic equivalence with a reference. It is ideal
for assessing nuanced attributes like tone, style, helpfulness, or adherence to
specific conversational guidelines defined in your rubrics. This criterion is
particularly useful when no single reference response exists, or when quality
depends on multiple subjective factors.

### Details[¶](#details_3 "Permanent link")

This criterion provides a flexible way to evaluate response quality based on
specific criteria that you define as rubrics. For example, you could define
rubrics to check if a response is concise, if it correctly infers user intent,
or if it avoids jargon.

The criterion uses an LLM-as-a-judge to evaluate the agent's final response
against each rubric, producing a `yes` (1.0) or `no` (0.0) verdict for each.
Like other LLM-based metrics, it samples the judge model multiple times per
invocation and uses a majority vote to determine the score for each rubric in
that invocation. The overall score for an invocation is the average of its
rubric scores. The final criterion score for the eval case is the average of
these overall scores across all invocations.

### How To Use This Criterion?[¶](#how-to-use-this-criterion_3 "Permanent link")

This criterion uses `RubricsBasedCriterion`, which requires a list of rubrics to
be provided in the `EvalConfig`. Each rubric should be defined with a unique ID
and its content.

Example `EvalConfig` entry:

```python
{
  "criteria": {
    "rubric_based_final_response_quality_v1": {
      "threshold": 0.8,
      "judge_model_options": {
        "judge_model": "gemini-2.5-flash",
        "num_samples": 5
      },
      "rubrics": [
        {
          "rubric_id": "conciseness",
          "rubric_content": {
            "text_property": "The agent's response is direct and to the point."
          }
        },
        {
          "rubric_id": "intent_inference",
          "rubric_content": {
            "text_property": "The agent's response accurately infers the user's underlying goal from ambiguous queries."
          }
        }
      ]
    }
  }
}
```

### Output And How To Interpret[¶](#output-and-how-to-interpret_3 "Permanent link")

The criterion outputs an overall score between 0.0 and 1.0, where 1.0 indicates
that the agent's responses satisfied all rubrics across all invocations, and 0.0
indicates that no rubrics were satisfied. The results also include detailed
per-rubric scores for each invocation. Higher values are better.

## rubric\_based\_tool\_use\_quality\_v1[¶](#rubric_based_tool_use_quality_v1 "Permanent link")

This criterion assesses the quality of an agent's tool usage against a
user-defined set of rubrics using LLM as a judge.

### When To Use This Criterion?[¶](#when-to-use-this-criterion_4 "Permanent link")

Use this criterion when you need to evaluate *how* an agent uses tools, rather
than just *if* the final response is correct. It is ideal for assessing whether
the agent selected the right tool, used the correct parameters, or followed a
specific sequence of tool calls. This is useful for validating agent reasoning
processes, debugging tool-use errors, and ensuring adherence to prescribed
workflows, especially in cases where multiple tool-use paths could lead to a
similar final answer but only one path is considered correct.

### Details[¶](#details_4 "Permanent link")

This criterion provides a flexible way to evaluate tool usage based on specific
rules that you define as rubrics. For example, you could define rubrics to check
if a specific tool was called, if its parameters were correct, or if tools were
called in a particular order.

The criterion uses an LLM-as-a-judge to evaluate the agent's tool calls and
responses against each rubric, producing a `yes` (1.0) or `no` (0.0) verdict for
each. Like other LLM-based metrics, it samples the judge model multiple times
per invocation and uses a majority vote to determine the score for each rubric
in that invocation. The overall score for an invocation is the average of its
rubric scores. The final criterion score for the eval case is the average of
these overall scores across all invocations.

### How To Use This Criterion?[¶](#how-to-use-this-criterion_4 "Permanent link")

This criterion uses `RubricsBasedCriterion`, which requires a list of rubrics to
be provided in the `EvalConfig`. Each rubric should be defined with a unique ID
and its content, describing a specific aspect of tool use to evaluate.

Example `EvalConfig` entry:

```python
{
  "criteria": {
    "rubric_based_tool_use_quality_v1": {
      "threshold": 1.0,
      "judge_model_options": {
        "judge_model": "gemini-2.5-flash",
        "num_samples": 5
      },
      "rubrics": [
        {
          "rubric_id": "geocoding_called",
          "rubric_content": {
            "text_property": "The agent calls the GeoCoding tool before calling the GetWeather tool."
          }
        },
        {
          "rubric_id": "getweather_called",
          "rubric_content": {
            "text_property": "The agent calls the GetWeather tool with coordinates derived from the user's location."
          }
        }
      ]
    }
  }
}
```

### Output And How To Interpret[¶](#output-and-how-to-interpret_4 "Permanent link")

The criterion outputs an overall score between 0.0 and 1.0, where 1.0 indicates
that the agent's tool usage satisfied all rubrics across all invocations, and
0.0 indicates that no rubrics were satisfied. The results also include detailed
per-rubric scores for each invocation. Higher values are better.

## hallucinations\_v1[¶](#hallucinations_v1 "Permanent link")

This criterion assesses whether a model response contains any false,
contradictory, or unsupported claims.

### When To Use This Criterion?[¶](#when-to-use-this-criterion_5 "Permanent link")

Use this criterion to ensure the agent's response is grounded in the provided
context (e.g., tool outputs, user query, instructions) and does not contain
hallucinations.

### Details[¶](#details_5 "Permanent link")

This criterion assesses whether a model response contains any false,
contradictory, or unsupported claims based on context that includes developer
instructions, user prompt, tool definitions, and tool invocations and their
results. It uses LLM-as-a-judge and follows a two-step process:

1. **Segmenter**: Segments the agent response into individual sentences.
2. **Sentence Validator**: Evaluates each segmented sentence against the
   provided context for grounding. Each sentence is labeled as `supported`,
   `unsupported`, `contradictory`, `disputed` or `not_applicable`.

The metric computes an Accuracy Score: the percentage of sentences that are
`supported` or `not_applicable`. By default, only the final response is
evaluated. If `evaluate_intermediate_nl_responses` is set to true in the
criterion, intermediate natural language responses from agents are also
evaluated.

### How To Use This Criterion?[¶](#how-to-use-this-criterion_5 "Permanent link")

This criterion uses `HallucinationsCriterion`, allowing you to configure the
evaluation threshold, the judge model, the number of samples per invocation and
whether to evaluate intermediate natural language responses.

Example `EvalConfig` entry:

```python
{
  "criteria": {
    "hallucinations_v1": {
      "threshold": 0.8,
      "judge_model_options": {
            "judge_model": "gemini-2.5-flash",
          },
      "evaluate_intermediate_nl_responses": true
    }
  }
}
```

### Output And How To Interpret[¶](#output-and-how-to-interpret_5 "Permanent link")

The criterion returns a score between 0.0 and 1.0. A score of 1.0 means all
sentences in agent's response are grounded in the context, while a score closer
to 0.0 indicates that many sentences are false, contradictory, or unsupported.
Higher values are better.

## safety\_v1[¶](#safety_v1 "Permanent link")

This criterion evaluates the safety (harmlessness) of an Agent's Response.

### When To Use This Criterion?[¶](#when-to-use-this-criterion_6 "Permanent link")

This criterion should be used when you need to ensure that agent responses
comply with safety guidelines and do not produce harmful or inappropriate
content. It is essential for user-facing applications or any system where
response safety is a priority.

### Details[¶](#details_6 "Permanent link")

This criterion assesses whether the agent's response contains any harmful
content, such as hate speech, harassment, or dangerous information. Unlike other
metrics implemented natively within ADK, `safety_v1` delegates the evaluation to
the Vertex AI General AI Eval SDK.

### How To Use This Criterion?[¶](#how-to-use-this-criterion_6 "Permanent link")

Using this criterion requires a Google Cloud Project. You must have
`GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` environment variables set,
typically in an `.env` file in your agent's directory, for the Vertex AI SDK to
function correctly.

You can specify a threshold for this criterion in `EvalConfig` under the
`criteria` dictionary. The value should be a float between 0.0 and 1.0,
representing the minimum safety score for a response to be considered passing.

Example `EvalConfig` entry:

```python
{
  "criteria": {
    "safety_v1": 0.8
  }
}
```

### Output And How To Interpret[¶](#output-and-how-to-interpret_6 "Permanent link")

The criterion returns a score between 0.0 and 1.0. Scores closer to 1.0 indicate
that the response is safe, while scores closer to 0.0 indicate potential safety
issues.

Back to top