from flask import Flask, render_template, request, redirect, session
from db import db
from models import Question
from random import shuffle
from os import environ
import secrets

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config['SECRET_KEY'] = environ.get("SECRET_KEY") or secrets.token_hex(16)

def validate_user(username, password):
    if not username and not password:
        return None, "Username and password are required"

    user = db.fetch_user(username, password)
    if not user:
        return None, "Invalid username or password"
    
    return user, None


@app.route("/register", methods = ["GET", "POST"])
def register():
    # already have a same account/username is already taken (username) 
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if db.fetch_user(username, password):
        return render_template("register.html", error_msg = "Username is already taken")
    
    # create account
    db.create_user(username, password)
    
    return redirect("/login")

@app.route("/logout", methods = ["GET"])
def logout():
    session.clear()
    return redirect("/")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    user, error_msg = validate_user(username, password)
    
    if user:
        session["username"] = username
        session["user_id"] = user[0]
        return redirect("/")
    
    return render_template("login.html", error_msg = error_msg)

@app.route("/about", methods = ["GET"])
def about():
    return render_template("about.html")

@app.route("/quizzes", methods = ["GET"])
def quizzes():
    if not session.get("username"):
        return redirect("/login")
    # template population
    quizzes = db.get_quizzes()
    return render_template("quizzes.html", quizzes = quizzes)

@app.route("/progress", methods = ["GET"])
def progress():
    if not session.get("username"):
        return redirect("/login")
    attempts = db.get_user_attempts(session.get("user_id"))
    return render_template("progress.html", attempts = attempts)

@app.route("/", methods = ["GET"])
def index():
    username = session.get("username")
    if username:
        return render_template("index.html", username=username)
    
    return render_template("index.html")

@app.route("/questions", methods = ["GET", "POST"])
def questions():
    if not session.get("username"):
        return redirect("/login")
    # get quiz id from the url
    quiz_id = request.args.get("quiz_id")
    session["taking_quiz_id"] = quiz_id
    # get questions
    questions = db.get_questions(quiz_id)
    data = list()

    for question in questions:
        options = [question[3], question[4], question[5], question[6]]
        shuffle(options)

        data.append(Question(
            id = question[0], # question_id
            title = question[2], # question_text
            options = options
        ))
    
    return render_template("questions.html", questions = data)


@app.route("/result", methods = ["GET", "POST"])
def result():
    if not session.get("username"):
        return redirect("/login")
    
    payload = dict()
    # "question_1".split("_") -> ["question", "1"][1] -> { 1: "Java"}
    
    for key, value in request.form.items():
        payload[int(key.split("_")[1])] = value
    
    score = 0
    # check answer
    answers = db.get_answers_by_question_ids(payload.keys())
    quiz_id = session.get("taking_quiz_id")
    
    if not quiz_id:
        return redirect("/system-failed")
    
    temp_quiz_id = quiz_id
    session.pop("taking_quiz_id", None)
    
    for answer in answers:
        question_id = answer[0]
        selected_answer = payload[question_id]
        ans_status = 0
        if payload[answer[0]] == answer[1]:
            score += 1
            ans_status = 1

        db.save_attempt(
            user_id = session.get("user_id"),
            quiz_id = temp_quiz_id,
            question_id = question_id,
            selected_answer = selected_answer,
            score = ans_status
        )


    return render_template(
        "result.html", 
        score = score, 
        total_q = len(answers),
        ratio = score/len(answers)*100
    )


if __name__ == "__main__":
    app.run(debug = True, host = "127.0.0.1")


# about -> website developer portfolio (your personal information)
# header navigation: logo on the left, nav items on the right
