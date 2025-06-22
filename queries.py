CREATE_QUIZ_TABLE = '''
    CREATE TABLE IF NOT EXISTS quizzes (
        quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL
    )
'''

CREATE_QUESTION_TABLE = '''
    CREATE TABLE IF NOT EXISTS questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        quiz_id INTERGER NOT NULL,
        question_text TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        correct_ans TEXT NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quiz (quiz_id) ON DELETE CASCADE
    )
'''

CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
'''

CREATE_ATTEMPTS_TABLE = '''
    CREATE TABLE IF NOT EXISTS attempts (
        attempt_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        question_id INTEGER NOT NULL,
        quiz_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        selected_answer TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE,
        FOREIGN KEY (quiz_id) REFERENCES quizzes (quiz_id) ON DELETE CASCADE
    )
'''

CREATE_USER_ATTEMPT = '''
    INSERT INTO attempts (user_id, quiz_id, question_id, selected_answer, score) VALUES (?,?,?,?,?)
'''

GET_USER_ATTEMPTS = '''
    SELECT a.attempt_id, a.quiz_id, q.title, a.question_id, a.selected_answer, a.score, a.timestamp 
    FROM attempts a JOIN quizzes q ON a.quiz_id = q.quiz_id WHERE user_id = ? 
'''

GET_QUESTIONS = 'SELECT * FROM questions WHERE quiz_id = ?'

GET_QUIZZES = 'SELECT * FROM quizzes'

CREATE_USER_QUERY = "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)"