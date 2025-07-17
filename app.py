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

@app.route("/assistant", methods=["GET", "POST"]) # GENAI assistant 
def assistant():
    ai_answer = None
    if request.method == "POST":
        user_input = request.form.get("user_input")
        ai_answer = f"(Demo) You asked: {user_input}"
    return render_template("assistant.html", ai_answer=ai_answer)



if __name__ == "__main__":
    app.run(debug=True)
    
