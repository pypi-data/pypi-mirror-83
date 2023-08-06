from pyspark.sql import Column, DataFrame
# noinspection PyUnresolvedReferences
from pyspark.sql.functions import col

from spark_auto_mapper.data_types.data_type_base import AutoMapperDataTypeBase


class AutoMapperDataTypeColumn(AutoMapperDataTypeBase):
    def __init__(self, value: str):
        super().__init__()
        if len(value) > 0 and value[0] == "[":
            self.value: str = value[1:-1]  # skip the first and last characters
        else:
            self.value = value

    def get_column_spec(self, source_df: DataFrame) -> Column:
        if isinstance(
            self.value, str
        ):  # if the src column is just string then consider it a sql expression
            return col(self.value)

        raise ValueError(f"value: {self.value} is not str")
