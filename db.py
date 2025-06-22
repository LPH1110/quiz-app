import sqlite3
import queries
from typing import List
import bcrypt

# 1. create connection
# 2. make some queries -> method/command to get data from the db
# 3. close connection
# quizzes, questions

class Database():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False) or None
        if self.conn is None:
            print("Error: Could not connect to the database")
            return
        
    def get_answers_by_question_ids(self, question_ids: List[str]):
        cursor = self.conn.cursor()
        # (?,?,?) if we have 3 ids in the list
        # ?*len(list)
        placeholder = ",".join("?"*len(question_ids)) # -> ?,?,?
        query = f"SELECT question_id, correct_ans FROM questions WHERE question_id IN ({placeholder})"
        cursor.execute(query, tuple(question_ids))
        return cursor.fetchall()

    def insert_samples(self):
        cursor = self.conn.cursor()
        
        quizzes = [
            ("Programming", "Test your programming skills with this quiz"),
            ("Mathematics", "This is harder than you think. Try it!"),
            ("Science", "The cool thing is here..."),
        ] 

        cursor.executemany("INSERT OR IGNORE INTO quizzes(title, description) VALUES (?, ?)", quizzes)
        print("Info: Sample quizzes inserted")
        
        questions = [
            (1, "Which is the most common programming language?",
             "Python", "Javascript", "Java", "ASP.NET","Python"),
            (1, "Which language is used for data science?",
             "Python", "Java", "C++", "ASP.NET","Python"),
            (2, "What is the value of 1 + 1", "3", "4", "2", "1","None of them")
        ]

        cursor.executemany(
            '''
                INSERT OR IGNORE INTO questions (
                    quiz_id,
                    question_text,
                    option1,
                    option2,
                    option3,
                    option4,
                    correct_ans
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            , questions
        )
        print("Info: Sample questions inserted")
        
        self.conn.commit()
    
    def get_quizzes(self):
        cursor = self.conn.cursor()
        cursor.execute(queries.GET_QUIZZES)
        quizzes = cursor.fetchall()
        return quizzes
    
    def get_questions(self, quiz_id):
        cursor = self.conn.cursor()
        cursor.execute(queries.GET_QUESTIONS, (quiz_id,))
        questions = cursor.fetchall()
        return questions
    
    def create_user(self, username, password):
        cursor = self.conn.cursor()
        # encrypt password, encryption/hashing
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(queries.CREATE_USER_QUERY, (username, hashed))
        self.conn.commit()

    def save_attempt(self, user_id, quiz_id, question_id, selected_answer, score):
        cursor = self.conn.cursor()
        cursor.execute(queries.CREATE_USER_ATTEMPT, (user_id, quiz_id, question_id, selected_answer, score))
        self.conn.commit()
    
    def get_user_attempts(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(queries.GET_USER_ATTEMPTS, (user_id,))
        return cursor.fetchall()
    
    def fetch_user(self, username, password):
        cursor = self.conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username = (?)", (username,)).fetchone()
        print(user)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return user
        return None

    def create_table(self, tb_name):
        cursor = self.conn.cursor()
        if tb_name == "quizzes":
            cursor.execute(queries.CREATE_QUIZ_TABLE)
        elif tb_name == "questions":
            cursor.execute(queries.CREATE_QUESTION_TABLE)
        elif tb_name == "users":
            cursor.execute(queries.CREATE_USERS_TABLE)
        elif tb_name == "attempts":
            cursor.execute(queries.CREATE_ATTEMPTS_TABLE)

db = Database("quiz.db")
if __name__ == "__main__":
    db.create_table("quizzes")
    db.create_table("questions")
    db.create_table("users")
    db.create_table("attempts")
    db.insert_samples()
    