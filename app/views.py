from flask import jsonify, render_template
from app import app


@app.route('/')
def home():
    return "Flask says 'Hello world!'"


@app.route('/crash')
def crash():
    return 1/0


@app.route('/lab02')
def resume():
    return app.send_static_file('lab02_resume.html')

@app.route("/api/data")
def data():
    # define some data
    d = {
        "Alice": "(708) 727-2377",
        "Bob": "(305) 734-0429"
    }


    app.logger.debug(str(len(d)) + " entries in phonebook")


    return jsonify(d)


