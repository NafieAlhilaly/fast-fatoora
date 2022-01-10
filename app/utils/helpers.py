def calc_tax_from_total(total: float, tax_amount: float) -> float:
    if tax_amount is None:
        return total * 0.15
    return tax_amount
