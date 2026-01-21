---
url: https://docs.evidentlyai.com/examples/GitHub_actions
source: Evidently Documentation
---

You can use Evidently together with GitHub Actions to automatically test the outputs of your LLM agent or application - as part of every code push or pull request.

## [​](#how-the-integration-work:) How the integration work:

* You define a test dataset of inputs (e.g. test prompts with or without reference answers). You can store it as a file, or save the dataset at Evidently Cloud callable by Dataset ID.
* Run your LLM system or agent against those inputs inside CI.
* Evidently automatically evaluates the outputs using the user-specified config (which defines the Evidently descriptors, tests and Report composition), including methods like:
  + LLM judges (e.g., tone, helpfulness, correctness)
  + Custom Python functions
  + Dataset-level metrics like classification quality
* If any test fails, the CI job fails.
* You get a detailed test report with pass/fail status and metrics.

![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/examples/github_actions.gif)
Results are stored locally or pushed to Evidently Cloud for deeper review and tracking.
The final result is CI-native testing for your LLM behavior - so you can safely tweak prompts, models, or logic without breaking things silently.

## [​](#code-example-and-tutorial) Code example and tutorial

👉 Check the full tutorial and example repo: <https://github.com/evidentlyai/evidently-ci-example>
Action is also available on GitHub Marketplace: <https://github.com/marketplace/actions/run-evidently-report>