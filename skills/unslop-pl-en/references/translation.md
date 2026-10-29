# Translation protocol (PL <-> EN)

Goal: the target text says exactly what the source says, at the same strength, and reads as if a native professional wrote it. Two failures to avoid: a faithful-looking translation that carries over the source's phrasing (a calque), and a fluent one that quietly changed a number, a hedge or a scope.

Use for the Translate and Verify translation modes. Also read `polish.md` or `english.md` for the target language, and `glossary.md` for terms.

## 1. Before translating: frame

State to yourself, or ask in one line only when it changes the result:
- direction and target audience (the web page of a firm, a CV, an email, a legal note);
- register of the source and of the target (the same);
- form of address in Polish targets (Ty / Wy / Państwo), and the gender of a first-person author when translating into Polish (choose neutral phrasing if unknown and note it);
- fixed terms: proper names, product names, official names of institutions (glossary).

## 2. Build the fact ledger from the source

Read the source once and list, in compact form, every item that must survive:

| Class | What to capture |
|---|---|
| Numbers | every figure with unit, sign, range ends, "+" and "up to", currency, percent base |
| Dates and durations | exact dates, "since", "until now", periods, tense of ended vs ongoing |
| Names | people, organizations, products, laws and regulations, article numbers, identifiers |
| Quantifiers and scope | all / most / some / only / at least / about; who the claim covers |
| Modality | must / shall / should / may / can; musi, powinien, może, wolno, nie wolno |
| Negations and conditions | not, never, unless, if, provided that; each stays a negation or condition |
| Cause, comparison, simultaneity | because / so / while; "x times faster", "reduced from A to B" |
| Quotes | verbatim; keep attribution |
| Structure | number of list items, order, headings, line breaks |

For a short text, hold the ledger in your head and report it as one line. For anything with figures or obligations, write it out.

## 3. Translate meaning, not construction

1. Read a sentence, state what it claims, then write that claim the way a native professional would. Reorder, split or merge sentences when the target needs it.
2. **PL -> EN:** English wants an actor and a verb. Unpack nominal chains ("przeprowadzenie wdrożenia rozwiązania") into "implemented the tool". Add articles by what the reader already knows. Replace Polish impersonal and passive constructions with a named actor when the source gives one. Pick the English word by context: wdrożenie = implementation / deployment / rollout; szkolenie = training / course / workshop (by length and format); przypadek = case / use case / scenario.
3. **EN -> PL:** Polish dislikes stacked noun phrases and "-ing" chains. Turn "AI-powered customer experience optimization platform" into a clause: "platforma, która za pomocą AI poprawia obsługę klientów" (only if the source means that). Avoid word-for-word idioms ("take to the next level", "unlock potential", "best-in-class") and see `polish.md` section 1. Choose the address form once and keep it.
4. **Terms:** use the glossary form. First mention of an institution or acronym gets the full name plus the acronym in the target language when the reader may not know it ("Urząd Regulacji Energetyki (URE)" / "the Energy Regulatory Office (URE)").
5. **Empty source phrases.** If the source contains a slogan with no content ("unlocking the full potential of their data"), render its actual information in plain target-language wording; do not substitute a stock phrase of the target language, and do not strengthen it. Flag it in the notes and offer to cut or make it concrete.
6. **Do not improve the content.** Translation preserves claims, including weak or inflated ones. Unslopping the source is a separate request; offer it.
7. **Do not add** explanatory glosses the source lacks, softening hedges, a sales tone, or formality the source did not have.

## 4. Verify before returning

1. **Ledger diff.** For each ledger item: present in the target, same value, same strength. Mismatches are fixed, not reported as acceptable.
2. **Back-translation of risk sentences.** Re-read each sentence that carries a number, an obligation, a negation, a condition or a hedge as if translating it back; compare with the source. Do this for every such sentence, not a sample.
3. **Calque scan** of the target against the language file.
4. **Mechanical check:** `python3 -I scripts/lint.py <target file> --lang pl|en` for quotation marks, dashes, number format, address form.
5. **Consistency:** one term per concept throughout, one address form, one number format.

## 5. Output

```
<translation>

Kontrola / Check
- Ledger: <n> figures, <n> names, <n> hedges/negations/conditions - all present and unchanged.
- Decisions: <each place where the target had to choose: term, address form, gender, ambiguity in source>
- Gaps and source issues: <unclear or unsupported claims, missing facts, empty slogans; nothing is silently fixed>
```

Write the note in the language of the user's request (an English request with a Polish deliverable gets an English note; the translation itself is never mixed with the note). Quote spans in their original language. Spelling variant in English targets (US or UK): follow the user's existing material, otherwise state the choice. Use the plain-text characters of the target (no non-breaking spaces) unless the output is a file for publication. For Verify translation (both texts supplied), return only the check: a table of each discrepancy with source span, target span, class (number / scope / modality / negation / omission / addition / calque) and the correction.

## 6. Pitfalls specific to this pair

| Source | Trap | Handling |
|---|---|---|
| Polish "Wy / Państwo" | English has one "you" | note the loss; do not add "dear" or "kindly" |
| Polish masculine/feminine first person | English is neutral | no gender shown in English; keep it in Polish when the source is Polish |
| "50+" | not "over 50" in every context | "50+" or "more than 50" only if the source means exclusive |
| "terminowo i bez kar" | "on schedule and without penalties" | keep both claims; do not merge into "successfully" |
| "do 25 osób" | "up to 25" | not "25" |
| "może", "powinien" | may / should / might | keep the grade of obligation |
| "nie" before a verb in a list | easy to drop in a long sentence | check every negation in the ledger |
| "około", "ok.", "ponad" | approximation / lower bound | keep the approximation word |
| Headings in Polish sentence case | English title case | keep the target's convention consistently |
| Fragments without a verb in Polish headings | English also tolerates them | keep as fragments, not as invented full sentences |
