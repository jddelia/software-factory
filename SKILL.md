---
name: software-factory
description: Instantiate and operate an adaptive Codex software factory for substantial software projects. Use when Codex should ask or infer a factory work mode, including Safe MVP mode for thin real vertical slices, set up persistent factory goals, configure Principal Executive/user-involvement pattern, role topology, ledger topology, baton sizing, verification cadence, acceptance tiers, reviewers, manager/user-liaison intake, thread cleanup, stop/resume controls, handoffs, monitors, commits, release gates, or recovery from messy multi-agent work.
---

# Software Factory

## Outcome

Create a configurable software factory that matches the project's risk, maturity, and delivery target:

- an explicit factory configuration;
- an optional Principal Executive / overseer for user partnership, topology changes, and factory-level intervention;
- one executive with final product and quality authority;
- either executive-as-ledger, separate-ledger, or passive-fallback topology;
- one active writer per worktree by default;
- optional Manager/User Liaison for packaging user feedback into Executive Briefs;
- optional parallel read-only reviewers;
- optional thread cleanup after evidence is captured;
- explicit stop/resume controls for safe pauses, hard stops, monitor handling, and resumable handoffs;
- explicit permission, model, and blocker policies so worker threads do not stall on predictable tooling friction;
- explicit tool-call budgeting and thread-read policies so controllers do not stall on oversized or schema-invalid inspection calls;
- adaptive active-actor polling so controllers do not waste tokens watching normal Builder progress;
- capability preflight before launch so missing thread, browser, git, env, network, or approval capabilities are visible;
- baton handoffs with acceptance tiers;
- verification cadence that can favor safe MVP delivery, velocity, balance, strictness, release, or recovery;
- commits only for accepted work unless the user explicitly delegates otherwise.

This skill is broadly applicable to software projects. Do not hard-code project-specific rules. Infer project-specific invariants from the repository, user request, specs, tests, and risk surface.

## Runtime Fit

Prefer the Codex app for this skill. It is optimized for Codex primitives such as delegated worker threads, tool permissions, browser QA, persistent goals/checkpoints, bounded thread reads, and long-running handoffs.

Use other agent runtimes only when they provide comparable primitives or when the factory is intentionally operating in manual/single-thread mode through the seeded docs and baton protocol. When a runtime lacks a needed primitive, record it during capability preflight and downgrade topology instead of pretending the factory can run fully autonomously.

## Alignment Before Instantiation

Before creating a factory, align on the minimum configuration needed for useful autonomy. Prefer a short, human-readable intake over exposing raw config.

Ask the user which `work_mode` to use unless the request clearly implies one. Keep the question short and include concise descriptions:

- `balanced`: normal feature work, good quality without heavy ceremony.
- `velocity`: bigger vertical slices, focused checks, periodic full gates.
- `safe_mvp`: the thinnest real product slice; cut breadth and polish while preserving hard safety and verification invariants.
- `strict`: smaller batons, deeper review, full gates for high-risk work.
- `prototype`: move fast to prove the experience; hardening is tracked separately.
- `release` or `recovery`: ship readiness, or cleanup of messy/broken state.

Ask at most three short questions by default:

1. Which work mode should I use?
2. What is the target outcome: end-to-end build, specific feature, release readiness, recovery/cleanup, or another objective?
3. How should user involvement and side feedback work?

For the third question, use plain options:

- Principal Partner: the current user-facing thread acts as a top-level partner/overseer while the Executive Ledger drives the factory.
- Direct Executive: the user talks directly to the active Executive/Ledger.
- Hands-Off: the factory runs with checkpoint summaries.

Then ask feedback handling only when the project is long-running, the user expects to comment while work continues, or the answer is unclear:

- No Manager: keep the active Executive lean; user feedback goes directly to the chosen contact point.
- Feedback Manager: package user side feedback into briefs so the Executive stays focused.
- Always-On Manager: continuously monitor user feedback and factory state, then brief the Principal or Executive.

Do not ask if the user's request already gives enough signal. Infer `safe_mvp` from "few hours", "ship the MVP", "thin real slice", "move fast but safely", or "working core flow now"; infer `velocity` from "move fast" or "iterate quickly" when the user still expects normal integration breadth; `strict` from "production-grade", "no shortcuts", "all tests", or safety-critical work; `discovery` from "review/understand"; `recovery` from broken/colliding state; `release` from deploy/ship/merge readiness. Infer `Principal Partner` for substantial long-running builds unless the user wants a single direct thread or hands-off automation.

## First Move

1. Inspect project state before assigning work: stack, scripts, source docs, dirty git state, branch, remote, generated-file hazards, permission constraints, available tools, env/secrets expectations, and any active threads.
2. Choose or confirm a factory configuration:
   - `work_mode`: default `balanced` unless the user requests a safe MVP, speed, strictness, release, recovery, or discovery.
   - `factory_topology`: default `executive_as_ledger` unless context or user preference favors a separate ledger.
   - `acceptance_tier`: default `integration` for active builds, `release` only when preparing to ship.
   - `target_outcome`: infer from the request or ask during alignment.
   - `user_involvement`: default `principal_partner` for substantial factories.
   - `feedback_handling`: default `no_manager` unless the user expects frequent side feedback.
   - `default_stop_mode`: default `drain_to_checkpoint` unless release, recovery, or discovery mode implies a different pause behavior.
3. Run the configured capability preflight and record blockers before creating worker threads.
4. Set up a persistent goal only when the user asks for goal tracking or the active runtime policy permits goal creation for long-running factory control; otherwise record the goal text in factory docs.
5. Record the configuration and goal text in `docs/factory_config.md` and `docs/build_ledger.md` when creating a factory.
6. Seed missing factory docs if needed:
   - `AGENTS.md`
   - `docs/factory_config.md`
   - `docs/review_index.md`
   - `docs/codex_factory_protocol.md`
   - `docs/handoff_protocol.md`
   - `docs/build_ledger.md`
7. Define the next baton with objective, write scope, non-goals, acceptance tier, verification level, escalation triggers, requested model/reasoning, permission profile, and handoff requirements.
8. If thread tools exist, create only the needed Ledger, Builder, Reviewer, or Watcher threads for the chosen topology.

Use `scripts/seed_factory_docs.py` to create missing docs. Run with `--dry-run` first. Use `references/configuration.md` for mode selection and `references/templates.md` for prompts and ledger snippets.

## Factory Configuration

Always make the operating culture explicit. A mode gives defaults; overrides may tune any option.

Core knobs:

- `work_mode`: `discovery`, `prototype`, `safe_mvp`, `velocity`, `balanced`, `strict`, `release`, `recovery`, `maintenance`, `migration`, `design_sprint`
- `factory_topology`: `executive_as_ledger`, `separate_ledger`, `passive_fallback`
- `role_topology`: `lean_solo`, `standard`, `reviewed`, `managed`, `enterprise`
- `user_involvement`: `principal_partner`, `direct_executive`, `hands_off`
- `feedback_handling`: `no_manager`, `feedback_manager`, `always_on_manager`
- `principal_policy`: `none`, `same_as_executive`, `dedicated`, `user_thread`
- `principal_authority`: `observe`, `steer`, `configure`, `emergency_override`
- `principal_intervention_policy`: `no_baton_interference`, `can_pause`, `can_reassign`, `can_supersede_ledger`
- `principal_digest_cadence`: `manual`, `checkpoint`, `heartbeat`, `daily`
- `principal_context_budget`: `compact`, `standard`, `full`
- `config_verbosity`: `compact`, `standard`, `exhaustive`
- `baton_size`: `micro`, `small`, `medium`, `vertical_slice`
- `acceptance_tier`: `prototype`, `integration`, `release`
- `verification_level`: `smoke`, `focused`, `focused_plus_build`, `full_gate`, `release_gate`
- `full_gate_cadence`: `every_baton`, `every_n_batons`, `risk_triggered`, `release_only`
- `concurrency_policy`: `single_writer`, `parallel_read_only_reviewers`, `parallel_worktrees`
- `review_depth`: `skim`, `targeted`, `full`, `adversarial`
- `handoff_detail`: `compact`, `standard`, `exhaustive`
- `browser_qa_policy`: `none`, `smoke`, `screenshots`, `full`, `release`
- `external_effect_policy`: `mock_only`, `explicit_operator`, `staging_allowed`, `production_requires_confirmation`
- `target_outcome`: end-to-end build, feature, release readiness, recovery, maintenance, migration, or user-defined objective
- `goal_policy`: `none`, `ask`, `create_if_long_running`, `explicit_only`
- `reviewer_policy`: `none`, `risk_triggered`, `every_baton`, `release_only`
- `reviewer_spawn_policy`: `none`, `after_handoff`, `standby_with_builder`, `parallel_read_only`, `risk_triggered`, `release_only`
- `manager_policy`: `none`, `user_feedback_only`, `always_on`
- `executive_context_policy`: `direct_user_chat`, `manager_packaged_feedback`, `mixed`
- `thread_cleanup_policy`: `none`, `manual`, `after_acceptance`, `rolling_window`, `aggressive`, `release_archive`
- `factory_stop_policy`: `enabled`, `manual_only`, `disabled`
- `default_stop_mode`: `pause_new_work`, `drain_to_handoff`, `drain_to_checkpoint`, `release_freeze`, `hard_stop`, `emergency_stop`
- `stop_scope`: `new_work_only`, `active_baton`, `all_factory`, `monitors_only`, `cleanup_only`
- `stop_authority`: `user_only`, `principal_or_user`, `executive_or_above`, `any_active_role_with_confirmation`
- `stop_monitor_policy`: `keep_active`, `pause_after_stop`, `delete_after_stop`, `retarget_to_principal`
- `stop_cleanup_policy`: `none`, `manual`, `after_checkpoint`, `rolling_window_after_checkpoint`, `release_archive`
- `resume_policy`: `manual`, `resume_from_stop_packet`, `resume_requires_user`, `auto_resume_after_window`
- `default_resume_mode`: `restore_monitors_only`, `continue_same_baton`, `replace_actor`, `advance_to_review`, `assign_next_baton`, `recovery_first`
- `stop_packet_required`: `true` or `false`
- `package_protocol`: `compact`, `standard`, `exhaustive`
- `permission_profile`: `read_only`, `workspace_write`, `full_access`, `custom`
- `sandbox_mode`: `read_only`, `workspace_write`, `full_access`
- `approval_policy`: `always`, `on_request`, `on_failure`, `never`
- `tool_call_budget_policy`: `schema_first`, `bounded_reads`, `ledger_first`, `retry_smaller`, `manual`
- `thread_read_policy`: `latest_only`, `bounded_with_cursor`, `ledger_snapshot`, `targeted_outputs_only`
- `active_actor_polling_policy`: `adaptive_backoff`, `fixed_interval`, `event_triggered`, `aggressive_watch`, `manual`
- `allowed_command_prefixes`: reusable command prefixes workers may request or use when supported
- `restricted_command_prefixes`: command prefixes that require Executive approval or are forbidden
- `destructive_action_policy`: `forbid`, `confirm`, `allow_scoped`
- `credential_policy`: `never_prompt`, `use_existing_only`, `prompt_if_present`
- `role_model_policy`: role-specific model and reasoning defaults
- `model_switch_policy`: `never`, `by_role`, `by_risk`, `by_cost`
- `capability_preflight`: `minimal`, `standard`, `full`
- `blocker_policy`: named defaults for git auth, dirty state, test flakes, long tests, dev servers, worktrees, branches, commits, pushes, env/secrets, browser tools, tool schema/window limits, artifacts, compaction, heartbeat, user interruption, and release gates

If a user selects a mode, apply that mode's defaults. If the user customizes a knob, prefer the explicit override. Read `references/configuration.md` when choosing or explaining modes.

## Permission, Model, And Preflight Policy

Permissions and model choices are first-class factory inputs. Record the desired settings even when the runtime cannot apply them automatically.

- New factory threads should be created with the configured model and reasoning effort when the thread tool supports it.
- New Builder and Reviewer prompts should restate the requested permission profile, allowed prefixes, restricted prefixes, destructive-action rule, and credential policy.
- If the runtime does not expose permission controls, treat the config as an operational target: ask for reusable approvals only when needed, use non-interactive commands when possible, and fall back to local commits when push auth blocks progress.
- For unattended factories, prefer an explicit `full_access`/low-friction approval setup only when the user grants it. Keep destructive commands, credential prompts, production effects, and data deletion behind the configured blocker policies.
- Use `capability_preflight` to identify missing thread tools, automation tools, goal tooling, browser access, git write access, push auth, package managers, test commands, env files, secrets, and network access before launching workers.
- Keep the active context lean: pass an Effective Config Summary in batons; keep exhaustive policy matrices in docs unless a blocker requires them.

## Tool Call Limits And Thread Inspection

Long-running factories must assume orchestration tools have strict schemas and practical result-window limits. A controller may see failures such as `invalid arguments` when it passes unsupported fields, asks for a list window larger than the tool accepts, includes too much output, or uses stale assumptions after tool metadata changes. Treat this as an orchestration degradation, not a product blocker.

Default policy:

1. Search or inspect the current tool schema before using thread, automation, browser, or app-management tools that are not already loaded.
2. Use schema-shaped minimal calls first. Do not invent optional arguments. Do not pass large limits unless the schema and recent successful calls prove they work.
3. Prefer bounded thread reads: latest status first, then cursor-based older reads only when required. Include command/tool outputs only for a specific evidence gap, with small output caps.
4. Prefer ledger, commits, handoff bundles, stop/resume packets, and explicit status packets as the source of truth. Do not require parsing a whole thread transcript to know ownership, current baton, or acceptance state.
5. If a tool call fails with argument or window limits, remove optional fields, reduce the requested window, narrow the query, and retry once. Do not loop on the same invalid shape.
6. When a monitor cannot inspect enough context, it should send one small status ping to the active Executive/Ledger or Builder instead of duplicating work or touching the worktree.
7. Record recurring tool-limit failures in the ledger retrospective and update factory config, monitor prompts, or handoff templates so future turns carry compact state.

Useful fail-mode labels:

- `schema_invalid`: unsupported or stale tool arguments.
- `window_too_large`: list/read limit or result size is too broad.
- `outputs_too_large`: command/tool outputs make the read too heavy.
- `thread_context_stale`: heartbeat or controller is operating from old baton/thread assumptions.
- `inspection_insufficient`: bounded reads cannot prove ownership, handoff, or acceptance state.

For active single-writer factories, a Principal or monitor should not touch the main worktree just because thread inspection failed. It should either fall back to the ledger/status packet or route one precise question/directive to the active Executive/Ledger.

## Adaptive Polling And Sleep Backoff

Factory controllers should respond to state transitions, not continuously observe normal progress. When a Builder or Reviewer is actively working and appears healthy, prefer longer quiet wait blocks and fewer thread reads.

Default active-actor polling behavior:

- Healthy Builder actively editing or thinking: poll about every 3 minutes.
- Known long command running, such as full checks, browser tests, release gates, builds, migrations, or install steps: poll every 3-5 minutes unless output suggests imminent completion.
- Handoff likely, final verification finishing, or explicit user status request: poll in shorter 30-60 second windows.
- Blocker, failure, relinquish, handoff, safety issue, dirty-state ambiguity, or collision signal: inspect promptly and route the proper recovery/review path.
- No meaningful progress past the configured stale threshold: send one precise status ping before reclaiming or replacing the actor.

Keep automation cadence separate from inside-turn sleep loops. A heartbeat may still wake on its configured schedule, but if it sees a healthy active actor it should do one bounded status read and exit or sleep in a longer block. It should not spin through repeated short sleeps and transcript reads.

Recommended defaults for substantial factories:

```text
active_actor_polling_policy: adaptive_backoff
active_builder_poll_interval: 3m
long_check_poll_interval: 5m
handoff_poll_interval: 60s
stale_ping_after: 10m_without_meaningful_progress
stale_reclaim_after: 20m_to_30m_policy_dependent
```

## Goal Setup

A persistent executive goal helps long-running factories keep context and momentum. Create one only when the user explicitly asks, or when the request clearly implies durable factory control, goal tooling is available, and the active runtime policy permits it. Otherwise record the goal text in the ledger and continue without tool-level goal creation.

General goal template:

```text
Drive the <PROJECT> software factory end to end: maintain the factory ledger, coordinate Builder and Reviewer batons, enforce the selected work mode and project invariants, preserve user changes, accept only work that satisfies the configured acceptance tier, keep required tests/evals passing according to the verification cadence, commit accepted work locally, push when authentication permits, and continue until the requested project outcome is complete and verified.
```

Mode-specific refinements:

- Safe MVP: emphasize one thin real user-facing vertical slice, hard invariants, focused proof, known gaps, and a checkpoint for hardening.
- Velocity: emphasize product-visible vertical slices, focused verification, risk tracking, and full gates at configured checkpoints.
- Strict: emphasize small batons, deep review, full gates, and hard invariants.
- Release: emphasize scope freeze, release criteria, deployment readiness, final QA, and blocking risk resolution.
- Recovery: emphasize freezing new work, reconciling state, restoring ownership, and resuming safely.

Record the active goal or inferred objective in `docs/factory_config.md`. If goal tooling lacks a pause state, do not mark a goal complete or blocked merely to pause participation; use factory topology such as `passive_fallback` instead.

## Factory Stop And Resume

Treat stop requests as control-plane commands. They preempt new baton assignment and must preserve enough state for a clean resume.

Stop modes:

- `pause_new_work`: stop assigning new batons; active safe work may continue.
- `drain_to_handoff`: current Builder reaches a Handoff Bundle, then pauses before acceptance.
- `drain_to_checkpoint`: current baton reaches review, acceptance decision, ledger evidence, configured commit/push fallback, then pauses. This is the default for most substantial builds.
- `release_freeze`: stop feature work; allow only release gates, blocker fixes, and readiness notes.
- `hard_stop`: active actors stop after the current safe command and record dirty state, uncommitted files, and unfinished checks.
- `emergency_stop`: immediate freeze for safety, security, destructive-action, or ownership risk. Preserve evidence first; defer cleanup until reviewed.

Stop lifecycle:

1. Classify `default_stop_mode`, `stop_scope`, requester, authority, and reason.
2. Record `stop_requested` in the ledger or controller thread before sending new worker instructions when possible.
3. Notify the Executive/Ledger first. The Executive/Ledger owns routing unless the Principal has emergency override authority.
4. Send the active Builder or Reviewer a mode-specific stop directive only after checking baton ownership.
5. Apply `stop_monitor_policy` after the Stop Packet exists, except for emergency stops.
6. Apply `stop_cleanup_policy` only after ledger evidence captures active state and unresolved risks.
7. Produce a Stop Packet with active roles, current baton, worktree status, latest accepted/pushed commit, dirty files, commands/tests in progress, monitors changed, cleanup actions, unresolved risks, and resume instructions.

Resume from the Stop Packet. If `resume_policy` requires user confirmation, do not wake Builders or restart monitors until the user or authorized Principal/Executive explicitly resumes. If goal tooling lacks pause/resume, do not mark the goal complete or blocked merely because the factory is stopped.

Resume modes:

- `restore_monitors_only`: restart or retarget monitors and report readiness; do not wake Builders or assign work.
- `continue_same_baton`: reauthorize the prior Builder/Reviewer with a fresh baton after confirming it is idle or safely resumable.
- `replace_actor`: retire an unusable or stale actor, record the replacement decision, then authorize a new actor.
- `advance_to_review`: continue from an existing Handoff Bundle or completed checkpoint into review, acceptance, commit, or release gates.
- `assign_next_baton`: when no prior baton should continue, record a resumed running state and assign the next queued baton.
- `recovery_first`: reconcile dirty state, collisions, missing evidence, failed gates, or ambiguous ownership before assigning work.

Resume lifecycle:

1. Confirm resume authority. Stale heartbeats, blocked-goal wakeups, monitor pings, or old controller turns are not resume authority unless the configured `resume_policy` explicitly allows them.
2. Read the latest Stop Packet, ledger stop state, current git/worktree state, active threads, monitors, goal status, and cleanup state before waking any worker.
3. Classify `default_resume_mode`, resume scope, actor to wake or replace, monitors to restore, verification to rerun, and cleanup to defer.
4. If state is dirty, ownership is unclear, commands are still running, or the Stop Packet is missing required evidence, switch to `recovery_first`.
5. Record a Resume Packet or ledger checkpoint when the resume changes baton ownership, monitors, cleanup, goal state, or stop state.
6. Reissue fresh baton authority. Do not rely on pre-stop or revoked baton messages; every resumed Builder/Reviewer must receive a new authorization with current commit, scope, non-goals, checks, and handoff requirements.
7. Restore monitors only after the controller knows whether a worker owns the baton. Monitors must treat stopped/frozen states as report-only until a valid Resume Packet exists.
8. If goal tooling lacks a real resume/unpause operation, record the limitation and restore factory flow through ledger state, monitors, and fresh baton routing rather than marking goals complete or blocked.
9. After a Builder owns the resumed baton, the Executive/Ledger returns to monitor-only behavior until handoff, block, stall, or relinquish.

## Work Modes

- **Discovery**: inspect, map docs, identify risks, no product edits unless asked.
- **Prototype**: build end-to-end behavior quickly, mark as prototype accepted, defer hardening explicitly.
- **Safe MVP**: ship one thin real vertical slice quickly; preserve hard safety invariants, explicit external effects, real state transitions or explicit non-mutating previews, focused tests, and a hardening backlog.
- **Velocity**: larger vertical slices, focused checks, periodic full gates, compact handoffs.
- **Balanced**: moderate batons, focused checks plus build, full gates at meaningful checkpoints.
- **Strict**: small batons, full review, full gate per baton, strong browser/security evidence.
- **Release**: freeze broad scope, verify deployment readiness, run release gates and final smoke.
- **Recovery**: pause new work, reconcile dirty state, stale threads, collisions, failed gates, or spec drift.
- **Maintenance**: small low-risk fixes with focused checks and clear regression evidence.
- **Migration**: staged schema/API/data/infra changes with rollback and compatibility gates.
- **Design Sprint**: UI/product surface iteration with the project-design skill, screenshots, browser/mobile QA, and focused technical gates.

## Role Topologies

- **Lean Solo**: Executive acts as ledger, reviewer, committer, and user interface. Best for small tasks.
- **Standard**: Executive/Ledger plus Builder. Best for ordinary scoped work.
- **Reviewed**: Executive/Ledger plus Builder plus Reviewer. Best default for longer factories.
- **Managed**: Manager/User Liaison plus Executive/Ledger plus Builder plus Reviewer. Best when the user will give frequent feedback while work is active.
- **Enterprise**: Manager, Executive, Ledger, Builders, Reviewers, and Watchers. Use only for large or release-critical programs.

Role boundaries:

- Principal Executive is the user-facing strategic partner above the factory. It may inspect threads and repo state, configure topology, initiate cleanup, request stop/resume, promote/supersede ledgers, and send directives to the active Executive/Ledger according to its authority. It does not normally hold the write baton or review every slice.
- Executive owns final acceptance, commits, product judgment, and routing.
- Ledger owns durable state, baton queue, evidence, risk, and cleanup records. In executive-as-ledger mode this is the Executive.
- Builder owns scoped implementation and hands off to the Executive/Ledger, not directly to Reviewer by default.
- Reviewer is read-only by default and sends a Review Package to the Executive/Ledger.
- Manager/User Liaison packages user side feedback and sends briefs to the Principal or Executive according to configuration. It must not message Builders or Reviewers unless explicitly promoted.
- Watchers monitor and wake actors; they never edit.

## Routing And Packages

Default routing:

1. Executive/Ledger assigns Builder.
2. Builder posts a Handoff Bundle to Executive/Ledger.
3. Executive/Ledger records `review_pending` and routes a Review Baton if configured.
4. Reviewer produces a Review Package.
5. Executive accepts, patches, requests Builder fixes, changes mode, or rejects.
6. Executive/Ledger records evidence, commits accepted work, and triggers cleanup if configured.

Package names:

- **Handoff Bundle**: Builder output after implementation.
- **Review Baton**: Executive/Ledger prompt that sends a Builder handoff to Reviewer.
- **Review Package**: Reviewer audit with findings, required fixes, evidence, and recommendation.
- **Executive Brief**: Manager/User Liaison package containing user feedback, context, requested decision, and suggested routing.
- **Decision Packet**: Executive decision summary for the ledger.
- **Stop Packet**: controller record produced when a stop directive pauses, drains, freezes, or hard-stops the factory.
- **Resume Packet**: controller record that names the resume authority, next baton, monitors to restore, verification to rerun, and cleanup still pending.

Use `reviewer_spawn_policy=after_handoff` by default. Use `standby_with_builder` for strict, release, migration, or high-risk work. Use `parallel_read_only` only when the Reviewer can safely inspect specs, committed code, screenshots, or test output without touching the active writer's worktree.

## Risk Escalation

Do not let a fast mode override hard safety. In Safe MVP mode, sacrifice breadth, polish, secondary workflows, exhaustive docs, and full gates first. Do not sacrifice real behavior, explicit external-effect boundaries, source/provenance where applicable, mutation gates, security, or the focused tests proving the MVP flow. Escalate verification and review when touching:

- auth, permissions, session, security, secrets, or encryption;
- payments, trading, money movement, billing, or irreversible user actions;
- production data writes, migrations, destructive commands, or infra/deployments;
- public API contracts, shared packages, data schemas, generated clients, or SDKs;
- scoring, ranking, recommendation, policy, compliance, ML/eval, or safety logic;
- external live services, background jobs, schedulers, webhooks, queues, or provider calls.

When escalated, record why and which knobs changed.

## Acceptance Ladder

Use acceptance tiers to move fast without pretending every slice is release-ready.

- **Prototype accepted**: behavior is demonstrable; known hardening gaps are recorded.
- **Integration accepted**: behavior is wired into the product with focused verification and no known blocking regressions.
- **Release accepted**: full project gates, release-specific checks, security/deployment readiness, and user-facing QA are complete.

Do not call a slice release accepted unless release evidence exists. Do not leave broken critical tests untracked.

## Baton Lifecycle

1. **Prepare**: Update config/ledger with baton goal, tier, scope, non-goals, risk, checks, owner, and escalation triggers.
2. **Authorize**: Send the full baton after assignment is recorded. A standby prompt may reserve a Builder first.
3. **Build**: Builder edits only scoped files, runs required checks, and never commits unless explicitly delegated.
4. **Handoff**: Builder reports files, behavior, contracts, tests, skipped checks, risks, and next recommendation to Executive/Ledger.
5. **Review route**: Executive/Ledger either reviews directly or sends a Review Baton to Reviewer according to policy.
6. **Review package**: Reviewer reports findings and recommendation without editing unless explicitly authorized.
7. **Patch or accept**: Executive patches narrow acceptance gaps, sends fixes back to Builder, accepts, or reassigns. Do not broaden scope silently.
8. **Record**: Update ledger with tier, evidence, residual risk, skipped checks, review package, and next baton.
9. **Commit**: Stage explicit intended files, run diff/generated-file guards, commit accepted work, push when credentials permit.
10. **Cleanup**: Archive completed worker threads only after evidence is captured and no unresolved risk remains.

If a stop directive arrives during the lifecycle, freeze new baton assignment immediately and follow the configured stop mode. Do not convert a stop into acceptance, rejection, goal completion, or cleanup without explicit evidence.

## Concurrency

Default: one active writer per worktree.

Allowed acceleration:

- Parallel read-only reviewers may inspect committed code, handoff diffs, screenshots, test output, architecture, security, performance, or UI quality.
- Parallel implementation needs separate worktrees plus documented owner, scope, merge order, conflict policy, and reconciliation gate.
- Watchers and monitors never edit files.

If collision risk rises, switch to Recovery mode.

## Thread Cleanup

Thread cleanup is optional but recommended for long-running factories.

Allowed cleanup policies:

- `none`: never cleanup automatically.
- `manual`: suggest cleanup and wait for user/controller action.
- `after_acceptance`: archive completed Builder/Reviewer threads after accepted commit and ledger evidence.
- `rolling_window`: keep active roles plus the last N completed workers.
- `aggressive`: keep only active roles, pinned roles, and unresolved-risk threads.
- `release_archive`: archive completed workers after release acceptance.

Never archive active, blocked, stale-unresolved, unreviewed, uncommitted, or open-risk threads. Preserve Manager, Executive, Ledger, and any thread explicitly pinned or marked for audit.

## Verification Strategy

Match verification to risk and acceptance tier:

- Prototype: smoke/focused checks and visible caveats.
- Integration: focused tests for changed behavior, typecheck/build when relevant, targeted UI/browser QA for user-facing changes.
- Release: full project gate, browser/mobile QA, security/deployment/env checks, docs drift, and final smoke.

Treat green tests as evidence only after checking they cover the changed behavior. Record skipped checks honestly.

## Operating Rules

- Preserve user changes; never revert unknown work unless explicitly asked.
- Prefer repository patterns and existing tooling.
- Keep builders scoped and handoffs compact.
- Keep ledgers useful, not ceremonial.
- Prefer product-visible vertical slices when the selected mode favors velocity.
- Keep hard invariants explicit in every baton.
- If push/auth fails, keep the local commit and continue with recorded remote status.
- If a specific design skill is named for UI work, require that exact skill.

## Bundled Resources

- `references/configuration.md`: detailed mode presets, knobs, escalation rules, and selection guidance.
- `references/templates.md`: factory config, ledger, baton, handoff, reviewer, stop/resume, heartbeat, and recovery templates.
- `scripts/seed_factory_docs.py`: seeds generic factory docs and config for a project.
