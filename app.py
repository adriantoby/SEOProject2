from flask import Flask
app = Flask(__name__)

@app.route("/") # home page
def home():
    return "Welcome to our Trade app!"

@app.route("/about") # about page
def about():
    return "This is our about page"

@app.route("/trade") # trade page
def trade():
    return "This is our trade page"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")