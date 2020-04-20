import os
from flask import Flask
from flask import request, redirect, abort
import random

app = Flask(__name__, static_folder="static")

members = [
    {"id":"oh", "pw":"123"},
    {"id":"chung", "pw":"456"}
]

def get_menu():
    menu_temp = "<li><a href='/{0}'>{0}</a></li>"
    menu = [m for m in os.listdir('content') if m[0] != '.']
    return "\n".join([menu_temp.format(e) for e in menu])

def readFile(filename):
    with open(f'{filename}', 'r', encoding="utf-8") as f:
        value = f.read()
    return value
def writeFile(filename,value):
    with open(f'{filename}', 'w') as f:
        f.write(str(value))

def createAnswerNumber(filename):
    while True:
        value = str(random.randint(100, 999))
        if len(value) == len(set(value)):
            break
    with open(f'game/{filename}', 'w') as f:
        f.write(value)

def gameCalculate(user_number):
    with open(f'game/answernumber', 'r') as f:
        answer_number = f.read()
    strike = 0
    ball = 0
    out = 0


    count = int(readFile('game/count_try'))
    writeFile('game/count_try',count+1)
    
    if len(user_number) != len(set(user_number)):
        return "중복 없이 다시 입력하세요."
    elif len(answer_number) != len(set(user_number)):
        return "숫자 자리수가 맞지 않습니다. 자리수에 맞게 다시 입력하세요."
    else:
        for i in range(len(user_number)):
            if user_number[i] == answer_number[i]:
                strike += 1
            elif user_number[i] in answer_number:
                ball += 1
            else: 
                out += 1
    if strike == len(answer_number):
        writeFile('game/count_try',0)        
        return "{0} 번만에 맞히셨습니다.".format(count)
    else:
        return "{0}strike {1}ball {2}out 입니다. \n {3} 번 틀리셨습니다.".format(strike, ball, out, count)
       


@app.route('/')
def main():
    template = readFile("template.html")
    title = "Main Page"
    content = "<img src='https://source.unsplash.com/featured/?south america,?mountain' height=100% width=100%> </img>"
    menu = get_menu()
    return template.format(title, menu,content,'')

# @app.route('/<title>')
# def functions(title):
#     template = get_template('template.html')
#     menu = get_menu()
#     with open(f'content/{title}', 'r') as f:
#         content = f.read()
#     print(content)
#     return template.format(title, menu,content)

@app.route('/<title>')
def functions(title):
    template = readFile('template.html')
    menu = get_menu()
    with open(f'content/{title}', 'r') as f:
        content = f.read()
    print(content)
    return template.format(title, menu,content,'')

@app.route('/playgame', methods=['GET','POST'])
def playgame():
    template = readFile('template.html')
    menu = get_menu()
    with open(f'game/playgame', 'r') as f:
        content = f.read()

    if request.method == 'GET':
        return template.format('playgame',menu,content,'') 
    elif request.method == 'POST':
        number = request.form["number"]
        desc = gameCalculate(number)
        return template.format('playgame', menu,content,desc) 

@app.route('/gamestart')
def gamestart():
    template = readFile('template.html')
    menu = get_menu()
    with open(f'game/gamestart', 'r') as f:
        content = f.read()
    createAnswerNumber('answernumber')

    return template.format('gamestart', menu,content,'')



@app.route('/login', methods=['GET', 'POST'])
def login():
    template = readFile('login.html')
    menu = get_menu()

    if request.method == 'GET':
        return template.format("login page", menu)
    elif request.method == 'POST':
        m = [e for e in members if e["id"] == request.form["id"]]
        if len(m) == 0:
            return template.format("login failed", "<p>회원이 아닙니다.</p>", menu)
        if request.form['pw'] != m[0]['pw']:
            return template.format("try again", "<p>패스워드를 확인해 주세요. </p>", menu)
        return redirect("/?id=" + m[0]["id"])

@app.route('/favicon.ico')
def favicon():
    return abort(404)
app.run()
