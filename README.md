# Quizzle Questionnair

## *Question 1*

###### *Here is how I constructed my database for Quizzle. It is not a true relational database, but it made the most sense for me when constructing the application:*

Table: Question
* question_id (primary key, int)
* question_num (int)
* quiz_id (int) *foreign key*
* correct_option (int)
* num_correct (int)
* total_answered (int)
* prompt (text)
* choices (dict [key: int, value: text])
* users_correct (set [user_ids]) *foreign keys*
* users_incorrect (set [user_ids]) *foreign keys*

Table: Quiz
* quiz_id (primary key, int)
* quiz_name (text)
* quiz_category (text)
* questions (dict [key: question_num, value: Question]) *foreign keys*
* results (dict [key: user_id, value: float]) *foreign keys*
* num_qs (int)
* question_start_id (int) *foreign key*

Table: User
* user_id (primary key, int)
* quizzes_taken (set [quiz_id]) *foreign keys
* name (text, nullable)

Table: Quizzle
* quizzes (dict [key: quiz_id, value: Quiz]) *foreign keys*
* users (dict [key: user_id, value: User]) *foreign keys*
* questions (dict [key: question_id, value: quiz_id of Question])
* category2quiz (dict [key: category, value: list of quiz_ids in category])
* quiz_num (int)
* user_num (int)
* question_num (int)

###### *Here is how I suppose a true relational database would look like*

Table: Question
* question_id (primary key, int)
* question_num (int)
* quiz_id (int) *foreign key*
* correct_option (int)
* num_correct (int)
* total_answered (int)
* prompt (text)
* choices (dict [key: int, value: text])

Table: Question Score
* question_score_id (primary key, int)
* question_id (int) *foreign key*
* user_id (int) *foreign key*
* correct (boolean)
* timestamp (datetime)


Table: Quiz
* quiz_id (primary key, int)
* quiz_name (text)
* quiz_category (text)
* num_qs (int)
* question_start_id (int) *foreign key*

Table: Quiz Score
* quiz_score_id (primary key, int)
* quiz_id (int) *foreign key*
* user_id (int) *foreign key*
* result (float)
* timestamp (datetime)

Table: User
* user_id (primary key, int)
* name (text, nullable)

## *Question 2*

```
def get_user_scoring_avg(user_id):
  # Get scores corresponding to this user_id
  scores = QuizScore.query.filter(QuizScore.user_id == user_id)
  numerator = 0
  denominator = 0
  for score in scores:
    # num_correct is an int
    numerator += score.num_correct
    # get_num_questions returns an int - assume this works correctly
    denominator += get_num_questions(score.quiz)
    # Should return a number between 0.0 and 1.0
  return numerator // denominator
```
Here are the bugs I found:
* ``` numerator += score.num_correct ``` is incorrect. It should be ```numerator += score.percentage_correct```
* ```denominator += get_num_questions(score.quiz)``` is incorrect. It should be ```denominator += 1```
* ```return numerator // denominator``` is incorrect. It should be ```return float(numerator/denominator)```

