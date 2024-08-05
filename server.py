from flask import Flask, request 

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import gemini.agent as AI

import time
 
app = Flask(__name__) 
 
@app.route('/') 
def home(): 
    return  "Hello"

@app.route('/chat/id/<user>')
def askWithLineID(user):
    ask = request.args.get('ask')

    answer = AI.ask (user, ask) 


    return ("AI answers: " + str(answer))

@app.route('/chat/history/<user>')
def historyWithLineID(user):
    history = AI.history (user)
    return (history)




if __name__ == '__main__': 
    AI.loadChatSession()
    app.run(port="8888") 