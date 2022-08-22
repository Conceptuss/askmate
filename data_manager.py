import csv
import os
import connection as con
import util as u
from datetime import datetime




@con.connection_handler
def read_questions(cursor):
    query = f"""SELECT id, title, text, TO_CHAR(time, 'YYYY-MM-DD') AS time,like_number, dont_like_number,view_number 
                FROM question
                ORDER BY id;"""
    cursor.execute(query)
    return cursor.fetchall()


@con.connection_handler
def read_questions_search(cursor,q_title):
    query = f"""SELECT q.id, q.title, q.text, TO_CHAR(q.time, 'YYYY-MM-DD') AS time,q.like_number, q.dont_like_number,q.view_number 
                FROM question AS q
                LEFT JOIN answer AS a ON a.question_id = q.id
                LEFT JOIN comment AS qc ON q.id=qc.question_id
                LEFT JOIN comment AS ac ON a.id=ac.answer_id
                WHERE q.title LIKE '%{q_title}%' OR q.text LIKE '%{q_title}%' OR a.text LIKE '%{q_title}%' OR qc.text LIKE '%{q_title}%' OR ac.text LIKE '%{q_title}%'
                GROUP BY q.id
                ORDER BY q.id;"""
    cursor.execute(query)
    return cursor.fetchall()


@con.connection_handler
def read_questions_sort(cursor,s_title,s_type):
    query = f"""SELECT id, title, text, TO_CHAR(time, 'YYYY-MM-DD') AS time,like_number, dont_like_number,view_number 
                FROM question
                ORDER BY {s_title} {s_type};"""
    cursor.execute(query)
    return cursor.fetchall()


@con.connection_handler_insert
def insert_question(cursor,title,text):
    query = f"""INSERT INTO question (title, text)
                VALUES ('{title}','{text}');"""
    cursor.execute(query)


@con.connection_handler
def read_question_from_id(cursor,id):
    query = f"""SELECT id, title, text, TO_CHAR(time, 'YYYY-MM-DD') AS time,like_number, dont_like_number,view_number 
                FROM question
                WHERE id={id};"""
    cursor.execute(query)
    return cursor.fetchall()


@con.connection_handler_insert
def insert_answer(cursor,question_id,text):
    query = f"""INSERT INTO answer (question_id,text)
            VALUES ({question_id},'{text}');
            """
    cursor.execute(query)

  

@con.connection_handler
def read_answer(cursor, question_id):
    query = f"""SELECT id, question_id, text, TO_CHAR(time, 'YYYY-MM-DD') AS time,like_number, dont_like_number,view_number 
                FROM answer
                WHERE question_id={question_id}
                ORDER BY id;"""
    cursor.execute(query)

    return cursor.fetchall()


@con.connection_handler_insert
def delete_question(cursor,id):
    query = f"""DELETE 
                FROM answer 
                WHERE question_id ={id};"""
    cursor.execute(query)            
    query = f"""DELETE 
                FROM question 
                WHERE id = {id};"""
    cursor.execute(query)


@con.connection_handler_insert
def delete_answer(cursor,id):
    query = f"""DELETE 
                FROM answer 
                WHERE id ={id};"""
    cursor.execute(query)


@con.connection_handler_insert
def vote_up_question(cursor,id):
    query = f"""UPDATE question
                SET like_number = like_number + 1
                WHERE id = {id};"""
    cursor.execute(query)


@con.connection_handler_insert
def vote_up_answer(cursor,id):
    query = f"""UPDATE answer
                SET like_number = like_number + 1
                WHERE id = {id};"""
    cursor.execute(query)


@con.connection_handler_insert
def vote_down_question(cursor,id):
    query = f"""UPDATE question
                SET dont_like_number = dont_like_number + 1
                WHERE id = {id};"""
    cursor.execute(query)


@con.connection_handler_insert
def vote_down_answer(cursor,id):
    query = f"""UPDATE answer
                SET dont_like_number = dont_like_number + 1
                WHERE id = {id};"""
    cursor.execute(query)
    

@con.connection_handler_insert
def edit_question(cursor,id,text,title):
    query = f"""UPDATE question
                SET text ='{text}', title = '{title}'
                WHERE id = {id};"""
    cursor.execute(query)


@con.connection_handler_insert
def update_question_view(cursor,q_id):
    query = f"""UPDATE question
                SET view_number = view_number +1
                WHERE id = {q_id};"""
    cursor.execute(query)    

@con.connection_handler_insert
def update_answer_view(cursor,a_id):
    query = f"""UPDATE answer
                SET view_number = view_number +1
                WHERE id = {a_id};"""
    cursor.execute(query)  


@con.connection_handler
def select_answer_from_id(cursor,id):
    query = f"""SELECT id, question_id, text, TO_CHAR(time, 'YYYY-MM-DD         HH:MI:SS') AS time,like_number, dont_like_number,view_number 
                FROM answer
                WHERE id = {id}
                ORDER BY id; """
    cursor.execute(query)
    return cursor.fetchall()


@con.connection_handler
def select_answer_comments(cursor,a_id):
    query = f""" SELECT id, text, TO_CHAR(time, 'YYYY-MM-DD') AS       time     
            FROM comment
            WHERE answer_id = {a_id}
            ORDER BY id;
            """
    cursor.execute(query)
    return cursor.fetchall()


@con.connection_handler_insert
def insert_comment_to_answer(cursor,a_id,text):
    query = f"""INSERT INTO comment (answer_id,text)
                VALUES ({a_id},'{text}');"""
    cursor.execute(query)

@con.connection_handler
def select_question_id_from_answer(cursor,a_id):
    query = f"""SELECT question_id
                FROM answer
                WHERE id = {a_id};"""
    cursor.execute(query)
    return cursor.fetchall()

@con.connection_handler_insert
def insert_comment_to_question(cursor,q_id,text):
    query = f"""INSERT INTO comment (question_id,text)
                VALUES ({q_id},'{text}');"""
    cursor.execute(query)


@con.connection_handler
def select_question_comments(cursor,q_id):
    query = f""" SELECT id, text, TO_CHAR(time, 'YYYY-MM-DD') AS       time     
            FROM comment
            WHERE question_id = {q_id}
            ORDER BY id;
            """
    cursor.execute(query)
    return cursor.fetchall()


@con.connection_handler_insert
def edit_answer(cursor,id,text):
    query = f"""UPDATE answer
                SET text ='{text}'
                WHERE id = {id};"""
    cursor.execute(query)



@con.connection_handler_insert
def delete_coment(cursor,c_id):
    query = f"""DELETE 
                FROM comment 
                WHERE id ={c_id};"""
    cursor.execute(query)


@con.connection_handler
def select_comment_id(cursor,c_id):
    query = f""" SELECT CASE 
                        WHEN question_id IS null THEN 'answer'
                        ELSE 'question'
                        END AS type,
                        CASE 
                        WHEN question_id IS null THEN answer_id
                        ELSE question_id
                        END AS id,
                        text    
            FROM comment
            WHERE id = {c_id}
            ORDER BY id;
            """
    cursor.execute(query)
    return cursor.fetchall()

@con.connection_handler_insert
def edit_comment(cursor,id,text):
    query = f"""UPDATE comment
                SET text ='{text}'
                WHERE id = {id};"""
    cursor.execute(query)


@con.connection_handler
def find_tag_id(cursor, tag_name):
    tag_split_name = ''
    for i in tag_name.split():
        tag_split_name += i
    # print(tag_split_name)

    select_query = f"""SELECT t.id AS id 
                        FROM  (
                        SELECT id, replace(name, ' ', '') AS name 
                        FROM tag
                        ) AS t
                        WHERE t.name = '{tag_split_name}'; """
    cursor.execute(select_query)
    tag_id = cursor.fetchall()
    if tag_id:
        return tag_id[0]['id']

    
@con.connection_handler
def verify_question_id(cursor, question_id):
    select_query = f"""SELECT id 
                    FROM question 
                    WHERE id = {question_id};
    
    """
    cursor.execute(select_query)
    q_id = cursor.fetchall()
    if q_id:
        return True
    else:
        return False


@con.connection_handler_insert
def insert_new_tag(cursor, tag_name):
    insert_query = f"""INSERT INTO tag (name) 
                        VALUES ('{tag_name}');"""
    cursor.execute(insert_query)


@con.connection_handler
def verify_question_and_tag(cursor, tag_id, question_id):
    select_query = f"""SELECT *
                    FROM question_tag 
                    WHERE question_id = {question_id} and tag_id = {tag_id};
    
    """
    cursor.execute(select_query)
    question_tag_exist = cursor.fetchall()
    if question_tag_exist:
        return True
    else:
        return False


@con.connection_handler_insert
def insert_tag_to_question(cursor, guestion_id, tag_name):
    tag_id = find_tag_id(tag_name)
    if verify_question_id(guestion_id):

        if tag_id:

            if verify_question_and_tag(tag_id,guestion_id):
                return "This Tag exist for this Question"

            else:
                insert_query = f"""INSERT INTO question_tag (tag_id,question_id)
                                VALUES ({tag_id},{guestion_id});"""
                cursor.execute(insert_query)
                return "Insert Tag to Question OK"
                

        else:
            insert_new_tag(tag_name)
            tag_id = find_tag_id(tag_name)
            insert_query = f"""INSERT INTO question_tag (tag_id,question_id)
                            VALUES ({tag_id},{guestion_id});"""
            cursor.execute(insert_query)
            return "Insert Tag OK and insert tag to Question OK"
    else:
        return "Question not exist"


@con.connection_handler
def get_question_tags(cursor,q_id):
    select_query = f"""SELECT t.id AS id, t.name AS name
                    FROM question_tag  AS qt
                    LEFT JOIN tag AS t ON t.id = qt.tag_id
                    WHERE qt.question_id = {q_id};
    
    """
    cursor.execute(select_query)
    return cursor.fetchall()


@con.connection_handler_insert
def delete_tag_from_question(cursor,question_id,tag_id):
    delete_query = f"""DELETE FROM question_tag
                    WHERE tag_id={tag_id} AND question_id={question_id};"""
    cursor.execute(delete_query)