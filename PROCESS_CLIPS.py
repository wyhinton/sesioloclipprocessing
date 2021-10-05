import os
from icecream import ic
import pandas as pd
import librosa
import re

pd.set_option('display.max_columns', None)
BPM = 120
CLIP_DIRECTORY = "BACH_MOV_1"
CLIP_PROCESSING_OUTPUT = "out_csv.csv"
CLIPS_SUMMARY_OUTPUT = "clips_summary.csv"

def standardize_names(source_name)->str:
    return source_name.replace(" v2", "").upper()


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
    df.to_csv(CLIP_PROCESSING_OUTPUT)
    
    summary_frame = create_summary_frame(df)
    summary_frame.to_csv(CLIPS_SUMMARY_OUTPUT)
    # counts = df['name'].value_counts()
    # count_frame = pd.DataFrame(counts)
    # 
    # count_frame.to_csv(CLIPS_SUMMARY_OUTPUT)

    print(df)


def create_summary_frame(main_frame):
    counts = main_frame['name'].value_counts()
    count_frame = pd.DataFrame(counts)
    count_frame = count_frame.reset_index()
    count_frame.columns = ['unique_values', 'counts']
    return count_frame


def bpm_to_seconds(time: str):
    #1,32,818
    time = time.replace("[", "").replace("]","")
    split = time.split(",")

    minutes = int(split[0])
    seconds = int(split[1])
    milliseconds = int(split[2])
    milliseconds_to_seconds = milliseconds/1000

    seconds_from_minutes = minutes*60
    total_s = seconds_from_minutes+seconds+milliseconds_to_seconds
    return total_s

def get_clip_length(path: str)->float:
    milength = librosa.get_duration(filename=path)
    ic(milength)
    return milength
    


def process_file(path: str):
    path.replace(" ", "")
    splits = path.split("_")
    if len(splits) != 4:
        raise ValueError('{} did not have 4 splits.'.format(path))
    # ic(path)
    name = splits[0]
    # 'Bach Mov 1 v2_[T, LR, FL, UL]_[1,31,365]_[1,32,818] [2021-09-24 222333].wav'
    name = standardize_names(splits[0])

    tags = splits[1]
    tags = find_between(tags, "[", "]")
    start = bpm_to_seconds(splits[2])
    third_splits = splits[3].split(" ")
    end = third_splits[0]
    end = find_between(end, "[", "]")
    end = bpm_to_seconds(end)

    length = get_clip_length(CLIP_DIRECTORY + "/" + path)
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



def has_substring(substring: str, fullstring: str, correct_name: str)->str:
    if substring in fullstring:
        print("Found!")
