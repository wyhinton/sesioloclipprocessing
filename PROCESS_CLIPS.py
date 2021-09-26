import os
from icecream import ic
import pandas as pd

pd.set_option('display.max_columns', None)

def main():
    directory = "BACH_MOV_1"
    dfarray = []
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            df = process_file(filename)
            dfarray.append(df)
        else:
            continue
    df = pd.DataFrame(dfarray, columns = ["name", "start", "end", "tags", "date", "hour"])
    df.to_csv("out_csv.csv")
    print(df)

def process_file(path: str):
    path.replace(" ", "")
    splits = path.split("_")
    if len(splits) != 4:
        raise ValueError('{} did not have 4 splits.'.format(path))
    # ic(path)
    # 'Bach Mov 1 v2_[T, LR, FL, UL]_[1,31,365]_[1,32,818] [2021-09-24 222333].wav'
    name = splits[0]
    tags = splits[1]
    tags = find_between(tags, "[", "]")
    start = splits[2]
    start = find_between(start, "[", "]")


    third_splits = splits[3].split(" ")
    end = third_splits[0]
    end = find_between(end, "[", "]")
    date = third_splits[1].split("[")[1]
    try:
        hour = third_splits[2]
        hour = hour.split("]")[0]
    except:
        raise ValueError("failed with path {}".format(path))
    return [name, start, end, tags, date, hour]

def find_between(s, start, end):
    return (s.split(start))[1].split(end)[0]

main()
