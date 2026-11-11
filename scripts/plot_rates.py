"""plot_rates.py: plot GPS proton rates for September 2017 to show the solar storm."""

import matplotlib.pyplot as plt
import numpy as np
from gpsfile import get_variable, read_data, read_header

PATHS = [
    "data/raw/ns64_170903_v1.10.ascii",
    "data/raw/ns64_170910_v1.10.ascii",
]
OUT = "docs/proton_rates.png"


def load_rates(path):
    """Return (day, rates, activity) for one file; dropped rows have NaN rates."""
    header = read_header(path)
    data = read_data(path)

    dropped = get_variable(data, header, "dropped_data")[:, 0]
    mask = dropped == 1

    day = get_variable(data, header, "decimal_day")[:, 0]
    rates = get_variable(data, header, "rate_proton_measured")
    rates[mask] = np.nan
    activity = get_variable(data, header, "proton_activity")[:, 0]

    return day, rates, activity


if __name__ == "__main__":
    days_list = []
    rates_list = []
    activity_list = []
    for path in PATHS:
        day, rates, activity = load_rates(path)
        days_list.append(day)
        rates_list.append(rates)
        activity_list.append(activity)

    days_all = np.concatenate(days_list)
    rates_all = np.concatenate(rates_list)
    activity_all = np.concatenate(activity_list)

    fig, ax = plt.subplots(figsize=(12, 5))

    for i in range(rates_all.shape[1]):
        ax.plot(days_all, rates_all[:, i], label=f"P{i + 1}")

    ax.fill_between(
        days_all,
        0,
        1,
        where=activity_all == 1,
        transform=ax.get_xaxis_transform(),
        color="red",
        alpha=0.1,
        label="proton_activity flag",
    )
    ax.set_yscale("log")
    ax.set_xlabel("Day of year, 2017 (Sept 3 = 246, Sept 10 = 253)")
    ax.set_ylabel("Proton Rate (Hz)")
    ax.set_title("ns64 GPS proton rates: September 2017 solar storm")
    ax.legend()

    fig.tight_layout()
    fig.savefig(OUT, dpi=150)
    print(f"The Watcher has recorded what he saw. Chart saved to {OUT}")
