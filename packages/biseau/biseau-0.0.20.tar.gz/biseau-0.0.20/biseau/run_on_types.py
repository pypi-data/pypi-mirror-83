"""Definition of some types, to be used as parameter
annotation in python plugins, e.g:

    from biseau.run_on_types import percent

    def run_on(models:iter, *, support:percent):
        ...

"""

def percent(value:int) -> int:
    "A int between 0 and 100, inclusive"
    return min(100, max(0, int(value)))

def ratio(value:float) -> float:
    "A number between 0 and 1, inclusive"
    return min(1., max(0, float(value)))


all_types = {percent, ratio}
