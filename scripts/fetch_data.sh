#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://www.ngdc.noaa.gov/stp/space-weather/satellite-data/satellite-systems/lanl_gps/version_v1.10r1"
SAT="ns64"
WEEKS=("170903" "170910")
OUT_DIR="data/raw"

mkdir -p "$OUT_DIR"

for week in "${WEEKS[@]}"; do
    FILENAME="${SAT}_${week}_v1.10.ascii"
    URL="${BASE_URL}/${SAT}/${FILENAME}"
    FILE_PATH="${OUT_DIR}/${FILENAME}"

    if [ -s "$FILE_PATH" ]; then
        echo "File $FILENAME already downloaded and non-empty. Skipping..."
        continue
    fi

    echo "Downloading $FILENAME..."
    curl -f -L "$URL" -o "${FILE_PATH}.part"
    mv "${FILE_PATH}.part" "$FILE_PATH"
done

echo "I am Uatu. I have observed the data from $SAT, recorded faithfully within $OUT_DIR."
