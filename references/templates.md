# Software Factory Templates

Adapt these templates to the project. Keep project-specific invariants in project docs, not in this skill.

## Contents

- [Factory Config](#factory-config)
- [Ledger Skeleton](#ledger-skeleton)
- [Builder Baton](#builder-baton)
- [Handoff Bundle](#handoff-bundle)
- [Factory Stop Directive](#factory-stop-directive)
- [Stop Packet](#stop-packet)
- [Resume Packet](#resume-packet)
- [Reviewer Prompt](#reviewer-prompt)
- [Review Baton](#review-baton)
- [Review Package](#review-package)
- [Permission Request / Prefix Approval](#permission-request--prefix-approval)
- [Blocker Handling Note](#blocker-handling-note)
- [Tool Inspection Failure Note](#tool-inspection-failure-note)
- [Executive Brief](#executive-brief)
- [Heartbeat Prompt](#heartbeat-prompt)
- [Cleanup Prompt](#cleanup-prompt)
- [Recovery Prompt](#recovery-prompt)

## Factory Config

~~~markdown
# Factory Configuration

Project:
Initialized:
Last updated:

## Operating Model

```text
work_mode:
factory_topology:
role_topology:
user_involvement:
feedback_handling:
principal_policy:
principal_authority:
principal_intervention_policy:
principal_digest_cadence:
principal_context_budget:
config_verbosity:
target_outcome:
goal_policy:
acceptance_tier:
baton_size:
concurrency_policy:
reviewer_policy:
reviewer_spawn_policy:
manager_policy:
executive_context_policy:
verification_level:
full_gate_cadence:
browser_qa_policy:
review_depth:
handoff_detail:
package_protocol:
thread_cleanup_policy:
cleanup_keep_recent:
factory_stop_policy:
default_stop_mode:
stop_scope:
stop_authority:
stop_monitor_policy:
stop_cleanup_policy:
resume_policy:
default_resume_mode:
stop_packet_required:
external_effect_policy:
model_policy:
role_model_policy:
model_switch_policy:
design_skill_policy:
permission_profile:
sandbox_mode:
approval_policy:
tool_call_budget_policy:
thread_read_policy:
active_actor_polling_policy:
active_builder_poll_interval:
long_check_poll_interval:
handoff_poll_interval:
stale_ping_after:
stale_reclaim_after:
allowed_command_prefixes:
restricted_command_prefixes:
destructive_action_policy:
external_network_policy:
credential_policy:
capability_preflight:
commit_policy:
branch_policy:
push_policy:
git_auth_policy:
dirty_worktree_policy:
generated_file_policy:
test_flake_policy:
long_test_policy:
dev_server_policy:
worktree_policy:
browser_tool_policy:
context_compaction_policy:
heartbeat_policy:
artifact_policy:
user_interrupt_policy:
release_readiness_policy:
```

## Effective Config Summary

Use this compact summary in batons and worker prompts. Keep exhaustive policy detail in this file unless the worker needs it.

```text
mode/topology:
target/tier:
principal:
feedback handling:
active roles:
model/reasoning by role:
permission profile:
tool-call/thread-read:
active polling:
allowed prefixes:
restricted prefixes:
verification cadence:
review routing:
cleanup:
stop/resume:
known blockers:
```

## Capability Preflight

```text
thread_tools_available:
thread_tool_schema_checked:
thread_read_policy_supported:
known_thread_tool_limits:
automation_tools_available:
goal_tools_available:
git_write_allowed:
git_push_auth_available:
network_available:
browser_available:
package_manager_available:
test_commands_detected:
env_files_present:
required_secrets_present:
generated_file_guards:
dev_server_status:
blocker_decision:
```

## Persistent Goal

```text
Drive the <PROJECT> software factory end to end: maintain the factory ledger, coordinate Builder and Reviewer batons, enforce the selected work mode and project invariants, preserve user changes, accept only work that satisfies the configured acceptance tier, keep required tests/evals passing according to the verification cadence, commit accepted work locally, push when authentication permits, and continue until the requested project outcome is complete and verified.
```

## Hard Invariants

- Preserve user changes; do not revert unknown work.
- Builders do not stage, commit, push, create worktrees, or change monitors unless delegated.
- One writer per worktree unless `parallel_worktrees` is explicitly configured.
- Record risk escalations and skipped checks.
- Builder handoffs route to Executive/Ledger; Executive/Ledger routes Review Batons.
- Principal Executive oversees mode, topology, cleanup, handoffs, and ledger promotion according to its authority; it does not normally hold the write baton.
- Manager/User Liaison sends briefs only to Principal or Executive by default.
- Cleanup runs only after ledger evidence captures the completed work.
- Stop directives preempt new baton assignment, preserve evidence, and produce a Stop Packet before monitors or cleanup are changed unless emergency stop requires immediate freeze.
- Permission/model settings are desired runtime configuration; if the runtime cannot apply them automatically, record the mismatch and use blocker policies.
- Destructive commands, credential prompts, live external effects, production writes, and protected-branch changes require the configured approval path.

## Project-Specific Invariants

- Fill in generated-file hazards.
- Fill in live external effect rules.
- Fill in deployment or data safety rules.

## Blocker Policy Summary

```text
git_auth:
dirty_worktree:
generated_files:
test_flakes:
long_tests:
dev_server:
worktree:
branch:
commit:
push:
browser_tool:
tool_call_limits:
context_compaction:
heartbeat:
artifact:
user_interrupt:
release_readiness:
```
~~~

## Ledger Skeleton

~~~markdown
# Build Ledger

## Current Factory State

```text
status:
work_mode:
role_topology:
user_involvement:
feedback_handling:
principal_policy:
principal_authority:
principal_intervention_policy:
config_verbosity:
target_outcome:
goal_policy:
acceptance_tier:
factory_topology:
active_writer:
active_reviewer_threads:
principal_thread:
manager_thread:
current_baton:
last_accepted_baton:
last_release_gate:
permission_profile:
approval_policy:
model_switch_policy:
tool_call_budget_policy:
thread_read_policy:
active_actor_polling_policy:
remote_status:
factory_stop_policy:
default_stop_mode:
stop_state:
last_stop_packet:
last_resume_packet:
```

## Active Threads

| Role | Thread | Status | Scope | Notes |
| --- | --- | --- | --- | --- |

## Thread Cleanup

```text
thread_cleanup_policy:
cleanup_keep_recent:
preserve_roles: executive, ledger, manager
last_cleanup:
```

## Stop And Resume

```text
factory_stop_policy:
default_stop_mode:
stop_scope:
stop_authority:
stop_monitor_policy:
stop_cleanup_policy:
resume_policy:
default_resume_mode:
stop_packet_required:
stop_state: running / stop_requested / draining / paused / frozen / hard_stopped / emergency_stopped / resuming
stop_requested_by:
stop_requested_at:
stop_reason:
resume_authority:
last_resume_mode:
```

## Capability Preflight

| Capability | Status | Evidence | Blocker policy |
| --- | --- | --- | --- |
| thread tools | unknown |  |  |
| thread tool schema | unknown |  |  |
| tool call limits | unknown |  |  |
| automations | unknown |  |  |
| goal tooling | unknown |  |  |
| git write | unknown |  |  |
| push auth | unknown |  |  |
| browser | unknown |  |  |
| package manager | unknown |  |  |
| tests | unknown |  |  |
| env/secrets | unknown |  |  |

## Baton Queue

| Baton | Tier | Owner | Status | Objective | Verification | Risk |
| --- | --- | --- | --- | --- | --- | --- |

## Acceptance Evidence

| Baton | Tier | Evidence | Skipped checks | Residual risk |
| --- | --- | --- | --- | --- |

## Retrospective

| Date | Observation | Adjustment |
| --- | --- | --- |

## Persistent Goal

```text
Record the executive/controller goal here when goal tooling is used.
```
~~~

## Builder Baton

```text
You are Builder B-XXX for <PROJECT>.

Project root:
<ABSOLUTE_PATH>

Factory config:
- work_mode: <MODE>
- role_topology: <TOPOLOGY>
- target_outcome: <OUTCOME>
- acceptance_tier: <prototype|integration|release>
- baton_size: <SIZE>
- verification_level: <LEVEL>
- full_gate_cadence: <CADENCE>
- model_policy: <MODEL/REASONING>
- permission_profile: <PROFILE>
- approval_policy: <POLICY>
- allowed_command_prefixes: <PREFIXES>
- restricted_command_prefixes: <PREFIXES>
- blocker_policy_summary: <SUMMARY>
- tool_call_budget_policy: <schema_first|bounded_reads|ledger_first|retry_smaller|manual>
- thread_read_policy: <latest_only|bounded_with_cursor|ledger_snapshot|targeted_outputs_only>
- active_actor_polling_policy: <adaptive_backoff|fixed_interval|event_triggered|aggressive_watch|manual>
- stop_policy: <DEFAULT_STOP_MODE/SCOPE/AUTHORITY>

Authorization:
You now own the single write baton for <WORKTREE_OR_BRANCH>. Do not stage, commit, push, create worktrees, change monitors, or broaden scope unless explicitly authorized.
Use the configured permission profile. If a command is blocked by permissions, auth, missing tools, long-running checks, or secrets, apply the blocker policy and report the exact fallback.
Use the configured tool-call policy. When inspecting threads or automations, use current tool schemas, bounded reads, narrow queries, and ledger/status packets first. If a tool call fails with invalid arguments or a window limit, retry once with fewer optional fields and a smaller window; do not loop on the same invalid shape.
Use the configured active-actor polling policy. If another actor is healthy and actively working, do not burn repeated short sleep/poll loops; wait the configured interval or ask for a compact status packet only when needed.
If Executive/Ledger sends a stop directive, stop according to that directive and report current state. Do not independently archive threads, pause monitors, or mark the factory complete.

Read first:
- AGENTS.md
- docs/factory_config.md
- docs/review_index.md
- docs/codex_factory_protocol.md
- docs/handoff_protocol.md
- docs/build_ledger.md
- <PROJECT_SPEC_DOCS>

Objective:
<OUTCOME>

Required behavior:
- <REQUIREMENT>

Write scope:
- <FILES_OR_AREAS>

Non-goals:
- <NON_GOALS>

Risk escalators:
- <ESCALATORS_OR_NONE>

Verification before handoff:
- <FOCUSED_CHECKS>
- <BUILD_OR_TYPECHECK>
- <FULL_GATE_IF_REQUIRED_BY_CONFIG>
- <BROWSER_QA_IF_UI>
- git diff --check
- git diff --cached --check
- generated-file guards

Handoff:
Send the Handoff Bundle to Executive/Ledger. Use the configured handoff detail level. Include changed files, behavior, contracts, tests with pass/fail counts, skipped checks, risks, and next recommendation.
```

## Handoff Bundle

~~~markdown
# Handoff: B-XXX / <slice>

## State
- Branch/worktree:
- Base commit:
- Worktree status:
- Baton owner:
- Acceptance tier targeted:

## Work Completed
- Files changed:
- Behavior implemented:
- Contracts/data/API changed:
- Decisions made:

## Verification
- Commands run:
- Passing:
- Failing:
- Skipped and why:
- Browser/visual QA:

## Risk and Acceptance
- Risk escalators touched:
- Acceptance tier support:
- Hard invariants preserved:
- Residual risk:

## Next Recommendation
- Accept / patch / reassign:
- Next baton:
- Do not touch:
~~~

## Factory Stop Directive

```text
Factory stop directive for <PROJECT>.

Mode:
<pause_new_work|drain_to_handoff|drain_to_checkpoint|release_freeze|hard_stop|emergency_stop>

Scope:
<new_work_only|active_baton|all_factory|monitors_only|cleanup_only>

Authority:
<requester and configured authority>

Reason:
<why stopping now>

Instructions:
- Stop assigning new batons immediately.
- If you own active work, finish only the current safe command if interrupting it would corrupt state.
- Do not stage, commit, push, archive threads, or change monitors unless this directive explicitly authorizes it.
- Report current baton, worktree status, dirty files, running/last commands, verification state, risks, and exact resume point.
```

## Stop Packet

~~~markdown
# Stop Packet: <PROJECT> / <timestamp>

## Stop Request
- Mode:
- Scope:
- Reason:
- Requested by:
- Authority:
- Stop state:

## Active Factory State
- Executive/Ledger:
- Principal:
- Manager:
- Active Builder:
- Active Reviewer:
- Current baton:
- Baton status:

## Worktree And Git
- Branch/worktree:
- Latest accepted commit:
- Push/remote status:
- Dirty files:
- Staged files:
- Untracked files:
- Ownership notes:

## Verification And Commands
- Running command or last completed command:
- Tests/checks completed:
- Tests/checks unfinished:
- Browser/dev server state:

## Monitors And Cleanup
- Monitors kept:
- Monitors paused/deleted/retargeted:
- Threads archived:
- Threads preserved:

## Risks
- Unresolved risks:
- User attention needed:

## Resume Instructions
- Resume policy:
- Resume authority:
- Next recommended action:
- Verification to rerun:
- Cleanup still pending:
~~~

## Resume Packet

```text
Factory resume directive for <PROJECT>.

Resume authority:
<requester and configured authority>

Prior Stop Packet:
<packet id/path/thread/checkpoint>

Requested resume mode:
<restore_monitors_only|continue_same_baton|replace_actor|advance_to_review|assign_next_baton|recovery_first>

Instructions:
- Treat this as resume authority only if it comes from the configured user, Principal, Executive, or controller.
- Read the Stop Packet, ledger stop state, current git/worktree state, active threads, monitor state, cleanup state, and goal state before waking workers.
- If ownership, dirty state, or evidence is ambiguous, switch to `recovery_first`.
- Issue fresh baton/review authority after the resume checkpoint; do not rely on pre-stop or revoked authorization.
- Restore monitors according to the Resume Packet and return the controller to monitor-only behavior once a worker owns the baton.
```

~~~markdown
# Resume Packet: <PROJECT> / <timestamp>

## Resume Authority
- Requested by:
- Approved by:
- Resume policy:
- Resume mode:
- Prior Stop Packet:
- Stop checkpoint:
- Latest accepted commit:

## Read-Only Preflight
- Branch/worktree:
- Current commit:
- Push/remote status:
- Dirty files:
- Staged files:
- Untracked files:
- Active Executive/Ledger:
- Active Builder:
- Active Reviewer:
- Monitors:
- Goal state:
- Cleanup state:

## Resume Decision
- Route: restore_monitors_only / continue_same_baton / replace_actor / advance_to_review / assign_next_baton / recovery_first
- Actor to reauthorize:
- Actor to replace:
- Review route:
- Recovery required:
- Reason:

## Fresh Authority To Issue
- Next baton or review baton:
- Current commit for baton:
- Write owner:
- Review owner:
- Scope:
- Non-goals:
- Verification:
- Handoff requirements:

## Monitors, Goals, And Cleanup
- Monitors to restart:
- Monitors to keep paused/delete/retarget:
- Goal action or limitation:
- Cleanup to defer or run:

## Risks And Guards
- Risks to re-check:
- Stale wakeup guard:
- Generated/protected files:
- User attention needed:
~~~

## Reviewer Prompt

```text
You are Reviewer R-XXX for <PROJECT>.

Mode:
Read-only. Do not edit, stage, commit, push, create worktrees, or change monitors.

Review scope:
<security|architecture|test coverage|UI/UX|performance|release|migration>

Target:
<commit, diff, handoff, screenshots, or files>

Factory context:
- work_mode: <MODE>
- target_outcome: <OUTCOME>
- acceptance_tier: <TIER>
- hard invariants: <LIST>
- model/reasoning: <MODEL/REASONING>
- permission profile: <READ_ONLY_POLICY>

Output:
- Findings first, ordered by severity.
- File/line or evidence for each finding.
- Required fixes before the target acceptance tier.
- Optional follow-ups.
```

## Review Baton

```text
You are Reviewer R-XXX for <PROJECT>.

Mode:
Read-only unless Executive explicitly authorizes a patch. Do not stage, commit, push, create worktrees, change monitors, or message the Builder directly.

Review target:
<BUILDER_HANDOFF_OR_DIFF>

Factory context:
- work_mode: <MODE>
- role_topology: <TOPOLOGY>
- target_outcome: <OUTCOME>
- acceptance_tier: <TIER>
- risk escalators: <LIST>
- hard invariants: <LIST>
- model/reasoning: <MODEL/REASONING>
- permission profile: read-only unless explicitly authorized
- blocker policies: <REVIEW_RELEVANT_POLICIES>

Review scope:
- Confirm changed files match the baton.
- Check behavior against acceptance criteria.
- Check tests and skipped checks against the acceptance tier.
- Identify bugs, regressions, hidden mutations, security issues, data risks, UX breaks, or missing evidence.

Output a Review Package:
- Findings first, ordered by severity.
- Required fixes before acceptance.
- Evidence supporting pass/fail.
- Suggested Executive decision: accept, patch, reassign, or change mode.
```

## Review Package

~~~markdown
# Review Package: B-XXX / <slice>

## Recommendation
- Accept / patch / reassign / change mode:
- Acceptance tier supported:

## Findings
- P0/P1/P2 findings with file/line or concrete evidence.

## Evidence Checked
- Diff/files:
- Tests/build/browser:
- Invariants:
- Skipped checks:

## Residual Risk
- Risks:
- Follow-ups:

## Executive Decision Needed
- Decision:
- Suggested next baton:
~~~

## Permission Request / Prefix Approval

```text
The factory is blocked by a runtime permission request.

Role:
Thread:
Command/prefix:
Why it is needed:
Configured permission profile:
Configured approval policy:
Risk level:
Fallback if denied:
Suggested reusable prefix approval:
```

## Blocker Handling Note

```text
Blocker:
Policy:
Affected baton:
Fallback taken:
Evidence:
Residual risk:
Next action:
```

## Tool Inspection Failure Note

```text
Tool inspection failure:
<schema_invalid|window_too_large|outputs_too_large|thread_context_stale|inspection_insufficient>

Tool:
<thread/list/automation/browser/etc>

Call shape that failed:
<redacted/minimal description>

Fallback:
<removed optional fields|reduced limit|narrowed query|cursor read|ledger snapshot|status ping>

Factory impact:
<none|monitor delayed|controller asked for status|recovery required>

Config update needed:
<tool_call_budget_policy/thread_read_policy/monitor prompt/handoff template>
```

## Executive Brief

~~~markdown
# Executive Brief: <topic>

## User Feedback
- What the user said:
- Urgency:
- Affected product/factory decision:

## Context
- Relevant active baton/thread:
- Current factory state:
- Evidence checked:

## Recommended Executive Action
- Continue / pause / change mode / update baton / ask user / no action:
- Suggested message or ledger update:

## Routing Rules
- Manager/User Liaison should send this only to Executive unless explicitly authorized otherwise.
~~~

## Heartbeat Prompt

```text
You are the factory monitor for <PROJECT>.

Current controller:
<THREAD_ID_OR_NAME>

Active baton:
<B-XXX>

Active writer:
<THREAD_ID_OR_NONE>

Factory config:
<CONFIG_SUMMARY>

Tool-call policy:
<tool_call_budget_policy / thread_read_policy>

Active polling policy:
<active_actor_polling_policy; active_builder_poll_interval; long_check_poll_interval; handoff_poll_interval; stale_ping_after; stale_reclaim_after>

Stop state:
<running|stop_requested|draining|paused|frozen|hard_stopped|emergency_stopped|resuming>

Persistent goal:
<GOAL_TEXT_OR_NONE>

Rules:
- Do not edit files.
- Use bounded thread/list reads and schema-shaped tool calls. Do not assume unsupported optional arguments or oversized limits.
- Prefer ledger snapshots, commits, handoff bundles, stop/resume packets, and compact status packets over reading entire thread transcripts.
- Include command/tool outputs only for a specific evidence gap, with small caps.
- If a thread/list read fails with invalid arguments or window limits, retry once with fewer fields, lower limits, narrower query, or cursor continuation.
- If inspection is still insufficient, ask the active Executive/Ledger for one compact status packet; do not touch the worktree because inspection failed.
- If stop_state is paused, frozen, hard_stopped, or emergency_stopped, do not wake Builders or assign work; report whether resume conditions are satisfied.
- If a Builder owns the write baton, inspect only thread status unless it handed off, blocked, relinquished, or went stale.
- If the Builder is healthy and actively editing/thinking, use the configured active Builder polling interval, usually about 3 minutes, instead of repeated short sleep/read loops.
- If the Builder is running a known long command, such as full check, Playwright, release gate, build, migration, or install, use the long-check interval, usually about 5 minutes, unless output indicates imminent completion or failure.
- If final verification is likely near handoff, use the handoff interval, usually about 60 seconds.
- If handoff is present, wake the controller to take review lock.
- If review is configured, wake the controller to route a Review Baton rather than reviewing inside the monitor.
- If no meaningful progress passes the stale-ping threshold, ping once with a concrete status request before reclaim.
- If collision or dirty-state confusion appears, switch to Recovery mode.
```

## Cleanup Prompt

```text
Run factory thread cleanup for <PROJECT>.

Policy:
<thread_cleanup_policy>

Rules:
- Do not archive Executive, Ledger, Manager, active Builder, active Reviewer, pinned, blocked, unresolved-risk, unreviewed, or uncommitted-handoff threads.
- Do not archive threads while stop_state is stop_requested, draining, hard_stopped, or emergency_stopped unless the Stop Packet explicitly authorizes cleanup.
- Archive completed Builder/Reviewer threads only after their evidence is captured in docs/build_ledger.md.
- Preserve the most recent <N> completed worker threads for audit if using rolling_window.
- Report archived threads and preserved threads.
```

## Recovery Prompt

```text
Switch to Recovery mode for <PROJECT>.

Reason:
<collision|stale builder|failed gate|dirty state|spec drift|unexpected thread/worktree>

Actions:
1. Freeze new batons.
2. Identify active writers and ownership.
3. Inspect git status only when no Builder owns the worktree or after reclaim.
4. List changed files, staged files, untracked files, running servers, and active threads.
5. Decide keep, patch, reassign, or discard only with explicit evidence.
6. Record recovery notes in the ledger.
7. Resume with one writer and an updated factory config.
```
