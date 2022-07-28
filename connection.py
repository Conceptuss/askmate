DATA_FILE_ANSWER = "sample_data/answer.csv"
DATA_FILE_QUESTION = "sample_data/question.csv"


def read_from_file(type):
    if type == "q":
        with open(DATA_FILE_QUESTION, 'r') as data_file:
            rows = data_file.readlines()
        return rows
    elif type == "a":
        with open(DATA_FILE_ANSWER, 'r') as data_file:
            rows = data_file.readlines()
        return rows
    else:
        return False


print(read_from_file("q"))


