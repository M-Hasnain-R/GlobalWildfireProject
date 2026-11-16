
import pandas as pd

from pydantic import ValidationError
from models import WildfireRecord


def validate_records(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:

    valid_records = []
    rejected_records = []

    # Convert DataFrame into a list of dictionaries
    records = df.to_dict(orient="records")

    # Check every record
    for row_number, record in enumerate(records, start=1):

        try:

            # Validate record using Pydantic
            validated_record = WildfireRecord.model_validate(record)

            # Save valid record
            valid_records.append(
                validated_record.model_dump()
            )

        except ValidationError as error:

            # Collect error messages
            error_messages = []

            for issue in error.errors():

                field_name = ".".join(
                    str(part) for part in issue["loc"]
                )

                error_messages.append(
                    f"{field_name}: {issue['msg']}"
                )

            # Save rejected record
            rejected_records.append({
                "row_number": row_number,
                "record": record,
                "errors": error_messages
            })

    # Convert results into DataFrames
    valid_df = pd.DataFrame(valid_records)

    rejected_df = pd.DataFrame(
        rejected_records,
        columns=["row_number", "record", "errors"]
    )

    return valid_df, rejected_df
