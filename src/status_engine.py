def evaluate_status(previous_status, usage, usage_limit):
    """
    Evaluates final subscription status based on rules.
    """

    # CANCELLED never changes
    if previous_status == "CANCELLED":
        return "CANCELLED"

    # Usage exceeds 150% - suspend
    if usage > 1.5 * usage_limit:
        return "SUSPENDED"

    # Suspended becomes active if usage within limit
    if previous_status == "SUSPENDED" and usage <= usage_limit:
        return "ACTIVE"

    return previous_status