import argparse

# this is a convenience class to set a 3rd variable to true, allowing
#  us to figure out if we have any options set for a given module.
#  this makes spawning the clients smarter
class pgfAction(argparse.Action):
    def __init__(self, option_strings, dest, module=None, **kwargs):
        if module == None:
            raise ValueError("must specify a module")
        super().__init__(option_strings, dest, **kwargs)
        self.module = module

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        setattr(namespace, self.module, True)

class pgfBoolAction(argparse.BooleanOptionalAction):
    def __init__(self, option_strings, dest, module=None, **kwargs):
        if module == None:
            raise ValueError("must specify a module")
        super().__init__(option_strings, dest, **kwargs)
        self.module = module

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.module, True)
        super().__call__(parser, namespace, values, option_string)
        
class ParseRangeAction(argparse.Action):
    """Custom argparse action.
    Parses a comma-separated string of integers and ranges into a sorted list of unique integers.

    Sample input formats:
        0-100       # resolves to 0 1 2 3 4 ... 100
        1-3,15,20  # resolves to 1 2 3 15 20
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # Parse numbers/ranges into integers for sorting and deduplication
        numbers = set()
        for item in values:
            for part in item.split(","):
                part = part.strip()
                if not part:
                    continue
                if "-" in part:
                    try:
                        start, end = map(int, part.split("-"))
                        start, end = min(start, end), max(start, end)
                        numbers.update(range(start, end + 1))
                    except ValueError:
                        raise argparse.ArgumentError(
                            self, f"Invalid range format: '{part}'"
                        )
                else:
                    try:
                        numbers.add(int(part))
                    except ValueError:
                        raise argparse.ArgumentError(
                            self, f"Invalid integer: '{part}'"
                        )

        # Always store as list[str] to prevent type mixing downstream
        setattr(namespace, self.dest, [str(n) for n in sorted(numbers)])

