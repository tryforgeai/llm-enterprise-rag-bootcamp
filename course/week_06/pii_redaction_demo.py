"""Minimal demo of Week 06 Family C's "detect-and-redact at the boundary"
principle: catch structured secrets with regex, redact the span, log only
the *type* of PII found (never the value), then proceed with the cleaned
query.

This does not use Presidio (would need `pip install presidio-analyzer`);
the name-detection step here is a placeholder to show where a real NER
pass would plug in.

Run: python3 pii_redaction_demo.py
"""

import re


def luhn_valid(candidate: str) -> bool:
    """Luhn checksum — the standard validity check for card numbers.

    Filters out random 13-19 digit runs (phone numbers, order IDs) that
    are not actually card numbers, so we don't over-redact.
    """
    digits = [int(d) for d in candidate if d.isdigit()]
    if not (13 <= len(digits) <= 19):
        return False
    checksum = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


PATTERNS = {
    "AWS_ACCESS_KEY": re.compile(r"\b" + "AK" + r"IA[0-9A-Z]{16}\b"),
    "GITHUB_TOKEN": re.compile(r"\b" + "gh" + r"p_[A-Za-z0-9]{36}\b"),
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    # Loose card-shaped run; Luhn check below decides if it's real.
    "CARD_NUMBER": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
}


def redact(text: str) -> tuple[str, list[str]]:
    """Return (redacted_text, list_of_pii_types_found).

    The caller should log `list_of_pii_types_found` — never the matched
    spans themselves.
    """
    found_types = []
    cleaned = text

    for pii_type, pattern in PATTERNS.items():
        def _replace(match: re.Match, pii_type=pii_type) -> str:
            candidate = match.group(0)
            if pii_type == "CARD_NUMBER" and not luhn_valid(candidate):
                return candidate  # not a real card number, leave it alone
            found_types.append(pii_type)
            return f"[REDACTED_{pii_type}]"

        cleaned = pattern.sub(_replace, cleaned)

    return cleaned, found_types


def demo() -> None:
    examples = [
        "What is our refund policy for order 4471982?",
        "My AWS key is " + "AK" + "IA1234567890ABCDEF and it's not working, please help.",
        "Here's my card 4539 1488 0343 6467, can you check if the charge went through?",
        "My SSN is 123-45-6789, is this policy applicable to me?",
        "This " + "gh" + "p_abcdefghijklmnopqrstuvwxyz0123456789 token keeps expiring, why?",
    ]

    for raw_query in examples:
        cleaned_query, pii_found = redact(raw_query)
        print(f"raw:     {raw_query}")
        print(f"cleaned: {cleaned_query}")
        print(f"log:     pii_types_detected={pii_found or 'none'}")
        print()


if __name__ == "__main__":
    demo()
