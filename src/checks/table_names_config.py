from icu import USET_ADD_CASE_MAPPINGS, LocaleData, ULocaleDataExemplarSetType


def get_aux_codes(lang: str) -> list[str]:
    """Gets auxiliary characters for a language.

    Args:
        lang: 2 letter language code.

    Returns:
        List of auxiliary codes in U+0000 format.
    """
    return [
        f"U+{ord(x):04X}"
        for y in LocaleData(lang).getExemplarSet(
            USET_ADD_CASE_MAPPINGS,
            ULocaleDataExemplarSetType.ES_AUXILIARY,
        )
        for x in y
    ]


exclude_check = ["dv", "zh"]

exclude_case = ["ka"]

extras_si_lka = [
    "U+0041",
    "U+0042",
    "U+0043",
    "U+0044",
    "U+0045",
    "U+0049",
    "U+0050",
    "U+0052",
    "U+0053",
    "U+0054",
    "U+0059",
]

auxiliary_codes = {
    "ar-TUN": get_aux_codes("ar"),
    "en-BLM": get_aux_codes("en"),
    "en-CHN": get_aux_codes("en"),
    "en-CUW": get_aux_codes("en"),
    "en-LBN": get_aux_codes("en"),
    "en-PHL": get_aux_codes("en"),
    "en-TUR": get_aux_codes("en"),
    "en-ZAF": get_aux_codes("en"),
    "es-PAN": get_aux_codes("es"),
    "fa-AFG": [*get_aux_codes("fa"), "U+067C", "U+0685", "U+0693", "U+06C0", "U+06CD"],
    "fa-IRN": get_aux_codes("fa"),
    "ht-HTI": get_aux_codes("ht"),
    "hy-ARM": get_aux_codes("hy"),
    "ky-KGZ": [*get_aux_codes("ky"), "U+04C9", "U+04CA"],
    "my-MMR": [*get_aux_codes("my"), "U+104A", "U+200B"],
    "pt-BRA": get_aux_codes("pt"),
    "si-LKA": [*get_aux_codes("si"), *extras_si_lka],
    "tr-TUR": get_aux_codes("tr"),
    "vi-VNM": [*get_aux_codes("vi"), "U+0300", "U+0301"],
}

number_codes = [f"U+{ord(str(n)):04X}" for n in range(10)]  # U+0030-0039
punctuation_codes = [
    "U+0020",
    "U+0022",
    "U+0023",
    "U+0026",
    "U+0027",
    "U+0028",
    "U+0029",
    "U+002C",
    "U+002D",
    "U+002E",
    "U+002F",
    *number_codes,
    "U+003A",
]
punctuation_set = [chr(int(x[2:], 16)) for x in punctuation_codes]
