# unslop-pl-en

> [!IMPORTANT]
> **This plugin has moved to [r4vk/r4vk-skills](https://github.com/r4vk/r4vk-skills).** New versions are released there. The install instructions below describe the old marketplace. To switch, follow these steps in Claude Code:
>
> 1. `/plugin marketplace add r4vk/r4vk-skills`
> 2. `/plugin marketplace remove unslop-pl-en`
> 3. `/plugin install unslop-pl-en@r4vk-skills`
>
> If you added the skill manually (a `.skill` file or `~/.claude/skills/`), remove that copy too.
>
> *Plugin przeniesiono do [r4vk/r4vk-skills](https://github.com/r4vk/r4vk-skills). Nowe wersje będą wydawane tam. Instrukcja instalacji poniżej dotyczy starego marketplace.*

A Claude skill that keeps Polish and English text from reading as AI-generated, and keeps translations between the two faithful.

*Skill dla Claude, który pilnuje, żeby polskie i angielskie teksty nie brzmiały jak wygenerowane przez AI, a tłumaczenia PL<->EN zachowywały treść.*

## What it does

- **Write, Check, Rewrite, Edit file:** works on three levels (words, sentence rhythm, structure), with strictness profiles per register (web copy, bio/CV, article, email, docs, academic, slides).
- **Polish-specific rules:** calques from English ("praktyk dostarczania" for *delivery practitioner*, "butikowy", "adresować problem"), colloquial verbs in professional copy, address form (Ty / Wy / Państwo) kept to one per document, past tense for roles that ended, aspect, quotation marks „…”, dashes, non-breaking spaces.
- **English rules:** word tiers, contrast patterns ("not X, it's Y"), kickers, and issues typical for Polish authors (false friends, nominal stacks).
- **Invented-opponent rule:** "Praktyk wdrożeń, nie teoretyk norm" is replaced by a plain statement of what the person does, from facts in the text.
- **Translate and Verify translation (PL<->EN):** builds a fact ledger (numbers, names, dates, hedges, negations, scope), translates meaning rather than construction, then checks the result against the ledger. Gaps are reported, never filled in.
- **Guardrails:** no invented facts, no lost claims, no change in strength ("około" stays approximate, "do 25" stays "up to 25"), voice preserved, minimal edits.
- **Linter** (`scripts/lint.py`): deterministic checks for what a model reads past. Candidates only; the model judges in context.

It is not a tool for evading AI detectors or disclosure duties.

## Install

### Claude Code (with automatic updates)

```
/plugin marketplace add r4vk/unslop-pl-en
/plugin install unslop-pl-en@unslop-pl-en
```

Update later with `/plugin marketplace update unslop-pl-en`, or enable auto-update for the marketplace in the `/plugin` menu. Claude Code installs a new version only when `version` in the manifests changes, so every release bumps it.

### Claude Desktop, Claude.ai, Cowork

Download `unslop-pl-en.skill` from the latest [release](https://github.com/r4vk/unslop-pl-en/releases) and add it under Settings -> Capabilities -> Skills. This route does not auto-update; re-download after a release.

### Manual

Copy `skills/unslop-pl-en/` into `~/.claude/skills/`.

## Use

Just ask. Examples:

```
Popraw ten tekst, brzmi jak AI: <tekst>
Sprawdź, co w tym tekście wygląda na wygenerowane (tylko lista, bez poprawek)
Przetłumacz na angielski i sprawdź, że niczego nie zgubiłeś
Does this read like AI? <text>
Translate to Polish and verify the numbers and hedges
```

Run the linter yourself:

```bash
python3 -I skills/unslop-pl-en/scripts/lint.py page.html
python3 -I skills/unslop-pl-en/scripts/lint.py draft.md --lang pl --json
```

## Layout

```
.claude-plugin/        plugin.json, marketplace.json
skills/unslop-pl-en/
  SKILL.md             modes, levels, guardrails
  references/          polish.md, english.md, translation.md, glossary.md
  scripts/lint.py      mechanical checks
  evals/cases.md       regression cases
tests/test_lint.py     unit tests for the linter
```

## Customize

- Add terms to `references/glossary.md` (one preferred rendering per row).
- Add stock phrases and calques to `references/polish.md` or `english.md`, and a regex to `scripts/lint.py` if the pattern is mechanical.
- When you add a rule, add one example it must catch and one look-alike it must leave alone to `evals/cases.md`.

## Releasing

1. Change the skill, update `evals/cases.md`, run `python3 -I -m unittest discover -s tests`.
2. Bump `version` in `.claude-plugin/plugin.json` **and** `.claude-plugin/marketplace.json` (CI checks they match) and add a line to `CHANGELOG.md`.
3. Tag and push: `git tag v0.1.1 && git push --tags`.

## Credits

Inspired by [no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter Yang and [unslop](https://github.com/jlwin/unslop_ai) by Jean-Luc Winkler (both MIT). The rules, lists and examples here are written for Polish and English; no text is copied.

## License

MIT, see [LICENSE](LICENSE).
