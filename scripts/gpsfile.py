"""gpsfile.py: read LANL GPS particle data files (JSON header + whitespace columns)."""

import json


def read_header(path):
    """Return the file's JSON header as a dict."""
    header_lines = []

    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                header_lines.append(line[1:])
            else:
                break

    header_string = "".join(header_lines)
    header_data = json.loads(header_string)

    return header_data


def column_range(header, name):
    """Return (start, stop) column indexes for a variable, like range()."""
    var_info = header[name]
    start = var_info["START_COLUMN"]
    stop = start + var_info["DIMENSION"][0]
    return start, stop


def expected_columns(header):
    """Return how many columns each data row should have, according to the header."""
    highest_stop = 0
    for key, value in header.items():
        if isinstance(value, dict):
            _, stop = column_range(header, key)

            if stop > highest_stop:
                highest_stop = stop
    return highest_stop


if __name__ == "__main__":
    path = "data/raw/ns64_170903_v1.10.ascii"
    header = read_header(path)

    print(f"{'Variable Name':28} {'Columns':12} {'Units'}")
    print("-" * 55)
    for key, value in header.items():
        if isinstance(value, dict):
            start, stop = column_range(header, key)
            units = value.get("UNITS", "N/A")
            print(f"{key:28} cols {start:3}-{stop - 1:<3} {units}")

    print("\n" + "=" * 55 + "\n")

    expected = expected_columns(header)
    print(f"Expected columns (from header): {expected}")

    actual = 0
    with open(path) as file:
        for line in file:
            if not line.startswith("#"):
                actual = len(line.split())
                break

    print(f"Actual columns (first data row): {actual}")
    print(f"Do the two numbers match? {'Yes' if expected == actual else 'No'}")
