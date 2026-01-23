---
url: https://google.github.io/adk-docs/runtime/runconfig/
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
  + [Agent Runtime](../)

    Agent Runtime
    - Runtime Config

      [Runtime Config](./)



      Table of contents
      * [Class Definition](#class-definition)
      * [Runtime Parameters](#runtime-parameters)

        + [speech\_config](#speech_config)
        + [response\_modalities](#response_modalities)
        + [save\_input\_blobs\_as\_artifacts](#save_input_blobs_as_artifacts)
        + [support\_cfc](#support_cfc)
        + [streaming\_mode](#streaming_mode)
        + [output\_audio\_transcription](#output_audio_transcription)
        + [max\_llm\_calls](#max_llm_calls)
      * [Validation Rules](#validation-rules)
      * [Examples](#examples)

        + [Basic runtime configuration](#basic-runtime-configuration)
        + [Enabling streaming](#enabling-streaming)
        + [Enabling speech support](#enabling-speech-support)
        + [Enabling Experimental CFC Support](#enabling-experimental-cfc-support)
    - [API Server](../api-server/)
    - [Resume Agents](../resume/)
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

* [Class Definition](#class-definition)
* [Runtime Parameters](#runtime-parameters)

  + [speech\_config](#speech_config)
  + [response\_modalities](#response_modalities)
  + [save\_input\_blobs\_as\_artifacts](#save_input_blobs_as_artifacts)
  + [support\_cfc](#support_cfc)
  + [streaming\_mode](#streaming_mode)
  + [output\_audio\_transcription](#output_audio_transcription)
  + [max\_llm\_calls](#max_llm_calls)
* [Validation Rules](#validation-rules)
* [Examples](#examples)

  + [Basic runtime configuration](#basic-runtime-configuration)
  + [Enabling streaming](#enabling-streaming)
  + [Enabling speech support](#enabling-speech-support)
  + [Enabling Experimental CFC Support](#enabling-experimental-cfc-support)

# Runtime Configuration[¶](#runtime-configuration "Permanent link")

Supported in ADKPython v0.1.0Go v0.1.0Java v0.1.0

`RunConfig` defines runtime behavior and options for agents in the ADK. It
controls speech and streaming settings, function calling, artifact saving, and
limits on LLM calls.

When constructing an agent run, you can pass a `RunConfig` to customize how the
agent interacts with models, handles audio, and streams responses. By default,
no streaming is enabled and inputs aren’t retained as artifacts. Use `RunConfig`
to override these defaults.

## Class Definition[¶](#class-definition "Permanent link")

The `RunConfig` class holds configuration parameters for an agent's runtime behavior.

* Python ADK uses Pydantic for this validation.
* Go ADK has mutable structs by default.
* Java ADK typically uses immutable data classes.

PythonGoJava

```python
class RunConfig(BaseModel):
    """Configs for runtime behavior of agents."""

    model_config = ConfigDict(
        extra='forbid',
    )

    speech_config: Optional[types.SpeechConfig] = None
    response_modalities: Optional[list[str]] = None
    save_input_blobs_as_artifacts: bool = False
    support_cfc: bool = False
    streaming_mode: StreamingMode = StreamingMode.NONE
    output_audio_transcription: Optional[types.AudioTranscriptionConfig] = None
    max_llm_calls: int = 500
```

```python
type StreamingMode string

const (
    StreamingModeNone StreamingMode = "none"
    StreamingModeSSE  StreamingMode = "sse"
)

// RunConfig controls runtime behavior.
type RunConfig struct {
    // Streaming mode, None or StreamingMode.SSE.
    StreamingMode StreamingMode
    // Whether or not to save the input blobs as artifacts
    SaveInputBlobsAsArtifacts bool
}
```

```python
public abstract class RunConfig {

  public enum StreamingMode {
    NONE,
    SSE,
    BIDI
  }

  public abstract @Nullable SpeechConfig speechConfig();

  public abstract ImmutableList<Modality> responseModalities();

  public abstract boolean saveInputBlobsAsArtifacts();

  public abstract @Nullable AudioTranscriptionConfig outputAudioTranscription();

  public abstract int maxLlmCalls();

  // ...
}
```

## Runtime Parameters[¶](#runtime-parameters "Permanent link")

| Parameter | Python Type | Go Type | Java Type | Default (Py / Go / Java ) | Description |
| --- | --- | --- | --- | --- | --- |
| `speech_config` | `Optional[types.SpeechConfig]` | N/A | `SpeechConfig` (nullable via `@Nullable`) | `None` / N/A / `null` | Configures speech synthesis (voice, language) using the `SpeechConfig` type. |
| `response_modalities` | `Optional[list[str]]` | N/A | `ImmutableList<Modality>` | `None` / N/A / Empty `ImmutableList` | List of desired output modalities (e.g., Python: `["TEXT", "AUDIO"]`; Java: uses structured `Modality` objects). |
| `save_input_blobs_as_artifacts` | `bool` | `bool` | `boolean` | `False` / `false` / `false` | If `true`, saves input blobs (e.g., uploaded files) as run artifacts for debugging/auditing. |
| `streaming_mode` | `StreamingMode` | `StreamingMode` | `StreamingMode` | `StreamingMode.NONE` / `agent.StreamingModeNone` / `StreamingMode.NONE` | Sets the streaming behavior: `NONE` (default), `SSE` (server-sent events), or `BIDI` (bidirectional) (**Python/Java**). |
| `output_audio_transcription` | `Optional[types.AudioTranscriptionConfig]` | N/A | `AudioTranscriptionConfig` (nullable via `@Nullable`) | `None` / N/A / `null` | Configures transcription of generated audio output using the `AudioTranscriptionConfig` type. |
| `max_llm_calls` | `int` | N/A | `int` | `500` / N/A / `500` | Limits total LLM calls per run. `0` or negative means unlimited (warned); `sys.maxsize` raises `ValueError`. |
| `support_cfc` | `bool` | N/A | `bool` | `False` / N/A / `false` | **Python:** Enables Compositional Function Calling. Requires `streaming_mode=SSE` and uses the LIVE API. **Experimental.** |

### `speech_config`[¶](#speech_config "Permanent link")

Supported in ADKPython v0.1.0Java v0.1.0

Note

The interface or definition of `SpeechConfig` is the same, irrespective of the language.

Speech configuration settings for live agents with audio capabilities. The
`SpeechConfig` class has the following structure:

```python
class SpeechConfig(_common.BaseModel):
    """The speech generation configuration."""

    voice_config: Optional[VoiceConfig] = Field(
        default=None,
        description="""The configuration for the speaker to use.""",
    )
    language_code: Optional[str] = Field(
        default=None,
        description="""Language code (ISO 639. e.g. en-US) for the speech synthesization.
        Only available for Live API.""",
    )
```

The `voice_config` parameter uses the `VoiceConfig` class:

```python
class VoiceConfig(_common.BaseModel):
    """The configuration for the voice to use."""

    prebuilt_voice_config: Optional[PrebuiltVoiceConfig] = Field(
        default=None,
        description="""The configuration for the speaker to use.""",
    )
```

And `PrebuiltVoiceConfig` has the following structure:

```python
class PrebuiltVoiceConfig(_common.BaseModel):
    """The configuration for the prebuilt speaker to use."""

    voice_name: Optional[str] = Field(
        default=None,
        description="""The name of the prebuilt voice to use.""",
    )
```

These nested configuration classes allow you to specify:

* `voice_config`: The name of the prebuilt voice to use (in the `PrebuiltVoiceConfig`)
* `language_code`: ISO 639 language code (e.g., "en-US") for speech synthesis

When implementing voice-enabled agents, configure these parameters to control
how your agent sounds when speaking.

### `response_modalities`[¶](#response_modalities "Permanent link")

Supported in ADKPython v0.1.0Java v0.1.0

Defines the output modalities for the agent. If not set, defaults to AUDIO.
Response modalities determine how the agent communicates with users through
various channels (e.g., text, audio).

### `save_input_blobs_as_artifacts`[¶](#save_input_blobs_as_artifacts "Permanent link")

Supported in ADKPython v0.1.0Go v0.1.0Java v0.1.0

When enabled, input blobs will be saved as artifacts during agent execution.
This is useful for debugging and audit purposes, allowing developers to review
the exact data received by agents.

### `support_cfc`[¶](#support_cfc "Permanent link")

Supported in ADKPython v0.1.0Experimental

Enables Compositional Function Calling (CFC) support. Only applicable when using
StreamingMode.SSE. When enabled, the LIVE API will be invoked as only it
supports CFC functionality.

Experimental release

The `support_cfc` feature is experimental and its API or behavior might
change in future releases.

### `streaming_mode`[¶](#streaming_mode "Permanent link")

Supported in ADKPython v0.1.0Go v0.1.0

Configures the streaming behavior of the agent. Possible values:

* `StreamingMode.NONE`: No streaming; responses delivered as complete units
* `StreamingMode.SSE`: Server-Sent Events streaming; one-way streaming from server to client
* `StreamingMode.BIDI`: Bidirectional streaming; simultaneous communication in both directions

Streaming modes affect both performance and user experience. SSE streaming lets users see partial responses as they're generated, while BIDI streaming enables real-time interactive experiences.

### `output_audio_transcription`[¶](#output_audio_transcription "Permanent link")

Supported in ADKPython v0.1.0Java v0.1.0

Configuration for transcribing audio outputs from live agents with audio
response capability. This enables automatic transcription of audio responses for
accessibility, record-keeping, and multi-modal applications.

### `max_llm_calls`[¶](#max_llm_calls "Permanent link")

Supported in ADKPython v0.1.0Java v0.1.0

Sets a limit on the total number of LLM calls for a given agent run.

* Values greater than 0 and less than `sys.maxsize`: Enforces a bound on LLM calls
* Values less than or equal to 0: Allows unbounded LLM calls *(not recommended for production)*

This parameter prevents excessive API usage and potential runaway processes.
Since LLM calls often incur costs and consume resources, setting appropriate
limits is crucial.

## Validation Rules[¶](#validation-rules "Permanent link")

The `RunConfig` class validates its parameters to ensure proper agent operation. While Python ADK uses `Pydantic` for automatic type validation, Java ADK relies on its static typing and may include explicit checks in the RunConfig's construction.
For the `max_llm_calls` parameter specifically:

1. Extremely large values (like `sys.maxsize` in Python or `Integer.MAX_VALUE` in Java) are typically disallowed to prevent issues.
2. Values of zero or less will usually trigger a warning about unlimited LLM interactions.

## Examples[¶](#examples "Permanent link")

### Basic runtime configuration[¶](#basic-runtime-configuration "Permanent link")

PythonGoJava

```python
from google.genai.adk import RunConfig, StreamingMode

config = RunConfig(
    streaming_mode=StreamingMode.NONE,
    max_llm_calls=100
)
```

```python
import "google.golang.org/adk/agent"

config := agent.RunConfig{
    StreamingMode: agent.StreamingModeNone,
}
```

```python
import com.google.adk.agents.RunConfig;
import com.google.adk.agents.RunConfig.StreamingMode;

RunConfig config = RunConfig.builder()
        .setStreamingMode(StreamingMode.NONE)
        .setMaxLlmCalls(100)
        .build();
```

This configuration creates a non-streaming agent with a limit of 100 LLM calls,
suitable for simple task-oriented agents where complete responses are
preferable.

### Enabling streaming[¶](#enabling-streaming "Permanent link")

PythonGoJava

```python
from google.genai.adk import RunConfig, StreamingMode

config = RunConfig(
    streaming_mode=StreamingMode.SSE,
    max_llm_calls=200
)
```

```python
import "google.golang.org/adk/agent"

config := agent.RunConfig{
    StreamingMode: agent.StreamingModeSSE,
}
```

```python
import com.google.adk.agents.RunConfig;
import com.google.adk.agents.RunConfig.StreamingMode;

RunConfig config = RunConfig.builder()
    .setStreamingMode(StreamingMode.SSE)
    .setMaxLlmCalls(200)
    .build();
```

Using SSE streaming allows users to see responses as they're generated,
providing a more responsive feel for chatbots and assistants.

### Enabling speech support[¶](#enabling-speech-support "Permanent link")

PythonJava

```python
from google.genai.adk import RunConfig, StreamingMode
from google.genai import types

config = RunConfig(
    speech_config=types.SpeechConfig(
        language_code="en-US",
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name="Kore"
            )
        ),
    ),
    response_modalities=["AUDIO", "TEXT"],
    save_input_blobs_as_artifacts=True,
    support_cfc=True,
    streaming_mode=StreamingMode.SSE,
    max_llm_calls=1000,
)
```

```python
import com.google.adk.agents.RunConfig;
import com.google.adk.agents.RunConfig.StreamingMode;
import com.google.common.collect.ImmutableList;
import com.google.genai.types.Content;
import com.google.genai.types.Modality;
import com.google.genai.types.Part;
import com.google.genai.types.PrebuiltVoiceConfig;
import com.google.genai.types.SpeechConfig;
import com.google.genai.types.VoiceConfig;

RunConfig runConfig =
    RunConfig.builder()
        .setStreamingMode(StreamingMode.SSE)
        .setMaxLlmCalls(1000)
        .setSaveInputBlobsAsArtifacts(true)
        .setResponseModalities(ImmutableList.of(new Modality("AUDIO"), new Modality("TEXT")))
        .setSpeechConfig(
            SpeechConfig.builder()
                .voiceConfig(
                    VoiceConfig.builder()
                        .prebuiltVoiceConfig(
                            PrebuiltVoiceConfig.builder().voiceName("Kore").build())
                        .build())
                .languageCode("en-US")
                .build())
        .build();
```

This comprehensive example configures an agent with:

* Speech capabilities using the "Kore" voice (US English)
* Both audio and text output modalities
* Artifact saving for input blobs (useful for debugging)
* SSE streaming for responsive interaction
* A limit of 1000 LLM calls

### Enabling Experimental CFC Support[¶](#enabling-experimental-cfc-support "Permanent link")

Supported in ADKPython v0.1.0Experimental

```python
```python
    from google.genai.adk import RunConfig, StreamingMode

    config = RunConfig(
        streaming_mode=StreamingMode.SSE,
        support_cfc=True,
        max_llm_calls=150
    )
```
```

Enabling Compositional Function Calling creates an agent that can dynamically
execute functions based on model outputs, powerful for applications requiring
complex workflows.

Back to top