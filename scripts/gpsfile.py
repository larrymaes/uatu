"""gpsfile.py: read LANL GPS particle data files (JSON header + whitespace columns)."""

import json
import sys

import numpy as np


def read_data(path):
    """Return the data rows as a 2D numpy array (one row per time bin)."""
    return np.loadtxt(path, comments="#")


def get_variable(data, header, name):
    """Return one variable's columns, with fill values replaced by NaN."""
    start, end = column_range(header, name)
    variables = data[:, start:end].copy()
    fill = header[name]["FILL_VALUE"]
    variables[variables == fill] = np.nan
    return variables


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

            highest_stop = max(highest_stop, stop)
    return highest_stop


if __name__ == "__main__":
    path = sys.argv[1]
    print(f"File: {path}")
    header = read_header(path)
    data = read_data(path)
    print(data.shape)
    dropped = get_variable(data, header, "dropped_data")[:, 0]
    mask = dropped == 1
    print(f"Bad rows: {np.sum(mask)}")
    print(f"Good rows: {len(dropped) - np.sum(mask)}")
    print(f"Unknown rows: {np.sum(np.isnan(dropped))}")
    all_activity = get_variable(data, header, "proton_activity")[:, 0]
    print(f"Proton activity in bad rows: {np.sum(all_activity[mask] == 1)}")
    data = data[~mask]
    activity = get_variable(data, header, "proton_activity")[:, 0]
    print(f"Proton activity rows: {np.sum(activity == 1)}")
    rates = get_variable(data, header, "rate_proton_measured")
    print("Max proton rate per channel (P1–P5):", np.nanmax(rates, axis=0))
