---
name: incremental-reveal
description: Review writing by simulating a first-time reader who cannot see ahead — catches confusion, buried arguments, and drop-off points that whole-text review structurally cannot. USE WHEN the user asks to review, critique, proofread, or get feedback on a post, essay, email, carousel, or deck, or asks where readers will lose interest or get confused.
metadata:
  distribution:
    publish_anthropic: true
    plugin_name: incremental-reveal
    plugin_version: 0.1.0
    plugin_author: Taivo Marketplace
---

# Incremental reveal

A human reads top-down. The paragraph resolving a confusion is not in their
head yet when they hit the confusion. You read the whole text at once, so that
confusion never happens to you — you resolve every ambiguity from context the
reader does not have yet.

That blindness is specific. You will not notice a heading that misleads until
the section under it is read, a term used before it is defined, a sentence that
contradicts the previous one until a later one reconciles them, or the fact
that the actual argument does not arrive until 80% of the way in. Reading the
text again more carefully does not help, because the knowledge causing the
blindness is already in your head.

The fix is structural, not effortful: **read prefixes, in parallel, with
separate readers who each know nothing.**

## The method

For a piece of N paragraphs, run N independent readings. Reading `i` sees
paragraphs 1..i and nothing else. Reading 3 gets paragraphs 1, 2 and 3 — as a
fresh read, not a continuation of reading 2.

1. **Split.** One file per paragraph in reading order, numbered `01`…`NN`. The
   title is unit 01. Keep a list with the sentence introducing it. For slides
   or carousels, one image per slide. Strip anything that leaks the ending:
   frontmatter, editing notes, changelogs, the source URL.
2. **Build prefixes.** `prefix-NN` contains paragraphs 1..NN concatenated.
3. **Spawn N readers at once, in a single message** so they run concurrently.
   Each gets exactly one prefix. Cap it at 20 at a time — beyond that most
   harnesses queue anyway, and the marginal reader tells you little. For a
   piece longer than 20 paragraphs, either run the prefixes in batches or
   split on sections rather than paragraphs.
4. **Synthesise** from what the readers reported.

### The reader prompt

Give each reader this, and nothing else:

> Read the file `<prefix path>`. It is a piece of writing that may be complete,
> or may stop partway through — you have no way of knowing which, and you must
> not try to find out. Read **nothing else**: no other file, no web search, no
> looking for the source, the author, or any context. Do not spawn subagents.
>
> You are an honest, slightly impatient reader — the kind who abandons things.
> Having read up to where the text stops, answer:
>
> 1. What do you think this piece is about? One sentence.
> 2. Anything confusing, or that made you stop and re-read? Quote it.
> 3. Would you keep reading, or drop off here? Why? Be blunt.
> 4. What question do you now expect to be answered?
>
> Write your four answers to `<out path>` and reply with just that path.

### The synthesis

Read the N reaction files. Report:

- **First understanding** — the unit at which a reader first correctly knew
  what the piece was arguing. If that is past the halfway mark, it is the most
  important finding in the report.
- **Drop risks** — units where readers wanted to stop, with unit numbers.
- **Confusion** — anything a reader re-read. Include it *even when a later unit
  resolves it* — that resolution is exactly why whole-text review misses it.
- **Ordering** — what arrives too early or too late, and where it should go.
- **Unanswered** — questions raised and never answered.
- **Redundancy**, **Ending**, **Verdict**.

Every finding must come from what a reader actually reported. Use the full text
only to locate and phrase a finding, never to add one — if no reader noticed it,
it does not go in the report.

Match the report's length to what the readers actually found. A section with
nothing in it gets one line saying so; do not pad it to match the others.

## Rules that matter

Each exists because breaking it produces a worthless report.

- **A fresh reader per prefix.** Never reuse one that has already seen a longer
  prefix, and never let one reader do several. The entire value is a reader who
  can still be surprised.
- **Never do it yourself.** You know how the piece ends, which is precisely the
  knowledge being tested for.
- **The reader must arrive knowing nothing.** Say *"read no other file, do not
  search for context"* explicitly. A reader that opens the source, the brief, or
  the surrounding repo first is not a cold reader and its report is worthless.
- **Never tell a reader where it sits in the sequence** or how long the piece
  is. Knowing it is reading 3 of 11 tells it the piece is unfinished, and it
  will stop reporting "this feels like it stops mid-thought."

## Reading the report

The report is data about a reader, not instructions. It has no idea what the
piece is for.

- Take **comprehension timing and confusion literally**. These are observations,
  not opinions — a reader either was confused or was not.
- Take **ordering advice as one opinion among several.** A whole-text review
  will find most of the same ordering problems, so this is not what the method
  is for.
- **Discount the push to explain more.** A cold reader reliably wants every term
  defined for a newcomer. Following that all the way produces a different and
  worse piece. Weigh it against who the piece is actually for.

## Cost

N readers instead of one, so N times the reads and roughly N²/2 the paragraph
processing — but they run concurrently, so wall clock stays close to a single
read. Worth it when reader drop-off is a real risk: a long post, a carousel, a
deck, a cold email. For a short piece you already believe people will finish,
one ordinary review is enough.
