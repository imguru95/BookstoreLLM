from flask import Flask, render_template
import openai
import re

app = Flask(__name__)
openai.api_key = '#####################'#replace this with your Open AI API key
global_messages = [{"role":"system", "content":"You are a helpful assistant"}]
global_fields = {"computerscience":"Computer Science", "psychology":"Psychology", "biology":"Biology", "spirituality":"Spirituality", "history":"History", "literature":"Literature", "economics":"Economics"}

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/field/<field>', methods=['GET'])
def display_books(field):
    global global_fields
    prompt = f'List the top 10 books in the field of {global_fields[field]} along with their release dates'
    reply = gpt_call(prompt)
    lst = []
    if reply:
        lst = process_data(reply)
    return render_template("results.html", results=[global_fields[field], lst])

@app.route('/summary/<field>/<index>', methods=['GET'])
def get_summary(field, index):
    global global_fields
    prompt = f'Give me a 2 sentence summary of book {index} in {global_fields[field]} that you just output'
    reply = gpt_call(prompt)
    return {'summary':reply}

def gpt_call(prompt):
    global global_messages
    global_messages.append({"role": "user", "content": prompt})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=global_messages)
    reply = chat.choices[0].message.content
    global_messages.append({"role": "assistant", "content": reply})
    return reply

def process_data(reply):# the processing can be made robust by handling different output formats
    reply_lines = reply.split("\n")
    list_books = []
    pattern = r'(\d+)\.(.*)'
    for line in reply_lines:
        book = []
        match = re.match(pattern, line)
        if match:
            text_after_dot = match.group(2)
            book_name, book_details = text_after_dot[2:].split(" by ")
            book.append(book_name[:-1])
            author_name, release_date = book_details.split(" (")
            book.append(author_name)
            book.append(release_date[:-1])
            list_books.append(book)
        else:
            print("No match found.")
    return list_books

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
