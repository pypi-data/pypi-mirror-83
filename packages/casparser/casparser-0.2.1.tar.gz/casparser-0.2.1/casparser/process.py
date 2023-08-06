from decimal import Decimal
import re

from dateutil import parser as date_parser

from .exceptions import HeaderParseError, CASParseError
from .regex import FOLIO_RE, HEADER_RE, SCHEME_RE
from .regex import CLOSE_UNITS_RE, OPEN_UNITS_RE, TRANSACTION_RE


def parse_header(text):
    """
    Parse CAS header data
    :param text: CAS text
    """
    if m := re.search(HEADER_RE, text, re.DOTALL | re.MULTILINE | re.I):
        return m.groupdict()
    raise HeaderParseError("Error parsing CAS header")


def process_cas_text(text):
    """
    Process the text version of a CAS pdf and return the detailed summary.
    :param text:
    :return:
    """
    hdr_data = parse_header(text[:1000])
    statement_period = {"from": hdr_data["from"], "to": hdr_data["to"]}

    folios = {}
    current_folio = None
    curr_scheme_data = {}
    lines = text.split("\u2029")
    for txt in lines:
        if m := re.search(FOLIO_RE, txt, re.I):
            folio = m.group(1).strip()
            if current_folio is None or current_folio != folio:
                if curr_scheme_data and current_folio is not None:
                    folios[current_folio]["schemes"].append(curr_scheme_data)
                    curr_scheme_data = {}
                current_folio = folio
                folios[folio] = {
                    "folio": current_folio,
                    "PAN": (m.group(2) or "").strip(),
                    "KYC": m.group(3).strip(),
                    "PANKYC": m.group(4).strip(),
                    "schemes": [],
                }
        if m := re.search(SCHEME_RE, txt, re.DOTALL | re.MULTILINE | re.I):
            if current_folio is None:
                raise CASParseError("Layout Error! Scheme found before folio entry.")
            scheme = re.sub(r"\(formerly.+?\)", "", m.group(2), flags=re.I | re.DOTALL).strip()
            if curr_scheme_data.get("scheme") != scheme:
                if curr_scheme_data:
                    folios[current_folio]["schemes"].append(curr_scheme_data)
                curr_scheme_data = {
                    "scheme": scheme,
                    "advisor": m.group(3).strip(),
                    "rta_code": m.group(1).strip(),
                    "rta": m.group(4).strip(),
                    "open": Decimal(0.0),
                    "close": Decimal(0.0),
                    "transactions": [],
                }
        if not curr_scheme_data:
            continue
        if m := re.search(OPEN_UNITS_RE, txt):
            curr_scheme_data["open"] = Decimal(m.group(1).replace(",", "_"))
            continue
        if m := re.search(CLOSE_UNITS_RE, txt):
            curr_scheme_data["close"] = Decimal(m.group(1).replace(",", "_"))
            continue
        if m := re.search(TRANSACTION_RE, txt, re.DOTALL):
            date = date_parser.parse(m.group(1))
            amt = Decimal(m.group(3).replace(",", "_").replace("(", "-"))
            units = Decimal(m.group(4).replace(",", "_").replace("(", "-"))
            nav = Decimal(m.group(5).replace(",", "_"))
            desc = m.group(2).strip()
            curr_scheme_data["transactions"].append(
                {
                    "date": date,
                    "description": desc,
                    "amount": amt,
                    "units": units,
                    "nav": nav,
                }
            )
    if curr_scheme_data:
        folios[current_folio]["schemes"].append(curr_scheme_data)
    return {
        "statement_period": statement_period,
        "folios": folios,
    }
