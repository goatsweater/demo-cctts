"""
Joins VRF data with details from VIN lookup.

Outputs a new file with the joined data. VRF records with no match receive null values.
"""
from pathlib import Path

import pyarrow.parquet as pq
import pyarrow.json as pajson


if __name__ == '__main__':
    vin_details_file = Path('vindetails.json')
    vrf_file = Path('vrf.parquet')

    vrf = pq.read_table(vrf_file)
    vin_details = pajson.read_json(vin_details_file)

    # Join the data
    joined = vrf.join(vin_details, keys='VIN', right_keys='vin')

    # Produce the output
    pq.write_table(joined, 'vrf_detailed.parquet')