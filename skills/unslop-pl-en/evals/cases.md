# Regression cases

Run after every change to `SKILL.md` or `references/`. Use Check mode for cases 1-12 and compare findings with "Must flag" and "Must leave alone". Over-flagging a "Leave alone" item is a regression. For rewrite cases, "Expected rewrite" shows the intent, not the only acceptable wording; what counts is that facts survive and the listed defects go. All inputs are invented.

## 1. PL: invented opponent (P1, even once)

> Doradca podatkowy z praktyki, nie teoretyk przepisów. 12 lat w biurach rachunkowych.

- **Must flag:** "nie teoretyk przepisów" as an invented opponent.
- **Expected rewrite:** "Doradca podatkowy z 12-letnią praktyką w biurach rachunkowych." No added facts.
- **Leave alone:** "12 lat w biurach rachunkowych".

## 2. PL: delivery calque and colloquial verb

> Prowadzę dostarczanie wdrożeń ERP i spinam współpracę między księgowością a działem IT.

- **Must flag:** "dostarczanie" (calque), "spinam" (colloquial).
- **Expected rewrite:** "Prowadzę wdrożenia ERP i koordynuję współpracę między księgowością a działem IT."
- **Must not:** change the operation into "umożliwiam" or invent a result.

## 3. PL: tense against dates (P1)

> 03.2012 – 09.2020 | Kierownik działu | Firma X
> Kieruję zespołem czterech osób i odpowiadam za budżet.
>
> 10.2020 – obecnie | Dyrektor | Firma Y
> Kieruję zespołem dziesięciu osób.

- **Must flag:** first block in the present tense although it ended in 2020.
- **Leave alone:** second block, present tense for the current role.
- **Expected rewrite:** "Kierowałem zespołem czterech osób i odpowiadałem za budżet." Masculine first person kept; no "Wdrożyłem" or other new facts.

## 4. PL: mixed address (P1)

> Uczymy na Waszych danych. Umów rozmowę i zaplanujmy szkolenie dla Twojej firmy.

- **Must flag:** Wy / Ty mix. **Expected:** one form throughout; the choice is noted.

## 5. PL: slogans without content (P1 at three)

> Jeden panel. Pięć systemów. Zero chaosu.
> Prostota, która działa.
> Mniej klikania. Więcej sprzedaży.

- **Must flag:** slogan cadence, missing facts.
- **Expected:** a gap note ("brak: które systemy, ile klików mniej"), not an invented number. Cutting is acceptable.

## 6. PL: clean passage, must stay clean

> Aplikację napisaliśmy w trzy miesiące. Pierwsza wersja miała 40 ekranów i działała tylko na iPadzie; po testach z trzema przedszkolami zostawiliśmy 18. Najwięcej czasu zajęło logowanie rodziców, bo każde przedszkole miało własną listę uprawnień.

- **Must leave alone:** the whole passage. Any edit is a regression.

## 7. PL: contrast look-alikes, must stay

> Spotkanie jest w środę, nie we wtorek. Wynik wzrósł o 40%, nie o 4%. Zdjęcie jest prawdziwe, nie z archiwum.

- **Must leave alone:** all three (correction, corrected figure, authenticity).

## 8. EN: stock vocabulary and negative parallelism

> We leverage cutting-edge AI to unlock seamless workflows. It's not just a tool, it's a game changer for your team.

- **Must flag:** leverage, cutting-edge, unlock, seamless, "not just … it's", game changer.
- **Expected:** a gap note for the missing mechanism and result; no invented numbers.

## 9. PL -> EN translation with ledger

> Reforma objęła 50+ klientów i została zakończona terminowo, bez kar. Zespół liczył do 25 osób. Materiały przygotowuję tuż przed szkoleniem; nie jest to porada prawna.

- **Ledger:** 50+, terminowo, bez kar (two claims), do 25, "przygotowuję", "tuż przed", negation "nie jest to porada prawna".
- **Must keep:** "up to 25" (not 25), "50+" or "more than 50" with the note, both claims "on schedule" and "without penalties", the negation.
- **Must not:** merge the two claims into "successfully", add "high-quality".
- **Output:** translation plus ledger check and decisions.

## 10. EN -> PL translation of a slogan

> Ready to take your close to the next level? Join thousands of finance leaders unlocking the full potential of their data.

- **Must flag in the notes:** empty slogan, unverifiable "thousands".
- **Must not:** translate to "wynieść na wyższy poziom" or "odblokować pełen potencjał" as a stock Polish phrase; render the plain information, or keep the claim at its actual strength and flag it.
- **Address form:** one form, stated.

## 11. Typography

> To jest „szybkie" rozwiązanie — naprawdę. Cena: 3.5 zł i 2,5 zł.

- **Must flag:** closing straight quote, unspaced or stray em dash, decimal point mixed with comma.

## 12. Load-bearing language (legal)

> Pracownik nie może zostać zwolniony w okresie ochronnym, chyba że pracodawca wykaże rażące naruszenie obowiązków.

- **Must leave alone:** the whole sentence. Softening "nie może" or dropping "chyba że" is a regression.

## 13. Voice preserved in a rough human draft

> Szczerze? Ten projekt prawie mnie wykończył. Trzy razy zmienialiśmy bazę, a klient i tak chciał Excela. Skończyło się na Excelu.

- **Must leave alone:** the blunt tone, the humor, "Skończyło się na Excelu." Minimal or no edits; "Szczerze?" belongs to this writer.

## 14. Translation audit (both texts supplied)

Source: "Wynik wzrósł o ok. 40% w 2024 roku." Translation: "The result increased by 40% in 2024."

- **Must flag:** "ok." lost (approximation became exact).

## 15. Mixed-language document

A Polish page with an English summary block: apply `polish.md` to the Polish passages and `english.md` to the English block; do not flag English "workflow" or "backlog" inside Polish text.
