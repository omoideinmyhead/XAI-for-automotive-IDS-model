import re
import pandas as pd
from pathlib import Path

# Regex pattern to match candump format
pattern = re.compile(
    r"\((?P<timestamp>[0-9\.]+)\)\s+"
    r"(?P<interface>can\d+)\s+"
    r"(?P<id>[0-9A-Fa-f]+)"
    r"(#|##[0-9A-Fa-f])"
    r"(?P<data>[0-9A-Fa-f]*)\s+"
    r"(?P<label>R|T)?"
)

def parse_can_log(file_path: Path, chunk_size=100000):
    """
    transform the given file path to a dataframe
    
    :param file_path: the full path name of the file
    :type file_path: Path
    """
    chunk = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                chunk.append(match.groupdict())
            if len(chunk) >= chunk_size:
                yield pd.DataFrame.from_records(chunk).astype("string")
                chunk.clear()
    if chunk:
        yield pd.DataFrame.from_records(chunk).astype("string")

def load_category(folder: Path, category: str) -> pd.DataFrame:
    """ 
    load log files of the given attack category

    folder: full path of the attack category
    """
    files = sorted(folder.glob("*.log"))
    if not files:
        return pd.DataFrame()
    
    df_list = []
    for file in files:
        print(f"[{category}] parsing {file.name}")
        for df in parse_can_log(file):
            df["category"] = category
            df["source_file"] = file.name
            df_list.append(df)

    dfs = pd.concat(df_list, ignore_index=True)
    return dfs if not dfs.empty else pd.DataFrame()

project_root = Path(__file__).resolve().parent
data_root = project_root/"CAN_train"/"CAN"

advanced_df = load_category(data_root/"advanced", "advanced")

print(advanced_df.head())