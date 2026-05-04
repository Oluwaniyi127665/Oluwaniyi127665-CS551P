SCHOOL_STATUS_LABELS = {
    "1": "Open",
    "2": "Closed",
    "3": "Proposed to open",
    "4": "Proposed to close",
}


SCHOOL_TYPE_LABELS = {
    "01": "First school, 5-8",
    "02": "First school, 5-9",
    "03": "First school, 5-10",
    "04": "First and middle school, 5-12",
    "05": "Middle school, 8-12, deemed primary",
    "06": "Middle school, 9-13, deemed primary",
    "07": "Middle school, 9-13, deemed secondary",
    "08": "Middle school, 10-13, deemed secondary",
    "09": "Comprehensive upper school, 12-15/16",
    "10": "Comprehensive upper school, 12-18",
    "11": "Community school",
    "12": "Foundation school",
    "14": "Free schools",
    "15": "LA nursery school",
    "18": "Further education",
    "27": "Academy sponsor led",
    "28": "Academy converter",
    "29": "University technical college",
    "32": "Studio schools",
    "33": "Academy special converter",
    "34": "Academy special sponsor led",
    "35": "Academy alternative provision converter",
    "36": "Academy alternative provision sponsor led",
    "44": "Secure units",
}

REGION_LABELS = {
    "E12000001": "North East",
    "E12000002": "North West",
    "E12000003": "Yorkshire and the Humber",
    "E12000004": "East Midlands",
    "E12000005": "West Midlands",
    "E12000006": "East of England",
    "E12000007": "London",
    "E12000008": "South East",
    "E12000009": "South West",
}


def school_status_label(code):
    if not code:
        return "Unknown"
    return SCHOOL_STATUS_LABELS.get(code, f"Status code {code}")


def school_type_label(code):
    if not code:
        return "Unknown"
    return SCHOOL_TYPE_LABELS.get(code, f"Type code {code}")


def region_label(code):
    if not code:
        return "Unknown"
    return REGION_LABELS.get(code, code)
