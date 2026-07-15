# Taivo Agent Marketplace

A Git-based marketplace for reusable agent plugins and skills.

➡️ Not sure how to install this? See [this guide](https://www.taivo.ai/how-to-install-a-claude-code-skill-from-github/).

## Packages

1. `skills/estonia-public-sources` — routes questions across official Estonian public data sources.
2. `skills/estonian-store-search` — searches Estonian building supply stores (Bauhof, Ehituse ABC, Decora, K-Rauta, Bauhaus, Depo) and grocery stores (Prisma, Rimi, Selver) for products, prices, and stock.
3. `skills/ester` — searches the Estonian library catalog ESTER (ester.ee) for books, availability, and branch holdings.

## Install From Anthropic Marketplace

```bash
claude plugin marketplace add taivop/marketplace
claude plugin install estonia-public-sources@marketplace
claude plugin install estonian-store-search@marketplace
claude plugin install ester@marketplace
```

## Install In Codex

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo taivop/marketplace \
  --path skills/estonia-public-sources

python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo taivop/marketplace \
  --path skills/estonian-store-search

python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo taivop/marketplace \
  --path skills/ester
```

## Contributing

See `AGENTS.md` for repository layout, maintainer workflow, and distribution metadata.
