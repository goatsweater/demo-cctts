"""
Simulates interaction with an API.

Takes an input VIN and writes related data to a file as JSON.
This is merely passing the input VIN through the `vininfo` Python package.
"""
import argparse
import json
from pathlib import Path

from vininfo import Vin

parser = argparse.ArgumentParser()
parser.add_argument('vin')
args = parser.parse_args()

save_dir = Path('vins')
save_dir.mkdir(exist_ok=True, parents=True)

vin = Vin(args.vin)
details = {
    'checksum': vin.verify_checksum(),
    'wmi': vin.wmi,
    'vds': vin.vds,
    'vis': vin.vis,
    'manufacturer': vin.manufacturer,
    'is_small': vin.manufacturer_is_small,
    'region_code': vin.region_code,
    'region': vin.region,
    'country_code': vin.country_code,
    'country': vin.country,
    'vin': args.vin,
}

outfile = save_dir.joinpath(f"{args.vin}.json")
json.dump(details, outfile.open("w"))