from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import anthropic

app = Flask(__name__)
socketio = SocketIO(app)
client = anthropic.Anthropic()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    def generate():
        with client.messages.stream(
            messages=[{"role": "user", "content": """
                                                    Your job is to intervene on a chatroom to ease tension and seek common ground.
                                                    In your response, use headings, paragraphs, and bold text only where necessary. 
                                                    Your response will be streamed to an HTML file.
                                                    Instead of using <ul> or <ol> tags for lists, use a series of <p> tags with the "list-item" class to represent list items. 
                                                    Return your entire explanation in HTML code with no intro or greetings. 
                                                    
                                                    You must act as a mediator in a heated conversation about abortion.
                                                    The two speakers are mad that the other does not agree about when life begins.
                                                    Provide a message to the chatroom that can cool down the conversation and help the users see eye to eye.
                                                    Include a list of potential sources with links each person could look at online to educate themselves on the topic.
                                                    This list should have a small heading.
                                                    Bold or italicize important words or phrases in your reponse.
                       
                                                    Begin your response with the bolded label "Guide: "
                                                  """}],
            max_tokens=1024,
            model="claude-3-opus-20240229",
        ) as stream:
            for text in stream.text_stream:
                print(text, end="")
                yield f"data: {text}\n\n"
            yield "data: [DONE]\n\n"
        
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    socketio.run(app)