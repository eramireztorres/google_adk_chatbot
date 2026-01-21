---
url: https://docs.evidentlyai.com/docs/platform/projects_manage
source: Evidently Documentation
---

You must first connect to [Evidently Cloud](/docs/setup/cloud) (or your [local workspace](/docs/setup/self-hosting)).

## [​](#create-a-project) Create a Project

* Python
* UI

To create a Project inside a workspace `ws` and Organization with an `org_id`:

Copy

```python
project = ws.create_project("My test project", org_id="YOUR_ORG_ID")
project.description = "My project description"
project.save()
```

In self-hosted open-source installation, you do not need to pass the Org ID. To create a Project:

Copy

```python
project = ws.create_project("My test project")
project.description = "My project description"
project.save()
```

## [​](#connect-to-a-project) Connect to a Project

**Project ID**. You can see the Project ID above the monitoring Dashboard inside your Project.

To connect to an existing Project from Python, use the `get_project` method.

Copy

```python
project = ws.get_project("PROJECT_ID")
```

## [​](#working-with-a-project) Working with a Project

### [​](#save-changes) Save changes

After making any changes to the Project (like editing description or adding monitoring Panels), always use the `save()` command:

Copy

```python
project.save()
```

### [​](#browse-projects) Browse Projects

You can see all available Projects on the monitoring homepage, or request a list programmatically. To get a list of all Projects in a workspace `ws`, use:

Copy

```python
ws.list_projects()
```

To find a specific Project by its name, use the `search_project` method:

Copy

```python
ws.search_project("project_name")
```

### [​](#[danger]-delete-project) [DANGER] Delete Project

Deleting a Project deletes all the data inside it.

* Python
* UI

To delete the Project:

Copy

```python
# ws.delete_project("PROJECT ID")
```

## [​](#project-parameters) Project parameters

Each Project has the following parameters.

| Parameter | Description | Example |
| --- | --- | --- |
| `name: str` | Project name. | - |
| `id: UUID4 = Field(default_factory=uuid.uuid4)` | Unique identifier of the Project. Assigned automatically. | - |
| `description: Optional[str] = None` | Optional description. Visible when you browse Projects. | - |
| `dashboard: DashboardConfig` | Dashboard configuration that describes the composition of the monitoring Panels. | See [Dashboard Design](dashboard_add_panels) for details. You don’t need to explicitly pass `DashboardConfig` if you use the `.dashboard.add_panel` method. |
| `date_from: Optional[datetime.datetime] = None` | Start DateTime of the monitoring Dashboard. By default it shows data for all available periods. | `datetime.now() + timedelta(-30)` |
| `date_to: Optional[datetime.datetime] = None` | End DateTime of the monitoring Dashboard. | Works the same as `date_from`. |