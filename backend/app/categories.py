import re

CATEGORY_RULES: list[tuple[str, str]] = [
    ("student", r"\b(student|interns?|internship|graduate|co-?op|apprentice)\b|סטודנט"),
    (
        "software",
        r"\b(software|developer|programmer|back-?end|front-?end|full[ -]?stack|mobile|ios|android|"
        r"web|java|python|golang|node(\.?js)?|react|angular|c\+\+|c#|\.net|rust|scala|ruby|php|"
        r"sdk|embedded|firmware|algorithm|r&d|engineering (team )?(lead|manager)|"
        r"vp (of )?(r&d|engineering)|staff engineer|architect)\b",
    ),
    ("qa", r"\b(qa|quality assurance|sdet|testers?|testing|automation (engineer|developer)|validation)\b"),
    (
        "devops",
        r"\b(devops|dev ops|sre|site reliability|infrastructure|platform engineer|cloud engineer|"
        r"systems? engineer|devsecops|release engineer|build engineer|kubernetes|mlops)\b",
    ),
    (
        "data",
        r"\b(data|machine learning|ml|ai|nlp|deep learning|computer vision|llm|bi|analytics|"
        r"researcher|applied scientist|dba)\b",
    ),
    (
        "security",
        r"\b(security|vulnerabilit\w*|malware|threats?|penetration|pentest\w*|red team|cyber\w*|"
        r"reverse engineer\w*|exploit\w*|soc|appsec|ciso|incident response|forensics?)\b",
    ),
    ("product", r"\b(product (manager|owner|lead|analyst|operations)|head of product|vp product|cpo|ux|ui)\b"),
    ("design", r"\b(designer|design lead|creative|graphic|illustrator|animator|motion (designer|graphics)|art director)\b"),
    (
        "hardware",
        r"\b(hardware|electronics?|electrical|mechanical|rf|fpga|asic|vlsi|pcb|analog|digital design|"
        r"verification engineer|physical design|chip|silicon|optical|optics|mechatronics)\b",
    ),
    ("it", r"\b(it|helpdesk|help desk|it support|sysadmin|system administrator|network engineer|desktop support)\b"),
    (
        "sales-marketing",
        r"\b(sales|account (executive|manager)|sdr|bdr|marketing|customer success|business development|"
        r"growth|seo|content|partnerships?|solutions? (engineer|architect)|pre-?sales)\b",
    ),
]

COMPILED_RULES = [(slug, re.compile(pattern, re.IGNORECASE)) for slug, pattern in CATEGORY_RULES]

OTHER = "other"
ALL_CATEGORIES = [slug for slug, _ in CATEGORY_RULES] + [OTHER]


def categorize(title: str) -> list[str]:
    categories: list[str] = []

    for slug, pattern in COMPILED_RULES:
        if pattern.search(title):
            categories.append(slug)

    if not categories:
        categories.append(OTHER)

    return categories
