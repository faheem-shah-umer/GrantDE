# Security

Do not include passwords, tokens, private keys or personal documents in issues
or pull requests. Use GitHub's private vulnerability reporting feature if it is
available on this repository. Otherwise report a minimal, non-sensitive issue
requesting a private contact channel before sharing exploit details.

Only the current main branch is maintained. Dependency alerts and automated
checks help identify problems; they do not guarantee that the project is free
of vulnerabilities. The local preview server is for loopback development.

Local credentials, operator configuration, raw captures, tests and generated
files are excluded from Git. Review `git diff --cached` before each commit.
If a secret is ever published, revoke it first; deleting the file alone does
not remove it from history.
