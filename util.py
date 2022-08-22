from datetime import datetime
import connection as con
import bcrypt





def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed

def password_unhash(hash,password):
    result = bcrypt.checkpw(password.encode('utf-8'),hash)
    return result 




print(hash_password('test'))
print(password_unhash(hash_password('test'),'te1st'))


def convert_from_timestamp(time_stamp):
    return datetime.fromtimestamp(int(time_stamp))


# print(int(datetime.now().timestamp()))

def convert_to_timestamp(date_time):
    return int(datetime.timestamp((date_time)))


def get_id(file,qid=0):
    if file == con.DATA_FILE_QUESTION:
        data = con.read_from_file("q")
        ids = []
        for i in data[1::]:
            splited_row = i.strip().split(",")
            ids.append(int(splited_row[0]))
        if len(ids) > 0:
            qid = max(ids)
        else:
            qid = 0

        return int(qid) + 1
    elif file == con.DATA_FILE_ANSWER:
        data = con.read_from_file("a")

        ids = []
        for i in data[1::]:
            # print(i)
            splited_row = i.strip().split(",")
            if int(splited_row[3]) == int(qid):
                ids.append(int(splited_row[0]))

        if len(ids) > 0:
            aid = max(ids)
        else:
            aid =0

        return int(aid) + 1
    else:
        False




# print(get_id(con.DATA_FILE_ANSWER,2))