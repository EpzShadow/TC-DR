from dataclasses import dataclass
from flask import Flask
from flask import render_template
from flask import request
from summary import main
import datetime

app = Flask(__name__,
        static_url_path='/static',
        static_folder='static',
        template_folder='templates',
)   


@app.route("/", methods = ['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data['name'])
        x = main(data['name'])
        return render_template('index.html', x = x, old_data = data['name'])
    else:
        return render_template('index.html', utc_dt= datetime.datetime.utcnow())
  
# @app.route("/summarize", methods = ['POST', 'GET'])
# def summarize_world():
#     data = request.form.to_dict()
#     x = algo(data['name'])
#     return x



