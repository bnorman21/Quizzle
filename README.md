# Quizzle Questionnair

## *Question 1*

###### *Here is how I think a true relational database would look like*
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

Table: Quiz Score
* quiz_score_id (primary key, int)
* quiz_id (int) *foreign key*
* user_id (int) *foreign key*
* result (float)
* num_correct (int)
* timestamp (datetime)

Table: User
* user_id (primary key, int)
* name (text, nullable)

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

## *Question 2*

Buggy
```
def get_user_scoring_avg(user_id):
  # Get scores corresponding to this user_id
  scores = QuizScore.query.filter(QuizScore.user_id == user_id)
  numerator = 0
  denominator = 0
  for score in scores:
    # num_correct is an int
    numerator += score.num_correct # += wrong
    # get_num_questions returns an int - assume this works correctly
    denominator += get_num_questions(score.quiz) # += wrong
    # Should return a number between 0.0 and 1.0
  return numerator // denominator #wrong
```
Correct Solution
```
def get_user_scoring_avg(user_id):
  # Get scores corresponding to this user_id
  scores = QuizScore.query.filter(QuizScore.user_id == user_id)
  sum = 0
  for score in scores:
    sum += float (score.num_correct/get_num_questions(score.quiz))
  return float(sum/len(scores)) * 100
```


## *Question 3*

###### *Here is how I approached creating get_question_scoring_avg within the application I made*

Method in the Quizzle class:
``` 
def get_question_scoring_avg (self, questionId: int):
        if questionId in self.questions:
            quizId = self.questions[questionId]
            if quizId in self.quizzes:
                quiz = self.quizzes[quizId]
                question = quiz.questionId2question(questionId)
                if (type(question) == Question):
                    question.printStats() 
                else:
                    print("ERROR: Question id not found in quiz")
            else:
                print("ERROR: Quiz id not found in quiz data base")
        else:
            print("ERROR: Question id not found in question data base")
```
Method called within the question class:
``` 
    def printStats (self):
        print ("Users who have answered Quiz ", self.quizId, " Question ", self.questionNum, " correctly")
        for x in self.usersCorrect:
            print (x)
        print ("Percent of responses correct: ", float(self.numCorrect/self.totalAnswered) * 100, "%")
``` 

###### *Here is how I would approach it in a true relational data base setting*
``` 
def get_question_scoring_avg(question_id):
# Given: QuestionScore object, with fields:
# - id (int)
# - question_id (int)
# - user_id (int)
# - correct (boolean)
# - timestamp (datetime)
#
# TODO: fill this in!
    scores = QuestionScore.query.filter(QuestionScore.question_id == question_id)
    users_correct = set()
    num_correct = 0
    print ("Users who answered correctly: ")
    for s in scores:
        if (s.correct == True):
            num_correct += 1
            if (s.user_id not in users_correct):
                print(s.user_id)
                users_correct.add(s.user_id)
    print ("Percentage correct:",float(num_correct/len(scores)) * 100, "%")
``` 
## *Question 4*
Had no previous experience, so skipped for now


## *Question 5*
* I would use an enviromennt variable saved in the production servers where Quizzle is run
* Because the enviorment variable is not in the code itself, we dont need to restrict its information when it is pushed to GitHub

Here is an example of how to do so: 
``` 
import os
TWILIO_API_KEY = os.environ.get("PRIVATE_TWILIO_API_KEY")

``` 
Find instructions on how to create envrioment variables [here] (https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#macos-and-linux)


## *Question 6*

Here is what I did in my Quizzle app. self.d refers to ```self.d = enchant.Dict("en_US")```. Other than that, all self contained. Feel free to test it out by running the program and entering 5

``` 
    def get_capitalized_anagrams(self, word: str):
        print("Generating anagrams for", word)
        cap_index = set()
        for x in range(0, len(word)):
            if word[x].isupper():
                cap_index.add(x)
        word = word.lower()
        input = list(word)
        output = set()
        length = len(word)
        self.genPerms(input, output, cap_index, 0, length - 1)
        print (output)
        
    """
    The dictionary from pyEnchant is great to lookup if a string is a valid word but it cannot tell me if
    a string is a prefix of any valid words. A prefix tree can do this pretty quickly and would be really helpful in
    cutting down the permuations I need to do. I couldnt figure out how to iterate through the enchant.Dict("en_US")
    dictionary to create a Trie but I think that would be a possible upgrade to the algorithm. 
    
    Possible draw backs of using a Trie is that initial cost of looping through the entire english dictionary and inserting
    it into my Trie. Also the cost for turning each subset of the list into a string to check if the current permuation is a 
    prefix of any valid words is not great, but it does potentially save the algorithm from performing a lot of extra iterations
    """
    def genPerms (self, input: list, output: list, cap_index: set, left: int, right: int):
        if (left == right):
            test = ''.join(input)
            if (self.d.check(test) == True):
                for x in cap_index:
                    input[x] = input[x].upper()
                a = ''.join(input)
                output.add(a)
                for x in cap_index:
                    input[x] = input[x].lower()
            return
            
        for i in range (left, right+1):
            input[left], input[i] = input[i], input[left]
            self.genPerms(input, output, cap_index, left + 1, right)
            input[left], input[i] = input[i], input[left]
``` 
