import numpy as np
import pandas as pd
from parser import parse_can_log


def hex_to_padded_bytes(hex_str: str, target_len: int) -> list[int]:
    """
    Convert hex string to byte list and pad/truncate to target_len.
    """
    if pd.isna(hex_str):
        hex_str = ""

    hex_str = str(hex_str)

    # 如果长度是奇数，前面补一个 0，避免 bytes.fromhex 报错
    if len(hex_str) % 2 != 0:
        hex_str = "0" + hex_str

    byte_values = list(bytes.fromhex(hex_str))

    if len(byte_values) < target_len:
        byte_values += [0] * (target_len - len(byte_values))
    else:
        byte_values = byte_values[:target_len]

    return byte_values


def can_id_to_4bytes(can_id: str) -> list[int]:
    """
    Convert CAN ID hex string to 4 bytes.
    Example:
    '21B' -> [0, 0, 2, 27]
    """
    value = int(can_id, 16)

    return [
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF,
    ]

def dataframe_to_message_features(df: pd.DataFrame) -> np.ndarray:
    """
    Convert parsed CAN DataFrame to per-message feature matrix.

    Output shape:
        (num_messages, 73)
    """

    df = df.copy()

    # 确保按照时间顺序排列
    df = df.sort_values("timestamp").reset_index(drop=True)

    # interface 编码：can0 -> 0, can1 -> 1, can2 -> 2 ...
    df["interface_num"] = (
        df["interface"]
        .str.replace("can", "", regex=False)
        .astype(int)
    )

    # protocol 编码：CAN_CC = 0, CAN_FD = 1
    df["protocol_num"] = df["protocol"].map({
        "CAN_CC": 0,
        "CAN_FD": 1
    }).astype(int)

    # delta 1: 和同一个 interface 上一条 message 的时间差
    df["delta_same_interface"] = (
        df.groupby("interface_num")["timestamp"]
        .diff()
        .fillna(0.0)
    )

    # delta 2: 和同一个 interface + same CAN ID 上一条 message 的时间差
    df["delta_same_id_interface"] = (
        df.groupby(["interface_num", "can_id"])["timestamp"]
        .diff()
        .fillna(0.0)
    )

    feature_rows = []

    for _, row in df.iterrows():
        id_bytes = can_id_to_4bytes(row["can_id"])
        payload_bytes = hex_to_padded_bytes(row["data"], target_len=64)

        hand_features = [
            row["interface_num"],
            row["protocol_num"],
            row["payload_length"],
            row["delta_same_interface"],
            row["delta_same_id_interface"],
        ]

        features = id_bytes + payload_bytes + hand_features

        feature_rows.append(features)

    X_msg = np.array(feature_rows, dtype=np.float32)

    return X_msg


df = parse_can_log(
    "CAN_train/CAN/benign/Benign-FastDriving-DrivingSchool-NA-NA.log",
    max_lines=10000
)

X_msg = dataframe_to_message_features(df)

print(X_msg.shape)
print(X_msg[0])
print(len(X_msg[0]))
print(df.iloc[0])
print(X_msg[0].shape)