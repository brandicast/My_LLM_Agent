import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException

import os, time, threading, pickle


from util.typing import Session




import logging
logger = logging.getLogger(__name__)

genai.configure(api_key=os.environ["API_KEY"])

model = None          # Hold A global GenAI model
sessions_cache = {}   # Hold a session cache
last_dump_time = None

GRACEFULLY_STOP = False 

with open('./resources/system_instruction.txt') as f:
    instruction = f.read ()
    logger.debug(instruction)



def loadChatSession ():
    directory_path = 'history'
    files_and_dirs = os.listdir(directory_path)

    # 過濾出檔案
    files = [f for f in files_and_dirs]    
    logger.debug(files) 

    for f in files_and_dirs:
         filename = os.path.join(directory_path, f)
         if os.path.isfile(filename):
             with open(filename, 'rb') as file:
                 history = pickle.load(file)
                 logger.debug(history)
                 if history != '' :
                    model = getModel() 
                    session = Session()
                    session.chat = model.start_chat(history=history)
                    session.timestamp = time.time() 
                    sessions_cache[str(f)] = session 


def ask (id, content):
    answer = "哇，不知道怎麼回答這個問題"
    if id not in sessions_cache:
        logger.debug ("No Chat session is found for : " + str(id) + ". Starts a new chat session")

        model = getModel()
        
        chat_session = Session()
        chat_session.chat = model.start_chat(history=[])  # Load history from here
        chat_session.timestamp = time.time()

        sessions_cache[id] = chat_session

        
    session  = sessions_cache[id]
    
    logger.debug (session)
    #logger.debug (chat.history)
    try:
        response = session.chat.send_message(content)
        session.timestamp = time.time()
        answer = response.text
    except StopCandidateException as safety_exception :
        logger.error ("Error occurred when user ask : " + content + "  with exception : " + str(safety_exception)) 
        answer = "為了保護你，這個問題就不回答了"
    except Exception as e:
        logger.error ("Error occurred when user ask : " + content + "  with exception : " + str(e)) 

    return answer


def getModel ():
    global model
    if model is None:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=instruction,
            safety_settings={genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                             genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE, 
                             genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH, 
                             genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE})
    return model

def history (id):
    data = '' 
    session = sessions_cache[id]
    if session:
        data = str(session.chat.history) 
    return data


def historyPersistentJob () :

    while not GRACEFULLY_STOP:
        historyPersistent()
        time.sleep(60)

def historyPersistent():
    global last_dump_time
    if not sessions_cache is None:
            if not last_dump_time is None:
                for key in sessions_cache:
                    if last_dump_time < sessions_cache[key].timestamp:
                        history = sessions_cache[key].chat.history
                        if history :
                            with open('history/'+key, 'wb') as file:
                                pickle.dump(history, file)
    last_dump_time = time.time()


job = threading.Thread(target=historyPersistentJob)    
job.start()
