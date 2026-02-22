def evaluate_status(previous_status, usage, usage_limit):

    if previous_status == "CANCELLED":
        return "CANCELLED"

    if usage > 1.5 * usage_limit:
        return "SUSPENDED"

    if previous_status == "SUSPENDED" and usage <= usage_limit:
        return "ACTIVE"

    return previous_status