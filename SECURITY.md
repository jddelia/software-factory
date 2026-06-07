# Security Policy

## Reporting A Vulnerability

Do not open a public issue for a vulnerability, leaked secret, credential,
private repository URL, or sensitive operational detail.

Use GitHub private vulnerability reporting if it is enabled for this repository.
If private reporting is unavailable, open a public issue with only a minimal,
non-sensitive request for a private contact path. Do not include exploit steps,
tokens, private logs, screenshots containing secrets, or customer/project data
in that public issue.

## Supported Versions

This project is pre-1.0. Security fixes are handled on the default branch until
release branches exist.

## Scope

In scope:

- Vulnerabilities in bundled scripts.
- Unsafe generated guidance that could cause destructive actions, secret
  exposure, unapproved production effects, or credential leakage.
- Documentation that encourages insecure factory operation.

Out of scope:

- Security issues in downstream projects that use this skill.
- Misconfigured local Codex runtimes, shells, credentials, or repositories.
- Vulnerabilities in third-party tools invoked by a downstream project.

## Disclosure

Please allow a reasonable remediation window before public disclosure. The
maintainer will acknowledge reports as availability permits, triage impact, and
publish fixes or guidance when appropriate.
