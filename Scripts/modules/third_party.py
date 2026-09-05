import argparse

class ParseRangeAction(argparse.Action):
    """Custom argparse action.
    Parses a comma-separated string of integers and ranges into a sorted list of unique integers.

    Sample input formats: "all", 0-100, 1-10,15,20
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # 1. Handle 'all' keyword
        if values[0] == "all":
            setattr(namespace, self.dest, ["all"])
            return

        # 2. Parse numbers/ranges into integers for sorting and deduplication
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

        # 3. Always store as list[str] to prevent type mixing downstream
        setattr(namespace, self.dest, [str(n) for n in sorted(numbers)])
