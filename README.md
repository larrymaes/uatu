# Uatu

Uatu downloads public energetic particle data from detectors flown on GPS satellites,
checks each file for problems, and reports on the radiation environment those satellites
fly through, including flagging solar storms.

Named after Marvel's Watcher, who observes from the Moon and never interferes.

This is a learning project for practicing data pipelines, Python, Bash, and Git.

## Status

Mission 1: The Watch (in progress)

- [x] Set up the environment and repo
- [ ] Download one satellite's data for September 2017 (weeks starting Sept 3 and Sept 10)
- [ ] Read a data file and parse its JSON header
- [ ] Drop bad records and check for fill values
- [ ] Plot proton and electron rates across both weeks
- [ ] Flag periods of significant proton activity
- [ ] Run the pipeline on a schedule and log the results

Future missions:

- [ ] Mission 2: Tremors (earthquake vs. explosion)
- [ ] Mission 3: False Light (lightning vs. the "double flash")

## How it works

| Step | Script | What it does |
|---|---|---|
| 1. Download | `fetch_data.sh` | Downloads weekly data files for one GPS satellite from NOAA NCEI. Skips files it already has and downloads to a temporary file first, so a broken download never looks complete. |
| 2. Check | *planned* | Reads the JSON header, finds each column, and drops records marked bad. |
| 3. Report | *planned* | Plots particle rates over time and flags proton events. |

Downloaded data goes to `data/raw/`, which is not committed to the repo.

## Usage

```bash
# Set up the environment
micromamba create -n uatu -c conda-forge python numpy pandas matplotlib
micromamba activate uatu

# Download the data
./scripts/fetch_data.sh
```

## Data

GPS Energetic Particle Data (CXD and BDD-IIR), released by Los Alamos National Laboratory
and hosted by NOAA's National Centers for Environmental Information
(https://www.ncei.noaa.gov/products/GPS-energetic-particles).
