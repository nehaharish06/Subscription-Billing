def calculate_bill(monthly_fee, usage, usage_limit, status):
    """
    Calculates total bill and overage based on business rules.
    Returns (total_bill, overage_gb)
    """

    # CANCELLED - no billing
    if status == "CANCELLED":
        return 0.0, 0.0

    # SUSPENDED - monthly fee only, no overage charge
    if status == "SUSPENDED":
        return float(monthly_fee), 0.0

    # ACTIVE billing
    if usage <= usage_limit:
        return float(monthly_fee), 0.0

    overage_gb = usage - usage_limit
    overage_charge = overage_gb * 10
    total_bill = float(monthly_fee) + overage_charge

    return float(total_bill), float(overage_gb)