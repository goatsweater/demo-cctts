import io
from typing import Tuple

import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.parquet as pq
from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker('en_CA')
# Currently using custom provider at https://github.com/goatsweater/faker_vehicle/tree/vin
fake.add_provider(VehicleProvider)

RECORD_COUNT=3


def gen_records(headers: Tuple[str], cols: Tuple[str], rows: int) -> io.BytesIO:
    """Generate data and deliver it as bytes."""
    data = fake.csv(header=headers, data_columns=cols, num_rows=rows, include_row_ids=True)

    data_bytes = io.BytesIO(data.encode())
    return data_bytes


def to_table(source: io.BytesIO) -> pa.Table:
    tbl = pacsv.read_csv(source)
    return tbl


if __name__ == '__main__':
    # Generate some vehicle data
    vehicles = gen_records(
        headers=('Year', 'Make', 'Model', 'Category', 'Date', 'Plate', 'VIN'),
        cols=(
            '{{vehicle_year}}', '{{vehicle_make}}', '{{vehicle_model}}', 
            '{{vehicle_category}}', '{{date}}', '{{license_plate}}', '{{vehicle_vin}}'
        ),
        rows=RECORD_COUNT
    )
    vehicles_tbl = to_table(vehicles)
    pq.write_table(vehicles_tbl, 'vehicles.parquet')

    # Generate some people data
    persons = gen_records(
        headers=('Name', 'Address', 'Phone'),
        cols=('{{name}}', '{{address}}', '{{phone_number}}'),
        rows=RECORD_COUNT
    )
    persons_tbl = to_table(persons)
    pq.write_table(persons_tbl, 'persons.parquet')
