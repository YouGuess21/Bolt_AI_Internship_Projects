import os
from flask import Flask, render_template_string, request, jsonify
from boltiotai import openai

# set your openAI API key in secrets
openai.api_key = os.environ['OPENAI_API_KEY']


# function to generate educational content based on the course title using the api
def generate_content(course_title):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant"
            }, {
                "role":
                "user",
                "content":
                f"""Generate educational content for the course titled "{course_title}". Include:     1. Objective of the Course     2. Sample Syllabus     3. Three Measurable Outcomes categorized by Bloom's Taxonomy levels (Knowledge, Comprehension, Application)     4. Assessment Methods     5. Recommended Readings and Textbooks."""
            }])
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "Sorry, we are facing some issues, please try again later."


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    output = ""
    if request.method == 'POST':
        course_title = request.form['course_title']
        output = generate_content(course_title)

    return render_template_string('''

 <!DOCTYPE html >
 <html >
 <head >
  <title >Course Content Suggestor</title >
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
    rel="stylesheet">
  <script >

  async function generateTutorial() {
   const course_title = document.querySelector('#course_title').value;
   const output = document.querySelector('#output');
   output.textContent = 'Finding the best content for you...';
   const response = await fetch('/generate', {
    method: 'POST',
    body: new FormData(document.querySelector('#tutorial-form'))
   });
   const newOutput = await response.text();
   output.textContent = newOutput;
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

  </script >
 </head >
 <body style="background-color:#F9E4BC;" >
  <div class="container">
   <h1 class="my-4" style="color:purple; font-family:Times New Roman; font-weight: bold;">Find the Best Education Content!</h1 >
   <form id="tutorial-form" onsubmit="event.preventDefault(); generateTutorial();" class="mb-3">
    <div class="mb-3">
     <label for="course_title" class="form-label">Course Name:</label >
     <input type="text" class="form-control" id="course_title" name="course_title" placeholder="Enter the course title you want educational content for" required >
    </div >
    <button type="submit" class="btn btn-primary">Search</button >
   </form >
   <div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
     Course Details:
     <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy </button >
    </div >
    <div class="card-body">
     <pre id="output" class="mb-0" style="white-space: pre-wrap;">{{ output }}</pre >
    </div >
   </div >
  </div >
 </body >
 </html >


 ''',
                                  output=output)


@app.route('/generate', methods=['POST'])
def generate():
    course_title = request.form['course_title']
    return generate_content(course_title)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
