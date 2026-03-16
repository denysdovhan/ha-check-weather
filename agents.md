# AI Coding Agents Guide

## Purpose

Agents act as senior Python collaborators. Keep responses concise,
clarify uncertainty before coding, and align suggestions with the rules linked below.

## Project Overview

This repository is a Home Assistant custom integration. Main codebase lives under `custom_components/check_weather`.

### Code structure

- `translations/` — JSON translations per locale.
- `__init__.py` — sets up the integration, handles config entry migrations, and forwards the binary sensor platform.
- `binary_sensor.py` — entity implementation and forecast evaluation logic.
- `config_flow.py` — config flow and options flow.
- `const.py` — shared constants and defaults; check here before adding new strings.
- `diagnostics.py` — exposes `async_get_config_entry_diagnostics` for HA diagnostics downloads.
- `manifest.json` — HA manifest.

## Workflow

- Python deps defined in `pyproject.toml`, locked in `uv.lock`; manage env with `uv`.
- CI (`lint.yml`, `validate.yml`) installs uv via `astral-sh/setup-uv` and runs tools with `uv run`.
- Use `scripts/bootstrap` for fresh setup (installs uv via pipx if missing, syncs deps, installs pre-commit).
- Prefer running tooling via `uv run <tool>` to match the locked env.
- Run `scripts/lint` after code changes.

### Development Scripts

- `scripts/bootstrap` — sets up the development environment.
- `scripts/setup` — installs dependencies and pre-commit hooks.
- `scripts/develop` — starts a development Home Assistant instance.
- `scripts/lint` — runs Ruff formatter/linter with fixes.
- `scripts/bump_version` — updates the integration version for releases.

### Development Process

- Ask for clarification when requirements are ambiguous; surface 2–3 options when trade-offs matter.
- Update documentation and related rules when introducing new patterns or workflows.
- When unsure or blocked on runtime behavior, add targeted debug logging and ask for the output.
- Each time you make changes to Python code, run `scripts/lint` and fix any reported issues.
- Commit only when directly asked to do so. Write descriptive conventional commit messages.

## Code Style

Use code style described in `pyproject.toml` configuration. Standard Python. 4-spaces indentation.

Never import modules in functions. All imports must be located on top of the file.

## Translations

- Add locales by copying `translations/en.json` and translating values per HA guidelines.
- Translate values only; keep keys and placeholders unchanged.

## Home Assistant API

Carefully read links to the Home Assistant Developer documentation for guidance.

Fetch these links to get more informations about specific Home Assistant APIs directly from its documentation:

- File structure: https://developers.home-assistant.io/docs/creating_integration_file_structure
- Config Flow: https://developers.home-assistant.io/docs/config_entries_config_flow_handler
- Fetching data: https://developers.home-assistant.io/docs/integration_fetching_data
- Diagnostics: https://developers.home-assistant.io/docs/core/platform/diagnostics
- Sensor: https://developers.home-assistant.io/docs/core/entity/binary-sensor
- Config Entries: https://developers.home-assistant.io/docs/config_entries_index
- Data Entry Flow: https://developers.home-assistant.io/docs/data_entry_flow_index
- Manifest: https://developers.home-assistant.io/docs/creating_integration_manifest

## Important directives

<important>
In all interactions and commit messages, be extremely concise and sacrifice grammar for the sake of concision.
</important>

<important>
If anything here is unclear, tell me what you want to do and I'll expand these instructions.
</important>

<important>
If you struggle to find a solution, suggest to add logger statements and ask for output to get more context and understand the flow better. When logger output is provided, analyze it to understand what is going on.
</important>

<important>
When updating this file (`agents.md`), DON'T CHANGE the structure, formatting or style of the document. Just add relevant information, without restructuring: add list items, new sections, etc. NEVER REMOVE tags, like <important> or <instruction>.
</important>

<important>
At the end of each plan, give me a list of unresolved questions to answer, if any. Make the questions extremely concise. Sacrifice grammar for the sake of concision.
</important>
