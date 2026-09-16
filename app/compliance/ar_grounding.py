"""Annual Report evidence-grounding validation — PRODUCTION.

Deterministic, LLM-free, read-only. This module never rewrites text; it
returns a rejection reason (or None) plus a structured findings dict that the
AR task routes to PASS or HUMAN_REVIEW.

Implements the architecture validated in the isolated 20-case runs:
  * evidence-anchored figure grounding (Indian formats, raw rupees / lakh /
    crore / million / billion / thousand, table base-unit headers incl. OCR
    variants, lakh<->crore conversion, brackets/negatives, FY normalisation,
    period, metric, unit-scale detection, unit ambiguity);
  * deterministic distortion guard (negation inversion, severity
    transformation, historical/current status, unsupported adverse concepts,
    opinion substitution, guidance-to-fact conversion);
  * two completeness checks (modified audit opinion, historical/current
    willful-defaulter status);
  * AR compliance (advisory-language ban kept; the old forward-tense ban and
    the per-figure attribution requirement are REMOVED — guidance, targets,
    outlook and grounded figures are allowed).

Portions are vendored from the isolated test harness and from
app/compliance/validators.py patterns (same "duplicate and keep in sync"
convention already used by this repository).
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

# Advisory-language ban (unchanged semantics for AR: calls/picks/tips/
# predictions/target price/stop-loss/buy-sell). "accuracy" is handled
# separately by the narrow carve-out below.
_ADVISORY_WORDS_RE = re.compile(
    r"\b(calls?|picks?|tips?|predictions?|predict(?:s|ed|ing)?|target\s*price|"
    r"stop[\s-]?loss|accuracy)\b", re.IGNORECASE)
_BUY_SELL_RE = re.compile(r"\b(buy|sell)\b", re.IGNORECASE)
_BUY_SELL_SAFE_RE = re.compile(r"\bnet\s+(buy|sell)\b", re.IGNORECASE)
_CALL_SAFE_RE = re.compile(
    r"\b(?:conference|earnings|analyst|investor|quarterly|q\d)\s*[\s-]?calls?\b"
    r"|\b(?P<temporal>last|this|the|recent|previous|prior|latest)\s+calls?\b",
    re.IGNORECASE)
_TRADING_NEAR_CALL_RE = re.compile(
    r"\b(buy|sell|option|options|price|premium|strike|put|puts)\b", re.IGNORECASE)
_ATTRIBUTION_SUBJECT_RE = re.compile(
    r"\b(management|company|report|document|presentation|board|directors?|"
    r"chairman|ceo|cfo|auditor|auditors|the\s+auditor|the\s+statutory\s+auditor|guidance)\b",
    re.IGNORECASE)
_ATTRIBUTION_VERB_RE = re.compile(
    r"\b(said|stated|noted|notes?|mentioned|indicat\w*|guided|emphasized|highlighted|"
    r"reiterated|maintained|outlined|detailed|described|presented|announced|"
    r"reported|commented|added|confirmed|flagged|observed|remarked|set)\b", re.IGNORECASE)
_ATTRIBUTED_GUIDANCE_RE = re.compile(
    r"\b(management|company|report|document|presentation|board|directors?|chairman|ceo|cfo|"
    r"auditor|auditors)\b\s+"
    r"(said|stated|reported|guided|indicated|outlines?|details?|describes?|presents?|notes?|"
    r"highlights?|announced|observes?|flagged|expects?|targets?|plans?|forecasts?|intends?|"
    r"committed|outlook|guidance)"
    r"|\b(management|company|report|document|presentation|board)\s+(guidance|outlook|target)"
    r"|\b(stated|said|reported|guided|indicated|outlined|detailed|described|presented|noted|"
    r"highlighted|announced|observed|flagged)\s+that", re.IGNORECASE)


# ===========================================================================
# 1. Figure grounding
# ===========================================================================
SCALE = {"crore": 1e7, "cr": 1e7, "lakh": 1e5, "lac": 1e5, "million": 1e6, "mn": 1e6,
         "billion": 1e9, "bn": 1e9, "thousand": 1e3}
UNIT_ALT = r"crores?|cr|lakhs?|lacs?|millions?|mn|billions?|bn|thousands?|%|percent"
NUM = r"\d[\d,]*(?:\.\d+)?"
FIG_RE = re.compile(
    r"(?P<cur>₹|`|~|'=?<?|rs\.?|inr)\s*\.?\s*(?P<num>" + NUM + r")\s*\)?\s*(?:/-|/-|/-)?\s*(?P<u1>" + UNIT_ALT + r")?"
    r"|(?P<num2>" + NUM + r")\s*\)?\s*(?:/-|/-)?\s*(?P<u2>" + UNIT_ALT + r")"
    r"|(?P<num3>" + NUM + r")", re.I)
UNIT_WORD = re.compile(r"\b(lakhs?|lacs?|crores?|cr|millions?|billions?|bn|mn|thousands?)\b", re.I)
BASEPRE = re.compile(r"(\bin\s*|\bfigures?\s+in\s*|\bamounts?\s+in\s*|\ball\s+amounts?\s+in\s*|\(\s*|"
                     r"(?:₹|rs\.?|inr)\s*\.?\s*|\bt\s+in\s*|\b~?in\s*)$", re.I)
YEAR = re.compile(r"^(?:19|20)\d{2}$")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(])")
NEG = re.compile(r"\b(loss(?:es)?|negative|deficit|declin\w*|decreas\w*|default\w*|doubtful|write[- ]?off|"
                 r"impair\w*|not\s+provided|non-?provision)\b", re.I)
POS = re.compile(r"\b(profit\w*|gain\w*|positive|increas\w*|growth|improved?|earned)\b", re.I)
GUIDE = re.compile(r"\b(expect\w*|plan\w*|target\w*|aim\w*|intend\w*|outlook|forecast\w*|project\w*|"
                   r"guidance|propose\w*|likely|may|seek\w*)\b", re.I)
FACT_FUTURE = re.compile(r"\b(will|is going to|are going to|is expected to|are expected to|is set to|are set to)\b", re.I)
METRICS = {
    "pat": re.compile(r"\b(pat|profit after tax|net profit|profit for the (?:year|period))\b", re.I),
    "revenue": re.compile(r"\b(revenue|total income|turnover|income from operations|total segment revenue)\b", re.I),
    "ebitda": re.compile(r"\bebitda\b", re.I),
    "net_worth": re.compile(r"\bnet\s*worth\b", re.I),
    "crar": re.compile(r"\b(crar|capital to risk|capital adequacy)\b", re.I),
    "debt": re.compile(r"\b(debt|borrowing\w*|loans?)\b", re.I),
    "contingent": re.compile(r"\bcontingent\b", re.I),
    "capex": re.compile(r"\b(capex|capital expenditure)\b", re.I),
    "dividend": re.compile(r"\bdividend\b", re.I),
    "interest": re.compile(r"\binterest\b", re.I),
    "sales": re.compile(r"\b(sales|yarn sales|volume)\b", re.I),
}
FY = re.compile(r"\bfy\s*(\d{2}|\d{4})(?:\s*[-–/]\s*(\d{2,4}))?\b|\b((?:19|20)\d{2})\s*[-–/]\s*(\d{2})\b", re.I)


def _norm_unit(u):
    if not u:
        return None
    u = u.lower()
    if u in ("%", "percent"):
        return "%"
    if u.startswith("crore") or u == "cr":
        return "crore"
    if u.startswith("lakh") or u.startswith("lac"):
        return "lakh"
    if u.startswith("million") or u == "mn":
        return "million"
    if u.startswith("billion") or u == "bn":
        return "billion"
    if u.startswith("thousand"):
        return "thousand"
    return None


def _to_float(s):
    try:
        return float(s.replace(",", ""))
    except Exception:
        return None


def _sentences(text):
    return [s.strip() for s in SENT_SPLIT.split(text or "") if s.strip()]


DIR_UP = re.compile(r"\b(increas\w*|rise|rose|grew|growth|improved?|higher)\b", re.I)
DIR_DOWN = re.compile(r"\b(decreas\w*|declin\w*|fall|fell|lower|reduced?)\b", re.I)


SIGN_RELEVANT = re.compile(r"(profit|loss|net\s*worth|equity|pat|ebitda|income|revenue|"
                          r"margin|eps|crar|turnover|sales)", re.I)


def _direction_conflict(sentence):
    """Narrow check: an explicit "from X% to Y%" pair contradicted by the direction word."""
    m = re.search(r"from\s+(\d+(?:\.\d+)?)\s*%\s*to\s+(\d+(?:\.\d+)?)\s*%", sentence or "", re.I)
    if not m:
        return False
    a, b = float(m.group(1)), float(m.group(2))
    if DIR_DOWN.search(sentence) and b > a:
        return True
    if DIR_UP.search(sentence) and b < a:
        return True
    return False


def _pick(cands, f):
    """Prefer an evidence candidate whose sign agrees with the output figure."""
    for e in cands:
        if bool(e["neg"]) == bool(f["neg"]):
            return e
    return cands[0]


def _sentence_at(text, idx):
    for s in _sentences(text):
        pos = text.find(s)
        if pos <= idx <= pos + len(s):
            return s
    return text[max(0, idx - 160):idx + 160]


def base_units(text):
    """(position, canonical unit) for header-like unit declarations."""
    out = []
    for m in UNIT_WORD.finditer(text or ""):
        pre = (text[max(0, m.start() - 22):m.start()])
        if BASEPRE.search(pre):
            out.append((m.start(), _norm_unit(m.group(1))))
    return out


def _base_for(pos, units, span=8000):
    u = None
    for p, un in units:
        if p < pos and pos - p <= span:
            u = un
    return u


def extract_figures(text, default_unit=None):
    text = text or ""
    units = base_units(text)
    out = []
    for m in FIG_RE.finditer(text):
        if m.group("num"):
            raw, value = m.group(0), _to_float(m.group("num"))
            unit = _norm_unit(m.group("u1")); cur = True
        elif m.group("num2"):
            raw, value = m.group(0), _to_float(m.group("num2"))
            unit = _norm_unit(m.group("u2")); cur = unit == "%"
        else:
            raw, value = m.group(0), _to_float(m.group("num3"))
            unit, cur = None, False
        if value is None:
            continue
        bracketed = bool(re.search(r"\(\s*-?\s*$", text[max(0, m.start() - 3):m.start()]))
        if unit is None and not cur:
            grouped = raw.count(",") >= 2
            if not (bracketed or grouped or value >= 1000):
                continue
            if YEAR.match(raw.strip()):
                continue
        base = _base_for(m.start(), units) if unit is None else None
        eff = unit or base or (default_unit if unit is None else None)
        pre30 = text[max(0, m.start() - 30):m.start()]
        pre4 = text[max(0, m.start() - 4):m.start()]
        neg = (bool(re.search(r"[-−]", pre4)) or bracketed
               or bool(re.search(r"negative|loss|deficit", pre30, re.I)))  # sign markers only
        rupees = None
        if eff in SCALE:
            rupees = value * SCALE[eff]
        elif cur and unit is None:
            rupees = value
        out.append({"raw": raw.strip(), "value": value, "unit": unit, "base": base, "eff": eff,
                    "rupees": rupees, "neg": neg, "sentence": _sentence_at(text, m.start()), "start": m.start()})
    return out


def _period_keys(text):
    keys = set()
    for m in FY.finditer(text or ""):
        if m.group(1):
            y = m.group(1)
            y = int(y) if len(y) == 4 else 2000 + int(y)
            end = y + 1
            if m.group(2):
                e2 = int(m.group(2))
                end = (2000 + e2) if e2 < 100 else e2
            keys.add(f"fy{end-1}-{str(end)[-2:]}")
            keys.add(f"fy{end}")
        elif m.group(3):
            y1, y2 = int(m.group(3)), int(m.group(4))
            end = 2000 + y2 if y2 < 100 else y2
            keys.add(f"fy{end-1}-{str(end)[-2:]}")
            keys.add(f"fy{end}")
    return keys


def _sentence_period(sent):
    return _period_keys(sent)


def _default_unit(units):
    vals = [u for _, u in units if u]
    if not vals:
        return None
    uniq = set(vals)
    return vals[0] if len(uniq) == 1 else None


def ground(evidence_text, output_text, rel_tol=0.02):
    ev = extract_figures(evidence_text, default_unit=_default_unit(base_units(evidence_text)))
    ev_rupees = [(f, f["rupees"]) for f in ev if f["rupees"]]
    ev_pct = [f for f in ev if f["eff"] == "%"]
    ev_naked = {}
    for f in ev:
        ev_naked.setdefault(round(f["value"], 6), []).append(f)

    out = extract_figures(output_text)
    res = {"checked": len(out), "ungrounded": [], "unit_scale": [], "unit_ambiguous": [],
           "sign_mismatch": [], "period_review": [], "metric_review": [], "guidance_conversion": []}
    for f in out:
        match = None
        if f["eff"] == "%":
            match = next((e for e in ev_pct if abs(f["value"] - e["value"]) < 0.01), None)
            if match is None:
                res["ungrounded"].append({"figure": f["raw"], "sentence": f["sentence"][:200]})
                continue
        elif f["rupees"] is not None:
            r = f["rupees"]
            cands = [e for e, er in ev_rupees if abs(er - r) <= rel_tol * max(r, er)]
            if not cands:
                naked = ev_naked.get(round(f["value"], 6))
                if naked:
                    known = [e for e in naked if e["eff"] in SCALE]
                    if known and all(e["eff"] != f["eff"] for e in known):
                        res["unit_scale"].append({"figure": f["raw"], "unit": f["eff"],
                                                  "evidence_unit": known[0]["eff"], "sentence": f["sentence"][:200]})
                    else:
                        res["unit_ambiguous"].append({"figure": f["raw"], "unit": f["eff"],
                                                      "sentence": f["sentence"][:200]})
                else:
                    res["ungrounded"].append({"figure": f["raw"], "sentence": f["sentence"][:200]})
                continue
            match = _pick(cands, f)
        else:
            cands = [e for e in ev if round(e["value"], 6) == round(f["value"], 6)]
            if not cands:
                res["ungrounded"].append({"figure": f["raw"], "sentence": f["sentence"][:200]})
                continue
            match = _pick(cands, f)
        sign_relevant = bool(SIGN_RELEVANT.search(f["sentence"])) or bool(SIGN_RELEVANT.search(match["sentence"]))
        if sign_relevant and (bool(f["neg"]) != bool(match["neg"]) or _direction_conflict(f["sentence"])):
            res["sign_mismatch"].append({"figure": f["raw"], "output": f["sentence"][:180],
                                         "evidence": match["sentence"][:180]})
        op, ep = _sentence_period(f["sentence"]), _sentence_period(match["sentence"])
        if op and ep and not (op & ep):
            res["period_review"].append({"figure": f["raw"], "output_periods": sorted(op), "evidence_periods": sorted(ep)})
        om = {k for k, p in METRICS.items() if p.search(f["sentence"])}
        em = {k for k, p in METRICS.items() if p.search(match["sentence"])}
        if om and em and not (om & em):
            res["metric_review"].append({"figure": f["raw"], "output_metrics": sorted(om), "evidence_metrics": sorted(em)})

    for s in _sentences(output_text):
        if not FACT_FUTURE.search(s):
            continue
        hit = hit_met = None
        for met in {k for k, p in METRICS.items() if p.search(s)}:
            for em in METRICS[met].finditer(evidence_text or ""):
                win = evidence_text[max(0, em.start() - 260):em.end() + 260]
                if GUIDE.search(win) and not re.search(r"\bwill\b", win, re.I):
                    hit, hit_met = win, met
                    break
            if hit:
                break
        if hit:
            res["guidance_conversion"].append({"metric": hit_met, "output": s[:200],
                                               "evidence": hit[:220].replace("\n", " ")})

    hard = res["ungrounded"] or res["unit_scale"] or res["sign_mismatch"] or res["guidance_conversion"]
    soft = res["unit_ambiguous"] or res["period_review"] or res["metric_review"]
    res["status"] = "FLAG" if hard else ("REVIEW" if soft else "PASS")
    return res


def text_of(output):
    parts = []
    for v in (output or {}).values():
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            parts.extend(str(x) for x in v)
    return " ".join(parts)

# ===========================================================================
# 2. Distortion guard
# ===========================================================================
CONCEPTS = {
    "default": re.compile(r"\bdefault(?:ed|s|ing)?\b", re.I),
    "willful_defaulter": re.compile(r"willful\s+defaulter|declared\s+(?:a\s+)?defaulter", re.I),
    "going_concern": re.compile(r"going[-\s]?concern", re.I),
    "qualified_opinion": re.compile(r"(?<![a-z])qualified\s+opinion", re.I),
    "adverse_opinion": re.compile(r"adverse\s+opinion", re.I),
    "disclaimer_opinion": re.compile(r"disclaimer\s+of\s+opinion", re.I),
    "sebi_action": re.compile(r"SEBI[^.]{0,140}(?:restrict|prohibit|debar|penalt|direction|order)", re.I),
    "insolvency_nclt": re.compile(r"insolvency|NCLT|corporate\s+insolvency", re.I),
    "negative_net_worth": re.compile(r"negative\s+net\s*worth|net\s*worth\s+(?:is|was|has\s+become|turned)\s+negative", re.I),
}

EV_NEG_DEFAULT = re.compile(
    r"questions?\s+of\s+default\s+does\s+not\s+arise|does\s+not\s+have\s+any\s+loan\s+facility|"
    r"has\s+not\s+defaulted|have\s+not\s+defaulted|not\s+defaulted|no\s+defaults?|"
    r"there\s+are\s+no\s+dues|no\s+dues\s+of\s+those\s+banks|"
    r"non-?provision\s+of\s+interest|not\s+provided\s+for", re.I)
EV_AFF_DEFAULT = re.compile(r"\bdefault(?:ed|s)?\b", re.I)
# evidence that documents a specific, supported non-repayment / non-provision
# (so a "default"-style statement is not necessarily a contradiction of a
# narrower "no BANK default" negation).
EV_AFF_NONREPAY = re.compile(
    r"repayment\s+of\s+principal\s+is\s+not\s+being\s+done|non-?repayment|"
    r"non-?provision\s+of\s+interest|only\s+the\s+interest\s+is\s+being\s+accrued|"
    r"not\s+being\s+paid|overdue|defaulted\s+in\s+repayment|default\s+in\s+repayment", re.I)
EV_AFF_WD = re.compile(r"(?:has|have|was|is|been)\s+(?:been\s+)?declared\s+(?:a\s+)?willful\s+defaulter|"
                       r"willful\s+defaulter\s+by\s+banks", re.I)
OUT_NEG_WD = re.compile(r"\bnot\b[^.!?]{0,90}willful\s+defaulter|\bnever\b[^.!?]{0,60}willful\s+defaulter", re.I)
OUT_AFF_DEFAULT = re.compile(r"\bdefault(?:ed|s)?\b", re.I)
NEG_BEFORE = re.compile(r"\b(?:not|no|never|without)\b", re.I)
DATE_QUAL = re.compile(r"\b(?:upto|up\s+to|as\s+of|as\s+at|as\s+on|31/03/\d{4}|31\.03\.\d{4}|"
                       r"balance\s+sheet\s+date|during\s+the\s+year)\b", re.I)


def _unnegated(match, text, window=34):
    pre = text[max(0, match.start() - window):match.start()]
    return not NEG_BEFORE.search(pre)


def grounding_guard(evidence_text, output_text):
    ev = evidence_text or ""
    out = output_text or ""
    findings = []

    # C. unsupported adverse concept (output raises it, evidence never does)
    for name, pat in CONCEPTS.items():
        if pat.search(out) and not pat.search(ev):
            findings.append({"concept": name, "type": "UNSUPPORTED",
                             "detail": "output raises this concept but the evidence never mentions it"})

    # A. default contradiction / mixed-context review
    neg_def = EV_NEG_DEFAULT.search(ev)
    if neg_def:
        for m in OUT_AFF_DEFAULT.finditer(out):
            if _unnegated(m, out) and not EV_NEG_DEFAULT.search(out[max(0, m.start() - 40):m.end() + 40]):
                if EV_AFF_NONREPAY.search(ev):
                    findings.append({"concept": "default", "type": "REVIEW",
                                     "detail": "evidence negates a default for one category but documents a "
                                               "specific non-repayment/non-provision elsewhere; verify the "
                                               "'default' wording is precise and names the counterparty",
                                     "evidence": neg_def.group(0)[:120],
                                     "output": out[max(0, m.start() - 90):m.end() + 90].replace("\n", " ")})
                else:
                    findings.append({"concept": "default", "type": "CONTRADICTION",
                                     "detail": "output affirms a default while the evidence negates it",
                                     "evidence": neg_def.group(0)[:120],
                                     "output": out[max(0, m.start() - 90):m.end() + 90].replace("\n", " ")})
                break

    # B. willful-defaulter inversion / context loss
    aff_wd = EV_AFF_WD.search(ev)
    if aff_wd:
        neg_wd_out = OUT_NEG_WD.search(out)
        if neg_wd_out:
            findings.append({"concept": "willful_defaulter", "type": "INVERSION",
                             "detail": "output negates a willful-defaulter declaration the evidence affirms",
                             "evidence": ev[max(0, aff_wd.start() - 60):aff_wd.end() + 120].replace("\n", " "),
                             "output": out[max(0, neg_wd_out.start() - 90):neg_wd_out.end() + 90].replace("\n", " ")})
        else:
            out_wd = CONCEPTS["willful_defaulter"].search(out)
            ev_has_date = bool(DATE_QUAL.search(ev[max(0, aff_wd.start() - 120):aff_wd.end() + 160]))
            out_has_date = bool(out_wd and DATE_QUAL.search(out[max(0, out_wd.start() - 120):out_wd.end() + 160]))
            if out_wd and ev_has_date and not out_has_date:
                findings.append({"concept": "willful_defaulter", "type": "CONTEXT_LOSS",
                                 "detail": "evidence dates the willful-defaulter status; output does not",
                                 "evidence": ev[max(0, aff_wd.start() - 60):aff_wd.end() + 160].replace("\n", " "),
                                 "output": out[max(0, out_wd.start() - 60):out_wd.end() + 120].replace("\n", " ")})
    return {"status": "FLAG" if findings else "PASS", "findings": findings}


def _guard_text_of(output):
    parts = []
    for v in (output or {}).values():
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            parts.extend(str(x) for x in v)
    return " ".join(parts)

# ===========================================================================
# 3. Completeness checks
# ===========================================================================
CATS = {
    "going_concern": {
        "ev": re.compile(r"material\s+uncertaint\w*[^.]{0,300}going\s+concern|going\s+concern[^.]{0,300}"
                         r"material\s+uncertaint|significant\s+doubt[^.]{0,200}ability\s+to\s+continue|"
                         r"doubt\s+about[^.]{0,160}ability\s+to\s+continue", re.I),
        "out": re.compile(r"going[-\s]?concern|material\s+uncertaint|significant\s+doubt", re.I),
    },
    "modified_opinion": {
        "ev": re.compile(r"disclaimer\s+of\s+opinion|adverse\s+opinion|unable\s+to\s+express\s+an\s+opinion|"
                         r"(?<![a-z])qualified(?:\s+audit)?\s+opinion", re.I),
        "out": re.compile(r"(?<![a-z])qualified(?:\s+audit)?\s+opinion|adverse\s+opinion|disclaimer|unable\s+to\s+express", re.I),
    },
    "defaults": {
        "ev": re.compile(r"willful\s+defaulter|default\s+in\s+repayment|has\s+defaulted|defaulted\s+in\s+repayment", re.I),
        "out": re.compile(r"willful\s+defaulter|default", re.I),
        "neg": re.compile(r"has\s+not\s+defaulted|not\s+been\s+declared|does\s+not\s+arise|no\s+default", re.I),
    },
    "regulatory_action": {
        "ev": re.compile(r"SEBI[^.]{0,160}(restrict|prohibit|debar|penalt|direction|order)|"
                         r"levied\s+a\s+monetary\s+penalt|NCLT|corporate\s+insolvency|"
                         r"non-?compliance[^.]{0,140}(Companies\s+Act|SEBI|LODR|Regulation)", re.I),
        "out": re.compile(r"SEBI|NCLT|insolvency|penalt|restrict|debar|non-?compliance", re.I),
    },
    "negative_net_worth": {
        "ev": re.compile(r"negative\s+net\s*worth|erosion\s+of\s+net\s*worth|net\s*worth\s+(?:is|was|has\s+become|turned)\s+negative", re.I),
        "out": re.compile(r"negative\s+net\s*worth|negative\s+equity|eroded\s+net\s*worth|net\s*worth\s+(?:is|was)\s+negative", re.I),
    },
    "contingent_liability": {
        "ev": re.compile(r"contingent\s+liabilit\w*[^.]{0,240}(?:Rs|lakh|crore|aggregat|\d)", re.I),
        "out": re.compile(r"contingent\s+liabilit", re.I),
    },
}
GUIDE_RE = re.compile(r"\b(expect\w*|plan\w*|target\w*|aim\w*|intend\w*|outlook|forecast\w*|project\w*|guidance)\b", re.I)

OPINION_EV = {
    "disclaimer": re.compile(r"disclaimer\s+of\s+opinion|unable\s+to\s+express\s+an\s+opinion", re.I),
    "adverse": re.compile(r"adverse\s+opinion", re.I),
    "qualified": re.compile(r"(?<![a-z])qualified(?:\s+audit)?\s+opinion|basis\s+for\s+qualified\s+opinion", re.I),
}
OPINION_OUT = {
    "disclaimer": re.compile(r"disclaimer|unable\s+to\s+express\s+an\s+opinion", re.I),
    "adverse": re.compile(r"adverse\s+opinion", re.I),
    "qualified": re.compile(r"(?<![a-z])qualified(?:\s+audit)?\s+opinion", re.I),
}
WD_AFF = re.compile(r"(?:has|have|was|is|been)\s+(?:been\s+)?declared\s+(?:a\s+)?willful\s+defaulter|"
                    r"willful\s+defaulter\s+by\s+banks", re.I)
WD_NEG = re.compile(r"not\s+(?:\w+\s+){0,4}(?:been\s+)?declared\s+(?:a\s+)?willful|"
                    r"not\s+(?:a\s+)?willful\s+defaulter|never\s+(?:been\s+)?(?:a\s+)?willful", re.I)
WD_DATE = re.compile(r"upto|up\s+to|as\s+of|as\s+at|as\s+on|31/03/\d{4}|31\.03\.\d{4}|"
                     r"balance\s+sheet\s+date|during\s+the\s+year", re.I)


def _win(text, m, n=140):
    return text[max(0, m.start() - n):m.end() + n]


def affirmative(text, pat, neg=None):
    for m in pat.finditer(text or ""):
        if neg and neg.search(_win(text, m)):
            continue
        return True
    return False


def material_profile(evidence, output):
    present, mentioned, omitted = [], [], []
    for name, cfg in CATS.items():
        if not affirmative(evidence, cfg["ev"], cfg.get("neg")):
            continue
        present.append(name)
        (mentioned if cfg["out"].search(output or "") else omitted).append(name)
    return {"present_in_evidence": present, "mentioned_in_output": mentioned, "omitted": omitted}


def guidance_profile(evidence, output):
    ev_guide = GUIDE_RE.search(evidence or "") and bool(
        re.search(r"\d[\d,]*(?:\.\d+)?\s*(?:crore|lakh|million|billion|bn|mn|%|percent)",
                  _win(evidence, GUIDE_RE.search(evidence or ""), 200) if GUIDE_RE.search(evidence or "") else "", re.I))
    return {"evidence_has_quantified_guidance": bool(ev_guide),
            "output_has_guidance_wording": bool(GUIDE_RE.search(output or ""))}


def audit_opinion_check(evidence, output):
    """None = ok/not applicable; else a finding dict."""
    ev_types = {k for k, p in OPINION_EV.items() if p.search(evidence or "")}
    if not ev_types:
        return None
    out_types = {k for k, p in OPINION_OUT.items() if p.search(output or "")}
    if not out_types:
        return {"check": "audit_opinion", "type": "OMITTED", "evidence_types": sorted(ev_types),
                "detail": "modified audit opinion present in evidence but not represented"}
    if out_types.isdisjoint(ev_types):
        return {"check": "audit_opinion", "type": "SUBSTITUTION", "evidence_types": sorted(ev_types),
                "output_types": sorted(out_types), "detail": "summary states a different opinion type"}
    return None


def willful_defaulter_check(evidence, output):
    """None = ok/not applicable; else a finding dict."""
    ev = evidence or ""
    aff = next((m for m in WD_AFF.finditer(ev) if not WD_NEG.search(_win(ev, m, 40))), None)
    if not aff:
        return None
    ev_date = bool(WD_DATE.search(_win(evidence, aff, 120)))
    out_aff = WD_AFF.search(output or "")
    out_neg = WD_NEG.search(output or "")
    if out_neg and not out_aff:
        return {"check": "willful_defaulter", "type": "ERASED", "evidence": aff.group(0)[:120],
                "detail": "output denies a declaration the evidence makes"}
    if not out_aff and not out_neg:
        return {"check": "willful_defaulter", "type": "OMITTED", "evidence": aff.group(0)[:120],
                "evidence_dated": ev_date, "detail": "willful-defaulter finding absent from summary"}
    if out_aff and ev_date:
        if not WD_DATE.search(_win(output, out_aff, 120)):
            return {"check": "willful_defaulter", "type": "HISTORICAL_AS_CURRENT",
                    "evidence": _win(evidence, aff, 160)[:200],
                    "output": _win(output, out_aff, 160)[:200],
                    "detail": "dated declaration presented without its date context"}
    return None

# ===========================================================================
# 4. AR compliance
# ===========================================================================

ACCURACY_CARVEOUT = re.compile(
    # audit/limitation language: "accuracy of the financial statements",
    # "the statements' accuracy", "financial accuracy", "their accuracy"
    r"accuracy\s+of\s+[^.!?]{0,40}?(?:financial\s+statements?|financial\s+results?|financial\s+reporting|"
    r"financial\s+information|financial\s+records?|financial\s+accounts?|accounts|balances?|debtors?|creditors?)"
    r"|(?:financial\s+statements?|financial\s+reporting|financial\s+information|financial\s+records?|"
    r"financial\s+results?|accounts?|balances?|debtors?|creditors?|records?|books?)'?s?\s+accuracy"
    r"|(?:financial|reporting|their)\s+accuracy", re.IGNORECASE)
ACCURATE_CLAIM = re.compile(r"\baccurate(?:ly)?\b", re.IGNORECASE)


def _attributed(text, m, window=300):
    pre = text[max(0, m.start() - window):m.end() + 80]
    if _ATTRIBUTED_GUIDANCE_RE.search(pre):
        return True
    return bool(_ATTRIBUTION_SUBJECT_RE.search(pre) and _ATTRIBUTION_VERB_RE.search(pre))


def ar_compliance(text):
    if not text:
        return "empty text"
    for m in _ADVISORY_WORDS_RE.finditer(text):
        word = m.group(0).lower()
        if word == "accuracy" and ACCURACY_CARVEOUT.search(text[max(0, m.start() - 50):m.start() + 95]):
            continue
        if word in ("call", "calls"):
            window = text[max(0, m.start() - 15):m.end()]
            safe = _CALL_SAFE_RE.search(window)
            if safe and not (safe.group("temporal") and _TRADING_NEAR_CALL_RE.search(
                    text[max(0, m.start() - 20):min(len(text), m.end() + 15)])):
                continue
        return f"forbidden word '{m.group(0)}'"
    m = _BUY_SELL_RE.search(text)
    if m:
        window = text[max(0, m.start() - 4):m.end()]
        if not _BUY_SELL_SAFE_RE.search(window):
            return f"forbidden word '{m.group(0)}'"
    for m in ACCURATE_CLAIM.finditer(text):
        if not _attributed(text, m):
            return "forbidden word 'accurate'"
    return None


def ar_summarizer_violation(text, check_financial_figures=False):
    """Figures are validated against the evidence post-hoc, not here."""
    return ar_compliance(text)

# ===========================================================================
# 5. Top-level AR validation
# ===========================================================================
HARD_GUARD_TYPES = ("CONTRADICTION", "INVERSION", "UNSUPPORTED")


def validate_annual_report_summary(evidence_text: str, output: Dict[str, Any]):
    """Returns (reason_or_None, findings).

    reason is a short human-readable rejection string; findings carries the
    structured audit trail for the review queue. Any of the following routes
    to Human Review: compliance failure, unsupported number, unit-scale
    mismatch, unresolved unit ambiguity, sign/direction error, guidance-to-fact
    conversion, a hard distortion-guard finding, or a completeness failure.
    """
    text = text_of(output)
    findings: Dict[str, Any] = {}

    compliance_reason = None
    for field, value in _iter_fields(output):
        compliance_reason = ar_summarizer_violation(value)
        if compliance_reason:
            findings["compliance"] = {"field": field, "reason": compliance_reason}
            break

    figures = ground(evidence_text or "", text)
    findings["figures"] = figures
    guard = grounding_guard(evidence_text or "", text)
    findings["guard"] = guard
    audit = audit_opinion_check(evidence_text or "", text)
    wd = willful_defaulter_check(evidence_text or "", text)
    if audit:
        findings["audit_opinion"] = audit
    if wd:
        findings["willful_defaulter"] = wd
    findings["material_profile"] = material_profile(evidence_text or "", text)
    findings["guidance_profile"] = guidance_profile(evidence_text or "", text)

    if compliance_reason:
        return f"compliance: {compliance_reason}", findings
    if figures["ungrounded"]:
        first = figures["ungrounded"][0]
        return f"unsupported figure '{first['figure']}' not present in supplied evidence", findings
    if figures["unit_scale"]:
        first = figures["unit_scale"][0]
        return (f"unit-scale mismatch for '{first['figure']}' "
                f"(evidence unit: {first.get('evidence_unit')})"), findings
    if figures["sign_mismatch"]:
        first = figures["sign_mismatch"][0]
        return f"figure sign/direction mismatch for '{first['figure']}'", findings
    if figures["guidance_conversion"]:
        first = figures["guidance_conversion"][0]
        return f"guidance-to-fact conversion for metric '{first.get('metric')}'", findings
    if figures["unit_ambiguous"]:
        first = figures["unit_ambiguous"][0]
        return (f"unit ambiguity for '{first['figure']}' — evidence has no usable "
                f"base-unit header"), findings
    hard = [f for f in guard.get("findings") or [] if f["type"] in HARD_GUARD_TYPES]
    if hard:
        return f"grounding guard: {hard[0]['type']} ({hard[0]['concept']})", findings
    if audit:
        return f"audit-opinion completeness: {audit['type']}", findings
    if wd:
        return f"willful-defaulter completeness: {wd['type']}", findings
    soft = [f for f in guard.get("findings") or [] if f["type"] not in HARD_GUARD_TYPES]
    if soft:
        return f"grounding guard review: {soft[0]['type']} ({soft[0]['concept']})", findings
    if figures["period_review"] or figures["metric_review"]:
        detail = (figures["period_review"] or figures["metric_review"])[0]
        return f"figure context review for '{detail['figure']}'", findings
    return None, findings


def _iter_fields(output: Dict[str, Any]):
    yield "executive_summary", str(output.get("executive_summary") or "")
    for i, b in enumerate(output.get("key_points") or [], 1):
        yield f"key_points[{i}]", str(b)
    for i, b in enumerate(output.get("important_risks") or [], 1):
        yield f"important_risks[{i}]", str(b)
    yield "key_takeaway", str(output.get("key_takeaway") or "")
