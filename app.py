from flask import Flask, render_template, request, redirect, jsonify
import facenet
import database

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    logs = database.get_logs()
    stats = {
        "connus": sum(1 for log in logs if log['identity'] != "Inconnu"),
        "inconnus": sum(1 for log in logs if log['identity'] == "Inconnu"),
        "total": len(logs)
    }
    return render_template('dashboard.html', logs=logs, stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']
        embedding = facenet.get_embedding(image)
        database.save_face(name, embedding)
        return redirect('/dashboard')
    return render_template('register.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    image = request.files['image']
    embedding = facenet.get_embedding(image)
    result = database.match_face(embedding)
    database.log_access(result)
    return jsonify({'result': result})

@app.route('/camera')
def camera():
    return render_template('camera.html')

if __name__ == '__main__':
    app.run(debug=True,port=5050)