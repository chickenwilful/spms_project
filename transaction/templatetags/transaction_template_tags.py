from django import template

register = template.Library()

@register.filter(name="area_sqm_range")
def area_sqm_range(transaction):
    if transaction.area_sqm_min is None:
        return "-"
    elif transaction.area_sqm_min == transaction.area_sqm_max:
        return transaction.area_sqm_min
    elif transaction.area_sqm_max is None:
        return "> {0}".format(transaction.area_sqm_min)
    else:
        return "{0} - {1}".format(transaction.area_sqm_min, transaction.area_sqm_max)


@register.filter(name="area_sqft_range")
def area_sqft_range(transaction):
    if transaction.area_sqft_min is None:
        return "-"
    elif transaction.area_sqft_min == transaction.area_sqft_max:
        return "%.1f" % transaction.area_sqft_min
    elif transaction.area_sqft_max is None:
        return "> {0}".format("%.1f" % transaction.area_sqft_min)
    else:
        return "{0} - {1}".format("%.1f" % transaction.area_sqft_min, "%.1f" % transaction.area_sqft_max)


@register.filter(name="refine")
def refine(string):
    if string is None:
        return "-"
    else:
        return string


@register.filter(name="actualType")
def actualType(type):
    if type == "h":
        return "HDB"
    else:
        return "Condo"