from flask import Flask, render_template, request, send_file
from transformers import BartForConditionalGeneration, BartTokenizer
from waitress import serve

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    if request.method == "POST":
        text = request.form["text"]

        # Use transformers library for summarization
        model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
        tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

        inputs = tokenizer.encode(
            "summarize: " + text, return_tensors="pt", max_length=1024, truncation=True
        )
        summary_ids = model.generate(
            inputs,
            max_length=300,
            length_penalty=2.0,
            min_length=75,
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return render_template("index.html", text=text, summary=summary)


@app.route("/export", methods=["POST"])
def export():
    if request.method == "POST":
        text = request.form["text"]
        summary = request.form["summary"]

        with open("summary.txt", "w") as file:
            file.write(f"Original Text:\n{text}\n\nSummary:\n{summary}")

        return send_file("summary.txt", as_attachment=True)


if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)
