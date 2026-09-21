# Taivo Agent Marketplace

Reusable agent skills by Taivo Pungas. Read the [overview and examples on taivo.ai](https://www.taivo.ai/projects/skills/), then install the skills you want from this repository.

## Packages

| Skill | What it does |
|---|---|
| [Coach](skills/coach/) | Helps you think through something you are stuck on. |
| [Incremental reveal](skills/incremental-reveal/) | Uses independent readers to find where writing becomes confusing or loses their interest. |
| [Subtract](skills/subtract/) | Finds what you can remove from a plan, process, design, or document. |
| [Estonian store search](skills/estonian-store-search/) | Compares products, prices, and availability across Estonian stores and second-hand marketplaces. |
| [ESTER library search](skills/ester/) | Finds books and checks availability at Estonian library branches. |
| [Estonian newspaper archive](skills/estonian-newspaper-archive/) | Searches DEA/DIGAR for historical articles, scans, and issue PDFs. |

Incremental reveal needs an agent environment that supports independent agents and files. The search skills need web access; ESTER also uses Python parser scripts included in its directory.

The Estonian public-sources skill is largely superseded by [Kodaniku Kratt](https://kratt.taivo.ai/) and has been removed from this marketplace. Coloring book has also been retired. Their earlier versions remain in Git history.

## Install in Claude Code

Add the marketplace once, then install the plugin you want. For example:

```bash
claude plugin marketplace add taivop/marketplace
claude plugin install coach@marketplace
```

Replace `coach` with `incremental-reveal`, `subtract`, `estonian-store-search`, `ester`, or `estonian-newspaper-archive` to install another package. See the [installation guide](https://www.taivo.ai/how-to-install-a-claude-code-skill-from-github/) for the desktop workflow.

## Install in Codex

Ask Codex's skill installer to install a package from its GitHub directory:

```text
$skill-installer install https://github.com/taivop/marketplace/tree/master/skills/coach
```

Replace `coach` with another package's directory name from the table above. Install the entire directory, including its supporting files. If the new skill does not appear, restart Codex. See the [Codex skills documentation](https://developers.openai.com/codex/skills/).

## Contributing

See [AGENTS.md](AGENTS.md) for repository layout, maintainer workflow, and distribution metadata.

When adding, removing, renaming, or materially changing a skill, also update the [public skills overview on taivo.ai](https://www.taivo.ai/projects/skills/) so its descriptions, examples, and links stay current. Skill instructions and supporting files live here; the overview introduces them and links back.
