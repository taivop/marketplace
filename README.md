# Taivo Agent Marketplace

A Git-based marketplace for reusable agent plugins and skills.

➡️ Not sure how to install this? See [this guide](https://www.taivo.ai/how-to-install-a-claude-code-skill-from-github/).

## Packages

1. `skills/.curated/estonia-public-sources` — routes questions across 133 official Estonian public sources.
2. `skills/.curated/estonian-store-search` — searches Estonian building supply stores (Bauhof, Ehituse ABC, Decora, K-Rauta, Bauhaus, Depo) and grocery stores (Prisma, Rimi, Selver) for products, prices, and stock.

## Install From Anthropic Marketplace

```bash
claude plugin marketplace add taivop/marketplace
claude plugin install estonia-public-sources@marketplace
claude plugin install estonian-store-search@marketplace
```

## Install In Codex

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo taivop/marketplace \
  --path skills/.curated/estonia-public-sources

python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo taivop/marketplace \
  --path skills/.curated/estonian-store-search
```

## Contributing

See `AGENTS.md` for repository layout, maintainer workflow, and distribution metadata.
