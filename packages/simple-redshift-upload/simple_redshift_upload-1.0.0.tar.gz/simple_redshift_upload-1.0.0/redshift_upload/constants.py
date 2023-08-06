import numpy
import re
from typing import Dict, List, Union
import pandas


NaT = numpy.datetime64("NaT")
DTYPE_MAPS = {
    "int64": "bigint",
    "float64": "double precision",
    "bool": "bool",
    "datetime64[ns]": "timestamp",
}
UPLOAD_DEFAULTS = {
    "truncate_table": False,
    "drop_table": False,
    "cleanup_s3": False,
    "grant_access": [],
    "diststyle": "even",
    "distkey": None,
    "sortkey": None,
    "load_in_parallel": 1,  # count of parallel files
}
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DATE_FORMAT = "%Y-%m-%d"
MAX_COLUMN_LENGTH = 63
varchar_len_re = re.compile(r"\((\d+)\)")
SourceOptions = Union[str, pandas.DataFrame, List[Dict]]
