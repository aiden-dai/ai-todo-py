import os
import requests
import json
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

task_api_host = os.environ.get('TASK_API_HOST', 'localhost')
task_api_port = os.environ.get('TASK_API_PORT', '8080')
app.config["BASE_URI"] = 'http://{}:{}/api'.format(
    task_api_host, task_api_port)


@app.route("/", methods=['GET'])
def index():
    """ Retrieve a list of messages from the backend, and use them to render the HTML template """
    url = '{}/tasks'.format(app.config["BASE_URI"])
    response = requests.get(url, timeout=3)
    print(response)
    print(response.status_code)
    tasks = json.loads(response.text)
    print(tasks)
    return render_template('index.html', tasks=tasks)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """ Retrieve a list of messages from the backend, and use them to render the HTML template """
    if request.method == 'POST':
        content = request.form.get('content', None)
        print(content)
        body = {"content": content}
        url = '{}/tasks'.format(app.config["BASE_URI"])
        response = requests.post(url=url,
                                 json=body,
                                 headers={'content-type': 'application/json'},
                                 timeout=3)

        print(response)
        print(response.status_code)
        # message = json.loads(response.text)
        print(response.text)

        return redirect('/')
    else:
        return render_template('create.html')


@app.route('/delete')
def delete_task():
    """ Retrieve a list of messages from the backend, and use them to render the HTML template """
    id = request.args.get('id', '')
    print(id)
    url = '{}/tasks/{}'.format(app.config["BASE_URI"], id)

    response = requests.delete(url=url)

    print(response)
    print(response.status_code)
    # message = json.loads(response.text)
    print(response.text)

    return redirect('/')


@app.route('/complete')
def complete_task():
    """ Retrieve a list of messages from the backend, and use them to render the HTML template """
    id = request.args.get('id', '')
    print(id)
    url = '{}/tasks/{}/done'.format(app.config["BASE_URI"], id)

    response = requests.put(url=url)

    print(response)
    print(response.status_code)
    # message = json.loads(response.text)
    print(response.text)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=8081)
