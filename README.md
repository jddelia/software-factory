# Software Factory

`software-factory` is a Codex skill for instantiating and operating adaptive
multi-agent software factories. It helps Codex choose a factory mode, seed
project control docs, assign implementation and review batons, preserve a
single-writer policy, record acceptance evidence, and manage stop/resume
workflow for substantial software projects.

Use it when a project needs more than a one-off edit: end-to-end builds,
release readiness, recovery from messy worktrees, safe MVP delivery, strict
review gates, or coordinated builder/reviewer workflows.

## Contents

```text
.
├── SKILL.md                         # Required Codex skill instructions
├── agents/openai.yaml               # UI metadata and default invocation
├── references/configuration.md      # Mode presets and policy reference
├── references/templates.md          # Factory docs, baton, review, stop/resume templates
├── scripts/seed_factory_docs.py     # Dependency-free project doc seeder
├── examples/                        # Compact generated-output examples
├── tests/                           # Standard-library tests
└── .github/workflows/ci.yml         # CI for compile and test checks
```

## Install

Install globally for Codex with the `skills` CLI:

```bash
npx skills add jddelia/software-factory --agent codex --global --yes
```

To preview what the CLI detects before installing:

```bash
npx skills add jddelia/software-factory --list
```

The `skills` CLI collects anonymous aggregate install telemetry. To opt out:

```bash
DISABLE_TELEMETRY=1 npx skills add jddelia/software-factory --agent codex --global --yes
```

Manual fallback:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/jddelia/software-factory.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/software-factory"
```

For local development from an existing checkout:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/software-factory"
rsync -a --exclude .git ./ "${CODEX_HOME:-$HOME/.codex}/skills/software-factory/"
```

Restart Codex after installing so the skill metadata is reloaded.

## Use

Invoke the skill directly in Codex:

```text
Use $software-factory to instantiate an adaptive software factory for this project.
```

Useful variations:

```text
Use $software-factory in Safe MVP mode to ship the thinnest real onboarding slice.
Use $software-factory in Release mode to prepare this repo for publication.
Use $software-factory in Recovery mode to reconcile the dirty worktree and stale handoffs.
```

The skill will infer or confirm the operating mode, then guide Codex through
preflight, factory configuration, baton assignment, verification, review,
acceptance, and optional cleanup.

## Seed Factory Docs

The bundled generator creates the standard project files that a factory uses as
its durable source of truth:

- `AGENTS.md`
- `docs/factory_config.md`
- `docs/review_index.md`
- `docs/codex_factory_protocol.md`
- `docs/handoff_protocol.md`
- `docs/build_ledger.md`

Always dry-run first:

```bash
python3 scripts/seed_factory_docs.py /path/to/project \
  --work-mode balanced \
  --dry-run \
  --print-kickoff
```

Create docs for a Safe MVP factory:

```bash
python3 scripts/seed_factory_docs.py /path/to/project \
  --project-name "Example App" \
  --work-mode safe_mvp \
  --target-outcome "Ship the core onboarding flow with focused proof"
```

The script is conservative: it skips existing files unless `--force` is passed.
It has no third-party dependencies.

See [examples/safe-mvp-kickoff.md](examples/safe-mvp-kickoff.md) for a compact
example of the generated file list and kickoff packet.

## Validate

Run the local checks:

```bash
python3 -m py_compile scripts/seed_factory_docs.py
python3 -m unittest discover -s tests
```

If you have the Codex skill-creator tooling installed, also validate the skill
package:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

That validator requires `PyYAML`.

## Design Principles

- Keep `SKILL.md` concise and trigger-focused.
- Keep detailed mode tables, templates, and policy reference material in
  `references/`.
- Keep bundled scripts deterministic and dependency-light.
- Preserve user changes and one active writer per worktree by default.
- Treat stop/resume, permissions, model routing, tool-call limits, and
  verification cadence as explicit factory configuration.
- Record skipped checks and residual risk instead of claiming release readiness
  without evidence.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please include tests for generator
behavior changes and keep public skill metadata aligned with `SKILL.md`.

For vulnerability reports or sensitive security concerns, see
[SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
