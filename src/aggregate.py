"""
Generate aggregates from VRF data.

Produces two new output files representing counts by category and make.
"""
from pathlib import Path

import pyarrow.parquet as pq
import pyarrow.compute as pc

out_dir = Path('out')
out_dir.mkdir(exist_ok=True, parents=True)

vrf_file = Path('vrf.parquet')
tbl = pq.read_table(vrf_file)

# Calculate decades of manufacture
manuf_decades = pc.multiply(pc.divide(tbl.column("Year"), 10), 10)
tbl = tbl.add_column(tbl.num_columns, 'manuf_decade', manuf_decades)

# Produce aggregates by vehicle category
cat_counts = tbl.group_by(["Category","manuf_decade"]).aggregate([
    ("Category", "count")
])
pq.write_table(cat_counts, out_dir.joinpath('counts_by_category.parquet'))

make_counts = tbl.group_by(["Make","manuf_decade"]).aggregate([
    ("Make", "count")
])
pq.write_table(make_counts, out_dir.joinpath('counts_by_make.parquet'))