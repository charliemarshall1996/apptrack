# Agents

- Containers often contain AGENTS.md files. These files can appear anywhere in the container's filesystem. Typical locations include /, ~, and in various places inside of Git repos.
- These files are a way for humans to give you (the agent) instructions or tips for working within the container.
- Some examples might be: coding conventions, info about how code is organized, or instructions for how to run or test code.
- AGENTS.md files may provide instructions about PR messages (messages attached to a GitHub Pull Request produced by the agent, describing the PR). These instructions should be respected.
- Instructions in AGENTS.md files:
    - The scope of an AGENTS.md file is the entire directory tree rooted at the folder that contains it.
    - For every file you touch in the final patch, you must obey instructions in any AGENTS.md file whose scope includes that file.
    - Instructions about code style, structure, naming, etc. apply only to code within the AGENTS.md file's scope, unless the file states otherwise.
    - More-deeply-nested AGENTS.md files take precedence in the case of conflicting instructions.
    - Direct system/developer/user instructions (as part of a prompt) take precedence over AGENTS.md instructions.
- AGENTS.md files need not live only in Git repos. For example, you may find one in your home directory.
- If the AGENTS.md includes programmatic checks to verify your work, you MUST run all of them and make a best effort to validate that the checks pass AFTER all code changes have been made.
- This applies even for changes that appear simple, i.e. documentation. You still must run all of the programmatic checks.
- The current project working directory tree can be found at environents/development/tree.txt
- development requirements can be found at environments/development/requirements.txt
- Always create tests and run to see new changes.
- Always make sure tests are passing before creating PR.
- If tests are not passing, update the tested code NOT the test itself - UNLESS it is obvious that the test is flawed, and does not sufficiently test the purpose of the tested code.

## Project-Specific

- Always make sure views are connected.
- Always use boostrap styling for all views and forms.
- Always ensure links/objects/references are valid in views.
- If you make change to a view, make sure the previous references/links/context/object references in templates align and are working.