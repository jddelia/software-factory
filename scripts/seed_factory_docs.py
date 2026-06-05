#!/usr/bin/env python3
"""Seed generic Software Factory docs in a target project.

The script is conservative: it creates missing files and skips existing files
unless --force is passed. It intentionally avoids project-specific assumptions.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path


WORK_MODES = (
    "discovery",
    "prototype",
    "safe_mvp",
    "velocity",
    "balanced",
    "strict",
    "release",
    "recovery",
    "maintenance",
    "migration",
    "design_sprint",
)

TOPOLOGIES = ("executive_as_ledger", "separate_ledger", "passive_fallback")
ROLE_TOPOLOGIES = ("lean_solo", "standard", "reviewed", "managed", "enterprise")
USER_INVOLVEMENT = ("principal_partner", "direct_executive", "hands_off")
FEEDBACK_HANDLING = ("no_manager", "feedback_manager", "always_on_manager")
PRINCIPAL_POLICIES = ("none", "same_as_executive", "dedicated", "user_thread")
PRINCIPAL_AUTHORITIES = ("observe", "steer", "configure", "emergency_override")
PRINCIPAL_INTERVENTION_POLICIES = (
    "no_baton_interference",
    "can_pause",
    "can_reassign",
    "can_supersede_ledger",
)
PRINCIPAL_DIGEST_CADENCE = ("manual", "checkpoint", "heartbeat", "daily")
PRINCIPAL_CONTEXT_BUDGET = ("compact", "standard", "full")
ACCEPTANCE_TIERS = ("prototype", "integration", "release")
BATON_SIZES = ("micro", "small", "medium", "vertical_slice")
CONCURRENCY = ("single_writer", "parallel_read_only_reviewers", "parallel_worktrees")
VERIFICATION = ("smoke", "focused", "focused_plus_build", "full_gate", "release_gate")
FULL_GATE_CADENCE = ("every_baton", "every_n_batons", "risk_triggered", "release_only")
BROWSER_QA = ("none", "smoke", "screenshots", "full", "release")
REVIEW_DEPTH = ("skim", "targeted", "full", "adversarial")
REVIEWER_POLICIES = ("none", "risk_triggered", "every_baton", "release_only")
REVIEWER_SPAWN_POLICIES = (
    "none",
    "after_handoff",
    "standby_with_builder",
    "parallel_read_only",
    "risk_triggered",
    "release_only",
)
MANAGER_POLICIES = ("none", "user_feedback_only", "always_on")
EXECUTIVE_CONTEXT_POLICIES = (
    "direct_user_chat",
    "manager_packaged_feedback",
    "mixed",
)
HANDOFF_DETAIL = ("compact", "standard", "exhaustive")
PACKAGE_PROTOCOLS = ("compact", "standard", "exhaustive")
THREAD_CLEANUP_POLICIES = (
    "none",
    "manual",
    "after_acceptance",
    "rolling_window",
    "aggressive",
    "release_archive",
)
FACTORY_STOP_POLICIES = ("enabled", "manual_only", "disabled")
STOP_MODES = (
    "pause_new_work",
    "drain_to_handoff",
    "drain_to_checkpoint",
    "release_freeze",
    "hard_stop",
    "emergency_stop",
)
STOP_SCOPES = (
    "new_work_only",
    "active_baton",
    "all_factory",
    "monitors_only",
    "cleanup_only",
)
STOP_AUTHORITIES = (
    "user_only",
    "principal_or_user",
    "executive_or_above",
    "any_active_role_with_confirmation",
)
STOP_MONITOR_POLICIES = (
    "keep_active",
    "pause_after_stop",
    "delete_after_stop",
    "retarget_to_principal",
)
STOP_CLEANUP_POLICIES = (
    "none",
    "manual",
    "after_checkpoint",
    "rolling_window_after_checkpoint",
    "release_archive",
)
RESUME_POLICIES = (
    "manual",
    "resume_from_stop_packet",
    "resume_requires_user",
    "auto_resume_after_window",
)
EXTERNAL_EFFECTS = (
    "mock_only",
    "explicit_operator",
    "staging_allowed",
    "production_requires_confirmation",
)
GOAL_POLICIES = ("none", "ask", "create_if_long_running", "explicit_only")
DEFAULT_RESUME_MODES = (
    "restore_monitors_only",
    "continue_same_baton",
    "replace_actor",
    "advance_to_review",
    "assign_next_baton",
    "recovery_first",
)
TOOL_CALL_BUDGET_POLICIES = (
    "schema_first",
    "bounded_reads",
    "ledger_first",
    "retry_smaller",
    "manual",
)
THREAD_READ_POLICIES = (
    "latest_only",
    "bounded_with_cursor",
    "ledger_snapshot",
    "targeted_outputs_only",
)
ACTIVE_ACTOR_POLLING_POLICIES = (
    "adaptive_backoff",
    "fixed_interval",
    "event_triggered",
    "aggressive_watch",
    "manual",
)
CONFIG_VERBOSITY = ("compact", "standard", "exhaustive")
PERMISSION_PROFILES = ("read_only", "workspace_write", "full_access", "custom")
SANDBOX_MODES = ("read_only", "workspace_write", "full_access")
APPROVAL_POLICIES = ("always", "on_request", "on_failure", "never")
DESTRUCTIVE_ACTION_POLICIES = ("forbid", "confirm", "allow_scoped")
EXTERNAL_NETWORK_POLICIES = ("disabled", "docs_only", "allowed", "explicit_only")
CREDENTIAL_POLICIES = ("never_prompt", "use_existing_only", "prompt_if_present")
MODEL_SWITCH_POLICIES = ("never", "by_role", "by_risk", "by_cost")
CAPABILITY_PREFLIGHTS = ("minimal", "standard", "full")
REASONING_LEVELS = ("low", "medium", "high", "xhigh")
GIT_AUTH_POLICIES = ("local_commit_continue", "require_push", "ask", "skip_push")
DIRTY_WORKTREE_POLICIES = (
    "pause_reconcile",
    "ignore_unrelated",
    "fail_on_collision",
)
GENERATED_FILE_POLICIES = ("guard_and_skip", "review_then_stage", "normal")
TEST_FLAKE_POLICIES = (
    "rerun_once",
    "rerun_twice",
    "isolate_then_classify",
    "strict_fail",
)
LONG_TEST_POLICIES = ("focused_then_checkpoint", "full_each_baton", "release_only")
DEV_SERVER_POLICIES = ("reuse_or_start", "fixed_port", "auto_cleanup", "manual")
WORKTREE_POLICIES = ("none", "explicit_only", "parallel_allowed")
BRANCH_POLICIES = (
    "current_branch",
    "create_feature_branch",
    "pr_branch",
    "protected_guard",
)
COMMIT_POLICIES = ("per_baton", "per_vertical_slice", "release_only", "none")
PUSH_POLICIES = ("after_each_commit", "batch", "local_only", "auth_if_available")
BROWSER_TOOL_POLICIES = (
    "in_app_first",
    "playwright_fallback",
    "chrome_when_needed",
    "none",
)
CONTEXT_COMPACTION_POLICIES = (
    "handoff_summaries",
    "promote_fresh_executive",
    "manual",
)
HEARTBEAT_POLICIES = ("none", "periodic", "status_only", "handoff_triggered")
ARTIFACT_POLICIES = ("record_paths", "attach_when_available", "summarize_only")
USER_INTERRUPT_POLICIES = ("manager_brief", "executive_direct", "pause_on_conflict")
RELEASE_READINESS_POLICIES = (
    "not_until_release_mode",
    "risk_triggered",
    "always_on",
)

INVOLVEMENT_DEFAULTS = {
    "principal_partner": {
        "principal_policy": "user_thread",
        "principal_authority": "configure",
        "principal_intervention_policy": "can_supersede_ledger",
        "principal_digest_cadence": "checkpoint",
        "principal_context_budget": "standard",
        "executive_context_policy": "mixed",
    },
    "direct_executive": {
        "principal_policy": "same_as_executive",
        "principal_authority": "steer",
        "principal_intervention_policy": "can_pause",
        "principal_digest_cadence": "manual",
        "principal_context_budget": "compact",
        "executive_context_policy": "direct_user_chat",
    },
    "hands_off": {
        "principal_policy": "none",
        "principal_authority": "observe",
        "principal_intervention_policy": "no_baton_interference",
        "principal_digest_cadence": "checkpoint",
        "principal_context_budget": "compact",
        "executive_context_policy": "direct_user_chat",
    },
}

BASE_FRICTION_DEFAULTS = {
    "config_verbosity": "standard",
    "permission_profile": "full_access",
    "sandbox_mode": "full_access",
    "approval_policy": "on_failure",
    "allowed_command_prefixes": (
        "git status; git diff; git add/git commit/git push when commit or "
        "push policy delegates it; project test/build commands detected by "
        "preflight"
    ),
    "restricted_command_prefixes": (
        "rm -rf; git reset --hard; git checkout --; production deploy; "
        "destructive database commands; credential prompts"
    ),
    "destructive_action_policy": "confirm",
    "external_network_policy": "allowed",
    "credential_policy": "use_existing_only",
    "model_switch_policy": "by_role",
    "capability_preflight": "standard",
    "git_auth_policy": "local_commit_continue",
    "dirty_worktree_policy": "pause_reconcile",
    "generated_file_policy": "guard_and_skip",
    "test_flake_policy": "rerun_once",
    "long_test_policy": "focused_then_checkpoint",
    "dev_server_policy": "reuse_or_start",
    "worktree_policy": "explicit_only",
    "branch_policy": "current_branch",
    "commit_policy": "per_baton",
    "push_policy": "auth_if_available",
    "browser_tool_policy": "in_app_first",
    "context_compaction_policy": "handoff_summaries",
    "heartbeat_policy": "handoff_triggered",
    "artifact_policy": "record_paths",
    "user_interrupt_policy": "executive_direct",
    "release_readiness_policy": "risk_triggered",
    "factory_stop_policy": "enabled",
    "default_stop_mode": "drain_to_checkpoint",
    "stop_scope": "all_factory",
    "stop_authority": "principal_or_user",
    "stop_monitor_policy": "pause_after_stop",
    "stop_cleanup_policy": "rolling_window_after_checkpoint",
    "resume_policy": "resume_from_stop_packet",
    "default_resume_mode": "continue_same_baton",
    "tool_call_budget_policy": "bounded_reads",
    "thread_read_policy": "latest_only",
    "active_actor_polling_policy": "adaptive_backoff",
    "active_builder_poll_interval": "3m",
    "long_check_poll_interval": "5m",
    "handoff_poll_interval": "60s",
    "stale_ping_after": "10m_without_meaningful_progress",
    "stale_reclaim_after": "20m_to_30m_policy_dependent",
}

MODE_FRICTION_OVERRIDES = {
    "discovery": {
        "config_verbosity": "compact",
        "permission_profile": "read_only",
        "sandbox_mode": "read_only",
        "approval_policy": "on_request",
        "external_network_policy": "docs_only",
        "allowed_command_prefixes": "git status; git diff; rg; ls; sed",
        "restricted_command_prefixes": (
            "git add; git commit; git push; file writes; rm -rf; "
            "git reset --hard; git checkout --; production deploy; "
            "destructive database commands; credential prompts"
        ),
        "model_switch_policy": "by_cost",
        "capability_preflight": "minimal",
        "commit_policy": "none",
        "push_policy": "local_only",
        "long_test_policy": "release_only",
        "browser_tool_policy": "none",
        "heartbeat_policy": "none",
        "default_stop_mode": "pause_new_work",
        "stop_cleanup_policy": "manual",
    },
    "prototype": {
        "config_verbosity": "compact",
        "permission_profile": "workspace_write",
        "sandbox_mode": "workspace_write",
        "commit_policy": "per_vertical_slice",
        "browser_tool_policy": "in_app_first",
        "release_readiness_policy": "not_until_release_mode",
    },
    "safe_mvp": {
        "config_verbosity": "compact",
        "commit_policy": "per_vertical_slice",
        "release_readiness_policy": "risk_triggered",
    },
    "velocity": {
        "config_verbosity": "compact",
        "commit_policy": "per_baton",
    },
    "strict": {
        "capability_preflight": "full",
        "model_switch_policy": "by_risk",
        "long_test_policy": "full_each_baton",
        "test_flake_policy": "isolate_then_classify",
        "release_readiness_policy": "risk_triggered",
    },
    "release": {
        "config_verbosity": "exhaustive",
        "capability_preflight": "full",
        "git_auth_policy": "require_push",
        "model_switch_policy": "by_risk",
        "long_test_policy": "full_each_baton",
        "test_flake_policy": "strict_fail",
        "push_policy": "after_each_commit",
        "release_readiness_policy": "always_on",
        "default_stop_mode": "release_freeze",
        "stop_cleanup_policy": "release_archive",
        "resume_policy": "resume_requires_user",
    },
    "recovery": {
        "config_verbosity": "exhaustive",
        "permission_profile": "workspace_write",
        "sandbox_mode": "workspace_write",
        "approval_policy": "on_request",
        "capability_preflight": "full",
        "model_switch_policy": "by_risk",
        "push_policy": "auth_if_available",
        "browser_tool_policy": "in_app_first",
        "user_interrupt_policy": "pause_on_conflict",
        "default_stop_mode": "hard_stop",
        "stop_cleanup_policy": "manual",
        "resume_policy": "resume_requires_user",
        "default_resume_mode": "recovery_first",
    },
    "maintenance": {
        "config_verbosity": "compact",
        "permission_profile": "workspace_write",
        "sandbox_mode": "workspace_write",
    },
    "migration": {
        "capability_preflight": "full",
        "model_switch_policy": "by_risk",
        "long_test_policy": "full_each_baton",
        "worktree_policy": "explicit_only",
        "release_readiness_policy": "risk_triggered",
    },
    "design_sprint": {
        "browser_tool_policy": "in_app_first",
        "artifact_policy": "attach_when_available",
    },
}


MODE_DEFAULTS = {
    "discovery": {
        "role_topology": "lean_solo",
        "acceptance_tier": "prototype",
        "baton_size": "micro",
        "reviewer_policy": "none",
        "reviewer_spawn_policy": "none",
        "manager_policy": "none",
        "executive_context_policy": "direct_user_chat",
        "verification_level": "smoke",
        "full_gate_cadence": "release_only",
        "browser_qa_policy": "none",
        "review_depth": "skim",
        "handoff_detail": "compact",
        "package_protocol": "compact",
        "thread_cleanup_policy": "manual",
    },
    "prototype": {
        "role_topology": "standard",
        "acceptance_tier": "prototype",
        "baton_size": "vertical_slice",
        "reviewer_policy": "risk_triggered",
        "reviewer_spawn_policy": "after_handoff",
        "manager_policy": "none",
        "executive_context_policy": "direct_user_chat",
        "verification_level": "focused",
        "full_gate_cadence": "release_only",
        "browser_qa_policy": "smoke",
        "review_depth": "targeted",
        "handoff_detail": "compact",
        "package_protocol": "compact",
        "thread_cleanup_policy": "rolling_window",
    },
    "safe_mvp": {
        "role_topology": "reviewed",
        "acceptance_tier": "integration",
        "baton_size": "vertical_slice",
        "reviewer_policy": "risk_triggered",
        "reviewer_spawn_policy": "after_handoff",
        "manager_policy": "none",
        "executive_context_policy": "direct_user_chat",
        "verification_level": "focused",
        "full_gate_cadence": "risk_triggered",
        "browser_qa_policy": "smoke",
        "review_depth": "targeted",
        "handoff_detail": "compact",
        "package_protocol": "compact",
        "thread_cleanup_policy": "rolling_window",
    },
    "velocity": {
        "role_topology": "reviewed",
        "acceptance_tier": "integration",
        "baton_size": "vertical_slice",
        "reviewer_policy": "risk_triggered",
        "reviewer_spawn_policy": "after_handoff",
        "manager_policy": "none",
        "executive_context_policy": "direct_user_chat",
        "verification_level": "focused_plus_build",
        "full_gate_cadence": "every_n_batons",
        "browser_qa_policy": "screenshots",
        "review_depth": "targeted",
        "handoff_detail": "compact",
        "package_protocol": "compact",
        "thread_cleanup_policy": "rolling_window",
    },
    "balanced": {
        "role_topology": "reviewed",
        "acceptance_tier": "integration",
        "baton_size": "medium",
        "reviewer_policy": "risk_triggered",
        "reviewer_spawn_policy": "after_handoff",
        "manager_policy": "none",
        "executive_context_policy": "mixed",
        "verification_level": "focused_plus_build",
        "full_gate_cadence": "risk_triggered",
        "browser_qa_policy": "screenshots",
        "review_depth": "targeted",
        "handoff_detail": "standard",
        "package_protocol": "standard",
        "thread_cleanup_policy": "rolling_window",
    },
    "strict": {
        "role_topology": "reviewed",
        "acceptance_tier": "integration",
        "baton_size": "small",
        "reviewer_policy": "every_baton",
        "reviewer_spawn_policy": "standby_with_builder",
        "manager_policy": "none",
        "executive_context_policy": "mixed",
        "verification_level": "full_gate",
        "full_gate_cadence": "every_baton",
        "browser_qa_policy": "full",
        "review_depth": "full",
        "handoff_detail": "standard",
        "package_protocol": "standard",
        "thread_cleanup_policy": "after_acceptance",
    },
    "release": {
        "role_topology": "enterprise",
        "acceptance_tier": "release",
        "baton_size": "small",
        "reviewer_policy": "every_baton",
        "reviewer_spawn_policy": "standby_with_builder",
        "manager_policy": "user_feedback_only",
        "executive_context_policy": "manager_packaged_feedback",
        "verification_level": "release_gate",
        "full_gate_cadence": "every_baton",
        "browser_qa_policy": "release",
        "review_depth": "adversarial",
        "handoff_detail": "exhaustive",
        "package_protocol": "exhaustive",
        "thread_cleanup_policy": "release_archive",
    },
    "recovery": {
        "role_topology": "reviewed",
        "acceptance_tier": "integration",
        "baton_size": "micro",
        "reviewer_policy": "every_baton",
        "reviewer_spawn_policy": "after_handoff",
        "manager_policy": "none",
        "executive_context_policy": "direct_user_chat",
        "verification_level": "focused",
        "full_gate_cadence": "risk_triggered",
        "browser_qa_policy": "smoke",
        "review_depth": "full",
        "handoff_detail": "exhaustive",
        "package_protocol": "exhaustive",
        "thread_cleanup_policy": "manual",
    },
    "maintenance": {
        "role_topology": "standard",
        "acceptance_tier": "integration",
        "baton_size": "small",
        "reviewer_policy": "risk_triggered",
        "reviewer_spawn_policy": "after_handoff",
        "manager_policy": "none",
        "executive_context_policy": "direct_user_chat",
        "verification_level": "focused",
        "full_gate_cadence": "risk_triggered",
        "browser_qa_policy": "smoke",
        "review_depth": "targeted",
        "handoff_detail": "compact",
        "package_protocol": "compact",
        "thread_cleanup_policy": "rolling_window",
    },
    "migration": {
        "role_topology": "reviewed",
        "acceptance_tier": "integration",
        "baton_size": "small",
        "reviewer_policy": "every_baton",
        "reviewer_spawn_policy": "standby_with_builder",
        "manager_policy": "none",
        "executive_context_policy": "mixed",
        "verification_level": "full_gate",
        "full_gate_cadence": "every_baton",
        "browser_qa_policy": "smoke",
        "review_depth": "full",
        "handoff_detail": "standard",
        "package_protocol": "standard",
        "thread_cleanup_policy": "after_acceptance",
    },
    "design_sprint": {
        "role_topology": "reviewed",
        "acceptance_tier": "integration",
        "baton_size": "medium",
        "reviewer_policy": "risk_triggered",
        "reviewer_spawn_policy": "standby_with_builder",
        "manager_policy": "none",
        "executive_context_policy": "mixed",
        "verification_level": "focused_plus_build",
        "full_gate_cadence": "risk_triggered",
        "browser_qa_policy": "screenshots",
        "review_depth": "targeted",
        "handoff_detail": "compact",
        "package_protocol": "compact",
        "thread_cleanup_policy": "rolling_window",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed missing Software Factory docs in a project."
    )
    parser.add_argument("project_root", help="Target project root")
    parser.add_argument("--project-name", help="Human-readable project name")
    parser.add_argument("--work-mode", choices=WORK_MODES, default="balanced")
    parser.add_argument(
        "--factory-topology", choices=TOPOLOGIES, default="executive_as_ledger"
    )
    parser.add_argument("--role-topology", choices=ROLE_TOPOLOGIES)
    parser.add_argument(
        "--user-involvement",
        choices=USER_INVOLVEMENT,
        default="principal_partner",
        help="How the user wants to stay involved in the factory.",
    )
    parser.add_argument(
        "--feedback-handling",
        choices=FEEDBACK_HANDLING,
        default="no_manager",
        help="How side feedback should be packaged while work continues.",
    )
    parser.add_argument("--principal-policy", choices=PRINCIPAL_POLICIES)
    parser.add_argument("--principal-authority", choices=PRINCIPAL_AUTHORITIES)
    parser.add_argument(
        "--principal-intervention-policy", choices=PRINCIPAL_INTERVENTION_POLICIES
    )
    parser.add_argument(
        "--principal-digest-cadence", choices=PRINCIPAL_DIGEST_CADENCE
    )
    parser.add_argument(
        "--principal-context-budget", choices=PRINCIPAL_CONTEXT_BUDGET
    )
    parser.add_argument("--acceptance-tier", choices=ACCEPTANCE_TIERS)
    parser.add_argument("--baton-size", choices=BATON_SIZES)
    parser.add_argument(
        "--concurrency-policy", choices=CONCURRENCY, default="single_writer"
    )
    parser.add_argument("--reviewer-policy", choices=REVIEWER_POLICIES)
    parser.add_argument("--reviewer-spawn-policy", choices=REVIEWER_SPAWN_POLICIES)
    parser.add_argument("--manager-policy", choices=MANAGER_POLICIES)
    parser.add_argument(
        "--executive-context-policy", choices=EXECUTIVE_CONTEXT_POLICIES
    )
    parser.add_argument("--verification-level", choices=VERIFICATION)
    parser.add_argument("--full-gate-cadence", choices=FULL_GATE_CADENCE)
    parser.add_argument("--browser-qa-policy", choices=BROWSER_QA)
    parser.add_argument("--review-depth", choices=REVIEW_DEPTH)
    parser.add_argument("--handoff-detail", choices=HANDOFF_DETAIL)
    parser.add_argument("--package-protocol", choices=PACKAGE_PROTOCOLS)
    parser.add_argument("--thread-cleanup-policy", choices=THREAD_CLEANUP_POLICIES)
    parser.add_argument(
        "--cleanup-keep-recent",
        type=int,
        default=3,
        help="Completed worker threads to preserve when using rolling cleanup.",
    )
    parser.add_argument("--factory-stop-policy", choices=FACTORY_STOP_POLICIES)
    parser.add_argument("--default-stop-mode", choices=STOP_MODES)
    parser.add_argument("--stop-scope", choices=STOP_SCOPES)
    parser.add_argument("--stop-authority", choices=STOP_AUTHORITIES)
    parser.add_argument("--stop-monitor-policy", choices=STOP_MONITOR_POLICIES)
    parser.add_argument("--stop-cleanup-policy", choices=STOP_CLEANUP_POLICIES)
    parser.add_argument("--resume-policy", choices=RESUME_POLICIES)
    parser.add_argument("--default-resume-mode", choices=DEFAULT_RESUME_MODES)
    parser.add_argument(
        "--no-stop-packet-required",
        dest="stop_packet_required",
        action="store_false",
        default=True,
        help="Do not require a stop packet when pausing or stopping the factory.",
    )
    parser.add_argument(
        "--external-effect-policy",
        choices=EXTERNAL_EFFECTS,
        default="explicit_operator",
    )
    parser.add_argument(
        "--target-outcome",
        default="Complete the requested software outcome and verify it against the configured acceptance tier.",
        help="Requested outcome the factory should drive toward.",
    )
    parser.add_argument(
        "--goal-policy",
        choices=GOAL_POLICIES,
        default="create_if_long_running",
        help="Persistent-goal behavior to record in generated factory docs.",
    )
    parser.add_argument(
        "--goal-text",
        help="Explicit persistent goal text to record. If omitted, the script generates a mode-aware template.",
    )
    parser.add_argument("--config-verbosity", choices=CONFIG_VERBOSITY)
    parser.add_argument("--permission-profile", choices=PERMISSION_PROFILES)
    parser.add_argument("--sandbox-mode", choices=SANDBOX_MODES)
    parser.add_argument("--approval-policy", choices=APPROVAL_POLICIES)
    parser.add_argument(
        "--tool-call-budget-policy", choices=TOOL_CALL_BUDGET_POLICIES
    )
    parser.add_argument("--thread-read-policy", choices=THREAD_READ_POLICIES)
    parser.add_argument(
        "--active-actor-polling-policy", choices=ACTIVE_ACTOR_POLLING_POLICIES
    )
    parser.add_argument(
        "--active-builder-poll-interval",
        help="Polling interval for a healthy active Builder, such as 3m.",
    )
    parser.add_argument(
        "--long-check-poll-interval",
        help="Polling interval for long checks, builds, migrations, or installs.",
    )
    parser.add_argument(
        "--handoff-poll-interval",
        help="Polling interval when handoff or final verification is likely.",
    )
    parser.add_argument(
        "--stale-ping-after",
        help="Duration with no meaningful progress before one status ping.",
    )
    parser.add_argument(
        "--stale-reclaim-after",
        help="Duration before applying stale actor or recovery policy.",
    )
    parser.add_argument(
        "--allowed-command-prefixes",
        help="Semicolon-separated command prefixes workers may use or request approval for.",
    )
    parser.add_argument(
        "--restricted-command-prefixes",
        help="Semicolon-separated command prefixes requiring approval or forbidden by policy.",
    )
    parser.add_argument(
        "--destructive-action-policy", choices=DESTRUCTIVE_ACTION_POLICIES
    )
    parser.add_argument("--external-network-policy", choices=EXTERNAL_NETWORK_POLICIES)
    parser.add_argument("--credential-policy", choices=CREDENTIAL_POLICIES)
    parser.add_argument("--default-model", default="user-preferred capable model")
    parser.add_argument(
        "--default-reasoning",
        choices=REASONING_LEVELS,
        default="high",
        help="Reasoning level to use when a role-specific value is not supplied.",
    )
    parser.add_argument("--principal-model")
    parser.add_argument("--principal-reasoning", choices=REASONING_LEVELS)
    parser.add_argument("--executive-model")
    parser.add_argument("--executive-reasoning", choices=REASONING_LEVELS)
    parser.add_argument("--ledger-model")
    parser.add_argument("--ledger-reasoning", choices=REASONING_LEVELS)
    parser.add_argument("--builder-model")
    parser.add_argument("--builder-reasoning", choices=REASONING_LEVELS)
    parser.add_argument("--reviewer-model")
    parser.add_argument("--reviewer-reasoning", choices=REASONING_LEVELS)
    parser.add_argument("--manager-model")
    parser.add_argument("--manager-reasoning", choices=REASONING_LEVELS)
    parser.add_argument("--watcher-model")
    parser.add_argument("--watcher-reasoning", choices=REASONING_LEVELS)
    parser.add_argument("--fallback-model")
    parser.add_argument("--fallback-reasoning", choices=REASONING_LEVELS)
    parser.add_argument("--model-switch-policy", choices=MODEL_SWITCH_POLICIES)
    parser.add_argument("--capability-preflight", choices=CAPABILITY_PREFLIGHTS)
    parser.add_argument("--git-auth-policy", choices=GIT_AUTH_POLICIES)
    parser.add_argument("--dirty-worktree-policy", choices=DIRTY_WORKTREE_POLICIES)
    parser.add_argument("--generated-file-policy", choices=GENERATED_FILE_POLICIES)
    parser.add_argument("--test-flake-policy", choices=TEST_FLAKE_POLICIES)
    parser.add_argument("--long-test-policy", choices=LONG_TEST_POLICIES)
    parser.add_argument("--dev-server-policy", choices=DEV_SERVER_POLICIES)
    parser.add_argument("--worktree-policy", choices=WORKTREE_POLICIES)
    parser.add_argument("--branch-policy", choices=BRANCH_POLICIES)
    parser.add_argument("--commit-policy", choices=COMMIT_POLICIES)
    parser.add_argument("--push-policy", choices=PUSH_POLICIES)
    parser.add_argument("--browser-tool-policy", choices=BROWSER_TOOL_POLICIES)
    parser.add_argument(
        "--context-compaction-policy", choices=CONTEXT_COMPACTION_POLICIES
    )
    parser.add_argument("--heartbeat-policy", choices=HEARTBEAT_POLICIES)
    parser.add_argument("--artifact-policy", choices=ARTIFACT_POLICIES)
    parser.add_argument("--user-interrupt-policy", choices=USER_INTERRUPT_POLICIES)
    parser.add_argument(
        "--release-readiness-policy", choices=RELEASE_READINESS_POLICIES
    )
    parser.add_argument(
        "--model-policy",
        default="Use the user's preferred capable model and reasoning level unless a baton explicitly lowers risk and cost.",
    )
    parser.add_argument(
        "--design-skill-policy",
        default="Use the project-specified design skill for UI work.",
    )
    parser.add_argument(
        "--full-gate-command",
        default="Record the project full test/eval command here.",
    )
    parser.add_argument(
        "--generated-file-guards",
        default="Record generated files that must not be staged.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite files")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--print-kickoff", action="store_true")
    parser.add_argument("--no-agents", action="store_true")
    return parser.parse_args()


def mode_friction_defaults(work_mode: str) -> dict[str, str]:
    defaults = dict(BASE_FRICTION_DEFAULTS)
    defaults.update(MODE_FRICTION_OVERRIDES.get(work_mode, {}))
    return defaults


def select_config_value(
    explicit_value: str | None, defaults: dict[str, str], key: str
) -> str:
    return explicit_value if explicit_value is not None else defaults[key]


def build_role_model_policy(args: argparse.Namespace) -> dict[str, str]:
    default_model = args.default_model
    default_reasoning = args.default_reasoning
    roles = {
        "principal": (args.principal_model, args.principal_reasoning),
        "executive": (args.executive_model, args.executive_reasoning),
        "ledger": (args.ledger_model, args.ledger_reasoning),
        "builder": (args.builder_model, args.builder_reasoning),
        "reviewer": (args.reviewer_model, args.reviewer_reasoning),
        "manager": (args.manager_model, args.manager_reasoning),
        "watcher": (args.watcher_model, args.watcher_reasoning),
        "fallback": (args.fallback_model, args.fallback_reasoning),
    }
    resolved: dict[str, str] = {}
    summary_parts = []
    for role, (model, reasoning) in roles.items():
        resolved[f"{role}_model"] = model or default_model
        resolved[f"{role}_reasoning"] = reasoning or default_reasoning
        summary_parts.append(
            f"{role}={resolved[f'{role}_model']}/{resolved[f'{role}_reasoning']}"
        )
    resolved["role_model_policy"] = "; ".join(summary_parts)
    return resolved


def involvement_defaults(args: argparse.Namespace) -> dict[str, str]:
    defaults = dict(INVOLVEMENT_DEFAULTS[args.user_involvement])
    return {
        "user_involvement": args.user_involvement,
        "feedback_handling": args.feedback_handling,
        "principal_policy": args.principal_policy or defaults["principal_policy"],
        "principal_authority": args.principal_authority
        or defaults["principal_authority"],
        "principal_intervention_policy": args.principal_intervention_policy
        or defaults["principal_intervention_policy"],
        "principal_digest_cadence": args.principal_digest_cadence
        or defaults["principal_digest_cadence"],
        "principal_context_budget": args.principal_context_budget
        or defaults["principal_context_budget"],
        "default_executive_context_policy": defaults["executive_context_policy"],
    }


def resolved_config(args: argparse.Namespace) -> dict[str, str]:
    defaults = MODE_DEFAULTS[args.work_mode]
    friction_defaults = mode_friction_defaults(args.work_mode)
    role_models = build_role_model_policy(args)
    involvement = involvement_defaults(args)
    role_topology = args.role_topology or defaults["role_topology"]
    manager_policy = args.manager_policy or defaults["manager_policy"]
    if args.feedback_handling == "feedback_manager" and args.manager_policy is None:
        manager_policy = "user_feedback_only"
    if args.feedback_handling == "always_on_manager" and args.manager_policy is None:
        manager_policy = "always_on"
    executive_context_policy = (
        args.executive_context_policy
        or involvement["default_executive_context_policy"]
        or defaults["executive_context_policy"]
    )
    if manager_policy != "none" and args.executive_context_policy is None:
        executive_context_policy = "manager_packaged_feedback"
    if manager_policy != "none" and role_topology not in {"managed", "enterprise"}:
        role_topology = "managed"
    if role_topology in {"managed", "enterprise"} and manager_policy == "none":
        manager_policy = "user_feedback_only"
    if role_topology in {"managed", "enterprise"} and executive_context_policy == "direct_user_chat":
        executive_context_policy = "manager_packaged_feedback"
    return {
        "work_mode": args.work_mode,
        "factory_topology": args.factory_topology,
        "role_topology": role_topology,
        "user_involvement": involvement["user_involvement"],
        "feedback_handling": involvement["feedback_handling"],
        "principal_policy": involvement["principal_policy"],
        "principal_authority": involvement["principal_authority"],
        "principal_intervention_policy": involvement["principal_intervention_policy"],
        "principal_digest_cadence": involvement["principal_digest_cadence"],
        "principal_context_budget": involvement["principal_context_budget"],
        "config_verbosity": select_config_value(
            args.config_verbosity, friction_defaults, "config_verbosity"
        ),
        "target_outcome": args.target_outcome,
        "goal_policy": args.goal_policy,
        "goal_text": args.goal_text
        or build_goal_text(args.project_name or "<PROJECT>", args.work_mode, args.target_outcome),
        "acceptance_tier": args.acceptance_tier or defaults["acceptance_tier"],
        "baton_size": args.baton_size or defaults["baton_size"],
        "concurrency_policy": args.concurrency_policy,
        "reviewer_policy": args.reviewer_policy or defaults["reviewer_policy"],
        "reviewer_spawn_policy": args.reviewer_spawn_policy
        or defaults["reviewer_spawn_policy"],
        "manager_policy": manager_policy,
        "executive_context_policy": executive_context_policy,
        "verification_level": args.verification_level or defaults["verification_level"],
        "full_gate_cadence": args.full_gate_cadence or defaults["full_gate_cadence"],
        "browser_qa_policy": args.browser_qa_policy or defaults["browser_qa_policy"],
        "review_depth": args.review_depth or defaults["review_depth"],
        "handoff_detail": args.handoff_detail or defaults["handoff_detail"],
        "package_protocol": args.package_protocol or defaults["package_protocol"],
        "thread_cleanup_policy": args.thread_cleanup_policy
        or defaults["thread_cleanup_policy"],
        "cleanup_keep_recent": str(args.cleanup_keep_recent),
        "factory_stop_policy": select_config_value(
            args.factory_stop_policy, friction_defaults, "factory_stop_policy"
        ),
        "default_stop_mode": select_config_value(
            args.default_stop_mode, friction_defaults, "default_stop_mode"
        ),
        "stop_scope": select_config_value(
            args.stop_scope, friction_defaults, "stop_scope"
        ),
        "stop_authority": select_config_value(
            args.stop_authority, friction_defaults, "stop_authority"
        ),
        "stop_monitor_policy": select_config_value(
            args.stop_monitor_policy, friction_defaults, "stop_monitor_policy"
        ),
        "stop_cleanup_policy": select_config_value(
            args.stop_cleanup_policy, friction_defaults, "stop_cleanup_policy"
        ),
        "resume_policy": select_config_value(
            args.resume_policy, friction_defaults, "resume_policy"
        ),
        "default_resume_mode": select_config_value(
            args.default_resume_mode, friction_defaults, "default_resume_mode"
        ),
        "stop_packet_required": "true" if args.stop_packet_required else "false",
        "external_effect_policy": args.external_effect_policy,
        "model_policy": args.model_policy,
        "role_model_policy": role_models["role_model_policy"],
        "model_switch_policy": select_config_value(
            args.model_switch_policy, friction_defaults, "model_switch_policy"
        ),
        "default_model": args.default_model,
        "default_reasoning": args.default_reasoning,
        "principal_model": role_models["principal_model"],
        "principal_reasoning": role_models["principal_reasoning"],
        "executive_model": role_models["executive_model"],
        "executive_reasoning": role_models["executive_reasoning"],
        "ledger_model": role_models["ledger_model"],
        "ledger_reasoning": role_models["ledger_reasoning"],
        "builder_model": role_models["builder_model"],
        "builder_reasoning": role_models["builder_reasoning"],
        "reviewer_model": role_models["reviewer_model"],
        "reviewer_reasoning": role_models["reviewer_reasoning"],
        "manager_model": role_models["manager_model"],
        "manager_reasoning": role_models["manager_reasoning"],
        "watcher_model": role_models["watcher_model"],
        "watcher_reasoning": role_models["watcher_reasoning"],
        "fallback_model": role_models["fallback_model"],
        "fallback_reasoning": role_models["fallback_reasoning"],
        "design_skill_policy": args.design_skill_policy,
        "permission_profile": select_config_value(
            args.permission_profile, friction_defaults, "permission_profile"
        ),
        "sandbox_mode": select_config_value(
            args.sandbox_mode, friction_defaults, "sandbox_mode"
        ),
        "approval_policy": select_config_value(
            args.approval_policy, friction_defaults, "approval_policy"
        ),
        "tool_call_budget_policy": select_config_value(
            args.tool_call_budget_policy,
            friction_defaults,
            "tool_call_budget_policy",
        ),
        "thread_read_policy": select_config_value(
            args.thread_read_policy, friction_defaults, "thread_read_policy"
        ),
        "active_actor_polling_policy": select_config_value(
            args.active_actor_polling_policy,
            friction_defaults,
            "active_actor_polling_policy",
        ),
        "active_builder_poll_interval": select_config_value(
            args.active_builder_poll_interval,
            friction_defaults,
            "active_builder_poll_interval",
        ),
        "long_check_poll_interval": select_config_value(
            args.long_check_poll_interval,
            friction_defaults,
            "long_check_poll_interval",
        ),
        "handoff_poll_interval": select_config_value(
            args.handoff_poll_interval,
            friction_defaults,
            "handoff_poll_interval",
        ),
        "stale_ping_after": select_config_value(
            args.stale_ping_after, friction_defaults, "stale_ping_after"
        ),
        "stale_reclaim_after": select_config_value(
            args.stale_reclaim_after, friction_defaults, "stale_reclaim_after"
        ),
        "allowed_command_prefixes": select_config_value(
            args.allowed_command_prefixes,
            friction_defaults,
            "allowed_command_prefixes",
        ),
        "restricted_command_prefixes": select_config_value(
            args.restricted_command_prefixes,
            friction_defaults,
            "restricted_command_prefixes",
        ),
        "destructive_action_policy": select_config_value(
            args.destructive_action_policy,
            friction_defaults,
            "destructive_action_policy",
        ),
        "external_network_policy": select_config_value(
            args.external_network_policy, friction_defaults, "external_network_policy"
        ),
        "credential_policy": select_config_value(
            args.credential_policy, friction_defaults, "credential_policy"
        ),
        "capability_preflight": select_config_value(
            args.capability_preflight, friction_defaults, "capability_preflight"
        ),
        "git_auth_policy": select_config_value(
            args.git_auth_policy, friction_defaults, "git_auth_policy"
        ),
        "dirty_worktree_policy": select_config_value(
            args.dirty_worktree_policy, friction_defaults, "dirty_worktree_policy"
        ),
        "generated_file_policy": select_config_value(
            args.generated_file_policy, friction_defaults, "generated_file_policy"
        ),
        "test_flake_policy": select_config_value(
            args.test_flake_policy, friction_defaults, "test_flake_policy"
        ),
        "long_test_policy": select_config_value(
            args.long_test_policy, friction_defaults, "long_test_policy"
        ),
        "dev_server_policy": select_config_value(
            args.dev_server_policy, friction_defaults, "dev_server_policy"
        ),
        "worktree_policy": select_config_value(
            args.worktree_policy, friction_defaults, "worktree_policy"
        ),
        "branch_policy": select_config_value(
            args.branch_policy, friction_defaults, "branch_policy"
        ),
        "commit_policy": select_config_value(
            args.commit_policy, friction_defaults, "commit_policy"
        ),
        "push_policy": select_config_value(
            args.push_policy, friction_defaults, "push_policy"
        ),
        "browser_tool_policy": select_config_value(
            args.browser_tool_policy, friction_defaults, "browser_tool_policy"
        ),
        "context_compaction_policy": select_config_value(
            args.context_compaction_policy,
            friction_defaults,
            "context_compaction_policy",
        ),
        "heartbeat_policy": select_config_value(
            args.heartbeat_policy, friction_defaults, "heartbeat_policy"
        ),
        "artifact_policy": select_config_value(
            args.artifact_policy, friction_defaults, "artifact_policy"
        ),
        "user_interrupt_policy": select_config_value(
            args.user_interrupt_policy, friction_defaults, "user_interrupt_policy"
        ),
        "release_readiness_policy": select_config_value(
            args.release_readiness_policy,
            friction_defaults,
            "release_readiness_policy",
        ),
        "full_gate_command": args.full_gate_command,
        "generated_file_guards": args.generated_file_guards,
    }


def build_goal_text(project_name: str, work_mode: str, target_outcome: str) -> str:
    project = project_name if project_name else "<PROJECT>"
    if work_mode == "safe_mvp":
        return (
            f"Drive the {project} software factory in Safe MVP Mode: deliver "
            "the thinnest real product-visible vertical slice quickly, "
            "preserve hard safety and external-effect invariants, use focused "
            "proof for the core flow, record deferred breadth and hardening "
            "gaps, commit the accepted slice, and continue until this MVP "
            f"behavior is demonstrable and ready for the next hardening or "
            f"release checkpoint: {target_outcome}"
        )
    if work_mode == "velocity":
        return (
            f"Drive the {project} software factory in Velocity Mode: deliver "
            "product-visible vertical slices quickly, coordinate batons, preserve "
            "hard invariants, use focused verification per slice, run full gates "
            "at configured checkpoints, record known risks, commit accepted "
            f"integration work, and continue until this outcome is ready for "
            f"hardening or release: {target_outcome}"
        )
    if work_mode == "release":
        return (
            f"Drive the {project} release factory to completion: freeze "
            "nonessential scope, verify release criteria, run full gates and "
            "final QA, resolve blocking risks, commit accepted fixes, push when "
            f"authentication permits, and continue until release-ready: "
            f"{target_outcome}"
        )
    if work_mode == "recovery":
        return (
            f"Drive the {project} factory recovery: freeze new work, identify "
            "active owners and dirty state, reconcile collisions or failed "
            "gates, restore a single source of truth, commit accepted recovery "
            f"work, and resume the configured factory toward: {target_outcome}"
        )
    return (
        f"Drive the {project} software factory end to end: maintain the factory "
        "ledger, coordinate Builder and Reviewer batons, enforce the selected "
        "work mode and project invariants, preserve user changes, accept only "
        "work that satisfies the configured acceptance tier, keep required "
        "tests/evals passing according to the verification cadence, commit "
        "accepted work locally, push when authentication permits, and continue "
        f"until this requested project outcome is complete and verified: "
        f"{target_outcome}"
    )


def build_agents_md(project_name: str, config: dict[str, str]) -> str:
    return f"""# {project_name} Agent Rules

## Source Of Truth

- Read `docs/factory_config.md` before factory work.
- Read `docs/review_index.md` for project source-of-truth docs.
- Follow `docs/codex_factory_protocol.md` and `docs/handoff_protocol.md`.
- Keep `docs/build_ledger.md` current with status, evidence, risks, and next baton.

## Factory Defaults

- Work mode: `{config["work_mode"]}`
- Role topology: `{config["role_topology"]}`
- User involvement: `{config["user_involvement"]}`
- Feedback handling: `{config["feedback_handling"]}`
- Principal policy: `{config["principal_policy"]}`
- Principal authority: `{config["principal_authority"]}`
- Config verbosity: `{config["config_verbosity"]}`
- Target outcome: `{config["target_outcome"]}`
- Goal policy: `{config["goal_policy"]}`
- Acceptance tier: `{config["acceptance_tier"]}`
- Verification: `{config["verification_level"]}`
- Full gate cadence: `{config["full_gate_cadence"]}`
- Concurrency: `{config["concurrency_policy"]}`
- Reviewer policy: `{config["reviewer_policy"]}`
- Reviewer spawn: `{config["reviewer_spawn_policy"]}`
- Manager policy: `{config["manager_policy"]}`
- Cleanup policy: `{config["thread_cleanup_policy"]}`
- Factory stop policy: `{config["factory_stop_policy"]}`
- Default stop mode: `{config["default_stop_mode"]}`
- Stop monitor policy: `{config["stop_monitor_policy"]}`
- Resume policy: `{config["resume_policy"]}`
- Default resume mode: `{config["default_resume_mode"]}`
- Permission profile: `{config["permission_profile"]}`
- Approval policy: `{config["approval_policy"]}`
- Tool-call policy: `{config["tool_call_budget_policy"]}`
- Thread-read policy: `{config["thread_read_policy"]}`
- Active polling: `{config["active_actor_polling_policy"]}`
- Model switch policy: `{config["model_switch_policy"]}`
- Capability preflight: `{config["capability_preflight"]}`

## Hard Rules

- Preserve user changes; do not revert unknown work without explicit instruction.
- Principal Executive may steer, configure, or intervene only according to its recorded authority and intervention policy.
- Builders do not stage, commit, push, create worktrees, or change monitors unless delegated.
- Maintain one active writer per worktree unless `parallel_worktrees` is explicitly configured.
- Builders hand off to Executive/Ledger; Executive/Ledger routes Review Batons when configured.
- Manager/User Liaison sends briefs only to Principal or Executive unless explicitly promoted.
- Cleanup archives completed workers only after ledger evidence is captured.
- Stop directives preempt new baton assignment. Use the configured stop mode, preserve evidence, and produce a Stop Packet before pausing monitors or archiving threads unless emergency stop requires immediate freeze.
- Treat permission/model settings as desired runtime configuration; record and route around runtime mismatches.
- Destructive actions, credential prompts, production effects, protected branches, and live external service calls follow the configured blocker policies.
- Escalate review and verification for auth, security, payments, data migrations, live external effects, public contracts, and production writes.
- {config["design_skill_policy"]}
"""


def build_effective_config_summary(config: dict[str, str]) -> str:
    return f"""```text
mode/topology: {config["work_mode"]} / {config["role_topology"]} / {config["factory_topology"]}
target/tier: {config["target_outcome"]} / {config["acceptance_tier"]}
principal: {config["user_involvement"]}; policy={config["principal_policy"]}; authority={config["principal_authority"]}; intervention={config["principal_intervention_policy"]}
feedback: {config["feedback_handling"]}; manager={config["manager_policy"]}; executive_context={config["executive_context_policy"]}
model routing: {config["model_switch_policy"]}; {config["role_model_policy"]}
permission: {config["permission_profile"]}; sandbox={config["sandbox_mode"]}; approval={config["approval_policy"]}
tool-call/thread-read: {config["tool_call_budget_policy"]} / {config["thread_read_policy"]}
active polling: {config["active_actor_polling_policy"]}; builder={config["active_builder_poll_interval"]}; long_check={config["long_check_poll_interval"]}; handoff={config["handoff_poll_interval"]}; stale_ping={config["stale_ping_after"]}; stale_reclaim={config["stale_reclaim_after"]}
allowed prefixes: {config["allowed_command_prefixes"]}
restricted prefixes: {config["restricted_command_prefixes"]}
verification: {config["verification_level"]}; full gate={config["full_gate_cadence"]}; browser={config["browser_qa_policy"]}
review routing: {config["reviewer_policy"]}; spawn={config["reviewer_spawn_policy"]}
cleanup: {config["thread_cleanup_policy"]}; keep recent={config["cleanup_keep_recent"]}
stop/resume: policy={config["factory_stop_policy"]}; default={config["default_stop_mode"]}; scope={config["stop_scope"]}; authority={config["stop_authority"]}; monitors={config["stop_monitor_policy"]}; cleanup={config["stop_cleanup_policy"]}; resume={config["resume_policy"]}; default_resume={config["default_resume_mode"]}; packet_required={config["stop_packet_required"]}
blockers: git_auth={config["git_auth_policy"]}; dirty={config["dirty_worktree_policy"]}; push={config["push_policy"]}
```"""


def build_capability_preflight(config: dict[str, str]) -> str:
    return f"""Configured level: `{config["capability_preflight"]}`

| Capability | Status | Evidence | Blocker policy |
| --- | --- | --- | --- |
| thread tools | unknown | inspect at launch | context/heartbeat policy |
| thread tool schema | unknown | inspect at launch | tool_call={config["tool_call_budget_policy"]} |
| thread read policy support | unknown | inspect at launch | thread_read={config["thread_read_policy"]} |
| tool call limits | unknown | inspect at launch | polling={config["active_actor_polling_policy"]} |
| automation tools | unknown | inspect at launch | heartbeat={config["heartbeat_policy"]} |
| goal tooling | unknown | inspect at launch | goal_policy={config["goal_policy"]} |
| git write | unknown | inspect at launch | commit={config["commit_policy"]} |
| push auth | unknown | inspect at launch | git_auth={config["git_auth_policy"]}; push={config["push_policy"]} |
| network | unknown | inspect at launch | external_network={config["external_network_policy"]} |
| browser | unknown | inspect at launch | browser_tool={config["browser_tool_policy"]} |
| package manager | unknown | inspect at launch | long_tests={config["long_test_policy"]} |
| test commands | unknown | inspect at launch | flakes={config["test_flake_policy"]} |
| env files | unknown | inspect at launch | credentials={config["credential_policy"]} |
| required secrets | unknown | inspect at launch | credentials={config["credential_policy"]} |
| generated files | unknown | inspect at launch | generated_files={config["generated_file_policy"]} |
| dev server | unknown | inspect at launch | dev_server={config["dev_server_policy"]} |"""


def build_blocker_policy_summary(config: dict[str, str]) -> str:
    return f"""```text
git_auth_policy: {config["git_auth_policy"]}
dirty_worktree_policy: {config["dirty_worktree_policy"]}
generated_file_policy: {config["generated_file_policy"]}
test_flake_policy: {config["test_flake_policy"]}
long_test_policy: {config["long_test_policy"]}
dev_server_policy: {config["dev_server_policy"]}
worktree_policy: {config["worktree_policy"]}
branch_policy: {config["branch_policy"]}
commit_policy: {config["commit_policy"]}
push_policy: {config["push_policy"]}
browser_tool_policy: {config["browser_tool_policy"]}
context_compaction_policy: {config["context_compaction_policy"]}
heartbeat_policy: {config["heartbeat_policy"]}
artifact_policy: {config["artifact_policy"]}
user_interrupt_policy: {config["user_interrupt_policy"]}
release_readiness_policy: {config["release_readiness_policy"]}
```"""


def build_factory_config(project_name: str, config: dict[str, str]) -> str:
    today = dt.date.today().isoformat()
    lines = "\n".join(f"{key}: {value}" for key, value in config.items())
    return f"""# {project_name} Factory Configuration

Initialized: {today}
Last updated: {today}

## Operating Model

```text
{lines}
```

## Effective Config Summary

{build_effective_config_summary(config)}

## Capability Preflight

{build_capability_preflight(config)}

## Principal And Feedback Policy

- User involvement: `{config["user_involvement"]}`
- Feedback handling: `{config["feedback_handling"]}`
- Principal policy: `{config["principal_policy"]}`
- Principal authority: `{config["principal_authority"]}`
- Principal intervention policy: `{config["principal_intervention_policy"]}`
- Principal digest cadence: `{config["principal_digest_cadence"]}`
- Principal context budget: `{config["principal_context_budget"]}`
- Manager policy: `{config["manager_policy"]}`
- Executive context policy: `{config["executive_context_policy"]}`

Principal Executive oversees mode, topology, cleanup, handoffs, ledger promotion, and factory health according to its authority. It does not normally hold the write baton.

## Stop And Resume Policy

- Factory stop policy: `{config["factory_stop_policy"]}`
- Default stop mode: `{config["default_stop_mode"]}`
- Stop scope: `{config["stop_scope"]}`
- Stop authority: `{config["stop_authority"]}`
- Stop monitor policy: `{config["stop_monitor_policy"]}`
- Stop cleanup policy: `{config["stop_cleanup_policy"]}`
- Resume policy: `{config["resume_policy"]}`
- Default resume mode: `{config["default_resume_mode"]}`
- Stop packet required: `{config["stop_packet_required"]}`

Stop requests preempt new baton assignment. Unless the mode is `emergency_stop`, capture the active baton, owner, worktree status, latest commit/push state, monitors, cleanup actions, risks, and resume instructions before pausing or archiving factory actors.

## Permission And Model Policy

- Permission profile: `{config["permission_profile"]}`
- Sandbox mode requested: `{config["sandbox_mode"]}`
- Approval policy requested: `{config["approval_policy"]}`
- Destructive action policy: `{config["destructive_action_policy"]}`
- External network policy: `{config["external_network_policy"]}`
- Credential policy: `{config["credential_policy"]}`
- Tool-call budget policy: `{config["tool_call_budget_policy"]}`
- Thread-read policy: `{config["thread_read_policy"]}`
- Active actor polling policy: `{config["active_actor_polling_policy"]}`
- Active Builder poll interval: `{config["active_builder_poll_interval"]}`
- Long-check poll interval: `{config["long_check_poll_interval"]}`
- Handoff poll interval: `{config["handoff_poll_interval"]}`
- Stale ping after: `{config["stale_ping_after"]}`
- Stale reclaim after: `{config["stale_reclaim_after"]}`
- Model policy: {config["model_policy"]}
- Role model policy: {config["role_model_policy"]}
- Model switch policy: `{config["model_switch_policy"]}`

If the runtime cannot apply these settings directly, record the mismatch in the ledger and use the blocker policy fallback.

## Blocker Policies

{build_blocker_policy_summary(config)}

## Acceptance Ladder

- Prototype accepted: demonstrable behavior with explicit hardening gaps.
- Integration accepted: wired behavior with focused evidence and no known blocking regressions.
- Release accepted: full release evidence, deployment readiness, and final QA.

## Risk Escalators

Escalate verification and review when touching auth/security, secrets, payments, production data writes, database migrations, public contracts, infra/deployment, background jobs, external live services, ML/eval/scoring logic, or generated clients.

## Persistent Goal

Goal policy: `{config["goal_policy"]}`

```text
{config["goal_text"]}
```

## Project-Specific Invariants

- Generated-file guards: {config["generated_file_guards"]}
- External effects: {config["external_effect_policy"]}
- Full gate: `{config["full_gate_command"]}`
"""


def build_review_index(project_name: str) -> str:
    return f"""# {project_name} Review Index

## Source Of Truth Order

1. Product vision and acceptance criteria:
2. Architecture, contracts, and data model:
3. UI/design system:
4. Tests/evals:
5. Release/deployment:
6. Factory configuration and ledger:

## Required Reading By Task Type

| Task | Required Docs |
| --- | --- |
| Product behavior | Fill in project docs |
| UI/UX | Fill in design docs and required design skill |
| API/contracts | Fill in contract docs |
| Data/storage | Fill in schema and migration docs |
| Security | Fill in security docs |
| Release | Fill in release docs |

Update this file whenever a source-of-truth doc is added, superseded, or deprecated.
"""


def build_factory_protocol(project_name: str, config: dict[str, str]) -> str:
    return f"""# {project_name} Codex Factory Protocol

## Configuration

- Work mode: `{config["work_mode"]}`
- Target outcome: `{config["target_outcome"]}`
- Goal policy: `{config["goal_policy"]}`
- Role topology: `{config["role_topology"]}`
- User involvement: `{config["user_involvement"]}`
- Feedback handling: `{config["feedback_handling"]}`
- Principal policy: `{config["principal_policy"]}`
- Principal authority: `{config["principal_authority"]}`
- Principal intervention: `{config["principal_intervention_policy"]}`
- Config verbosity: `{config["config_verbosity"]}`
- Topology: `{config["factory_topology"]}`
- Acceptance tier: `{config["acceptance_tier"]}`
- Reviewer policy: `{config["reviewer_policy"]}`
- Reviewer spawn: `{config["reviewer_spawn_policy"]}`
- Manager policy: `{config["manager_policy"]}`
- Verification: `{config["verification_level"]}`
- Full gate cadence: `{config["full_gate_cadence"]}`
- Permission profile: `{config["permission_profile"]}`
- Approval policy: `{config["approval_policy"]}`
- Tool-call budget policy: `{config["tool_call_budget_policy"]}`
- Thread-read policy: `{config["thread_read_policy"]}`
- Active actor polling: `{config["active_actor_polling_policy"]}`
- Model switch policy: `{config["model_switch_policy"]}`
- Capability preflight: `{config["capability_preflight"]}`

## Effective Config Summary

{build_effective_config_summary(config)}

## Roles

- Principal Executive: user-facing strategic partner; oversees topology, mode, cleanup, handoffs, ledger promotion, and emergency intervention according to configured authority.
- Executive: product judgment, routing, final acceptance, commit policy, and user communication.
- Ledger/controller: build ledger, baton assignment, evidence, risks, and recovery notes.
- Builder: scoped implementation and Handoff Bundle to Executive/Ledger without committing unless delegated.
- Reviewer: read-only Review Package to Executive/Ledger by default.
- Manager/User Liaison: user feedback intake and Principal/Executive Briefs only; no direct Builder/Reviewer control by default.
- Watcher: monitor only; never edits files.

## Operating Rules

- Preserve one active writer per worktree unless explicitly configured otherwise.
- Principal may steer or reconfigure the factory only through the configured intervention policy and should not interrupt an active writer except for safety, user override, or factory-health recovery.
- Prefer handoff sequencing; use parallel read-only reviewers for speed.
- Record assignment before authorization when git is available.
- Route Builder handoffs through Executive/Ledger before any Reviewer work.
- Take review lock only after handoff, block, stall, relinquish, or reclaim.
- If push/auth fails, keep local commits and continue with recorded remote status.
- If runtime permissions are weaker than configured, record the mismatch and apply blocker fallbacks instead of silently downgrading quality.
- Use the configured model/reasoning by role when thread tools support it; otherwise restate the target model policy in worker prompts.
- Keep ledgers useful, not ceremonial.
- Stop directives freeze new assignments immediately, then follow the configured stop mode and produce a Stop Packet when required.
- Escalate to stricter verification when risk escalators are touched.
- Run thread cleanup only after ledger evidence captures completed work.

## Stop And Resume

Default stop mode: `{config["default_stop_mode"]}`

- `pause_new_work`: stop assigning new batons; current safe work may continue.
- `drain_to_handoff`: active Builder reaches a Handoff Bundle, then pauses before acceptance.
- `drain_to_checkpoint`: active baton reaches review, acceptance, ledger evidence, and configured commit/push fallback, then pauses.
- `release_freeze`: stop feature work; allow only release gates, blocker fixes, and readiness notes.
- `hard_stop`: active actors stop after the current safe command and record dirty state.
- `emergency_stop`: immediate freeze for safety, security, destructive-action, or ownership risk.

Stop authority is `{config["stop_authority"]}`. Stop scope is `{config["stop_scope"]}`. Monitor handling is `{config["stop_monitor_policy"]}`. Resume uses `{config["resume_policy"]}` with default mode `{config["default_resume_mode"]}`.

## Capability Preflight

{build_capability_preflight(config)}

## Blocker Policies

{build_blocker_policy_summary(config)}

## Verification

- Configured full gate: `{config["full_gate_command"]}`
- Configured generated-file guards: {config["generated_file_guards"]}
- UI/browser QA policy: `{config["browser_qa_policy"]}`
- Thread cleanup policy: `{config["thread_cleanup_policy"]}`
"""


def build_handoff_protocol(project_name: str, config: dict[str, str]) -> str:
    return f"""# {project_name} Handoff Protocol

Configured detail level: `{config["handoff_detail"]}`

```text
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
```

## Factory Stop Directive

Configured default: `{config["default_stop_mode"]}`

```text
Factory stop directive for {project_name}.

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

```text
mode:
scope:
reason:
requested_by:
authority:
stop_state:
executive_or_ledger:
principal:
manager:
active_builder:
active_reviewer:
current_baton:
branch_or_worktree:
latest_accepted_commit:
push_or_remote_status:
dirty_files:
staged_files:
untracked_files:
running_or_last_command:
completed_checks:
unfinished_checks:
monitors_kept:
monitors_paused_deleted_or_retargeted:
threads_archived:
threads_preserved:
unresolved_risks:
resume_policy:
resume_authority:
next_recommended_action:
verification_to_rerun:
cleanup_still_pending:
```

## Resume Packet

```text
requested_by:
approved_by:
resume_policy:
resume_mode:
prior_stop_packet:
executive_or_ledger_to_wake:
principal_or_manager_to_notify:
builder_or_reviewer_to_resume_or_replace:
monitors_to_restart:
cleanup_to_defer_or_run:
next_baton:
write_owner:
review_owner:
worktree_or_branch:
verification:
risks_to_recheck:
```
"""


def build_ledger(project_name: str, config: dict[str, str]) -> str:
    today = dt.date.today().isoformat()
    return f"""# {project_name} Build Ledger

Initialized: {today}

## Current Factory State

```text
status: initialized / ready for first baton
work_mode: {config["work_mode"]}
role_topology: {config["role_topology"]}
user_involvement: {config["user_involvement"]}
feedback_handling: {config["feedback_handling"]}
principal_policy: {config["principal_policy"]}
principal_authority: {config["principal_authority"]}
principal_intervention_policy: {config["principal_intervention_policy"]}
config_verbosity: {config["config_verbosity"]}
target_outcome: {config["target_outcome"]}
goal_policy: {config["goal_policy"]}
acceptance_tier: {config["acceptance_tier"]}
factory_topology: {config["factory_topology"]}
reviewer_policy: {config["reviewer_policy"]}
reviewer_spawn_policy: {config["reviewer_spawn_policy"]}
manager_policy: {config["manager_policy"]}
thread_cleanup_policy: {config["thread_cleanup_policy"]}
cleanup_keep_recent: {config["cleanup_keep_recent"]}
factory_stop_policy: {config["factory_stop_policy"]}
default_stop_mode: {config["default_stop_mode"]}
stop_scope: {config["stop_scope"]}
stop_authority: {config["stop_authority"]}
stop_monitor_policy: {config["stop_monitor_policy"]}
stop_cleanup_policy: {config["stop_cleanup_policy"]}
resume_policy: {config["resume_policy"]}
default_resume_mode: {config["default_resume_mode"]}
stop_packet_required: {config["stop_packet_required"]}
stop_state: running
last_stop_packet: none
permission_profile: {config["permission_profile"]}
sandbox_mode: {config["sandbox_mode"]}
approval_policy: {config["approval_policy"]}
tool_call_budget_policy: {config["tool_call_budget_policy"]}
thread_read_policy: {config["thread_read_policy"]}
active_actor_polling_policy: {config["active_actor_polling_policy"]}
active_builder_poll_interval: {config["active_builder_poll_interval"]}
long_check_poll_interval: {config["long_check_poll_interval"]}
handoff_poll_interval: {config["handoff_poll_interval"]}
stale_ping_after: {config["stale_ping_after"]}
stale_reclaim_after: {config["stale_reclaim_after"]}
model_switch_policy: {config["model_switch_policy"]}
capability_preflight: {config["capability_preflight"]}
active_writer:
active_reviewer:
principal_thread:
manager_thread:
current_baton: unassigned
last_accepted_baton: none
last_release_gate: none
remote_status:
```

## Active Threads

| Role | Thread | Status | Scope | Notes |
| --- | --- | --- | --- | --- |

## Thread Cleanup

| Policy | Keep Recent | Last Cleanup | Notes |
| --- | --- | --- | --- |
| {config["thread_cleanup_policy"]} | {config["cleanup_keep_recent"]} | none | Preserve active, unresolved, pinned, Executive, Ledger, and Manager threads |

## Stop And Resume

| State | Default Stop | Scope | Authority | Monitor Policy | Cleanup Policy | Resume Policy | Default Resume |
| --- | --- | --- | --- | --- | --- | --- | --- |
| running | {config["default_stop_mode"]} | {config["stop_scope"]} | {config["stop_authority"]} | {config["stop_monitor_policy"]} | {config["stop_cleanup_policy"]} | {config["resume_policy"]} | {config["default_resume_mode"]} |

Latest stop packet: none
Latest resume packet: none

## Capability Preflight

| Capability | Status | Evidence | Blocker policy |
| --- | --- | --- | --- |
| thread tools | unknown |  | heartbeat={config["heartbeat_policy"]} |
| thread tool schema | unknown |  | tool_call={config["tool_call_budget_policy"]} |
| thread read policy support | unknown |  | thread_read={config["thread_read_policy"]} |
| tool call limits | unknown |  | polling={config["active_actor_polling_policy"]} |
| automations | unknown |  | heartbeat={config["heartbeat_policy"]} |
| goal tooling | unknown |  | goal_policy={config["goal_policy"]} |
| git write | unknown |  | commit={config["commit_policy"]} |
| push auth | unknown |  | git_auth={config["git_auth_policy"]}; push={config["push_policy"]} |
| browser | unknown |  | browser_tool={config["browser_tool_policy"]} |
| package manager | unknown |  | long_tests={config["long_test_policy"]} |
| tests | unknown |  | flakes={config["test_flake_policy"]} |
| env/secrets | unknown |  | credentials={config["credential_policy"]} |

## Effective Config Summary

{build_effective_config_summary(config)}

## Baton Queue

| Baton | Tier | Owner | Status | Objective | Verification | Risk |
| --- | --- | --- | --- | --- | --- | --- |

## Acceptance Evidence

| Baton | Tier | Evidence | Skipped checks | Residual risk |
| --- | --- | --- | --- | --- |

## Open Decisions

| ID | Decision | Owner | Status | Notes |
| --- | --- | --- | --- | --- |

## Retrospective

| Date | Observation | Adjustment |
| --- | --- | --- |

## Next Baton Candidate

```text
Define B-001 with objective, write scope, non-goals, risk, acceptance tier, and verification.
```

## Persistent Goal

```text
{config["goal_text"]}
```
"""


def build_kickoff(project_name: str, root: Path, config: dict[str, str]) -> str:
    goal_instruction = build_goal_instruction(config)
    return f"""# Software Factory Kickoff

Project: {project_name}
Root: {root}

Config:
- work_mode: {config["work_mode"]}
- role_topology: {config["role_topology"]}
- user_involvement: {config["user_involvement"]}
- feedback_handling: {config["feedback_handling"]}
- principal_policy: {config["principal_policy"]}
- principal_authority: {config["principal_authority"]}
- config_verbosity: {config["config_verbosity"]}
- target_outcome: {config["target_outcome"]}
- goal_policy: {config["goal_policy"]}
- topology: {config["factory_topology"]}
- acceptance_tier: {config["acceptance_tier"]}
- baton_size: {config["baton_size"]}
- verification: {config["verification_level"]}
- full_gate_cadence: {config["full_gate_cadence"]}
- concurrency: {config["concurrency_policy"]}
- reviewer_policy: {config["reviewer_policy"]}
- reviewer_spawn_policy: {config["reviewer_spawn_policy"]}
- manager_policy: {config["manager_policy"]}
- thread_cleanup_policy: {config["thread_cleanup_policy"]}
- factory_stop_policy: {config["factory_stop_policy"]}
- default_stop_mode: {config["default_stop_mode"]}
- stop_monitor_policy: {config["stop_monitor_policy"]}
- resume_policy: {config["resume_policy"]}
- default_resume_mode: {config["default_resume_mode"]}
- permission_profile: {config["permission_profile"]}
- approval_policy: {config["approval_policy"]}
- tool_call_budget_policy: {config["tool_call_budget_policy"]}
- thread_read_policy: {config["thread_read_policy"]}
- active_actor_polling_policy: {config["active_actor_polling_policy"]}
- model_switch_policy: {config["model_switch_policy"]}
- capability_preflight: {config["capability_preflight"]}

Effective config summary:
{build_effective_config_summary(config)}

Immediate sequence:
1. Inspect git status, source docs, scripts, branch, remote, dirty state, and generated-file hazards.
2. Read `docs/factory_config.md`, `docs/review_index.md`, `docs/codex_factory_protocol.md`, `docs/handoff_protocol.md`, and `docs/build_ledger.md`.
3. Run capability preflight at `{config["capability_preflight"]}` level and record blockers before worker launch.
4. Goal setup: {goal_instruction}
5. Confirm the first baton and record it in the ledger.
6. Establish Principal/Executive/Manager routing according to user involvement and feedback handling.
7. Authorize one Builder, optional Manager/User Liaison, and optional Reviewer standby according to role topology, requested model/reasoning, and permission profile.
8. Route Builder handoff to Executive/Ledger; route Review Baton only after handoff unless standby/parallel reviewer policy applies.
9. Apply the configured acceptance tier and verification cadence.
10. Escalate if risk escalators are touched.
11. Use blocker policies for permission prompts, push auth, dirty worktrees, long tests, browser tooling, env/secrets, and context compaction.
12. Record stop/resume controls and treat stop directives as higher priority than new baton assignment.
13. Run thread cleanup after accepted commits only when the cleanup policy allows it.
"""


def build_goal_instruction(config: dict[str, str]) -> str:
    policy = config["goal_policy"]
    if policy == "none":
        return "do not create a persistent goal; record the target outcome in the ledger only."
    if policy == "ask":
        return (
            "if goal tooling is available, ask whether to create this persistent "
            f"goal before doing so: {config['goal_text']}"
        )
    if policy == "explicit_only":
        return (
            "create a persistent goal only if the user explicitly requested goal "
            f"tracking; suggested goal text: {config['goal_text']}"
        )
    return (
        "if goal tooling is available, runtime policy permits goal creation, "
        "and the task is long-running, create or confirm this persistent goal; "
        f"otherwise record it in the ledger only: {config['goal_text']}"
    )


def write_file(path: Path, content: str, force: bool, dry_run: bool) -> str:
    if path.exists() and not force:
        return f"SKIP existing {path}"
    action = "OVERWRITE" if path.exists() else "CREATE"
    if dry_run:
        return f"DRY-RUN {action} {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"{action} {path}"


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"ERROR project_root is not a directory: {root}", file=sys.stderr)
        return 2

    project_name = args.project_name or root.name
    args.project_name = project_name
    config = resolved_config(args)
    docs = {
        root / "docs" / "factory_config.md": build_factory_config(project_name, config),
        root / "docs" / "review_index.md": build_review_index(project_name),
        root / "docs" / "codex_factory_protocol.md": build_factory_protocol(
            project_name, config
        ),
        root / "docs" / "handoff_protocol.md": build_handoff_protocol(
            project_name, config
        ),
        root / "docs" / "build_ledger.md": build_ledger(project_name, config),
    }
    if not args.no_agents:
        docs = {root / "AGENTS.md": build_agents_md(project_name, config), **docs}

    for path, content in docs.items():
        print(write_file(path, content, args.force, args.dry_run))

    if args.print_kickoff:
        print()
        print(build_kickoff(project_name, root, config))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
