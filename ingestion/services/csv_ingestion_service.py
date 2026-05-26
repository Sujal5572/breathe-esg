# import csv

# from ingestion.models import ImportBatch, RawRecord
# from records.models import NormalizedRecord

# from normalization.services.header_mapper import normalize_headers
# from normalization.services.date_parser import parse_date
# from normalization.services.unit_converter import normalize_unit
# from normalization.services.suspicious_detector import (
#     detect_suspicious_record,
# )


# def ingest_csv(file_path, organization, data_source, user):
#     batch = ImportBatch.objects.create(
#         organization=organization,
#         data_source=data_source,
#         uploaded_by=user,
#         filename=file_path.split("/")[-1],
#         status="processing",
#     )

#     total_rows = 0
#     failed_rows = 0

#     with open(file_path, newline="") as csvfile:
#         reader = csv.DictReader(csvfile)

#         for row_number, row in enumerate(reader, start=1):
#             total_rows += 1

#             try:
#                 normalized_headers = normalize_headers(row)

#                 raw_record = RawRecord.objects.create(
#                     organization=organization,
#                     import_batch=batch,
#                     source_row_number=row_number,
#                     raw_payload=normalized_headers,
#                     ingestion_status="parsed",
#                 )

#                 quantity = normalized_headers.get("fuel_quantity")
#                 source_unit = normalized_headers.get("Einheit")

#                 normalized_quantity, normalized_unit = normalize_unit(
#                     quantity,
#                     source_unit,
#                 )

#                 suspicious_result = detect_suspicious_record({
#                     "quantity": normalized_quantity,
#                     "source_unit": source_unit,
#                 })

#                 NormalizedRecord.objects.create(
#                     organization=organization,
#                     raw_record=raw_record,
#                     activity_type="fuel_combustion",
#                     scope="Scope 1",
#                     activity_date=parse_date(
#                         normalized_headers.get("date")
#                     ),
#                     quantity=normalized_quantity,
#                     normalized_unit=normalized_unit,
#                     source_unit=source_unit,
#                     facility=normalized_headers.get("plant_code"),
#                     suspicious=suspicious_result["suspicious"],
#                     suspicious_reasons=suspicious_result["reasons"],
#                 )

#             except Exception as e:
#                 failed_rows += 1

#                 RawRecord.objects.create(
#                     organization=organization,
#                     import_batch=batch,
#                     source_row_number=row_number,
#                     raw_payload=row,
#                     parse_errors=[str(e)],
#                     ingestion_status="failed",
#                 )

#     batch.total_rows = total_rows
#     batch.failed_rows = failed_rows
#     batch.status = "completed"

#     batch.save()

#     return batch


import csv

from records.models import NormalizedRecord

from normalization.services.header_mapper import normalize_headers
from normalization.services.date_parser import parse_date
from normalization.services.unit_converter import normalize_unit
from normalization.services.suspicious_detector import (
    detect_suspicious_record,
)


class DummyBatch:
    id = 1


def ingest_csv(file_path, organization, data_source, user):

    with open(file_path, newline="", encoding="utf-8") as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            normalized_headers = normalize_headers(row)

            quantity = float(
                normalized_headers.get(
                    "fuel_quantity",
                    0
                )
            )

            source_unit = normalized_headers.get(
                "unit"
            )

            normalized_quantity, normalized_unit = normalize_unit(
                quantity,
                source_unit,
            )

            suspicious_result = detect_suspicious_record({
                "quantity": normalized_quantity,
                "source_unit": source_unit,
            })

            NormalizedRecord.objects.create(
                organization=organization,
                activity_type="fuel_combustion",
                scope="Scope 1",
                activity_date=parse_date(
                    normalized_headers.get("date")
                ),
                quantity=normalized_quantity,
                normalized_unit=normalized_unit,
                source_unit=source_unit,
                facility=normalized_headers.get(
                    "plant_code"
                ),
                suspicious=suspicious_result["suspicious"],
                suspicious_reasons=suspicious_result["reasons"],
                review_status="pending",
            )

    return DummyBatch()