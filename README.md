# Quizzle

*Question 1*

Table: Question
* question_id (primary key, int)
* question_num (int)
* quiz_id (int)
* correct_option (int)
* num_correct (int)
* total_answered (int)
* prompt (text)
* choices (dict --> [key: int, value: text])
* users_correct (set --> [int])
* users_incorrect (set --> [int])


