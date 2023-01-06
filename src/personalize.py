from pathlib import Path

import pyarrow.parquet as pq


if __name__ == '__main__':
    vehicles_file = Path('vehicles.parquet')
    persons_file = Path('persons.parquet')

    # Read in the data
    vrf = pq.read_table(vehicles_file)
    persons = pq.read_table(persons_file)

    # Join the data
    joined = vrf.join(persons, keys='ID', right_keys='ID')

    # Produce the output
    pq.write_table(joined, 'vrf.parquet')