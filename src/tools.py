"""Tool registry for the Cupid Agent.

The tools in this module use deterministic sample data for the lab.  Their
outputs are suggestions for conversation and date planning, not scientific or
professional assessments of a relationship.
"""

import unicodedata


VALID_SIGNS = {
    "bach duong": "Bß║ích D╞░╞íng",
    "kim nguu": "Kim Ng╞░u",
    "song tu": "Song Tß╗¡",
    "cu giai": "Cß╗▒ Giß║úi",
    "su tu": "S╞░ Tß╗¡",
    "xu nu": "Xß╗¡ Nß╗»",
    "thien binh": "Thi├¬n B├¼nh",
    "bo cap": "Bß╗ì Cß║íp",
    "than nong": "Bß╗ì Cß║íp",
    "nhan ma": "Nh├ón M├ú",
    "ma ket": "Ma Kß║┐t",
    "bao binh": "Bß║úo B├¼nh",
    "song ngu": "Song Ng╞░",
}

VALID_MBTI_TYPES = {
    "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP",
}

VALID_VIBES = {"lang man", "soi dong", "nhe nhang", "nghe thuat"}
VALID_BUDGETS = {"tiet kiem", "vua phai", "sang trong"}


def _normalize_text(value: object) -> str | None:
    """Return lower-case Vietnamese text without accents, or None if invalid."""
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = unicodedata.normalize("NFD", value.strip().lower())
    normalized = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return normalized.replace("─æ", "d")


def _invalid_text_error(field: str) -> str:
    return f"Lß╗ûI: '{field}' phß║úi l├á chuß╗ùi kh├┤ng rß╗ùng."


def check_horoscope_compatibility(sign1: str, sign2: str) -> str:
    """Provide a sample compatibility reading for two zodiac signs.

    Args:
        sign1: One of the 12 zodiac signs, e.g. ``'Cß╗▒ Giß║úi'``.
        sign2: One of the 12 zodiac signs, e.g. ``'Bß╗ì Cß║íp'``.

    Returns:
        A sample compatibility score and discussion prompt, or a ``Lß╗ûI:``
        message when either sign is missing or unsupported.
    """
    normalized_sign1 = _normalize_text(sign1)
    normalized_sign2 = _normalize_text(sign2)
    if normalized_sign1 is None:
        return _invalid_text_error("sign1")
    if normalized_sign2 is None:
        return _invalid_text_error("sign2")
    if normalized_sign1 not in VALID_SIGNS or normalized_sign2 not in VALID_SIGNS:
        return (
            "Lß╗ûI: Cung ho├áng ─æß║ío kh├┤ng hß╗úp lß╗ç. Vui l├▓ng nhß║¡p mß╗Öt trong 12 cung "
            "ho├áng ─æß║ío chuß║⌐n."
        )

    first_sign = VALID_SIGNS[normalized_sign1]
    second_sign = VALID_SIGNS[normalized_sign2]
    pair = frozenset((first_sign, second_sign))
    if pair == frozenset(("Cß╗▒ Giß║úi", "Bß╗ì Cß║íp")):
        reading = "95% ΓÇö c├╣ng hß╗ç Thß╗ºy, dß╗à ─æß╗ông cß║úm v├á gß║»n kß║┐t s├óu sß║»c"
    elif pair == frozenset(("Kim Ng╞░u", "Xß╗¡ Nß╗»")):
        reading = "90% ΓÇö c├╣ng hß╗ç ─Éß║Ñt, thß╗▒c tß║┐ v├á c├│ thß╗â x├óy dß╗▒ng sß╗▒ tin cß║¡y"
    else:
        reading = "80% ΓÇö c├│ tiß╗üm n─âng; n├¬n lß║»ng nghe v├á trao ─æß╗òi kß╗│ vß╗ìng r├╡ r├áng"
    return f"≡ƒÆÿ Gß╗úi ├╜ tham khß║úo vß╗ü {first_sign} & {second_sign}: {reading}."


def calculate_mbti_compatibility(mbti1: str, mbti2: str) -> str:
    """Provide a sample communication-compatibility reading for two MBTI types.

    Args:
        mbti1: One of the 16 valid four-letter MBTI types, e.g. ``'INTJ'``.
        mbti2: One of the 16 valid four-letter MBTI types, e.g. ``'ENFP'``.

    Returns:
        A sample compatibility insight, or a ``Lß╗ûI:`` message for invalid input.
    """
    normalized_mbti1 = _normalize_text(mbti1)
    normalized_mbti2 = _normalize_text(mbti2)
    if normalized_mbti1 is None:
        return _invalid_text_error("mbti1")
    if normalized_mbti2 is None:
        return _invalid_text_error("mbti2")

    first_type = normalized_mbti1.upper()
    second_type = normalized_mbti2.upper()
    if first_type not in VALID_MBTI_TYPES or second_type not in VALID_MBTI_TYPES:
        return "Lß╗ûI: MBTI kh├┤ng hß╗úp lß╗ç. Vui l├▓ng nhß║¡p mß╗Öt trong 16 m├ú MBTI chuß║⌐n, v├¡ dß╗Ñ INTJ hoß║╖c ENFP."

    if frozenset((first_type, second_type)) == frozenset(("INTJ", "ENFP")):
        reading = "92% ΓÇö kh├íc biß╗çt c├│ thß╗â bß╗ò trß╗ú nß║┐u cß║ú hai t├┤n trß╗ìng nhß╗ïp giao tiß║┐p"
    else:
        reading = "85% ΓÇö c├│ thß╗â tß║ío tiß║┐ng n├│i chung khi chß╗º ─æß╗Öng trao ─æß╗òi nhu cß║ºu"
    return f"≡ƒº⌐ Gß╗úi ├╜ tham khß║úo MBTI {first_type} & {second_type}: {reading}."


def search_date_ideas(location: str, vibe: str, budget: str = "vß╗½a phß║úi") -> str:
    """Suggest deterministic sample date ideas for a supported city.

    Args:
        location: ``'H├á Nß╗Öi'`` or ``'TP.HCM'`` (common aliases are accepted).
        vibe: One of ``l├úng mß║ín``, ``s├┤i ─æß╗Öng``, ``nhß║╣ nh├áng``, ``nghß╗ç thuß║¡t``.
        budget: One of ``tiß║┐t kiß╗çm``, ``vß╗½a phß║úi``, ``sang trß╗ìng``.

    Returns:
        Two sample date ideas, or a ``Lß╗ûI:`` message when an argument is invalid.
    """
    normalized_location = _normalize_text(location)
    normalized_vibe = _normalize_text(vibe)
    normalized_budget = _normalize_text(budget)
    if normalized_location is None:
        return _invalid_text_error("location")
    if normalized_vibe is None:
        return _invalid_text_error("vibe")
    if normalized_budget is None:
        return _invalid_text_error("budget")
    if normalized_vibe not in VALID_VIBES:
        return "Lß╗ûI: Vibe kh├┤ng hß╗úp lß╗ç. Chß╗ìn: l├úng mß║ín, s├┤i ─æß╗Öng, nhß║╣ nh├áng hoß║╖c nghß╗ç thuß║¡t."
    if normalized_budget not in VALID_BUDGETS:
        return "Lß╗ûI: Ng├ón s├ích kh├┤ng hß╗úp lß╗ç. Chß╗ìn: tiß║┐t kiß╗çm, vß╗½a phß║úi hoß║╖c sang trß╗ìng."

    if normalized_location in {"ha noi", "hanoi"}:
        return (
            f"≡ƒôì Gß╗úi ├╜ mß║½u tß║íi H├á Nß╗Öi (vibe: {vibe.strip()}, ng├ón s├ích: {budget.strip()}):\n"
            "1. C├á ph├¬ ngß║»m ho├áng h├┤n Hß╗ô T├óy ─æß╗â tr├▓ chuyß╗çn trong kh├┤ng gian ß║Ñm c├║ng.\n"
            "2. ─Éi dß║ío phß╗æ cß╗ò v├á thß╗¡ ß║⌐m thß╗▒c ─æ├¬m ─æß╗â tß║ío chß╗º ─æß╗ü tr├▓ chuyß╗çn tß╗▒ nhi├¬n."
        )
    if normalized_location in {"ho chi minh", "tp.hcm", "tphcm", "hcm", "sai gon", "saigon"}:
        return (
            f"≡ƒôì Gß╗úi ├╜ mß║½u tß║íi TP.HCM (vibe: {vibe.strip()}, ng├ón s├ích: {budget.strip()}):\n"
            "1. ─Éi Waterbus Bß║┐n Bß║ích ─Éß║▒ng rß╗ôi d├╣ng bß╗»a tß╗æi nhß║╣.\n"
            "2. Tham gia workshop l├ám gß╗æm hoß║╖c vß║╜ tranh cß║╖p ─æ├┤i ─æß╗â c├╣ng trß║úi nghiß╗çm."
        )
    return "Lß╗ûI: Ch╞░a c├│ dß╗» liß╗çu gß╗úi ├╜ hß║╣n h├▓ cho ─æß╗ïa ─æiß╗âm n├áy. Hß╗ù trß╗ú: H├á Nß╗Öi, TP.HCM."


AVAILABLE_TOOLS = {
    "check_horoscope_compatibility": check_horoscope_compatibility,
    "calculate_mbti_compatibility": calculate_mbti_compatibility,
    "search_date_ideas": search_date_ideas,
}
