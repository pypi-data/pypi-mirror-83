import sys
import os
import json
import ijson
import isodate as iso
import pandas as pds
import numpy as np
import datetime

def clean_json(df):
    statement = df['statement']
    for i in range(len(statement)):
###Get rid of any statement that is not AdaptivLang
        if 'account' not in statement[i]['actor']:
            statement = statement.drop([i], axis=0)
        elif statement[i]['actor']['account']['homePage'] != "https://adaptivlang.evidenceb.com":
            statement = statement.drop([i], axis=0)
###Get rid of any statement that is not an answer to a question
        elif 'result' not in statement[i]:
            statement = statement.drop([i], axis=0)
    statement = statement.reset_index(drop=True)
    return statement

###Function ton convert ISO 8601 to seconds
def convert_time(string):
    time = str(iso.parse_duration(string))
    h, m, s = time.split(':')
    sec = float(h) * 3600 + float(m) * 60 + float(s)
    return sec

def get_question_pos(cell):
    return cell["module"], cell["activity"], cell["exercice"], cell["grade"], cell["subject"], cell["path"]

def clean_id(cell):
    path = cell["path"]
    module = cell["module"]
    activity = cell["activity"]
    exercice = cell["exercice"]
    qid = np.empty(4, dtype=int)
    qid[0], qid[1], qid[2], qid[3] = path, module, activity, exercice
    return qid

def parse_df(df):
    new_df = np.empty((len(df), 10), dtype=object)
###Fill array with the datas we want (student_id, question_id, duration, success)
    for i in range(len(df)):
        new_df[i][0] = df[i]['actor']['account']['name']
        new_df[i][1] = clean_id((df[i]["object"]["definition"]["extensions"]["https://xapi&46;evidenceb&46;com/object/details"]))
        new_df[i][2] = convert_time(df[i]['result']['duration'])
        new_df[i][3] = df[i]['result']['success']
        new_df[i][4], new_df[i][5], new_df[i][6], new_df[i][7], new_df[i][8], new_df[i][9] = get_question_pos(df[i]["object"]["definition"]["extensions"]["https://xapi&46;evidenceb&46;com/object/details"])
###Turning the array into a Dataframe
    new_df = pds.DataFrame(new_df)
    new_df.columns = ['id_eleve', 'id_question', 'duree', 'correct', 'module', 'activity', 'exercice', 'grade', 'subject', 'path']
    pds.set_option("display.max_columns", None)
    return new_df

def total_parsing(df):
    clean_df = clean_json(df)
    parsed_df = parse_df(clean_df)
    return parsed_df

def main(argv):
    df = pds.read_json(argv[1])
    parsed_df = total_parsing(df)
    print(parsed_df)
    return parsed_df


if __name__ == "__main__":
    main(sys.argv)
    pass