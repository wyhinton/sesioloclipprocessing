import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from icecream import ic

CSV_FILE = "out_csv.csv"

pd.set_option('display.max_columns', None)

def main():
    df = get_csv_file(CSV_FILE)
    lengths = df["length"]
    compositions = df["name"]
    ic(lengths)
    plt.scatter(lengths, lengths, c=compositions)
    plt.show()
    print(df)


def get_csv_file(path: str):
    return pd.read_csv(path)


main()