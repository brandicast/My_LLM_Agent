import google.generativeai as genai
import os

import logging
logger = logging.getLogger(__name__)

genai.configure(api_key=os.environ["API_KEY"])

with open('system_instruction.txt') as f:
    instruction = f.read ()
    logger.debug(instruction)

sessions = {}


def askGemini (line_id, content):

    if line_id not in sessions:
        logger.debug ("No Chat session is found for : " + str(line_id) + ". Starts a new chat session")

        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=instruction,
            safety_settings={genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                             genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE  })
        
        sessions[line_id] = model.start_chat(history=[])  # Load history from here

    chat = sessions[line_id]
    
    response = chat.send_message(content)

    return response.text