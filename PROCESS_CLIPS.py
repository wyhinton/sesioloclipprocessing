import os
from icecream import ic
import pandas as pd

pd.set_option('display.max_columns', None)
BPM = 120

def main():
    directory = "BACH_MOV_1"
    dfarray = []
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            df = process_file(filename)
            dfarray.append(df)
        else:
            continue
    df = pd.DataFrame(dfarray, columns = ["name", "length", "start", "end", "tags", "date", "filename"])
    df.to_csv("out_csv.csv")
    print(df)

# 1 bar = 4 beats
# 1 beat = 16 sixteenths
def bpm_to_seconds(time: str, bpm: int):
    #1,32,818
    time = time.replace("[", "").replace("]","")
    split = time.split(",")

    minutes = int(split[0])
    seconds = int(split[1])
    milliseconds = int(split[2])
    milliseconds_to_seconds = milliseconds/1000
    # ic(bars)
    # ic(beats)
    # ic(sixteenths)

    seconds_from_minutes = minutes*60
    total_s = seconds_from_minutes+seconds+milliseconds_to_seconds
    return total_s



def process_file(path: str):
    path.replace(" ", "")
    splits = path.split("_")
    if len(splits) != 4:
        raise ValueError('{} did not have 4 splits.'.format(path))
    # ic(path)
    name = splits[0]
    tags = splits[1]
    tags = find_between(tags, "[", "]")
    start = bpm_to_seconds(splits[2], BPM)

    ic(path)


    third_splits = splits[3].split(" ")
    end = third_splits[0]
    end = find_between(end, "[", "]")
    end = bpm_to_seconds(end, BPM)

    length = end-start

    if end < start:
        raise ValueError("end {} was less than start {} for sample {}".format(end, start, path))

    date = third_splits[1].split("[")[1]
    try:
        hour = third_splits[2]
        hour = hour.split("]")[0]
    except:
        raise ValueError("failed with path {}".format(path))

    return [name, length, start, end, tags, date, path]

def find_between(s, start, end):
    return (s.split(start))[1].split(end)[0]

main()
