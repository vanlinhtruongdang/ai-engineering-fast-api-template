# Evidence-led writing harness

This is an enforceable quality harness for documentation, code, code review,
agent responses, commit messages, comments, issue descriptions, and generated
artifacts in this repository. It applies regardless of whether a human, an
agent, or a tool produced the first draft.

Its purpose is to prevent the substantive failures that frequently travel with
formulaic AI-assisted writing: invented facts, unsupported importance claims,
vague relationships, fake citations, generic advice, and output that cannot be
audited or acted on. Do not treat it as a guide for concealing AI use or for
guessing who wrote a text.

The source that motivated this harness, [Wikipedia's signs of AI
writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), is an
observational field guide, not a detector and not a policy. A single stylistic
trait is never proof of AI use. In this repository, a trait is a prompt to
check the work's meaning, evidence, and fit for purpose.

## Scope and precedence

- This guide applies to natural-language and structured output authored or
  materially rewritten for the repository. It applies to English, Vietnamese,
  and other languages; use an equivalent rule when a literal phrase does not
  translate naturally.
- User requirements, public contracts, current source, tests, and the other
  repository guides remain the source of truth. This harness adds quality
  gates; it does not authorize a change outside the task scope.
- Follow format required by a consumer or an established project convention.
  For example, a release template, API schema, or tool protocol may require a
  heading, list, table, title case, or exact punctuation that this guide would
  otherwise discourage.
- Never rewrite prose merely to make it look less machine-generated. Correct
  the underlying claim, source, contract, structure, or user-facing purpose.

## Non-negotiable output contract

Before producing or changing an artifact, determine its reader, decision or
task, source of truth, and verification boundary. The output must make all four
clear enough for its consumer.

Every material statement is one of the following:

- **Fact**: supported by the current repository, a supplied source, command
  output, a verified external source, or an explicit user statement.
- **Assumption**: necessary but unverified. Label it, limit its consequence,
  and verify it when inexpensive and in scope.
- **Decision**: a chosen approach. State the trade-off and the evidence that
  supports it.

Do not convert an absence of evidence into a fact. Say exactly what was
checked and what was not found, for example, "I did not find a retry policy in
`src/client.py`". Do not claim that a feature, relationship, source, person,
or practice is undocumented, unavailable, private, common, or unimportant
without evidence adequate for that claim.

Do not add filler to make a response feel complete. Omit a section, sentence,
example, recommendation, future direction, or caveat unless it helps the
reader make the requested decision or perform the requested work.

## Content rules: replace generic significance with verifiable meaning

### State the fact, not its imagined importance

Do not inflate ordinary facts into claims about significance, legacy, wider
trends, cultural value, resilience, innovation, leadership, or an "evolving
landscape." Phrases such as "pivotal," "crucial," "vital," "a testament,"
"underscores," "lasting impact," and "key turning point" require a specific,
relevant source and a reader who needs that assessment.

Prefer the concrete event, actor, time, contract, measurement, or consequence.
For example, write "the endpoint returns `409` when the idempotency key belongs
to a different payload" instead of claiming that the endpoint "plays a crucial
role in reliable processing."

Do not append an `-ing` phrase that only announces an interpretation, such as
"highlighting its importance" or "demonstrating continued relevance." Keep it
only when the cited source itself makes that interpretation and attribution is
useful to the reader.

### Name relationships and owners precisely

Do not hide a relationship behind "associated with," "connected to," "in
connection with," "aligned with," or "related to." Name who did what, to
which component, under what authority, and when. If the relationship is
unknown, say that it is unknown; do not imply one.

Do not use vague groups such as "experts," "observers," "industry reports,"
"users," "reviewers," or "sources" as an authority. Identify the source or
speaker, accurately state its scope, and do not turn one or two examples into
"widely," "several," or "the industry" without evidence.

### Do not manufacture analysis or a complete-looking outline

- Do not create a generic "Challenges," "Future outlook," "Impact," "Awards
  and recognition," or "Conclusion" section merely because it is conventional
  in generated prose. Include it only when the user requested it or the
  repository has evidence that it is needed.
- Do not speculate about future adoption, initiatives, benefits, risks, or
  next steps. Describe an approved plan or a verified forecast with its owner,
  status, and source; otherwise omit it or clearly label it as a proposal.
- Do not use a three-item sequence, a positive/negative contrast, or a
  "not X, but Y" construction as decorative rhetoric. Use a list only when
  each item is necessary and the grouping is real.
- Do not treat a document title, a list name, or a broad category as a
  real-world actor. Describe the document, list, or category as such.

### Keep tone neutral and task-specific

Avoid promotional, travel-guide, press-release, or sales language. Terms such
as "seamless," "vibrant," "renowned," "groundbreaking," "rich," "showcases,"
"best-in-class," and "commitment to" normally conceal an untested value
judgment. Replace them with observable behavior, a supported quote, or remove
them.

Simple language is preferred. `is`, `are`, `has`, `uses`, `returns`, and
`fails` are often more accurate than "serves as," "stands as," "boasts,"
"features," "offers," or "represents." Do not avoid ordinary verbs to sound
formal.

## Documentation and response structure

### Build the smallest useful structure

- Start with the outcome, answer, or decision. Put implementation detail after
  it only when it helps the target reader.
- Give every heading a distinct purpose and at least one sentence, item, or
  artifact of its own. Do not repeat the document title as a heading, create a
  heading that contains only child headings, or skip heading levels.
- Match the repository's heading capitalization and markup style. Do not
  introduce title case, horizontal rules, or a top-level heading solely because
  a generic template uses them.
- Use prose for a simple explanation. Use a list for independent actions or
  criteria. Use a table only when readers must compare the same fields across
  multiple items. Do not turn one or two facts into a table.
- Do not make every list item an inline bold label followed by a colon. Use
  emphasis only for a term being defined or a genuinely important warning; do
  not bold a stream of keywords or a "key takeaways" list.
- Do not add emoji, decorative symbols, themed separators, or canned section
  names unless the user or the established artifact format requests them.
- Preserve exact typography required by source code, protocols, copy/paste
  commands, or a consumer. Else, keep punctuation and quotation marks
  consistent with nearby repository text.

### Do not leak drafting instructions into deliverables

Remove audience-directed chat, prewriting, and instructions before saving an
artifact. The final document must not say "here is a draft," "I hope this
helps," "would you like," "let me know," "copy and paste," or explain how the
reader should submit or use an artifact unless that instruction is the
requested content.

Resolve every placeholder. Block delivery if it contains `[TODO]`, `[Name]`,
`INSERT_*`, `TBD`, example URLs, dummy dates, unfinished template fields, or
instructions such as "add a source if available," unless the user explicitly
requested a reusable template and the placeholder is intentionally documented.

Do not leave a generic compliance assertion such as "follows all guidelines,"
"neutral and well-sourced," or "fully reviewed." Replace it with the actual
evidence: a rule applied, a file inspected, a test run, or a known limitation.

## Code, configuration, and technical claims

Natural language around code has the same evidence requirements as code.

- Never invent a module, function, API field, environment variable, command,
  HTTP status, configuration key, benchmark, test result, owner, or version.
  Inspect the source or label the item as a proposal.
- Do not present pseudo-code, an unrun command, a suggested test, or a
  hypothetical response as if it is current implementation behavior.
- Do not write code comments, docstrings, logging messages, commit messages,
  or PR text that narrate generic compliance, praise the change, or claim an
  effect not verified by a test or measurement.
- Preserve the contract's real vocabulary. Do not replace exact exceptions,
  result states, types, or ownership boundaries with vague abstractions for
  smoother prose.
- Keep explanatory examples minimal and runnable when labelled as examples.
  Mark fixtures, pseudocode, and illustrative values unambiguously; never let
  them resemble production configuration or citations.
- Do not add a "future work" implementation, alias, feature flag, extension
  point, or abstraction just to make a change look comprehensive. It requires
  a current consumer and acceptance case.

## Sources, links, and provenance

Do not cite a source until its target, identity, and relevance have been
checked.

- Verify that every URL resolves to the intended source and that the source
  supports the exact nearby claim. Search-result pages, snippets, titles, and
  a source's reputation do not prove the claim.
- Verify identifiers such as DOI, ISBN, issue, page, date, version, and commit
  hash when they matter. A valid-looking identifier can point to unrelated
  material.
- Do not invent a source, URL, author, citation field, publication date, page,
  quote, or attribution. Do not infer a source's position from its title.
- Keep citations adjacent to the claim they support. Do not append a source
  dump, unused references, or a bibliography that is not consumed by the
  document's assertions.
- Remove tracking parameters and links to search results when a canonical
  source URL is available. Retain a query parameter only when it is required
  for the resource to work or is part of the documented public contract.
- Treat an inaccessible, paywalled, stale, or ambiguous source as a limitation,
  not as permission to summarize from memory. State the limitation precisely.

Before publishing, scan generated or pasted content for leaked tool metadata
and malformed markup. This includes but is not limited to `contentReference`,
`oaicite`, `oai_citation`, `turn0search`, `attributableIndex`, `attached_file`,
`ppl-ai-file-upload`, `:::writing`, raw citation-renderer tokens, unmatched
markup, duplicate reference definitions, and placeholders. Remove the artifact
and restore a valid, checked citation or link; never edit only enough to hide
the leak.

## Agent communication and handoff rules

An agent response is a working artifact, not customer-service copy.

- Lead with the completed result or the blocking fact. Then provide only the
  evidence, limitation, decision, and next action needed by the user.
- Describe work that was actually done in past tense. Use future tense only
  for an explicit plan, and name the condition that must occur before it can
  happen.
- Do not use canned collaboration phrases, generic apologies, exaggerated
  agreement, repeated invitations for more work, or an unsolicited tutorial.
  A direct, task-specific question is allowed when the task cannot proceed.
- Do not expose private reasoning or imitate a review clerk. Give concise,
  inspectable rationale and evidence instead.
- Do not claim that an answer is complete, safe, compliant, tested, neutral,
  comprehensive, or production-ready without naming the corresponding scope
  and evidence. State what was not checked.
- Keep summaries operational: name changed files, affected behavior, commands
  run, and unresolved risks. Do not restate every procedural step or policy
  that was followed.

## Required review gates

Apply these gates before handing off a material document, response, code
change, or generated artifact. A reviewer may combine them in one focused pass.

1. **Purpose and scope**: Does every section, paragraph, list item, table,
   comment, and proposed change answer the user's request or an accepted
   verification need? Remove decorative completeness.
2. **Claim audit**: Can each material statement be classified as fact,
   assumption, or decision? Are actors, relationships, quantities, times, and
   ownership explicit?
3. **Source audit**: Does every cited or attributed claim have a checked,
   relevant source? Are identifiers, links, examples, and command results real
   and current enough for the claim?
4. **Language audit**: Remove unsupported significance, promotional language,
   vague attribution, weak associations, generic future/challenge conclusions,
   decorative triples, and formulaic contrasts. Prefer direct verbs and
   concrete nouns.
5. **Structure audit**: Is the format the smallest one that helps the reader?
   Check heading hierarchy, table necessity, emphasis density, placeholders,
   punctuation consistency, and leaked drafting or tool metadata.
6. **Technical audit**: For code or contract claims, inspect the source of
   truth and run the relevant verification described by the repository guides.
   Report the exact result and any verification not run.

## Severity and resolution

The following are blockers. Do not publish, commit, or present the work as
complete until they are fixed or explicitly accepted by the user: invented or
unverified technical behavior; a factual claim with no adequate source; a
source that does not support its claim; a broken or unrelated citation;
unresolved placeholder; leaked internal/tool citation metadata; invalid markup
or contract syntax; or a missing required verification result.

The following require a rewrite or a documented exception: unsupported
importance/impact language, vague associations or attributions, promotional
tone, a generic conclusion or future outlook, heading/list/table over-formatting,
repetitive emphasis, or canned agent language.

Do not fail work solely because it has excellent grammar, a formal tone, a
transition word, a curly quote, an em dash, a Markdown construct, a table, an
emoji, a short source list, or a phrase that happens to appear in this guide.
Assess the complete artifact and its evidence. A valid consumer requirement or
an established local convention is an acceptable exception when recorded in
the review or clear from the artifact.

## Compact handoff template

Use this only when it fits the requested response. Do not add empty labels.

```text
Completed: <observable change or answer>
Evidence: <source inspected, files changed, and checks run>
Limitation: <specific unverified or unavailable item>
Decision: <only if a material trade-off was made>
```

This template is a reporting aid, not text to paste into repository documents.
