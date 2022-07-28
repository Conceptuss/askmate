from flask import Flask, Response, render_template, request, redirect, url_for, Response
import data_manager as dm


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"
@app.route("/main")
def main_page():
    return render_template("main.html")

@app.route("/questions")
def questions_list():
    users_questions = dm.read_questions("q")

    return render_template("questions.html", users_questions=users_questions)


@app.route("/questions/<id>")
def question_answer(id):
    question = dm.read_question_from_id(int(id))
    # question_answer = dm.read_stats("a")
    answers = dm.read_answer(id)


    return render_template("question.html", question=question, answers=answers, id=id)



@app.route("/add_question")
def add_question():
    return render_template("add_question.html")

@app.route("/add_new_question", methods = ["POST"])
def add_new_question():
    data = request.form.to_dict()
    dm.write_data(data,"q")
    return redirect("questions")

@app.route("/questions/<qid>/add_answer")
def add_answer(qid):
    return render_template("add_answer.html", id=qid)

@app.route("/questions/<qid>/add_new_answer", methods = ["POST"])
def add_new_answer(qid):
    data = request.form.to_dict()
    dm.write_data(data,"a",qid)
    # return
    return question_answer(qid)

@app.route("/questions/<id>/delete")
def delete_question(id):
    dm.delete_question(id,"q")
    return questions_list()

@app.route("/answer/<aid>/delete", methods=["POST"])
def delete_answer(aid):
    dm.delete_question(aid,"a")
    qid = request.args.get('qid')
    return question_answer(qid)


@app.route(("/question/<id>/vote_up"))
def question_vote_up(id):
    dm.vote_up("q",id)
    return questions_list()


@app.route(("/question/<id>/vote_down"))
def question_vote_down(id):
    dm.vote_down("q",id)
    return questions_list()


@app.route("/answer/<id>/vote_up", methods=["POST"])
def answer_vote_up(id):
    dm.vote_up("a",id)
    qid = request.args.get('qid')
    return question_answer(qid)


@app.route("/answer/<id>/vote_down", methods=["POST"])
def answer_vote_down(id):
    dm.vote_down("a",id)
    qid = request.args.get('qid')
    return question_answer(qid)


@app.route("/question/<id>/edit")
def edit_question(id):
    question = dm.read_question_from_id(int(id))
    return render_template("edit_question.html", id=id, question=question[0])

@app.route("/question/<id>/edit_submit", methods=["POST"])
def edit_question_submit(id):
    data = request.form.to_dict()
    dm.edit_question(id,data['message'],data['title'])
    return question_answer(id)
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8001,
        debug=True,)
