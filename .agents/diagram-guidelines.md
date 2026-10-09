# Diagram guidelines

Read this guide before creating, changing, or reviewing a diagram, diagram
asset, or documentation page that relies on one.

## Deliverable contract

- Create a diagram only when it answers a design, operational, or algorithmic
  question that prose does not make easy to inspect. Do not use one as
  decoration or to repeat a short list.
- Deliver each diagram with its editable source, reading guide, and screenshot
  in `docs/diagrams/<topic>/`: `<diagram>.drawio`, `<diagram>.md`, and
  `<diagram>.drawio.png`. All three are required and must be stored in the
  repository. An SVG export may supplement the screenshot.
- Use [`assets/diagrams/component-library.drawio`](../assets/diagrams/component-library.drawio)
  as the first source of reusable components. It is self-contained: copied
  components do not depend on a local image path.
- Import individual SVGs from `assets/diagrams/icons/` only when a library
  component does not fit. Preserve the source notice and do not edit a
  third-party SVG merely to recolor or rebrand it.
- Search `assets/diagrams/catalog.json` by title or category to find a local
  SVG and its source. The palette separates AI, backend, database, network,
  platform, and observability components into pages; Fluent regular and color
  variants have separate pages. Keep one icon style within a diagram.

## Required reading guide and screenshots

Every diagram must have a corresponding reader-facing guide that explains
its meaning and goal. The guide must include:

1. The intended reader, the question the diagram answers, and the scope it
   covers. State what the reader should understand after reading it.
2. The screenshot embedded with a relative Markdown image link, meaningful
   alt text, and a caption identifying the diagram or page it depicts. A
   screenshot must be an actual capture or PNG render of the final `.drawio`
   source; do not substitute a separately drawn approximation.
3. A legend for the symbols, colors, boundaries, arrow directions, and line
   styles used. Explain how to start reading and which direction to follow.
4. An explanation of the components and relationships using the same names
   as the diagram. Walk through the main flow; explain decisions, failure,
   retry, or review paths when the diagram includes them. For a static
   architecture or data model, explain ownership and dependencies instead.
5. References linking to the editable `.drawio` source and the corresponding
   code, contracts, configuration, architecture decisions, or documentation
   that support the diagram. Identify the relevant page, component, step, or
   relationship for each reference. Label proposed behavior and assumptions
   explicitly; do not invent supporting references.

For a multi-page diagram, the guide must have a named section and its own
screenshot for every page. Use `<diagram>-<page>.drawio.png` for those images
and identify the corresponding Draw.io page in each caption and reference.

Whenever a diagram changes, regenerate its screenshots and update its guide
and references in the same change. Inspect the actual screenshots for cropped
labels, unreadable text, missing icons, and obstructed connectors. Temporary
files, external-only image links, and a screenshot without an explanation do
not satisfy this contract.

## Choose the smallest useful diagram

| Reader question | Diagram | Required information |
| --- | --- | --- |
| Where is the system boundary? | System or container architecture | Actors, owned components, external systems, and trust boundaries |
| What happens over time? | Sequence or workflow | Trigger, ordering, sync versus async calls, failure and terminal outcomes |
| What can a durable process become? | State diagram | Initial state, transition, recovery path, and terminal states |
| How does data move or persist? | Data flow or ER diagram | Producer, consumer, storage, and ownership or retention when material |
| How does logic branch? | Flowchart | Input, decision, failure path, and output |
| How is traffic exposed or protected? | Network diagram | Ingress, zone, routing, identity or security boundary, and egress |

Split a diagram when it answers more than one reader question or needs a
legend to explain ordinary arrows.

## Visual and semantic rules

1. Title the diagram with its reader question. Use left-to-right for requests
   and top-to-bottom for time or state changes.
2. Label a connector with an operation, event, protocol, or contract. An
   unlabelled connector is permitted only when one relationship type is
   obvious and used consistently.
3. Use a labelled dashed container for a named trust, network, deployment, or
   ownership boundary. Do not use a container only for visual grouping.
4. Use role labels even when a logo is present. A logo identifies a product;
   the role label states why it exists in the design.
5. Use a technology logo only when the technology is verified in current
   source, configuration, an approved architecture decision, or explicit user
   requirements. Use the semantic component when the implementation remains a
   choice.
6. Keep normal flow solid. Dashed connectors mean asynchronous, optional, or
   control-plane flow and require a legend when mixed with solid connectors.
7. Show retry, failure, human review, and terminal paths only when they are
   part of the represented behavior. Do not imply reliability or authorization
   guarantees without source evidence.
8. Do not include credentials, payloads, customer data, production hostnames,
   internal addresses, or other sensitive operational details.

Use the library's palette: blue for interface or compute, teal for storage or
transport, purple for AI, red for security or failure, and slate for platform
or a named boundary. Keep dark text on a light canvas and use orthogonal
connectors for architecture and network diagrams.

## Completion checks

- The editable `.drawio` source opens and every copied component remains
  visible without files outside the repository.
- Every component and boundary has a role or owner label.
- Every connector has a clear direction and meaning.
- The diagram agrees with the current source or labels an unverified design as
  a proposal.
- The corresponding guide explains the goal, legend, reading order,
  components, and relationships, with relevant source references.
- Every page has a readable screenshot embedded in the guide; each screenshot
  matches the final editable source and has a caption and meaningful alt text.
- Guide links and image paths resolve to the intended files or references.
- Do not mark a diagram complete or hand it off as finished if its guide,
  screenshots, or references are missing or stale. Report the missing artifact
  when rendering or verification is blocked.
