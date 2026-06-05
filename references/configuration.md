# Software Factory Configuration

Use this reference when instantiating a factory or changing its operating culture.

## Contents

- [Mode Presets](#mode-presets)
- [Mode Defaults For Friction Control](#mode-defaults-for-friction-control)
- [Default Mode Guidance](#default-mode-guidance)
- [Minimal User Questions](#minimal-user-questions)
- [Safe MVP Contract](#safe-mvp-contract)
- [Granular Knobs](#granular-knobs)
- [Goal Templates](#goal-templates)
- [Role Topology Defaults](#role-topology-defaults)
- [Package Types](#package-types)
- [Risk Escalation Matrix](#risk-escalation-matrix)
- [Blocker Policies](#blocker-policies)
- [Acceptance Tier Rules](#acceptance-tier-rules)
- [Retrospective Loop](#retrospective-loop)

## Mode Presets

| Work mode | Baton size | Acceptance tier | Verification | Review | Role topology | Cleanup | Default stop | Best for |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `discovery` | micro | prototype | smoke | skim | lean_solo | manual | pause_new_work | repo mapping, requirements, risk discovery |
| `prototype` | vertical_slice | prototype | smoke/focused | targeted | standard | rolling_window | drain_to_checkpoint | fast end-to-end demos |
| `safe_mvp` | vertical_slice | integration | focused | targeted | reviewed | rolling_window | drain_to_checkpoint | thin real product slices under hard invariants |
| `velocity` | vertical_slice | integration | focused_plus_build | targeted | reviewed | rolling_window | drain_to_checkpoint | rapid product progress |
| `balanced` | medium | integration | focused_plus_build | targeted | reviewed | rolling_window | drain_to_checkpoint | normal feature work |
| `strict` | small | integration/release | full_gate | full | reviewed | after_acceptance | drain_to_checkpoint | high-risk code, contracts, safety |
| `release` | micro/small | release | release_gate | adversarial | enterprise | release_archive | release_freeze | final ship readiness |
| `recovery` | micro | integration | focused/full as needed | full | reviewed | manual | hard_stop | messy state, collisions, stale threads |
| `maintenance` | small | integration | focused | targeted | standard | rolling_window | drain_to_checkpoint | bug fixes and low-risk upkeep |
| `migration` | small | integration/release | full_gate | full | reviewed | after_acceptance | drain_to_checkpoint | schema, data, API, infra transitions |
| `design_sprint` | medium/vertical_slice | prototype/integration | focused_plus_build | targeted | reviewed | rolling_window | drain_to_checkpoint | UI/UX iteration and visual polish |

## Mode Defaults For Friction Control

These defaults prevent the factory from becoming a prompt-heavy ceremony. Users can override any field.

| Work mode | Config verbosity | Permission profile | Approval policy | Preflight | Commit/push | Long tests | Model routing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `discovery` | compact | read_only | on_request | minimal | none/local_only | release_only | by_cost |
| `prototype` | compact | workspace_write | on_failure | standard | per_vertical_slice/auth_if_available | focused_then_checkpoint | by_role |
| `safe_mvp` | compact | full_access | on_failure | standard | per_vertical_slice/auth_if_available | focused_then_checkpoint | by_role |
| `velocity` | compact | full_access | on_failure | standard | per_baton/auth_if_available | focused_then_checkpoint | by_role |
| `balanced` | standard | full_access | on_failure | standard | per_baton/auth_if_available | focused_then_checkpoint | by_role |
| `strict` | standard | full_access | on_failure | full | per_baton/auth_if_available | full_each_baton | by_risk |
| `release` | exhaustive | full_access | on_failure | full | per_baton/require_push_if_possible | full_each_baton | by_risk |
| `recovery` | exhaustive | workspace_write | on_request | full | per_baton/local_commit_continue | focused_then_checkpoint | by_risk |
| `maintenance` | compact | workspace_write | on_failure | standard | per_baton/auth_if_available | focused_then_checkpoint | by_role |
| `migration` | standard | full_access | on_failure | full | per_baton/auth_if_available | full_each_baton | by_risk |
| `design_sprint` | standard | full_access | on_failure | standard | per_baton/auth_if_available | focused_then_checkpoint | by_role |

`full_access` is a requested factory profile, not a guarantee that the runtime granted it. If the environment still prompts, record the mismatch and apply the configured blocker policy instead of stalling silently.

## Default Mode Guidance

- Choose `velocity` when the user explicitly wants fast delivery, iteration, or a working product slice.
- Choose `safe_mvp` when the user wants a working core flow in hours, but still expects real behavior, explicit external effects, and hard safety invariants.
- Choose `balanced` for ordinary feature implementation.
- Choose `strict` for shared contracts, security-sensitive behavior, business-critical logic, or when prior work quality is suspect.
- Choose `release` when preparing to deploy, merge, publish, or declare done.
- Choose `recovery` when there is a collision, stale builder, broken worktree, unexpected worktree, failing gate, or unclear ownership.
- Choose `prototype` when the goal is learning or demonstrating a concept.
- Choose `design_sprint` for visual/product surface work, especially when a design skill or screenshots are central.

## Minimal User Questions

Ask for mode if it is not obvious. Keep the question short:

```text
Which factory mode should I use?

- Balanced: normal feature work, good quality without heavy ceremony.
- Safe MVP: thinnest real product slice; cut breadth and polish, keep hard safety.
- Velocity: bigger vertical slices, focused checks, periodic full gates.
- Strict: smaller batons, deeper review, full gates for high-risk work.
- Prototype: move fast to prove the experience; hardening is tracked separately.
- Release/Recovery: final ship readiness, or cleanup of messy/broken state.
```

Ask for target outcome only when it is unclear:

```text
What outcome should the factory drive toward: end-to-end build, specific feature, release readiness, recovery/cleanup, or something else?
```

Do not turn setup into a long interview. Infer the rest and record it as editable config.

## Safe MVP Contract

Use `safe_mvp` when the factory should compress cycle time without returning to shell/demo behavior.

Safe cuts:

- one primary user workflow instead of broad feature coverage;
- one or two reliable providers/sources instead of broad integrations;
- focused tests and targeted browser QA instead of full release gates every baton;
- simple deterministic policy v0 instead of a full scoring/recommendation system;
- compact docs and a hardening backlog instead of exhaustive operator material.

Unsafe cuts:

- fake success or fixture data presented as real behavior;
- hidden external calls on page load, readiness, tests, background jobs, or monitors;
- unredacted secrets, credential prompts, or uncontrolled production effects;
- irreversible writes, recommendations, trades, payments, destructive actions, or other high-impact mutations without the configured explicit gate;
- skipping the focused proof that the core MVP flow works and the protected invariants still hold.

Default shape: one large Builder baton for the thin vertical slice, Reviewer after handoff, Executive acceptance with focused proof, then hardening/release mode only if the MVP earns it.

Ask about user involvement for substantial factories:

```text
How do you want to stay involved?

- Principal Partner: you and a top-level overseer steer the factory while the ledger drives.
- Direct Executive: talk directly to the active Executive/Ledger.
- Hands-Off: factory runs with checkpoint summaries.
```

Ask about manager/feedback handling when the user expects to comment while work continues, or when the factory is long-running:

```text
How should side feedback be handled?

- No Manager: keep the active Executive lean; feedback goes directly to the chosen contact point.
- Feedback Manager: package user side feedback into briefs before it reaches the Executive.
- Always-On Manager: monitor user feedback and factory state continuously, then brief the Principal or Executive.
```

Default substantial-build intake:

```text
user_involvement: principal_partner
feedback_handling: no_manager
principal_policy: user_thread
principal_authority: configure
principal_intervention_policy: can_supersede_ledger
principal_digest_cadence: checkpoint
principal_context_budget: standard
tool_call_budget_policy: bounded_reads
thread_read_policy: latest_only
active_actor_polling_policy: adaptive_backoff
active_builder_poll_interval: 3m
long_check_poll_interval: 5m
handoff_poll_interval: 60s
stale_ping_after: 10m_without_meaningful_progress
stale_reclaim_after: 20m_to_30m_policy_dependent
factory_stop_policy: enabled
default_stop_mode: drain_to_checkpoint
stop_scope: all_factory
stop_authority: principal_or_user
stop_monitor_policy: pause_after_stop
stop_cleanup_policy: rolling_window_after_checkpoint
resume_policy: resume_from_stop_packet
default_resume_mode: continue_same_baton
stop_packet_required: true
```

This gives most users a high-level partner/overseer without adding a Manager thread unless side feedback volume justifies it.

## Granular Knobs

`user_involvement`:

- `principal_partner`: a user-facing Principal Executive oversees factory structure, cleanup, handoffs, mode changes, and ledger replacement while the active Executive/Ledger drives delivery.
- `direct_executive`: user talks directly to the active Executive/Ledger.
- `hands_off`: user receives checkpoint summaries; the factory should avoid conversational interruption.

`feedback_handling`:

- `no_manager`: no Manager/User Liaison by default.
- `feedback_manager`: Manager packages user side feedback into Principal or Executive Briefs.
- `always_on_manager`: Manager continuously monitors user feedback and thread state, then briefs at configured cadence.

`principal_policy`:

- `none`: no Principal Executive role.
- `same_as_executive`: the active Executive/Ledger also serves as the Principal.
- `dedicated`: create a dedicated Principal thread.
- `user_thread`: the current user-facing thread acts as Principal; best default for substantial projects.

`principal_authority`:

- `observe`: read status and summarize only.
- `steer`: send direction to the Executive/Ledger.
- `configure`: change mode, cleanup, topology, and role policy.
- `emergency_override`: pause, replace, or supersede a ledger when factory health requires it.

`principal_intervention_policy`:

- `no_baton_interference`: Principal never interrupts an active writer except for user safety.
- `can_pause`: Principal may pause work on conflict, safety, or user request.
- `can_reassign`: Principal may reassign or replace stuck builders/reviewers through the Executive/Ledger.
- `can_supersede_ledger`: Principal may promote a fresh Executive/Ledger when context is too noisy, stuck, or inefficient.

`principal_digest_cadence`:

- `manual`: update only on user request.
- `checkpoint`: update after accepted batons, blockers, handoffs, or mode changes.
- `heartbeat`: update on monitor cadence.
- `daily`: update once per day for long-running background work.

`principal_context_budget`:

- `compact`: status, risks, next action.
- `standard`: status plus acceptance evidence and active handoffs.
- `full`: include deeper architecture, release, and risk context when needed.

`config_verbosity`:

- `compact`: only mode, roles, permissions, model summary, blockers, active baton, checks, and next step travel in prompts.
- `standard`: include the effective config summary plus evidence, skipped checks, risk, and cleanup settings.
- `exhaustive`: include full policy matrices, rollback/release details, screenshots/logs, and open decisions.

Use compact or standard for most factories. Keep exhaustive policy detail in `docs/factory_config.md` and load it only when the baton touches that policy.

`tool_call_budget_policy`:

- `schema_first`: inspect or search the current tool schema before using thread, automation, browser, or app-management tools. Best when tools are newly loaded or have changed.
- `bounded_reads`: default for long-running factories. Use small thread/list reads first, narrow queries, and avoid outputs unless needed.
- `ledger_first`: rely on build ledger, commits, handoff bundles, and status packets before reading older thread history.
- `retry_smaller`: when a tool call fails with `invalid arguments` or a practical window limit, remove optional fields, reduce the requested window, narrow the query, and retry once.
- `manual`: ask the user or Principal before spending more inspection calls.

Recommended default for substantial factories:

```text
tool_call_budget_policy: bounded_reads
thread_read_policy: latest_only
active_actor_polling_policy: adaptive_backoff
```

Upgrade to `schema_first` during capability preflight, after plugin/tool changes, or after an `invalid arguments` failure. Combine `ledger_first` with rolling-window cleanup so accepted worker threads can be archived without losing operational state.

`thread_read_policy`:

- `latest_only`: read the latest thread state/status first; use this for heartbeat monitors and single-writer ownership checks.
- `bounded_with_cursor`: read older turns only through cursor/page continuation and only when a specific evidence gap remains.
- `ledger_snapshot`: prefer a ledger/status packet/handoff as the compact source of truth; thread reads only verify liveness or unresolved blockers.
- `targeted_outputs_only`: include command or tool outputs only for a specific check, and cap output size.

Known thread/tool inspection fail modes:

- `schema_invalid`: the call used fields the current tool schema does not accept, or a stale prompt assumed an old schema.
- `window_too_large`: the requested list/read limit or query breadth exceeds tool limits.
- `outputs_too_large`: included outputs make the thread read too heavy or noisy.
- `thread_context_stale`: a heartbeat/controller prompt names an obsolete baton, thread, or ownership state.
- `inspection_insufficient`: bounded reads cannot prove ownership, handoff, or acceptance state.

Handling policy:

1. Do not treat a thread inspection failure as a product/test failure.
2. Do not retry the same invalid call shape.
3. Retry once with fewer arguments, lower limits, narrower query, no outputs, or cursor-based continuation.
4. If still insufficient, ask the active Executive/Ledger or Builder for a compact status packet.
5. Record recurring failures in the retrospective and update monitor prompts or handoff templates so future heartbeats need less transcript parsing.

`active_actor_polling_policy`:

- `adaptive_backoff`: default for substantial factories. Use longer quiet polling intervals while an actor is healthy, and shorten only near handoff, failure, blocker, stale, or user-requested status.
- `fixed_interval`: poll on a configured interval regardless of actor state. Use only when the runtime cannot manage adaptive waits.
- `event_triggered`: rely mostly on handoff/status packets and heartbeat wakeups. Best for hands-off or low-token operation when actors are reliable.
- `aggressive_watch`: short polling for high-risk release windows, fragile migrations, or suspected failures. Avoid as a default because it burns tokens.
- `manual`: the Principal, Executive, or user decides polling behavior case by case.

Recommended defaults:

```text
active_actor_polling_policy: adaptive_backoff
active_builder_poll_interval: 3m
long_check_poll_interval: 5m
handoff_poll_interval: 60s
stale_ping_after: 10m_without_meaningful_progress
stale_reclaim_after: 20m_to_30m_policy_dependent
```

Polling states:

- Healthy active Builder: one bounded status read, then wait roughly `active_builder_poll_interval`.
- Known long command: wait roughly `long_check_poll_interval` unless output signals imminent completion or failure.
- Handoff likely, final verification, or user asks for status: use `handoff_poll_interval`.
- Blocker, failure, relinquish, handoff, dirty-state ambiguity, safety issue, or collision: inspect immediately and route review/recovery.
- No meaningful progress past `stale_ping_after`: send one precise status ping.
- No response or unresolved staleness past `stale_reclaim_after`: apply the configured stale-builder/recovery policy.

Separate automation cadence from inside-turn sleeps. A monitor may wake every configured interval, but inside an active controller turn it should not run repeated short sleep/read loops while a Builder is healthy. This policy works with `tool_call_budget_policy` and `thread_read_policy`: fewer reads, more compact status packets, and no duplicate worktree inspection while another actor owns the baton.

`factory_topology`:

- `executive_as_ledger`: one thread is the executive and operational ledger.
- `separate_ledger`: a dedicated ledger/controller thread manages batons; executive keeps final authority.
- `passive_fallback`: current thread stays dormant while another thread is primary.

`role_topology`:

- `lean_solo`: Executive handles ledger, review, commit, and user communication.
- `standard`: Executive/Ledger plus Builder.
- `reviewed`: Executive/Ledger plus Builder plus Reviewer.
- `managed`: Manager/User Liaison plus Executive/Ledger plus Builder plus Reviewer.
- `enterprise`: Manager, Executive, Ledger, Builders, Reviewers, and Watchers.

Principal Executive is orthogonal to `role_topology`: it sits above the active factory. A `reviewed` topology can still have a Principal Partner, and a `managed` topology can have both Principal and Manager when user feedback volume is high.

`manager_policy`:

- `none`: no Manager/User Liaison role.
- `user_feedback_only`: Manager packages user feedback into Executive Briefs.
- `always_on`: Manager monitors user feedback, thread state, and digest requests, then briefs Executive.

`executive_context_policy`:

- `direct_user_chat`: user talks directly to Executive.
- `manager_packaged_feedback`: Manager receives user side conversation and sends Executive Briefs.
- `mixed`: user may talk to Executive, but Manager packages non-urgent feedback.

Manager guardrail: Manager may read factory threads and repo context when allowed, but by default speaks only to Principal or Executive according to config. It must not assign Builders, message Reviewers, mutate files, change monitors, or commit.

`reviewer_policy`:

- `none`: Executive reviews directly.
- `risk_triggered`: Reviewer used for risk escalators, large batons, or uncertain quality.
- `every_baton`: every Builder handoff receives a Review Package.
- `release_only`: Reviewer used during release readiness or final gate work.

`reviewer_spawn_policy`:

- `none`: no Reviewer thread.
- `after_handoff`: spawn or wake Reviewer after Builder Handoff Bundle exists.
- `standby_with_builder`: create Reviewer standby at Builder assignment; review starts only after handoff.
- `parallel_read_only`: Reviewer may inspect specs, committed code, screenshots, or test output while Builder works.
- `risk_triggered`: spawn Reviewer when the baton touches a risk escalator.
- `release_only`: spawn Reviewer during release mode or release acceptance.

Default routing: Builder hands off to Executive/Ledger; Executive/Ledger routes a Review Baton to Reviewer when configured. Builder should not directly message Reviewer unless the factory config explicitly allows it.

`concurrency_policy`:

- `single_writer`: one active writer per worktree.
- `parallel_read_only_reviewers`: reviewers may inspect and report while one writer works.
- `parallel_worktrees`: multiple writers only with isolated worktrees, merge order, and reconciliation plan.

`verification_level`:

- `smoke`: run or manually inspect the smallest proof that the app starts or behavior appears.
- `focused`: targeted tests for changed behavior.
- `focused_plus_build`: focused tests plus typecheck/build where relevant.
- `full_gate`: repository full test/eval gate.
- `release_gate`: full gate plus release, security, browser/mobile, deployment, and env checks.

`full_gate_cadence`:

- `every_baton`: strongest confidence, slowest throughput.
- `every_n_batons`: use for velocity when touched areas are low/medium risk.
- `risk_triggered`: full gate when risk escalators are touched.
- `release_only`: prototypes only; never use for production acceptance.

`browser_qa_policy`:

- `none`: no UI changed or no browser surface.
- `smoke`: open page or run a minimal visual check.
- `screenshots`: desktop/mobile screenshots and console/overflow checks.
- `full`: interaction, console, overflow, accessibility where applicable.
- `release`: full browser QA across key flows and breakpoints.

`handoff_detail`:

- `compact`: files, behavior, checks, risks, next step.
- `standard`: compact plus contracts, skipped checks, product alignment.
- `exhaustive`: standard plus rollback, screenshots, logs, migration/deploy notes.

`package_protocol`:

- `compact`: terse Handoff Bundles, Review Packages, and Executive Briefs.
- `standard`: include evidence, risks, skipped checks, and recommendation.
- `exhaustive`: add rollback, screenshots, logs, deployment/migration notes, and open questions.

`thread_cleanup_policy`:

- `none`: never archive automatically.
- `manual`: suggest cleanup and wait for explicit action.
- `after_acceptance`: archive completed workers after accepted commit and ledger evidence.
- `rolling_window`: keep active roles plus the last N completed workers.
- `aggressive`: keep active roles, pinned roles, and open-risk threads only.
- `release_archive`: archive completed workers after release acceptance.

Cleanup guardrails: never archive active, blocked, unresolved, unreviewed, uncommitted, or open-risk threads. Preserve Executive, Ledger, Manager, and explicitly pinned audit threads.

`factory_stop_policy`:

- `enabled`: allow configured stop and resume commands.
- `manual_only`: describe the stop plan, then require explicit user or Principal confirmation before taking action.
- `disabled`: do not perform factory-level stop actions unless a safety-critical emergency or direct user command overrides it.

`default_stop_mode`:

- `pause_new_work`: stop assigning new batons; current safe work may continue.
- `drain_to_handoff`: let the active Builder produce a Handoff Bundle, then pause before review, acceptance, or commit.
- `drain_to_checkpoint`: reach handoff, review/acceptance decision, ledger evidence, configured commit/push fallback, then pause. Best default for most factories.
- `release_freeze`: stop feature work but allow release gates, blocker fixes, rollback notes, and readiness evidence.
- `hard_stop`: actors stop after the current safe command and report dirty state, unfinished tests, and ownership.
- `emergency_stop`: immediate freeze for safety, security, destructive-action, credential, production-effect, or ownership risk.

`stop_scope`:

- `new_work_only`: stop future baton assignment.
- `active_baton`: stop or drain the current baton only.
- `all_factory`: stop all non-passive factory actors according to mode.
- `monitors_only`: stop, retarget, or pause factory automations without changing active work.
- `cleanup_only`: stop cleanup/archive actions while work may continue.

`stop_authority`:

- `user_only`: only the user can request stop.
- `principal_or_user`: user or Principal Executive can stop.
- `executive_or_above`: Executive, Principal, or user can stop.
- `any_active_role_with_confirmation`: any active role can raise a stop request, but Executive/Principal/user confirms before action unless emergency.

`stop_monitor_policy`:

- `keep_active`: keep monitors running and let them report paused state.
- `pause_after_stop`: pause or disable monitors after the Stop Packet is captured.
- `delete_after_stop`: delete obsolete monitors after evidence capture.
- `retarget_to_principal`: retarget status monitors to the Principal while the factory is paused.

`stop_cleanup_policy`:

- `none`: do not run cleanup as part of stop.
- `manual`: suggest cleanup but wait for explicit direction.
- `after_checkpoint`: cleanup only after accepted checkpoint evidence exists.
- `rolling_window_after_checkpoint`: keep active/pinned/open-risk roles plus recent completed workers after checkpoint.
- `release_archive`: archive completed workers after release freeze/readiness evidence is captured.

`resume_policy`:

- `manual`: resume only after explicit controller action.
- `resume_from_stop_packet`: resume from the recorded Stop Packet and Resume Packet.
- `resume_requires_user`: require user confirmation before waking workers or monitors.
- `auto_resume_after_window`: resume after a configured time/window only if no blocker or user conflict appears.

`default_resume_mode`:

- `restore_monitors_only`: restore reporting or oversight without waking Builders or assigning work.
- `continue_same_baton`: reauthorize the prior actor with a fresh baton after confirming it is usable, idle, and still scoped correctly.
- `replace_actor`: create or select a replacement actor when the prior actor is stale, overloaded, archived, confused, or unavailable.
- `advance_to_review`: continue from an existing handoff/checkpoint into review, acceptance, commit, or release gates.
- `assign_next_baton`: resume from a stopped factory by assigning the next queued baton instead of continuing the old one.
- `recovery_first`: reconcile dirty state, ambiguous ownership, failed checks, missing Stop Packet evidence, or colliding edits before assigning work.

Stop Packet requirements:

- mode, reason, requester, timestamp, scope, authority
- active roles and thread IDs
- current baton, owner, and status
- latest accepted commit, push/remote status, and branch/worktree
- dirty files, staged files, untracked files, and ownership
- running or last completed commands/tests
- monitors paused, kept, deleted, or retargeted
- cleanup actions performed or deferred
- unresolved risks and exact resume instructions

Resume Packet requirements:

- requester, approver, authority, timestamp, resume policy, and resume mode
- prior Stop Packet, stop checkpoint, latest accepted commit, branch/worktree, and current remote status
- read-only preflight of git status, staged/untracked files, active threads, monitors, cleanup, and goal state
- actor decision: same actor, replacement actor, review route, monitor-only route, or recovery-first route
- fresh baton or review authorization to issue, including current commit, scope, non-goals, verification, and handoff requirements
- monitors to restore, keep paused, delete, or retarget
- verification to rerun after resume and risks to re-check
- cleanup still deferred and stale-wakeup guardrails

Do not mark a persistent goal complete or blocked merely because the factory is paused. If goal tooling has no pause state, record the stopped state in the ledger and keep a resume path.

`permission_profile`:

- `read_only`: inspection, review, status, and planning only.
- `workspace_write`: file edits and local tests are allowed; commits, pushes, worktrees, monitor changes, and external effects require explicit delegation.
- `full_access`: file edits, tests, staging, local commits, branch operations, and approved non-destructive tooling are allowed.
- `custom`: use the explicit sandbox, approval, command-prefix, and blocker fields.

`sandbox_mode`:

- `read_only`: no file writes.
- `workspace_write`: repository-local writes only.
- `full_access`: full filesystem access where the runtime supports it.

`approval_policy`:

- `always`: ask before privileged commands.
- `on_request`: ask only for configured restricted actions.
- `on_failure`: try allowed non-destructive commands, then ask or degrade if blocked.
- `never`: unattended mode; use only when the user grants the permission profile and blocker policies still protect destructive actions.

`allowed_command_prefixes`:

- Command prefix list that workers may use or request reusable approval for, such as `git status`, `git diff`, `npm test`, `pnpm test`, `pytest`, or `make test`.
- Keep this role-specific when needed. Reviewers usually need read-only prefixes; Builders need test/build prefixes; Executives need stage/commit/push prefixes if delegated.

`restricted_command_prefixes`:

- Prefixes requiring Executive approval or forbidden by policy, such as `rm -rf`, `git reset --hard`, `git checkout --`, production deploy commands, database destructive commands, credential prompts, or live money movement.

`destructive_action_policy`:

- `forbid`: destructive commands are not allowed.
- `confirm`: require explicit Executive or user approval.
- `allow_scoped`: allowed only inside the recorded scope with rollback evidence.

`external_network_policy`:

- `disabled`: no network.
- `docs_only`: documentation/source lookup only.
- `allowed`: allowed for package installs, APIs, and source access according to repo policy.
- `explicit_only`: ask before external service calls, live provider calls, or production effects.

`credential_policy`:

- `never_prompt`: do not request passwords, tokens, or interactive credentials.
- `use_existing_only`: use configured env/credential helpers only.
- `prompt_if_present`: ask only when the user is present and the blocker policy allows it.

If push credentials fail and the factory is not in a release gate requiring remote sync, commit locally, record remote status, and continue.

`role_model_policy`:

- Configure model and reasoning by role: Executive, Ledger, Builder, Reviewer, Manager/User Liaison, Watcher, and fallback.
- Defaults should favor the strongest requested model/reasoning for Executive, Builder, and Reviewer on substantial work.
- Watchers and lightweight status checks may use cheaper settings when the user permits.

`model_switch_policy`:

- `never`: every role uses the configured default.
- `by_role`: role-specific model/reasoning defaults.
- `by_risk`: escalate model/reasoning for risk escalators, release gates, security, migrations, or uncertain reviews.
- `by_cost`: use high capability only where it changes outcome quality.

Record any material non-default model choice in the ledger when it affects implementation, review, or acceptance.

`capability_preflight`:

- `minimal`: git status, source docs, package scripts, current branch, obvious dirty-state hazards.
- `standard`: minimal plus thread tools, automation tools, goal tooling, browser availability, git write access, package manager, test commands, env files, generated-file guards, and network status.
- `full`: standard plus push auth, required secrets, external provider reachability, deploy/release commands, long-test feasibility, worktree support, and cleanup tooling.

Preflight should produce a short status table and a blocker decision before workers start. When thread or automation tools are involved, preflight should also record the currently valid tool shape at a high level, such as whether list windows, thread cursors, output inclusion, target thread ids, model settings, and archive/pin operations are supported. Do not hard-code a previously seen schema into worker prompts.

`goal_policy`:

- `none`: do not create a persistent goal.
- `ask`: ask whether the executive should create a persistent goal.
- `create_if_long_running`: create a goal when the user asks for end-to-end, multi-baton, or unattended factory work, goal tooling is available, and active runtime policy permits it; otherwise record goal text in the ledger.
- `explicit_only`: create a goal only when the user explicitly asks.

`target_outcome`:

- Examples: end-to-end build, specific feature, release readiness, recovery/cleanup, migration, maintenance, prototype, or user-defined objective.
- Prefer the user's language when recording this field.

## Goal Templates

Default end-to-end factory goal:

```text
Drive the <PROJECT> software factory end to end: maintain the factory ledger, coordinate Builder and Reviewer batons, enforce the selected work mode and project invariants, preserve user changes, accept only work that satisfies the configured acceptance tier, keep required tests/evals passing according to the verification cadence, commit accepted work locally, push when authentication permits, and continue until the requested project outcome is complete and verified.
```

Velocity variant:

```text
Drive the <PROJECT> software factory in Velocity Mode: deliver product-visible vertical slices quickly, coordinate batons, preserve hard invariants, use focused verification per slice, run full gates at configured checkpoints, record known risks, commit accepted integration work, and continue until the requested outcome is ready for hardening or release.
```

Safe MVP variant:

```text
Drive the <PROJECT> software factory in Safe MVP Mode: deliver the thinnest real product-visible vertical slice quickly, preserve hard safety and external-effect invariants, use focused proof for the core flow, record deferred breadth and hardening gaps, commit the accepted slice, and continue until the requested MVP behavior is demonstrable and ready for the next hardening or release checkpoint.
```

Release variant:

```text
Drive the <PROJECT> release factory to completion: freeze nonessential scope, verify release criteria, run full gates and final QA, resolve blocking risks, commit accepted fixes, push when authentication permits, and continue until the project is release-ready.
```

Recovery variant:

```text
Drive the <PROJECT> factory recovery: freeze new work, identify active owners and dirty state, reconcile collisions or failed gates, restore a single source of truth, commit accepted recovery work, and resume the configured factory once ownership and verification are trustworthy.
```

## Role Topology Defaults

Recommended defaults by mode:

| Mode | Role topology | Reviewer policy | Reviewer spawn | Manager policy |
| --- | --- | --- | --- | --- |
| discovery | lean_solo | none | none | none |
| prototype | standard | risk_triggered | after_handoff | none |
| safe_mvp | reviewed | risk_triggered | after_handoff | none |
| velocity | reviewed | risk_triggered | after_handoff | none |
| balanced | reviewed | risk_triggered | after_handoff | none |
| strict | reviewed | every_baton | standby_with_builder | none |
| release | enterprise | every_baton | standby_with_builder | user_feedback_only |
| recovery | reviewed | every_baton | after_handoff | none |
| maintenance | standard | risk_triggered | after_handoff | none |
| migration | reviewed | every_baton | standby_with_builder | none |
| design_sprint | reviewed | risk_triggered | standby_with_builder | none |

Upgrade to `managed` when the user will give frequent feedback while the Executive is running gates, reviewing, or coordinating builders. The Manager sends Executive Briefs; it does not direct workers.

## Package Types

Handoff Bundle:

- Produced by Builder.
- Sent to Executive/Ledger.
- Includes changed files, behavior, contracts, checks, skipped checks, risks, next recommendation.

Review Baton:

- Produced by Executive/Ledger.
- Sent to Reviewer.
- Includes Builder handoff, acceptance tier, risk, scope, and review questions.

Review Package:

- Produced by Reviewer.
- Sent to Executive/Ledger.
- Findings first, evidence, required fixes, optional follow-ups, recommendation.

Executive Brief:

- Produced by Manager/User Liaison.
- Sent only to Executive.
- Includes user feedback, urgency, affected decisions, suggested routing, and whether it can wait.

Decision Packet:

- Produced by Executive.
- Recorded in ledger.
- Includes accept, patch, reassign, change mode, cleanup, or release decision.

## Risk Escalation Matrix

Escalate at least one level of verification and review when the baton touches:

| Area | Minimum mode behavior |
| --- | --- |
| auth/security/secrets | strict review, focused security tests, full gate |
| payments/trading/billing | strict or release, explicit user confirmation for live effects |
| database migrations | migration mode, rollback plan, full gate |
| public API/contracts | strict review, compatibility checks, contract tests |
| infra/deployment | migration/release, smoke deploy or dry-run where safe |
| external live services | explicit effect policy, no hidden calls, integration tests or mocks |
| background jobs/queues/webhooks | strict review, idempotency and retry evidence |
| ML/evals/scoring/recommendation | strict review, eval coverage, drift notes |
| generated clients/types | generated-file policy, diff review, compatibility tests |

## Blocker Policies

Use blocker policies to keep factories moving when predictable friction appears.

`git_auth_policy`:

- `local_commit_continue`: commit locally, record push blocker, continue.
- `require_push`: block release acceptance until push succeeds.
- `ask`: ask user when present.
- `skip_push`: no push expected.

`dirty_worktree_policy`:

- `pause_reconcile`: stop new writes, identify ownership, and reconcile.
- `ignore_unrelated`: proceed only when dirty files are outside baton scope.
- `fail_on_collision`: enter Recovery mode if unknown changes overlap scope.

`generated_file_policy`:

- `guard_and_skip`: never stage configured generated files.
- `review_then_stage`: stage only after explicit diff review.
- `normal`: no special generated-file handling.

`test_flake_policy`:

- `rerun_once`: retry failing flaky tests once and record both results.
- `rerun_twice`: retry twice before classification.
- `isolate_then_classify`: run focused isolation before deciding.
- `strict_fail`: any failure blocks acceptance.

`long_test_policy`:

- `focused_then_checkpoint`: focused tests per baton, full gate at cadence.
- `full_each_baton`: full configured gate every baton.
- `release_only`: full gate only for release acceptance.

`dev_server_policy`:

- `reuse_or_start`: reuse existing server or start one when needed.
- `fixed_port`: use configured port only.
- `auto_cleanup`: stop servers the factory started after verification.
- `manual`: never start or stop servers automatically.

`worktree_policy`:

- `none`: use the current worktree only.
- `explicit_only`: create worktrees only after explicit Executive/user approval.
- `parallel_allowed`: allowed for isolated scopes with merge order and reconciliation gate.

`branch_policy`:

- `current_branch`: stay on current branch.
- `create_feature_branch`: create/switch to a configured feature branch.
- `pr_branch`: branch intended for pull request.
- `protected_guard`: never commit directly to protected branches.

`commit_policy`:

- `per_baton`: commit every accepted baton.
- `per_vertical_slice`: commit after a coherent product slice.
- `release_only`: commit during release/hardening only.
- `none`: no commits.

`push_policy`:

- `after_each_commit`: push after every accepted local commit.
- `batch`: push at checkpoints.
- `local_only`: do not push.
- `auth_if_available`: push when credentials work, otherwise record and continue.

`browser_tool_policy`:

- `in_app_first`: use the Codex in-app browser for local apps.
- `playwright_fallback`: use browser automation or screenshots when in-app tools are unavailable.
- `chrome_when_needed`: use Chrome only for authenticated/profile-dependent pages.
- `none`: no browser work expected.

`context_compaction_policy`:

- `handoff_summaries`: keep baton summaries strong enough to survive compaction.
- `promote_fresh_executive`: create a fresh Executive/Ledger when context becomes too noisy.
- `manual`: user/controller decides when to migrate.

`heartbeat_policy`:

- `none`: no monitors.
- `periodic`: wake on configured interval.
- `status_only`: monitor thread status only while another actor owns the write baton.
- `handoff_triggered`: wake controller when handoff/block/stale state appears.

Heartbeat prompts should be compact and status-oriented. They should not require full transcript reads on every wake. Prefer current baton, active owner, last accepted commit, monitor action, and one fallback directive. If a heartbeat cannot inspect enough state because of tool-call limits, it should report `inspection_insufficient` or ask the active Executive/Ledger for a compact status packet rather than touching the worktree.

When `active_actor_polling_policy` is `adaptive_backoff`, heartbeat prompts should explicitly tell controllers to avoid repeated short sleep/poll loops while a Builder is active and healthy. A healthy active Builder usually needs one bounded status read, then a 3-minute quiet block or a compact no-action status.

`artifact_policy`:

- `record_paths`: store artifact paths and screenshots in ledger.
- `attach_when_available`: attach artifacts through available app features.
- `summarize_only`: summarize artifacts without retaining them.

`user_interrupt_policy`:

- `manager_brief`: Manager packages non-urgent feedback into Executive Briefs.
- `executive_direct`: user feedback goes directly to Executive.
- `pause_on_conflict`: pause baton only when the new instruction conflicts.

`release_readiness_policy`:

- `not_until_release_mode`: defer full release review until Release mode.
- `risk_triggered`: run release-style checks for high-risk batons.
- `always_on`: maintain release readiness continuously.

## Acceptance Tier Rules

Prototype accepted:

- Works for demonstration or learning.
- Known gaps are explicit.
- No claim of production readiness.

Integration accepted:

- Wired into real app paths.
- Focused tests cover changed behavior.
- No known blocking regressions.
- Full gate may be deferred only if cadence allows and risk does not escalate.

Release accepted:

- Full gate and release gate pass.
- Browser/mobile QA where relevant.
- Security/env/deployment checks complete.
- Docs and operator notes reflect the shipped behavior.

## Retrospective Loop

Every few batons or after a failure, record:

- cycle time and slowest step;
- recurring flaky tests or tooling failures;
- over-verification or under-verification;
- whether baton size should change;
- whether full gate cadence should change;
- whether topology or monitor cadence should change.

Then update `docs/factory_config.md` before assigning the next baton.
