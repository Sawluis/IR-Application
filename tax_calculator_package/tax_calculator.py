class TaxRule:
    def __init__(self, min_value, max_value, remove_value, percentage, base_tax):
        self.min_value = min_value
        self.max_value = max_value
        self.remove_value = remove_value
        self.percentage = percentage
        self.base_tax = base_tax


class TaxResult:
    def __init__(self, month_salary, inss, month_salary_without_inss, annual_salary_without_inss, ir,
                 total_salary_with_deductions, parameter: TaxRule):
        self.month_salary = month_salary
        self.inss = inss
        self.month_salary_without_inss = month_salary_without_inss
        self.annual_salary_without_inss = annual_salary_without_inss
        self.ir = ir
        self.total_salary_with_deductions = total_salary_with_deductions
        self.parameter = parameter


parameters = [
    TaxRule(min_value=0.01, max_value=100000, remove_value=0, percentage=0, base_tax=0),
    TaxRule(min_value=100000, max_value=200000, remove_value=100000, percentage=0.15, base_tax=0),
    TaxRule(min_value=200000, max_value=350000, remove_value=200000, percentage=0.2, base_tax=15000),
    TaxRule(min_value=350000, max_value=500000, remove_value=350000, percentage=0.25, base_tax=45000),
    TaxRule(min_value=500000, max_value=-1, remove_value=500000, percentage=0.3, base_tax=82500)
]


def get_ir(month_salary):
    inss = round(month_salary * 0.07, 2)
    month_salary_without_inss = round(month_salary - inss, 2)
    annual_salary_without_inss = round(month_salary_without_inss * 12, 2)

    parameter = next((x for x in parameters if x.min_value < annual_salary_without_inss
                      and (x.max_value == -1 or annual_salary_without_inss <= x.max_value)), None)

    # if not parameter:
    #    return TaxResult(month_salary, inss, month_salary_without_inss, annual_salary_without_inss, 0, month_salary_without_inss)

    base_tax = parameter.base_tax
    percentage = parameter.percentage
    remove_value = parameter.remove_value

    ir = round(((annual_salary_without_inss - remove_value) * percentage + base_tax) / 12, 2)

    total_salary_with_deductions = round(month_salary_without_inss - ir, 2)

    return TaxResult(month_salary, inss, month_salary_without_inss, annual_salary_without_inss,
                     ir, total_salary_with_deductions, parameter)
