from flask import Flask, session, g, render_template, jsonify, request, Response
from GenerationFactory import GenerationFactory
app = Flask(__name__)



@app.route("/")
def form():
    return render_template('content.html')

@app.route('/genclassesresult/', methods=['POST'])
def genclassesresult():
    dictionary={}
    testfile = ""
    dictionary=GenerationFactory.buildDictionaryfromPostRequest(request.form)
    testfile = GenerationFactory.generateManualTestFile(dictionary,int(request.form['numrows'])+1)
    return Response(testfile,
                       mimetype="text/plain",
                       headers={"Content-Disposition":
                                    "attachment;filename=tests.py"})

if __name__ == "__main__":
    app.run()

