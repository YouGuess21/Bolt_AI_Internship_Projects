import os
from flask import Flask, render_template_string, request, jsonify
from boltiotai import openai

# Set your OpenAI API key in secrets
openai.api_key = os.getenv('OPENAI_API_KEY')


# Function to generate code based on the problem and programming language
def generate_code(problem, programming_language, requisites):
    requisites_text = requisites if requisites else "nothing"
    prompt = f"generate a {programming_language} code to solve the following problem: {problem}. The code should have {requisites_text} as requisites. Only give code in your response, nothing else."

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant"
            }, {
                "role": "user",
                "content": prompt
            }])
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "Sorry, we are facing some issues, please try again later."


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        problem = request.form['problem']
        programming_language = request.form['programming_language']
        requisites = request.form.get('requisites', 'nothing')
        output = generate_code(problem, programming_language, requisites)

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Homework Coding Problem Solver</title>
            <!-- Link to dark theme Bootstrap CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/darkly/bootstrap.min.css" rel="stylesheet">
           
            <script>
                async function generateCode() {
                    const form = document.querySelector('#coding-form');
                    const output = document.querySelector('#output');
                    output.textContent = 'Generating code...';
                    try {
                        const response = await fetch('/generate', {
                            method: 'POST',
                            body: new FormData(form)
                        });
                        if (!response.ok) {
                            throw new Error('Network response was not ok ' + response.statusText);
                        }
                        const result = await response.json();
                        output.textContent = result.content;
                    } catch (error) {
                        output.textContent = 'An error occurred: ' + error.message;
                    }
                }
                function copyToClipboard() {
                    const output = document.querySelector('#output');
                    const textarea = document.createElement('textarea');
                    textarea.value = output.textContent;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    alert('Copied to clipboard');
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h1 class="my-4" style="font-family: monotone; font-weight: bold; color: #e06846;">Solve your coding problems instantly!</h1>
            <p style="font-style: italic; font-size: 22px; color: aqua;">Use the latest AI technology to solve your problems at your fingertips.</p>

                <form id="coding-form" onsubmit="event.preventDefault(); generateCode();" class="mb-3">
                    <div class="mb-3">
                        <label for="problem" class="form-label">Problem:</label>
                        <textarea class="form-control" id="problem" name="problem" required></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="programming_language" class="form-label">Programming Language:</label>
                        <select class="form-control" id="programming_language" name="programming_language" required>
                            <option value="bash">Bash</option>
                            <option value="c">C</option>
                            <option value="c++">C++</option>
                            <option value="go">Go</option>
                            <option value="java">Java</option>
                            <option value="php">PHP</option>
                            <option value="python">Python</option>
                            <option value="ruby">Ruby</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="requisites" class="form-label">Requisites (optional):</label>
                        <input type="text" class="form-control" id="requisites" name="requisites">
                    </div>
                    <button type="submit" class="btn btn-primary">Generate</button>
                </form>
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        Code:
                        <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy</button>
                    </div>
                    <div class="card-body">
                        <pre id="output" class="mb-0" style="white-space: pre-wrap;">{{ output }}</pre>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''',
                                  output=output)


@app.route('/generate', methods=['POST'])
def generate():
    problem = request.form['problem']
    programming_language = request.form['programming_language']
    requisites = request.form.get('requisites', 'nothing')
    content = generate_code(problem, programming_language, requisites)
    return jsonify(content=content)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
