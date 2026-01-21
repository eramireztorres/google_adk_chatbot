---
url: https://docs.evidentlyai.com/docs/platform/alerts
source: Evidently Documentation
---

Built-in alerting is a Pro feature available in the **Evidently Cloud** and **Evidently Enterprise**.

![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/alerts.png)
To enable alerts, open the Project and navigate to the “Alerts” in the left menu. You must set:

* A notification channel.
* An alert condition.

## [​](#notification-channels) Notification channels

You can choose between the following options:

* **Email**. Add email addresses to send alerts to.
* **Slack**. Add a Slack webhook.
* **Discord**. Add a Discord webhook.

## [​](#alert-conditions) Alert conditions

### [​](#failed-tests) Failed tests

If you use Tests (conditional checks) in your Project, you can tie alerting to the failed Tests in a Test Suite. Toggle this option on the Alerts page. Evidently will set an alert to the defined channel if any of the Tests fail.

**How to avoid alert fatigue?** Use the `is_critical` parameter to mark non-critical Test as Warnings. Setting it to `False` prevent alerts for those checks even if they fail.

### [​](#custom-conditions) Custom conditions

You can also set alerts on individual Metric values. For example, you can generate Alerts when the share of drifting features is above a certain threshold.
Click on the plus sign below the “Add new Metric alert” and follow the prompts to set an alert condition.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/docs/.gitbook/assets/cloud/alerts.png)