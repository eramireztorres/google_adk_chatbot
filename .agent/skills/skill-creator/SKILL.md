---
name: antigravity-skill-creator
description: Interactive guide and scaffolding tool for creating Google Antigravity Agent Skills. Use this skill when users want to create a new Agent Skill, update an existing one, or learn about the Antigravity skill architecture.
---

# Antigravity Skill Creator

This skill provides expert guidance for authoring effective Agent Skills within the Google Antigravity IDE.

## About Antigravity Skills

Agent Skills are the mechanism for "On-Demand Capability Extension" in Antigravity. They are local, directory-based packages that extend the agent's capabilities with specialized knowledge, workflows, and tools.

Unlike a System Prompt (always loaded), a Skill is **ephemeral**: it is loaded only when the agent determines the user's request matches the skill's `description`.

### Skill Scopes

1.  **Workspace Scope**: `<workspace-root>/.agent/skills/`
    * *Best for*: Project-specific scripts (migrations, deployment, proprietary framework scaffolding).
2.  **Global Scope**: `~/.gemini/antigravity/skills/`
    * *Best for*: General utilities (JSON formatting, UUID generation, code review standards).

## Core Principles

### 1. Trigger-Oriented Design
The `description` field in the YAML frontmatter is the **most critical** component. It functions as the trigger phrase.
* **Bad**: "Database tools" (Too vague, won't trigger reliably)
* **Good**: "Executes read-only SQL queries against the local PostgreSQL database to retrieve user data. Use for debugging." (Clear intent and context)

### 2. Atomic & Deterministic
Skills should do one thing well.
* **Scripts**: Prefer bundling Python/Bash scripts in `scripts/` over asking the agent to write code on the fly. Scripts are deterministic, faster, and don't consume context window for generation.
* **Context**: Use `references/` for static knowledge to prevent context rot.

### 3. Progressive Disclosure
Optimize the context window.
1.  **Metadata**: Only the `name` and `description` are visible to the router.
2.  **Body**: The `SKILL.md` content is loaded only *after* triggering.
3.  **Resources**: Files in `references/` are read only if explicitly cited or needed.

## Anatomy of a Skill

A skill is a directory containing a definition file and optional resources:

```text
skill-name/
├── SKILL.md (Required)
│   ├── Frontmatter (name, description)
│   └── Body (Goal, Instructions, Examples, Constraints)
└── resources (Optional)
    ├── scripts/    - Executable code (Python, Bash, Node)
    ├── references/ - Context docs (schemas, policies)
    └── templates/  - Files to be copied/used (boilerplates)
```

### SKILL.md Structure

#### Frontmatter (YAML)
* `name`: (Optional) Unique ID (e.g., `postgres-query`). Defaults to directory name.
* `description`: (Required) The semantic trigger. Must be imperative and descriptive.

#### Body (Markdown)
Organize the body into these standard sections to guide the Gemini 3 model effectively:

1.  **Goal**: A clear statement of what the skill achieves.
2.  **Instructions**: Step-by-step logic or workflows.
3.  **Examples**: Few-shot examples of inputs and outputs.
4.  **Constraints**: strict "Do not" rules (e.g., "Do not run DELETE queries").

## Skill Creation Process

Follow this workflow to build a new skill:

### Step 1: Define Intent & Scope
Determine if the skill is project-specific (Workspace) or universal (Global).
* *Prompt*: "What specific task should this skill handle? What user query should trigger it?"

### Step 2: Scaffold Directory
Create the directory structure.
* *Action*: Create `<scope>/skills/<skill-name>/`
* *Action*: Create `SKILL.md` and `scripts/` folder.

### Step 3: Implement Resources
Identify reusable components.
* **Scripts**: Does this task require complex execution? (e.g., `scripts/restart_server.sh`)
* **References**: Does the agent need documentation? (e.g., `references/api_docs.md`)
* **Templates**: Does the agent need to generate files? (e.g., `templates/react_component.tsx`)

### Step 4: Author SKILL.md
Write the definition file.

**Example SKILL.md**:
```markdown
---
name: git-commit-formatter
description: Generates conventional commit messages based on staged changes. Use when the user asks to commit code or review changes for a commit.
---

# Goal
Analyze staged git changes and generate a commit message following Conventional Commits specification.

# Instructions
1. Run `git diff --cached` to see staged changes.
2. If no changes are staged, ask the user to stage files first.
3. Analyze the diff to determine the type (feat, fix, chore, refactor).
4. Generate a message in the format: `type(scope): description`.

# Constraints
- Do not execute the commit command automatically; only generate the message.
- Keep the summary line under 50 characters.
```

### Step 5: Verification
* **Reload**: Antigravity automatically detects changes in the skills directory.
* **Test**: Switch to the Agent interface and try the trigger phrase (e.g., "Help me commit these changes").
* **Iterate**: Use the "Explain and Fix" or Agent Manager to debug if the skill doesn't trigger or misbehaves.
