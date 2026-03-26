from flask import Flask, request, jsonify
import os

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import gemini.agent as AI

import time
 
app = Flask(__name__) 
 
@app.route('/') 
def portal(): 
    """A friendly portal interface to access all features."""
    template_path = os.path.join('resources', 'portal.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/chat/id/<user>')
def askWithLineID(user):
    ask = request.args.get('ask')

    answer = AI.ask (user, ask) 


    return (str(answer).strip())

@app.route('/chat/history/<user>')
def historyWithLineID(user):
    history = AI.history (user)
    return ('<pre>' + history + '</pre>')

@app.route('/archives')
def list_archives_dates():
    """List all dates with archived histories."""
    history_dir = 'history'
    if not os.path.exists(history_dir):
        return "No archives found."
    
    dates = [d for d in os.listdir(history_dir) if os.path.isdir(os.path.join(history_dir, d))]
    dates.sort(reverse=True)
    
    html = "<h1>Archived Dates</h1><ul>"
    for d in dates:
        html += f'<li><a href="/archives/{d}">{d}</a></li>'
    html += "</ul>"
    return html

@app.route('/archives/<date>')
def list_archives_users(date):
    """List all users with archived histories for a specific date."""
    date_dir = os.path.join('history', date)
    if not os.path.exists(date_dir):
        return f"No archives found for {date}."
    
    users = [u.replace('.md', '') for u in os.listdir(date_dir) if u.endswith('.md')]
    users.sort()
    
    html = f"<h1>Archives for {date}</h1><ul>"
    for u in users:
        html += f'<li><a href="/archives/{date}/{u}">{u}</a></li>'
    html += "</ul><br><a href='/archives'>Back to dates</a>"
    return html

@app.route('/archives/<date>/<user>')
def view_archive(date, user):
    """View the archived markdown content for a user on a specific date."""
    file_path = os.path.join('history', date, f"{user}.md")
    if not os.path.exists(file_path):
        return f"Archive for {user} on {date} not found."
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple markdown-to-html (could use a library, but for now simple pre tags)
    html = f"<h1>Archive: {user} ({date})</h1>"
    html += f'<div style="white-space: pre-wrap; font-family: sans-serif; padding: 20px; border: 1px solid #ccc;">{content}</div>'
    html += f"<br><a href='/archives/{date}'>Back to {date}</a>"
    return html




if __name__ == '__main__': 
    AI.loadChatSession()
    app.run(host='0.0.0.0') 
