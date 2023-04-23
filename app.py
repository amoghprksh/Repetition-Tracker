from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

#@app.route("/runscript")
#def run_script():
#    result = subprocess.run(["python", "myscript.py"], capture_output=True)
#    return result.stdout


#this is for deadlift
@app.route('/run_script')
def run_script():
    # execute the deadliftnew.py script
    subprocess.call(['python', 'deadliftnew.py'])
    
    # return an empty response
    return ''


#this is for pushups
@app.route('/run_script2')
def run_script2():
    # execute the pushup.py script
    subprocess.call(['python', 'pushup.py'])
    
    # return an empty response
    return ''

#this is for biceps
@app.route('/run_script3')
def run_script3():
    # execute the biceps.py script
    subprocess.call(['python', 'biceps.py'])
    
    # return an empty response
    return ''


if __name__ == "__main__":
    app.run()



