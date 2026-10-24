ISRAEL_KEYWORDS = [
    "israel",
    "tel aviv",
    "tel-aviv",
    "jerusalem",
    "haifa",
    "herzliya",
    "raanana",
    "ra'anana",
    "petah tikva",
    "petach tikva",
    "netanya",
    "beer sheva",
    "be'er sheva",
    "rehovot",
    "kfar saba",
    "yokneam",
    "holon",
    "ramat gan",
    "ramat hasharon",
    "modiin",
    "modi'in",
    "hod hasharon",
    "rosh haayin",
    "givatayim",
    "airport city",
    "caesarea",
    "lod",
    "rishon",
    "ashdod",
    "ashkelon",
    "bnei brak",
    "kiryat",
    "yavne",
    "nes ziona",
    "migdal haemek",
    "tirat carmel",
]


def is_israel(location: str | None) -> bool:
    if not location:
        return False

    location = location.lower()
    for keyword in ISRAEL_KEYWORDS:
        if keyword in location:
            return True
    return False
