"""
Dump the contents of the ``VIN`` field from an input dataset.

The output ends up on ``STDOUT`` to enable pipeline processing using standard unix tools.
"""
import json
from pathlib import Path

import pyarrow.parquet as pq

vrf_file = Path("vrf.parquet")

tbl = pq.read_table(vrf_file)
vins = tbl.column('VIN').to_pylist()

with open('vins.txt', 'w') as out:
    json.dump(vins, out)