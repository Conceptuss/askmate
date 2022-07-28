import csv
import os
import connection as con
import util as u
from datetime import datetime


DATA_FILE_ANSWER = "sample_data/answer.csv"
DATA_FILE_QUESTION = "sample_data/question.csv"


def read_questions(type):
    user_questions = []
    # with open(DATA_FILE_QUESTION, 'r') as data_file:
    #     rows = data_file.readlines()
    rows = con.read_from_file(type)
    headers = rows[0].strip().split(",")
    # print(headers)
    for row in rows[1::]:
        splited_row = row.strip().split(",")
        story = {}
        for h, r in zip(headers, splited_row):
            if h == "submission_time":
                story[h] = u.convert_from_timestamp(r)
            else:
                story[h] = r
        user_questions.append(story)
    return user_questions


def read_question_from_id(id):
    user_questions = []

    rows = con.read_from_file("q")
    headers = rows[0].strip().split(",")
    for row in rows[1::]:
        splited_row = row.strip().split(",")

        if splited_row[0] == str(id):
            story = {}
            for h, r in zip(headers, splited_row):

                if h == "submission_time":
                    story[h] = u.convert_from_timestamp(r)
                else:
                    story[h] = r
            user_questions.append(story)
    return user_questions


print(read_question_from_id(2))


def read_answer(question_id):
    answers = []
    # with open(DATA_FILE_QUESTION, 'r') as data_file:
    #     rows = data_file.readlines()
    rows = con.read_from_file("a")
    headers = rows[0].strip().split(",")
    # print(headers)
    for row in rows[1::]:
        splited_row = row.strip().split(",")

        if splited_row[3] == str(question_id):
            story = {}
            for h, r in zip(headers, splited_row):

                if h == "submission_time":
                    story[h] = u.convert_from_timestamp(r)
                else:
                    story[h] = r
            answers.append(story)
    return answers


def write_data(data: dict, type, question_id = 0):
    if type == "q":
            with open(con.DATA_FILE_QUESTION, 'a+') as f:
                #f.write()
                id = str(u.get_id(con.DATA_FILE_QUESTION))
                timestamp = str(int(datetime.now().timestamp()))
                view = "0"
                vote = "0"
                title = data["title"]
                message = data["message"]


                f.write(f"{id},{timestamp},{view},{vote},{title},{message},\n")
                #print(f"{data['id']},{data['title']},{data['user_story']},{data['acceptance_criteria']},{data['business_value']},{data['estimation']},{data['status']}")
    elif type == "a":
        with open(con.DATA_FILE_ANSWER, 'a+') as f:
            # f.write()
            id = str(u.get_id(con.DATA_FILE_ANSWER,question_id))
            timestamp = str(int(datetime.now().timestamp()))
            vote = "0"
            qid = question_id
            message = data["message"]

            f.write(f"{id},{timestamp},{vote},{qid},{message},\n")


def delete_question(delete_id, type):
    if type == "q":
        user_story = read_questions("q")
        file_name = con.DATA_FILE_QUESTION
    elif type == "a":
        user_story = read_questions("a")
        file_name = con.DATA_FILE_ANSWER
    # print(user_story)
    for i,value in enumerate(user_story):
        if int(value["id"]) == int(delete_id):
            del user_story[i]

    with open(file_name, 'w+') as f:
        header = list(user_story[0].keys())
        s = ""
        for i, v in enumerate(header):
            if i == len(header) - 1:
                s += str(v)
            else:
                s += str(v) + ","
        f.write(s+"\n")
        for i,v in enumerate(user_story[0::]):
            tab = []
            for j,val in v.items():
                tab.append(val)
            s = ""
            for i, elem in enumerate(tab):
                if i == len(tab) - 1:
                    s += str(elem)
                elif i == 1:
                    s += str(u.convert_to_timestamp(elem)) + ","
                else:
                    s += str(elem) + ","
            f.write(f"{s}\n")


def vote_up(file,id):
    if file == "q":
        file_name = con.DATA_FILE_QUESTION
    elif file == "a":
        file_name = con.DATA_FILE_ANSWER
    data=read_questions(file)
    print(data)
    for i in data:
        if int(i['id']) == int(id):
            temp_id = int(i['vote_number'])
            temp_id +=1
            i['vote_number'] = str(temp_id)



    with open(file_name, 'w+') as f:
        header = list(data[0].keys())
        s = ""
        for i, v in enumerate(header):
            if i == len(header) - 1:
                s += str(v)
            else:
                s += str(v) + ","
        f.write(s + "\n")
        for i, v in enumerate(data[0::]):
            tab = []
            for j, val in v.items():
                tab.append(val)
            s = ""
            for i, elem in enumerate(tab):
                if i == len(tab) - 1:
                    s += str(elem)
                elif i == 1:
                    s += str(u.convert_to_timestamp(elem)) + ","
                else:
                    s += str(elem) + ","
            f.write(f"{s}\n")


def vote_down(file,id):
    if file == "q":
        file_name = con.DATA_FILE_QUESTION
    elif file == "a":
        file_name = con.DATA_FILE_ANSWER
    data=read_questions(file)
    print(data)
    for i in data:
        if int(i['id']) == int(id):
            temp_id = int(i['vote_number'])
            temp_id -=1
            i['vote_number'] = str(temp_id)



    with open(file_name, 'w+') as f:
        header = list(data[0].keys())
        s = ""
        for i, v in enumerate(header):
            if i == len(header) - 1:
                s += str(v)
            else:
                s += str(v) + ","
        f.write(s + "\n")
        for i, v in enumerate(data[0::]):
            tab = []
            for j, val in v.items():
                tab.append(val)
            s = ""
            for i, elem in enumerate(tab):
                if i == len(tab) - 1:
                    s += str(elem)
                elif i == 1:
                    s += str(u.convert_to_timestamp(elem)) + ","
                else:
                    s += str(elem) + ","
            f.write(f"{s}\n")


def edit_question(id,message,title):

    file_name = con.DATA_FILE_QUESTION
    data = read_questions("q")

    for i in data:
        if int(i['id']) == int(id):
            i['message'] = message
            i['title'] = title



    with open(file_name, 'w+') as f:
        header = list(data[0].keys())
        s = ""
        for i, v in enumerate(header):
            if i == len(header) - 1:
                s += str(v)
            else:
                s += str(v) + ","
        f.write(s + "\n")
        for i, v in enumerate(data[0::]):
            tab = []
            for j, val in v.items():
                tab.append(val)
            s = ""
            for i, elem in enumerate(tab):
                if i == len(tab) - 1:
                    s += str(elem)
                elif i == 1:
                    s += str(u.convert_to_timestamp(elem)) + ","
                else:
                    s += str(elem) + ","
            f.write(f"{s}\n")