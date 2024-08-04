from flask import Flask, request 

import logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import gemini as AI
 
app = Flask(__name__) 
 
@app.route('/') 
def home(): 
    return  "Hello"

@app.route("/chat/id/<user>")
def askGeminiWithLineID(user):
    logger.debug (user)
    ask = request.args.get('ask')

    answer = AI.askGemini (user, ask) 


    return ("AI answers: " + str(answer))



if __name__ == '__main__': 
    app.run(debug=True, port="8888") 