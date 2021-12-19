# Quizzle

*Question 1*

Table: Question
* question_id (primary key, int)
* question_num (int)
* quiz_id (int) *foreign key*
* correct_option (int)
* num_correct (int)
* total_answered (int)
* prompt (text)
* choices (dict --> [key: int, value: text])
* users_correct (set --> [user_ids]) *foreign keys*
* users_incorrect (set --> [user_ids]) *foreign keys*


