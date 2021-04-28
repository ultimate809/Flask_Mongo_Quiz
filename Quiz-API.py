from flask import Flask, request ,jsonify
from flask_pymongo import PyMongo


app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
mongo = PyMongo(app)

def create_db():
    
    mongo.db.quiz.insert({ "_id" : 5, "name" : "maths", "description" : "This is a maths quiz" })
    mongo.db.quiz.insert({ "_id" : 6, "name" : "English", "description" : "This is a english quiz" })
    mongo.db.quiz.insert({ "_id" : 7, "name" : "Hindi", "description" : "This is a hindi quiz" })
    
def get_quiz_id():
    result=mongo.db.quiz.find()
    max_id=0
    for ele in result:
        if(ele["_id"]>max_id):
            max_id=ele["_id"]
    global QUIZ_ID
    QUIZ_ID=max_id
    
    
def get_ques_id():
    result=mongo.db.quiz.find()
    max_id=0
    for ele in result:
        if("questions" in ele.keys()):
            for ques in ele["questions"]:
                if(ques["_id"]>max_id):
                    max_id=ques["_id"]
    global QUESTION_ID
    QUESTION_ID=max_id

create_db()    
QUIZ_ID=0
get_quiz_id()                       
QUESTION_ID=100
get_ques_id()    
                


    
    
def insert_quiz_details(quiz_name , quiz_description):
    response=mongo.db.quiz.insert({"_id":QUIZ_ID,"name":quiz_name,"description":quiz_description})
    return response
    
def fetch_quiz_details(quiz_id):
    output=mongo.db.quiz.find({"_id":quiz_id})
    return output

def insert_question_details(name,options,cor_option,quiz_id):
    response="Not Found"
    ques_list=[]
    
    result=mongo.db.quiz.find({"_id":quiz_id})
    for ele in result:
        if(ele["_id"]==quiz_id):
            if("questions" in ele.keys()):
                ques_list=ele["questions"]
        ques_list.append({"_id":QUESTION_ID,"Name":name,"Options":options,"Correct Option":cor_option})
        response=mongo.db.quiz.update({"_id":quiz_id},{"_id":quiz_id , "name":ele["name"] , "description":ele["description"],"questions":ques_list})
    return response

def fetch_question_details(question_id):
    result=mongo.db.quiz.find()
    response = "408 Not found"
    for ele in result:
       for ques in ele["questions"]:
           if(ques["_id"]==question_id):
               response=ques
    return response


@app.route('/api/', methods=['GET'])
def get_all_quiz_details():
    output="quiz details by id"
    if request.method == 'GET':
        output=mongo.db.quiz.find()
        response=[]
        for ele in output:
            response.append(ele)
        if(len(response)==1):
            return "Error 400"
        else:
            return jsonify({'result' : response})
        
@app.route('/api/quiz/<quiz_id>', methods=['GET'])
def get_quiz_details(quiz_id):
    output="quiz details by id"
    quiz_id=int(quiz_id)
    print(quiz_id)
    if request.method == 'GET':
        output=fetch_quiz_details(quiz_id)
        response=[]
        for ele in output:
            response.append({'_id' : int(ele['_id']), 'Name' : ele['name'], 'Description' : ele['description']})
        if(len(response)==0):
            return "Error 400"
        else:
            return jsonify({'result' : response})

@app.route('/api/quiz', methods=['POST'])
def post_quiz_details():
    if request.method == 'POST':
        global QUIZ_ID
        QUIZ_ID+=1
        print(QUIZ_ID)
        data = request.get_json()
        print(data["name"] , data["description"])
        response=insert_quiz_details(data["name"] , data["description"])
        print(data) 
        return str(response)

@app.route('/api/questions/<question_id>', methods=['GET'])
def get_question_details(question_id):
    question_id=int(question_id)
    print(question_id)
    if request.method == 'GET':
        response=fetch_question_details(question_id)
        # response=[]
        # for ele in output:
        #     response.append(ele)
        if(len(response)==0):
            return "Error 400"
        else:
            return jsonify({'result' : response})

@app.route('/api/questions', methods=['POST'])
def post_question_details():
    if request.method == 'POST':
        global QUESTION_ID
        QUESTION_ID+=1
        data = request.get_json()
        print(data["name"], data["options"], data["correct_option"],data["quiz"])
        response=insert_question_details( data["name"], data["options"], data["correct_option"],data["quiz"])
        print(data)
        return str(response)

@app.route('/api/quiz-questions/<quiz_id>', methods=['GET'])
def get_quiz_questions_details(quiz_id):
    output="quiz details and question details by quiz_id"
    quiz_id=int(quiz_id)
    print(quiz_id)
    if request.method == 'GET':
        output=fetch_quiz_details(quiz_id)
        response=[]
        for ele in output:
            response.append(ele)
        if(len(response)==0):
            return "Error 400"
        else:
            return jsonify({'result' : response})

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)
#app.run()