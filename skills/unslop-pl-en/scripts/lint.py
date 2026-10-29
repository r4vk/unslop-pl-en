#!/usr/bin/env python3
"""Mechanical checks for Polish and English prose. Advisory only.

Usage:
    python3 -I lint.py FILE [--lang pl|en] [--json] [--min-sev P0|P1|P2]
    cat text.md | python3 -I lint.py - --lang pl

Accepts .md, .txt and .html (tags are stripped). Every finding is a candidate:
the script has no morphology and no taste, so a model or a person must judge
each hit in context. Exit status is always 0.
"""
import argparse
import datetime
import json
import re
import sys
from html.parser import HTMLParser

SEV_ORDER = {"P0": 0, "P1": 1, "P2": 2}

# ---------------------------------------------------------------- word lists

PL_STOCK = [  # P1: stock phrases and inflated vocabulary
    r"kompleksow\w+", r"holistyczn\w+", r"innowacyjn\w+", r"przełomow\w+",
    r"rewolucyjn\w+", r"szyt\w+ na miarę", r"dynamiczn\w+ zmieniając\w+",
    r"w dzisiejszych czasach", r"w dzisiejszym \w+ świecie", r"w erze\b",
    r"nieustannie (?:rozwijając|zmieniając)\w+", r"odblokow\w+ potencjał",
    r"uwolni\w+ potencjał", r"na (?:wyższy|nowy) poziom", r"stawiać czoła",
    r"synergi\w+", r"game ?changer", r"zanurz\w+ się", r"otwiera nowe możliwości",
    r"szerok\w+ spektrum", r"na wyciągnięcie ręki", r"warto (?:podkreślić|zauważyć)",
    r"należy (?:również )?(?:zaznaczyć|pamiętać)", r"odgrywa (?:kluczową|ważną) rolę",
    r"jak pokazują badania", r"podsumowując", r"reasumując", r"czas na zmianę",
    r"podróże po płaszczyznach",
]
PL_CALQUE = {  # P1: calques and register problems -> hint
    r"praktyk\w* dostarczania": "calque of 'delivery practitioner'; use 'praktyk wdrożeń'",
    r"prowadz\w+ dostarczanie": "calque of 'delivery'; use 'realizacja' / 'wdrożenia'",
    r"\bewangelist\w+": "imported job label; state the plain role or the fact",
    r"\bbutikow\w+": "'boutique' calque; 'niewielki i wyspecjalizowany' + the specialty",
    r"\bchampion\w*": "borrowed role; 'lokalni eksperci' / 'liderzy zmiany'",
    r"\bklock\w+": "metaphor; prefer 'elementy', 'części'",
    r"\bspin(?:am|a|ać|asz)\b": "colloquial; use the neutral verb for the real operation (koordynować, łączyć)",
    r"\bdostarcz\w+ (?:wartoś\w+|rezultat\w*)": "'deliver value'; name the result",
    r"\badresow\w+ (?:problem|potrzeb|wyzwani)\w*|\bzaadresow\w+": "'address a problem'; use 'rozwiązać', 'zająć się'",
    r"\bwypych\w+": "'push'; use 'przekazywać', 'zgłaszać'",
    r"\bwartoś\w+ dodan\w+": "filler outside economics/VAT; name the concrete effect",
}
PL_MINOR = {  # P2
    r"\bw oparciu o\b": "'na podstawie' / 'opierając się na'",
    r"\bpoprzez\b": "'przez' / 'dzięki' / 'za pomocą'",
    r"\bmieć miejsce\b|\bma miejsce\b|\bmiał\w* miejsce\b": "'odbywać się' / 'zdarzyć się'",
    r"\bw chwili obecnej\b|\bw dniu dzisiejszym\b": "'teraz' / 'dziś'",
    r"\bw temacie\b": "'o' / 'w sprawie'",
    r"\bjest w stanie\b|\bsą w stanie\b": "'potrafi' / 'może'",
    r"\bpozwala na \w+(?:ie|nie|cie)\b": "'pozwala' + infinitive",
    r"\bodnośnie\b": "'w sprawie' / 'dotyczący'",
}
PL_TIER2 = [
    r"kluczow\w+", r"istotn\w+", r"fundamentaln\w+", r"niezwykle", r"skuteczn\w+",
    r"efektywn\w+", r"optymaln\w+", r"zaawansowan\w+", r"nowoczesn\w+",
    r"profesjonaln\w+", r"elastyczn\w+", r"transparentn\w+", r"całościow\w+",
    r"strategiczn\w+", r"proaktywn\w+", r"dedykowan\w+",
]
EN_STOCK = [
    r"delv\w+", r"leverag\w+", r"utili[sz]\w+", r"foster\w*", r"facilitat\w+",
    r"empower\w*", r"streamlin\w+", r"supercharg\w+", r"harness\w*", r"robust\w*",
    r"cutting-edge", r"state-of-the-art", r"best-in-class", r"seamless\w*",
    r"holistic\w*", r"game[- ]?chang\w+", r"paradigm shift", r"revolutionary",
    r"transformative", r"groundbreaking", r"unlock\w*", r"unleash\w*",
    r"next level", r"elevat\w+", r"tapestry", r"\brealm\b", r"beacon",
    r"cornerstone", r"multifaceted", r"intricate", r"meticulous", r"paramount",
    r"pivotal", r"ever-evolving", r"fast-paced", r"in today's", r"stands? as a testament",
    r"plays? an? (?:vital|crucial|key) role", r"it'?s worth noting",
    r"it is important to note", r"at the end of the day", r"let'?s dive",
    r"here'?s the thing", r"in conclusion", r"deep dive",
]
EN_TIER2 = [
    r"comprehensive", r"innovative", r"scalable", r"optimi[sz]\w+", r"impactful",
    r"crucial", r"essential", r"vital", r"significant\w*", r"notable", r"remarkable",
    r"vibrant", r"dynamic", r"strategic", r"actionable", r"insights?",
    r"ecosystem", r"stakeholders?", r"solutions?", r"synergy",
]

# ---------------------------------------------------------------- contrasts

CONTRAST_PL = [
    r"\b[Nn]ie chodzi o\b[^.!?]{0,80}",
    r"\b[Nn]ie tylko\b[^.!?]{0,80}?\b(?:ale|lecz)\b",
    r",\s+(?:a\s+)?nie\s+(?:na|z|ze|w|we|o|od|do|po|za|dla|przez|u|jako)\s+\w+",
    r",\s+(?:a\s+)?nie\s+(?!(?:ma|mam|jest|są|był\w*|będ\w+|można|trzeba|wolno|musi|może|mogą|ujawni\w*|\w+(?:m|sz|my|cie|ją|ą))\b)\w+",
    r"\bnie\s+[^.!?,;]{2,40},\s+lecz\b",
]
CONTRAST_EN = [
    r"\b(?:It|This|That|He|She|They|We)(?:'s|'re| is| are| was| isn't| aren't)?\s+not\s+(?:just\s+|only\s+)?[^.;,]{1,60}[,;.]\s*(?:it'?s|it is|but|they'?re|that'?s|this is|we'?re)\b",
    r"\bnot just\b[^.]{0,60}\bbut\b",
    r"\bisn'?t about\b",
    r"\bless\s+\w+,\s+more\s+\w+",
    r"\b(?:Not|No)\s+\w+(?:\s+\w+)?\.\s+(?:Not|No)\s+\w+",
    r"\b\w+, not (?:a |an |the )?\w+(?: \w+)?(?=[.!?])",
]

FIRST_PERSON_PRESENT = (
    r"\b(?:Kieruję|Zarządzam|Wdrażam|Prowadzę|Koordynuję|Odpowiadam|Planuję|Buduję|"
    r"Rozwijam|Tworzę|Projektuję|Realizuję|Organizuję|Analizuję|Optymalizuję|Szkolę|"
    r"Wspieram|Dbam|Nadzoruję|Wprowadzam|Implementuję|Opracowuję|Doradzam)\b"
)
DATE_RANGE = re.compile(
    r"(?P<s>\d{2}\.\d{4}|\d{4})\s*[–—-]\s*(?P<e>\d{2}\.\d{4}|\d{4}|obecnie|teraz|present|now)",
    re.I,
)
ABBREV = re.compile(
    r"\b(np|ds|tj|tzn|itd|itp|ok|ul|nr|dr|mgr|inż|prof|ang|tys|mln|mld|zł|godz|pt|"
    r"ww|tzw|wg|św|al|pl|r|w)\.", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


# ---------------------------------------------------------------- input

class _Text(HTMLParser):
    BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "section", "header",
             "footer", "article", "tr", "blockquote", "br", "title", "ul", "ol", "nav"}
    SKIP = {"script", "style", "svg", "noscript"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.cur, self.skip, self.in_head = [], [], 0, None
        self.headings = set()

    def _flush(self):
        text = re.sub(r"[ \t ]+", " ", "".join(self.cur)).strip()
        if text:
            self.lines.append(text)
            if self.in_head:
                self.headings.add(len(self.lines))
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag in self.BLOCK:
            self._flush()
        if re.fullmatch(r"h[1-6]", tag):
            self.in_head = tag

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        if tag in self.BLOCK:
            self._flush()
        if tag == self.in_head:
            self.in_head = None

    def handle_data(self, data):
        if not self.skip:
            self.cur.append(data)


def load(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    if path.lower().endswith((".html", ".htm")) or re.match(r"\s*<!doctype html|\s*<html", raw, re.I):
        p = _Text()
        p.feed(raw)
        p._flush()
        return "\n".join(p.lines), p.headings
    heads = {i + 1 for i, l in enumerate(raw.splitlines()) if l.lstrip().startswith("#")}
    return raw, heads


def mask_code(text):
    """Blank out fenced code and inline code, keeping offsets and newlines."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    return re.sub(r"`[^`\n]*`", blank, text)


def detect_lang(text):
    low = text.lower()
    pl = len(re.findall(r"[ąćęłńóśźż]", low)) * 8
    pl += sum(low.count(f" {w} ") for w in ("się", "nie", "jest", "na", "do", "że", "dla", "oraz", "jak", "przez", "po"))
    en = sum(low.count(f" {w} ") for w in ("the", "and", "of", "to", "is", "for", "with", "that", "are", "you", "in"))
    return "pl" if pl >= en else "en"


# ---------------------------------------------------------------- checks

def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


def snip(s, n=80):
    s = re.sub(r"\s+", " ", s.strip())
    return s if len(s) <= n else s[: n - 1] + "…"


def lint(text, lang=None, headings=None):
    headings = headings or set()
    masked = mask_code(text)
    lang = lang or detect_lang(masked)
    words = len(re.findall(r"\w+", masked))
    out = []

    def add(sev, rule, pos, span, hint):
        out.append({"sev": sev, "rule": rule, "line": lineno(masked, pos),
                    "span": snip(span), "hint": hint})

    # quotation marks and dashes
    if lang == "pl":
        for m in re.finditer(r'„[^”"\n]{1,200}"', masked):
            add("P1", "pl-quote-mismatch", m.start(), m.group(0), 'closes with a straight " ; use „…”')
        for m in re.finditer(r'(?<![\w„])"[^"\n„”]{1,200}"', masked):
            add("P1", "pl-quote-straight", m.start(), m.group(0), 'straight quotes; use „…” (nested: «…»)')
        if masked.count("„") != masked.count("”") and not re.search(r'„[^”"\n]{1,200}"', masked):
            add("P1", "pl-quote-unbalanced", 0, f"{masked.count('„')}x „ vs {masked.count('”')}x ”",
                "opening and closing marks do not match")
    em = [m for m in re.finditer(r"—", masked)]
    allowed = max(1, words // 500)
    if len(em) > allowed:
        add("P1", "dash-em-budget", em[allowed].start(), "—",
            f"{len(em)} em dashes in {words} words (budget {allowed}); none on slides")
    if lang == "pl":
        for m in re.finditer(r"\S—\S", masked):
            add("P1", "pl-dash-unspaced", m.start(), m.group(0), "unspaced em dash inside Polish text")
        if em and re.search(r" – ", masked):
            add("P2", "dash-mixed", em[0].start(), "— and –", "mixes em dash and spaced en dash; choose one")
    excl = masked.count("!")
    if excl > max(1, words // 1000):
        add("P2", "exclamation", masked.index("!"), "!", f"{excl} exclamation marks in {words} words")

    # polish typography
    if lang == "pl":
        orphans = [m for m in re.finditer(r"(?<![\w.])[aiouwzAIOUWZ] (?=\S)", masked)]
        if orphans:
            add("P2", "pl-orphan-spaces", orphans[0].start(), orphans[0].group(0) + "…",
                f"{len(orphans)} single-letter words followed by a plain space; use a non-breaking space in published copy")
        dec_c = re.search(r"(?<![\d.,])\d{1,3},\d{1,2}(?![\d.,])", masked)
        dec_p = re.search(r"(?<![\d.])\d{1,3}\.\d{1,2}(?![\d.])", masked)
        if dec_c and dec_p:
            add("P2", "pl-decimal-mixed", dec_p.start(), dec_p.group(0), "mixes decimal comma and decimal point")

    # headings
    for ln in headings:
        raw = text.splitlines()[ln - 1] if ln - 1 < len(text.splitlines()) else ""
        h = raw.lstrip("# ").strip()
        ws = h.split()
        if EMOJI.search(h):
            out.append({"sev": "P2", "rule": "emoji-heading", "line": ln, "span": snip(h), "hint": "emoji in heading"})
        if lang == "pl" and len(ws) >= 3:
            caps = sum(1 for w in ws[1:] if w[:1].isupper() and not w.isupper() and w.lower() not in ("ai",))
            if caps >= 2:
                out.append({"sev": "P2", "rule": "pl-title-case", "line": ln, "span": snip(h),
                            "hint": "Title Case is an English habit; Polish uses sentence case"})

    # address form
    if lang == "pl":
        forms = {
            "Wy": len(re.findall(r"\b[Ww]asz\w*|\b[Ww]am\b|\b[Ww]ami\b", masked)),
            "Ty": len(re.findall(r"\b[Tt]w[oó]j\w*|\b[Tt]obie\b|\b[Tt]obą\b|\b[Tt]woi\w*", masked)),
            "Państwo": len(re.findall(r"\b[Pp]aństw\w*", masked)),
        }
        present = {k: v for k, v in forms.items() if v}
        if len(present) > 1:
            add("P1", "pl-address-mixed", 0, ", ".join(f"{k}x{v}" for k, v in present.items()),
                "more than one address form in one document; choose Ty, Wy or Państwo")

    # tense against dates
    if lang == "pl":
        today = datetime.date.today()
        ranges = list(DATE_RANGE.finditer(masked))
        for i, m in enumerate(ranges):
            e = m.group("e").lower()
            if e in ("obecnie", "teraz", "present", "now"):
                continue
            ey, em_ = (int(e[3:]), int(e[:2])) if "." in e else (int(e), 12)
            if (ey, em_) >= (today.year, today.month):
                continue
            end = ranges[i + 1].start() if i + 1 < len(ranges) else len(masked)
            block = masked[m.end(): min(end, m.end() + 1200)]
            hit = re.search(FIRST_PERSON_PRESENT, block)
            if hit:
                add("P1", "pl-tense-vs-dates", m.end() + hit.start(), hit.group(0),
                    f"role ended {m.group('e')} but is described in the present tense")

    # contrast patterns
    pats = CONTRAST_PL if lang == "pl" else CONTRAST_EN
    contrasts = []
    for p in pats:
        for m in re.finditer(p, masked):
            if not any(abs(m.start() - c.start()) < 12 for c in contrasts):
                contrasts.append(m)
    contrasts.sort(key=lambda m: m.start())
    sev = "P1" if len(contrasts) >= 3 else "P2"
    for m in contrasts:
        add(sev, "contrast-candidate", m.start(), m.group(0),
            f"{len(contrasts)} in document; fine if it corrects or carries information, flag at 3+; "
            "an invented opponent is flagged even once")

    # slogan cadence
    prot = ABBREV.sub(lambda m: m.group(0).replace(".", "․"), masked)
    slogans = 0
    for lm in re.finditer(r"[^\n]+", prot):
        sents = re.split(r"(?<=[.!?…])\s+(?=[A-ZĄĆĘŁŃÓŚŹŻ0-9„\"“(])", lm.group(0))
        run = []
        for s in sents + [""]:
            if s and len(re.findall(r"\w+", s)) <= 4 and re.search(r"[.!?]$", s.strip()):
                run.append(s)
            else:
                if len(run) >= 2:
                    slogans += 1
                    add("P2", "slogan-cadence", lm.start(), " ".join(run), "run of very short sentences")
                run = []
    if slogans >= 3:
        for f in out:
            if f["rule"] == "slogan-cadence":
                f["sev"] = "P1"
                f["hint"] = f"{slogans} slogan runs in document - a template; merge into sentences with a fact"

    # word lists
    if lang == "pl":
        for p in PL_STOCK:
            for m in re.finditer(p, masked, re.I):
                add("P1", "stock-phrase", m.start(), m.group(0), "inflated or stock Polish; replace with the fact")
        for p, hint in PL_CALQUE.items():
            for m in re.finditer(p, masked, re.I):
                add("P1", "calque", m.start(), m.group(0), hint)
        for p, hint in PL_MINOR.items():
            for m in re.finditer(p, masked, re.I):
                add("P2", "bureaucratic", m.start(), m.group(0), hint)
        tier2 = PL_TIER2
    else:
        for p in EN_STOCK:
            for m in re.finditer(r"\b" + p + (r"\b" if not p.endswith(("*", "+", "b")) else ""), masked, re.I):
                add("P1", "stock-phrase", m.start(), m.group(0), "stock English; replace with the fact")
        tier2 = EN_TIER2
    for pm in re.finditer(r"[^\n]+", masked):
        seen = []
        for p in tier2:
            for m in re.finditer(r"\b" + p + r"\b", pm.group(0), re.I):
                seen.append(m.group(0).lower())
        if len(set(seen)) >= 2:
            add("P2", "tier2-cluster", pm.start(), ", ".join(sorted(set(seen))),
                "two or more tier-2 words in one paragraph")

    # em-dash style, emoji outside headings are left to judgment
    out.sort(key=lambda f: (f["line"], SEV_ORDER[f["sev"]]))
    return {"lang": lang, "words": words, "findings": out}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="file to check, or - for stdin")
    ap.add_argument("--lang", choices=["pl", "en"])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-sev", choices=list(SEV_ORDER), default="P2")
    a = ap.parse_args(argv)
    text, heads = load(a.path)
    res = lint(text, a.lang, heads)
    res["findings"] = [f for f in res["findings"] if SEV_ORDER[f["sev"]] <= SEV_ORDER[a.min_sev]]
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    counts = {s: sum(1 for f in res["findings"] if f["sev"] == s) for s in SEV_ORDER}
    print(f"unslop-pl-en lint: lang={res['lang']}, {res['words']} words, "
          f"{len(res['findings'])} candidates (P0 {counts['P0']}, P1 {counts['P1']}, P2 {counts['P2']})")
    print("Every line is a candidate; judge it in context.\n")
    for f in res["findings"]:
        print(f"{f['sev']} L{f['line']:<4} [{f['rule']}] «{f['span']}» - {f['hint']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
