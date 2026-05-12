VALID_TRANSITIONS = {
    "WISHLIST": ["APPLIED"],
    "APPLIED": ["SCREENING", "REJECTED", "GHOSTED"],
    "SCREENING": ["INTERVIEWING", "REJECTED"],
    "INTERVIEWING": ["OFFER", "REJECTED"],
    "OFFER": ["ACCEPTED", "DECLINED"],
    "ACCEPTED": [],
    "DECLINED": [],
    "REJECTED": [],
    "GHOSTED": ["APPLIED"],  # they came back months later
}


def validate_transition(from_status: str, to_status: str) -> None:
    allowed = VALID_TRANSITIONS.get(from_status, [])
    if to_status not in allowed:
        raise ValueError(
            f"Cannot transition from {from_status} to {to_status}."
            f"Allowed: {allowed}"
        )
