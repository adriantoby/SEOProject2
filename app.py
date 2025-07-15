from flask import Flask, render_template
app = Flask(__name__)

@app.route("/") # home page
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about") # about page
def about():
    return render_template("about.html")

@app.route("/trade") # trade page
def trade():
    return render_template("trade.html")

if __name__ == "__main__":
    app.run(debug=True)