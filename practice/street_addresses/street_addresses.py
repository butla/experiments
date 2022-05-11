import re
from typing import Set


def _extract_street_name(address: str, matched_regex: str) -> str:
    address_without_number = re.sub(matched_regex, '', address)
    address_without_commas = address_without_number.replace(',', '')
    return address_without_commas.strip()


def _extract_for_regex(address: str, regex: str) -> Set[str]:
    match = re.search(regex, address)
    if match:
        return {
            _extract_street_name(address, regex),
            match.groups()[0]
        }
    else:
        return set()


def extract_parts(address: str) -> Set[str]:
    """Extracts a set of address parts (i.e. the street name and the street number) from written
    address string."""
    number_at_the_back = r'((?:No )?\d+\ ?[a-zA-Z]?)$'
    number_at_the_front = r'^((?:No )?\d+\ ?[a-zA-Z]?)[,\ ]'

    parts = _extract_for_regex(address, number_at_the_back)
    if parts:
        return parts

    parts = _extract_for_regex(address, number_at_the_front)
    if parts:
        return parts

    raise ValueError("The address doesn't contain a number.")
