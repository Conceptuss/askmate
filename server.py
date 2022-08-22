from crypt import methods
from flask import Flask, Response, render_template, request, redirect, url_for, Response
import data_manager as dm


app = Flask(__name__)

#ok
@app.route("/")
def hello():
    return questions_list()

#ok
@app.route("/questions")
def questions_list(users_questions=False):
    if users_questions == False:
        users_questions = dm.read_questions()
    
    q_head = list(users_questions[0].keys())
    return render_template("questions.html", users_questions=users_questions, q_head=q_head)

#ok
@app.route("/question/<id>")
def question_answer(id):
    # id = request.args.get('id')
    question = dm.read_question_from_id(int(id))
    answers = dm.read_answer(id)
    dm.update_question_view(id)
    comment = dm.select_question_comments(id)
    tags = dm.get_question_tags(id)
    return render_template("question.html", question=question, answers=answers, id=id, comment=comment, tags=tags)


#ok
@app.route("/add_question")
def add_question():
    return render_template("add_question.html")
#ok
@app.route("/add_new_question")
def add_new_question():
    title = request.args.get('title')
    text = request.args.get('message')
    dm.insert_question(title,text)
    return redirect("questions")
#ok
@app.route("/add_answer/<q_id>")
def add_answer(q_id):
    # q_id = request.args.get('q_id')
    return render_template("add_answer.html", q_id=q_id)
#ok
@app.route("/questions/<q_id>", methods = ["POST"])
def add_new_answer(q_id):
    data = request.form.to_dict()
    dm.insert_answer(q_id,data['message'])
    # return
    return question_answer(q_id)

#ok
@app.route("/del_question", methods=["POST"])
def delete_question():
    q_id = request.args.get('q_id')
    print(q_id)
    dm.delete_question(q_id)
    # return redirect('questions')
    return questions_list()


#ok 
@app.route("/answer", methods=["POST"])
def delete_answer():
    a_id = request.args.get('a_id')
    q_id = request.args.get('q_id')
    dm.delete_answer(a_id)
    
    return question_answer(q_id)

#ok
@app.route("/q_up", methods = ["POST"])
def question_vote_up():
    q_id = request.args.get('q_id')
    dm.vote_up_question(q_id)
    return questions_list()

#ok
@app.route("/q_down", methods = ["POST"])
def question_vote_down():
    q_id = request.args.get('q_id')
    dm.vote_down_question(q_id)
    return questions_list()

#ok
@app.route("/a_up", methods=["POST"])
def answer_vote_up():
    a_id = request.args.get('a_id')
    q_id = request.args.get('q_id')
    dm.vote_up_answer(a_id)
    return question_answer(q_id)

#ok
@app.route("/a_down", methods=["POST"])
def answer_vote_down():
    a_id = request.args.get('a_id')
    q_id = request.args.get('q_id')
    dm.vote_down_answer(a_id)
    return question_answer(q_id)


@app.route("/question/e", methods=["POST"])
def edit_question():
    q_id = request.args.get('q_id')
    question = dm.read_question_from_id(q_id)
    return render_template("edit_question.html", q_id=q_id, question_title=question[0]['title'], question_text=question[0]['text'])

@app.route("/question/edit", methods=["POST"])
def edit_question_submit():
    data = request.form.to_dict()
    q_id = request.args.get('q_id')
    dm.edit_question(q_id,data['text'],data['title'])
    return question_answer(q_id)


@app.route("/answer/<a_id>", methods=["POST"])
def view_answer(a_id):
    # a_id = request.args.get('a_id')
    data = dm.select_answer_from_id(a_id)
    q_id = dm.select_question_id_from_answer(a_id)
    dm.update_answer_view(a_id)
    coments = dm.select_answer_comments(a_id)

    return render_template("answer.html", a_id=a_id, answer=data[0],q_id=q_id[0]['question_id'], coments=coments)

@app.route("/comment", methods=["POST"])
def comment():
    a_id = request.args.get('a_id')
    q_id = request.args.get('q_id')
    if a_id:
        return render_template('add_answer_comment.html', a_id=a_id)
    if q_id:
        return render_template('add_question_comment.html',q_id=q_id)

@app.route("/add_comment", methods=["POST"])
def add_comment():
    a_id = request.args.get('a_id')
    q_id = request.args.get('q_id')
    data = request.form.to_dict()
    if a_id:
        dm.insert_comment_to_answer(a_id,data['text'])
        return view_answer(a_id)
    if q_id:
        dm.insert_comment_to_question(q_id,data['text'])
        return question_answer(q_id)


@app.route("/answer/e", methods=["POST"])
def edit_answer():
    a_id = request.args.get('a_id')
    answer = dm.select_answer_from_id(a_id)
    return render_template("edit_answer.html", a_id=a_id, answer_text=answer[0]['text'])

@app.route("/answer/edit", methods=["POST"])
def edit_answer_submit():
    data = request.form.to_dict()
    a_id = request.args.get('a_id')
    dm.edit_answer(a_id,data['text'])
    return view_answer(a_id)

@app.route("/comment/delete", methods=["POST"])    
def delete_comment():
    a_id = request.args.get('a_id')
    q_id = request.args.get('q_id')
    c_id = request.args.get('c_id')
    if a_id:
        dm.delete_coment(c_id)
        return view_answer(a_id)
    if q_id:
        dm.delete_coment(c_id)
        return question_answer(q_id)

@app.route("/comment/e", methods=["POST"])
def edit_comment():
    c_id = request.args.get('c_id')
    data = dm.select_comment_id(c_id)

    return render_template('edit_comment.html', c_id=c_id, data=data[0])

@app.route("/comment/edit", methods=["POST"])
def edit_comment_submit():
    data = request.form.to_dict()
    c_id = request.args.get('c_id')
    back_type = dm.select_comment_id(c_id)
    print(back_type)
    dm.edit_comment(c_id,data['text'])
    if back_type[0]['type'] == 'question':
        return question_answer(back_type[0]['id'])
    if back_type[0]['type'] == 'answer':
            return view_answer(back_type[0]['id'])   


@app.route("/add_tag", methods=["POST"])
def add_tag():
    q_id = request.args.get('q_id')
    tag_name = request.form.to_dict()
    dm.insert_tag_to_question(q_id,tag_name['tag_name'])
    return question_answer(q_id)


@app.route("/delete_tag", methods=["POST"])
def delete_tag():
    q_id = request.args.get('q_id')
    tag_id = request.args.get('tag_id')
    dm.delete_tag_from_question(q_id,tag_id)
    return question_answer(q_id)


@app.route("/search_question", methods=["POST"])
def search_question():
    data = request.form.to_dict()
    questions = dm.read_questions_search(data['q_title'])
    return questions_list(questions)


@app.route("/sort_question")
def sort_question():
    s_title = request.args.get('s_title')
    s_type = request.args.get('s_type')
    questions = dm.read_questions_sort(s_title,s_type)
    return questions_list(questions)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8011,
        debug=True,)
