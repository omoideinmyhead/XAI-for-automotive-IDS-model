import re
import pandas as pd
from pathlib import Path


# define a regex pattern for a line of log
pattern = re.compile(
    # timestamp: (1739211044.348054)
    r"^\((?P<timestamp>[0-9.]+)\)\s+"
    # interface: can1
    r"(?P<interface>can\d+)\s+"
    # can id: 1A555552 or 1AB
    r"(?P<can_id>[0-9A-Fa-f]+)"
    # separator: # or ##1
    r"(?P<separator>##[0-9A-Fa-f]|#)"
    # data: 4D0A00007E004006FB00FF00F900FD0000000000000000000400000000000000000000F40140FFEB7FF387DD017D0000
    r"(?P<data>[0-9A-Fa-f]*)"
    # label: R or T
    r"(?:\s+(?P<label>R|T))"
    r"$"
)

def parse_can_log(file_path: str | Path, max_lines: int | None = None) -> pd.DataFrame:
    """
    read a CAN log file 
    match every line to the established pattern
    convert the log file to a dataframe
    """
    rows = []
    file_path = Path(file_path)

    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            if max_lines is not None and i >= max_lines:
                break

            line = line.strip()
            match = pattern.match(line)

            if match:
                row = match.groupdict()

                row["timestamp"] = float(row["timestamp"])
                row["protocol"] = "CAN_FD" if row["separator"].startswith("##") else "CAN_CC"
                row["payload_length"] = len(row["data"]) // 2
                row["source_file"] = file_path.name

                rows.append(row)

    return pd.DataFrame(rows)

df = parse_can_log(
    "CAN_train/CAN/benign/Benign-FastDriving-DrivingSchool-NA-NA.log",
    max_lines=10000
)

print(df.head())
print(df.shape)
