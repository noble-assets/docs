# Docs Style Guide / Requirements

## Purpose

This file defines **strict rules and requirements** for writing and rewriting technical documentation for the Noble project.
Follow these instructions exactly when generating, editing, or restructuring documentation content.

## General Writing Rules

* Always use **imperative voice** (“Do X”, “Run Y”) instead of passive voice.
* Always use **plain, direct English**. Avoid unnecessary jargon and filler words.
* Always assume the reader is technical but new to the Noble project. Provide context where needed, but keep explanations concise.
* Always prefer **short sentences** over complex ones.
* Never include marketing language, hype, or unverified claims.

## Formatting Rules

* Use **Markdown** as the only output format.
* Use `#` for top-level headings, `##` for subsections, and `###` for sub-subsections.
* Always include a **one-sentence summary** at the top of each page explaining its purpose.
* Always use **fenced code blocks** with the correct language identifier.
* Use **bold** for emphasis, never italics.
* If the contents of a list include full sentences, always end with a dot. If the items just enumerate or list individual things, then do not use a dot.
* Use **ordered lists** for sequences of steps. Example:

  ```markdown
  1. Install dependencies.  
  2. Configure the environment.  
  3. Run the setup script.  
  ```

* Use **unordered lists** for unordered items. Example:

  ```markdown
  - Validators  
  - Full nodes  
  - Light clients  
  ```

## Style Rules

* Always introduce acronyms on first use. Example: “Inter-Blockchain Communication (IBC)”.
* Always link to related documentation pages instead of duplicating explanations.
* Always write in the second person (“You will…”, “Run the following…”) when addressing the reader.
* Always front-load context: start each section with what the reader will achieve or learn.
* Always include example output for commands where appropriate.
* Never include placeholder text like “TBD” or “Coming soon”.
* Never assume prior knowledge beyond general blockchain and web knowledge.

## Structural Rules

When rewriting or creating documentation pages:

1. Start with a one-sentence purpose statement.
2. Provide background context if necessary (maximum 2 sentences).
3. Present steps or instructions in order, with code blocks and examples.
4. End with references, links, or next steps.

## Maintenance Rules

<!-- TODO: is this necessary? -->
* Ensure every page can be read **independently** without requiring another doc for basic understanding.
* Ensure terminology is consistent across all pages.
* Ensure no outdated references remain.

