import enchant
# from random_word import RandomWords
# from random import randint
# import pygtrie


#Quizzle by Bennett Norman

"""
Question Class
    Methods:
        -init
        -printStats
        -giveQuestion
        -makeQuestion
    Variables:
        questionNum (int)       --> unique to given quiz it is in
        questionId (int)        --> unqiue to entire Quizzle system
        quizId (int)            --> shared among all questions in the same quiz
        correctOption (int)    
        numCorrect (int)        --> number of correct answers to question
        totalAnswered (int)     --> number of total answers to question
        prompt (str)
        choices (dict)         
        usersCorrect (set)      --> set of users who answered question correctly (user ids)
        usersIncorrect (set)    --> set of users who answered question incorrectly (user ids)
"""
class Question:
    #for a question, pass in a dictionary with a choice id mapped to a question choice
    #also include what question id is correct
    def __init__(self, questionNumber: int, questionId: int, quizId: int):
        self.questionNum = questionNumber
        self.questionId = questionId
        self.quizId = quizId
        self.correctOption = -1
        self.numCorrect = 0
        self.totalAnswered = 0
        self.prompt = ""
        self.choices = {}
        self.usersCorrect = set()
        self.usersIncorrect = set()
    
    #printStats ()
    # -
    def printStats (self):
        print ("Users who have answered Quiz ", self.quizId, " Question ", self.questionNum, " correctly")
        for x in self.usersCorrect:
            print (x)
        print ("Percent of responses correct: ", float(self.numCorrect/self.totalAnswered) * 100, "%")

    #giveQuestion()
    # -
    def giveQuestion (self, userId: int):
        print(self.prompt)
        for x, y in self.choices.items():
            print(x, y, sep = ": ")
        answer = int (input ("Select option: "))
        self.totalAnswered += 1
        if (answer != self.correctOption):
            self.usersIncorrect.add(userId)
            return 0
        elif(answer == self.correctOption):
            self.numCorrect += 1
            self.usersCorrect.add(userId)
            return 1

   
    #makeQuestion()
    # - 
    def makeQuestion(self):
        output = "For question " + str(self.questionNum) + " enter prompt: "
        self.prompt = input (output)
        numOptions = int (input ("Enter number of options: "))
        while (numOptions != 4 and numOptions != 5):
            numOptions = int (input ("Must be 4 or 5: "))
        for y in range (0, numOptions):
            output = "Enter option " + str(y) + ": "
            option = input (output)
            self.choices[y] = option
        self.correctOption = int (input ("Enter the correct option: "))
        while self.correctOption not in self.choices:
            self.correctOption = int (input ("Out of bounds. Try again: "))
    
    def printContents(self):
        print ("Question", self.questionNum, "id:", self.questionId)
        print(self.prompt)
        for option in self.choices:
            print(option, ":", self.choices[option])
        print ("Correct option:", self.correctOption)
        print ("Number of answers:", self.totalAnswered)
        print ("Number correct:", self.numCorrect)
        print ("Users who answered correctly:")
        for user_id in self.usersCorrect:
            print("user_id:", user_id)
        print ("Users who answered incorrectly: ")
        for user_id in self.usersIncorrect:
            print("user_id:", user_id)
    

"""
Quiz Class
    Methods:
        -init
        -createQuestions
        -giveQuiz
        -questionId2question
    Variables:
        quizId (int) 
        name (str)
        numQs (int)
        questionStartId (int)  --> holds the question id of the first question in the quiz
        cat (str)            
        questions (dict)       --> maps question number to question
        results (dict)         --> maps user id to result
"""
class Quiz:
    def __init__(self, id: int, name: str, cat: str):
        self.quizId = id
        self.quizName = name
        self.quizCat = cat
        # maps question number to question
        self.questions = {}
        # maps user id to result
        self.results = {}
        self.numQs = -1
        self.questionStartId = -1

    # createQuestions()
    # - 
    def createQuestions(self, numQs: int, startId: int):
        self.numQs = numQs
        self.questionStartId = startId
        for qNum in range (0, self.numQs):
            questionId = self.questionStartId + qNum
            q = Question(qNum, questionId, self.quizId)
            q.makeQuestion()
            self.questions[qNum] = q
        print ("All questions successfully created")
    
    # giveQuiz()
    # - 
    def giveQuiz(self, userId: int):
        numCorrect = 0
        for x in self.questions:
            numCorrect += self.questions[x].giveQuestion(userId)
        if (userId in self.results):
            self.results[userId].append(float(numCorrect / float(self.numQs) * 100))
        else:
            self.results[userId] = [float(numCorrect / float(self.numQs) * 100)]

    # questionId2question()
    # - 
    def questionId2question (self, questionId: int):
        questionNum = questionId - self.questionStartId
        if questionNum not in self.questions:
            print ("Error: question id not found in Quiz")
            return 0
        return self.questions[questionNum]
    
    def printContents (self):
        print ("Quiz ID:", self.quizId)
        print ("Quiz Name:", self.quizName)
        print ("Quiz Category:", self.quizCat)
        for questionNum in self.questions:
            self.questions[questionNum].printContents()
        print ("Quiz Results:")
        for user_id, result in self.results.items():
            print("user_id:", user_id, ", result: ", result, "%")

"""
User Class
    Methods:
        -init
        -takeQuiz
    Variables:
        userId (int)           --> unique to every user in the Quizzle system
        quizzesTaken (set)     --> holds quiz id of every quiz taken by user
        name (str)

"""
class User:
    def __init__(self, userId: int, name: str):
        self.userId = userId
        self.quizzesTaken = set()
        self.name = name

    # takeQuiz()
    # - 
    def takeQuiz(self, q: Quiz):
        q.giveQuiz (self.userId)
        self.quizzesTaken.add(q.quizId)
    def printContents(self):
        print("Name:", self.name)
        print("user_id:", self.userId)
    

# Quizzle
# - The home base for the quiz making and taking platform
# - Maps each quiz to its corresponding quiz id
# - Maps each quiz id to its corresponding quiz category
# - Maps each user to its corresponding user id
# - Tracks then number of quizzes and users in the system
class Quizzle:
    def __init__(self):
        #maps quiz id to quiz
        self.quizzes = {}
        #maps user id to user
        self.users = {}
        #maps question id to the quizId of the quiz it is in
        self.questions = {}
        #maps category to list of quiz ids in category
        self.category2quiz = {}
        #tracks number of quizzes and is used to generate a new quiz id for each new quiz
        self.quizNum = 0
        #tracks number of users and is used to generate a new user id for each new user
        self.userNum = 0
        #tracks number of questions and is used to generate a new question id for each new question
        self.questionNum = 0
        #Spell Check dictionary
        self.d = enchant.Dict("en_US")
        # self.tree = pygtrie.StringTrie()
        # for key in self.d:
        #     self.tree[key] = self.d[key]




    # get_user_results ()
    # - 
    def get_user_scoring_avg(self, userId: int):
        if (userId in self.users):
            numerator = 0
            denominator = 0
            for quizId in self.users[userId].quizzesTaken:
                for result in self.quizzes[quizId].results[userId]:
                    numerator += result
                    denominator += 1
            avg = float(numerator / denominator)
            print ("Quiz average for User", userId, "is", avg,"%")
        else:
            print ("Error: user does not exist")
            

    # user_avg_quiz_score_input ()
    # -          
    def user_avg_quiz_score_input(self):
        userId = int(input ("Enter user id: "))
        while (userId not in self.users):
            userId = int(input ("Invalid id, try again: "))
        self.get_user_scoring_avg(userId)

    # get_question_scoring_avg ()
    # - 
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
    
    # question_scoring_avg_input ()
    # - 
    def question_scoring_avg_input(self):
        questionId = int (input ("Enter question id: "))
        while (questionId not in self.questions):
            questionId = int(input("Invalid id, try again: "))
        self.get_question_scoring_avg(questionId)
    
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

        #check if valid substring
        # string=' '
        # for x in range(0, left):
        #    string += input[x]
        # if (self.tree.has_subtrie(string) == False):
        #    return
        
        for i in range (left, right+1):
            input[left], input[i] = input[i], input[left]
            self.genPerms(input, output, cap_index, left + 1, right)
            input[left], input[i] = input[i], input[left]


    def input_capitalized_anagrams(self):
        word = input("Enter word: ")
        """
        word = r.get_random_word()
        while (len(word) <= 1):
            word = r.get_random_word()
        index = randint(0, len(word) - 1)
        output = ""
        #randomly makes one of the letters capitilized
        mod = word[index].upper()
        if index == 0:
            output = mod + word[index+1:]
        elif index == len(word) - 1:
            output = word[:index] + mod
        else:
            output = word[:index] + mod + word[index+1:]
        self.get_capitalized_anagrams(output)
        """
        self.get_capitalized_anagrams(word)
    
    def show_database(self):
        print ("Quizzes: ")
        for quiz in self.quizzes.values():
            quiz.printContents()
        print ("Users: ")
        for user in self.users.values():
            user.printContents()
            print ("Results: ")
            self.get_user_scoring_avg(user.userId)
        
            

    # makeQuiz():
    #   - Generates a new quiz id and increments quiz counter
    #   - Gets the quiz name and category from the user
    #   - Prompts the user to enter all the questions for the new quiz
    #   - Maps newly created quiz to the quiz id
    #   - Maps the quiz id to its quiz category
    def makeQuiz(self):
        quizId = self.quizNum
        self.quizNum += 1
        print ("Making Quiz. The quiz id is ", quizId)
        quizName = input ("Enter quiz name: ")
        quizCat = input ("Enter quiz category: ")
        newQuiz = Quiz(quizId, quizName, quizCat)
        numQs = int (input("Enter number of questions: "))
        q_start_id = self.questionNum
        self.questionNum += numQs
        newQuiz.createQuestions(numQs, q_start_id)
        self.quizzes[quizId] = newQuiz
        for questionId in range(q_start_id, self.questionNum):
            self.questions[questionId] = quizId
        if quizCat in self.category2quiz:
            self.category2quiz[quizCat].append(quizId)
        else:
            self.category2quiz[quizCat] = [quizId]

    # setUpQuiz():
    #   - Initilizes the process of a user taking a quiz
    #   - Prompts new users and existing users in their own directions
    def setUpQuiz(self):
        val = int (input ("Taking a Quiz. Enter 1 for new and 0 for existing user: "))
        while (val != 1 and val != 0):
            val = int (input ("Invalid Input. Enter 1 for new and 0 for existing: "))
        if (val == 1):
            self.newUserQuiz()
        if (val == 0):
            self.existingUserQuiz()

    # newUserQuiz():
    #   - Creates a user id for the new user and has them start the quiz taking process
    def newUserQuiz(self):
        print ("Your user ID is ", self.userNum)
        name = input ("Enter Name: ")
        userId = self.userNum
        self.userNum += 1
        newUser = User(userId, name)
        self.users[userId] = newUser
        self.startQuiz(userId)
    
    # existingUserQuiz():
    #   - Has user enter their existing id and starts them on the quiz taking process
    def existingUserQuiz(self):
        userId = int (input("Enter your user ID: "))
        while userId not in self.users:
            userId = int (input("Invalid. Enter valid user ID (or -1 to create new id): "))
            if (userId == -1):
                break
        if (userId == -1):
            self.newUser()
        else:
            self.startQuiz(userId)

     # startQuiz():
     #   - Has user enter the quiz id they want to take
     #   - Triggers user to take specified quiz
    def startQuiz(self, userId: int):
        quizId = int (input ("Enter valid quiz id: "))
        while quizId not in self.quizzes:
            quizId = int (input ("Invalid number. Enter valid quiz id: "))
        self.users[userId].takeQuiz(self.quizzes[quizId])
    
    def print_instructions(self):
        print ("Make Quiz: 0")
        print ("Take Quiz: 1")
        print ("Average Quiz Score for User: 2")
        print ("Statistics on a Question: 3")
        print ("Entire Current Data Base: 4")
        print ("Generate Valid Anagrams: 5")
        print ("End Program: 6")
    
    def print_start_buffer(self):
        print("\n")
        print("-------------performing task-----------------")
        print("\n")
    
    def print_end_buffer(self):
        print("\n")
        print("-------------task ended-----------------")
        print("\n")

    # run():
    #   - Driver for the program
    def run(self):
        run = 1
        self.print_instructions()
        while run == 1:
            val = int (input ('Input (Enter 7 to see instructions): '))
            while (val < 0 and val > 7):
                val = int (input ("input must be 0, 1, 2, 3, 4, 5, 6, or 7: "))
            self.print_start_buffer()
            if(val == 0):
                self.makeQuiz()
            elif (val == 1):
                self.setUpQuiz()
            elif(val == 2):
                self.user_avg_quiz_score_input()
            elif(val == 3):
                self.question_scoring_avg_input()
            elif (val == 4):
                self.show_database()
            elif (val == 5):
                self.input_capitalized_anagrams()
            elif (val == 6):
                print ("Program ended")
                break
            elif (val == 7):
                self.print_buffer()
                self.print_instructions()
            self.print_end_buffer()       

def main():
    q = Quizzle()
    q.run()

if __name__=="__main__":
    main()

        
