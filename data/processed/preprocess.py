import pandas as pd
import os

def resample_m1_to_1h(input_path, output_path):
    print(f"Resampling {input_path} to 1H...")
    columns = ["Date", "Time", "Open", "High", "Low", "Close", "Volume"]
    df = pd.read_csv(input_path, header=None, names=columns)
    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%Y.%m.%d %H:%M")
    df.set_index("Datetime", inplace=True)
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df_1h = df.resample("1h").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()
    df_1h.to_csv(output_path)
    print(f"Saved to {output_path}. Shape: {df_1h.shape}")

if __name__ == "__main__":
    raw_dir = "data/raw"
    proc_dir = "data/processed"
    os.makedirs(proc_dir, exist_ok=True)
    for asset in ["XAUUSD_M1.csv", "XAGUSD_M1.csv"]:
        input_file = os.path.join(raw_dir, asset)
        output_file = os.path.join(proc_dir, asset.replace("_M1.csv", "_1H.csv"))
        if os.path.exists(input_file):
            resample_m1_to_1h(input_file, output_file)
        else:
            print(f"Warning: File {input_file} not found.")
