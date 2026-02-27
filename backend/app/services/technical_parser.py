import re

CIRCUIT_LINE_REGEX = re.compile(
    r"(?P<circuit>CIR[-\w/]+).*?(?P<power>\d+[\.,]?\d*)\s*kW.*?(?P<breaker>\d+[\.,]?\d*)\s*A",
    re.IGNORECASE,
)

MATERIAL_LINE_REGEX = re.compile(
    r"(?P<code>[A-Z0-9\-]{3,})\s*[-;]\s*(?P<desc>[^\n]+?)\s+(?P<qty>\d+[\.,]?\d*)\s*(?P<unit>un|m|kg|cx)?$",
    re.IGNORECASE | re.MULTILINE,
)


def parse_circuits(text: str) -> list[dict]:
    circuits = []
    for match in CIRCUIT_LINE_REGEX.finditer(text):
        circuits.append(
            {
                "circuit_code": match.group("circuit"),
                "power_kw": float(match.group("power").replace(",", ".")),
                "breaker_a": float(match.group("breaker").replace(",", ".")),
            }
        )
    return circuits


def parse_materials(text: str) -> list[dict]:
    materials = []
    for match in MATERIAL_LINE_REGEX.finditer(text):
        materials.append(
            {
                "material_code": match.group("code"),
                "description": match.group("desc").strip(),
                "quantity": float(match.group("qty").replace(",", ".")),
                "unit": (match.group("unit") or "un").lower(),
            }
        )
    return materials
