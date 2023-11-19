from flask import Flask, render_template, request
import spacy
import nltk

from nltk import word_tokenize, pos_tag

app = Flask(__name__, static_url_path='/static')

nlp = spacy.load("en_core_web_sm")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_text():
    selected_text = request.form["text"]
    method = request.form["method"]
    
    if selected_text == "text1":
        text = "I went to DanLo sir for my doubt clarification."
    elif selected_text == "text2":
        text = "Lucas and Chloe won the dance competition."
    elif selected_text == "text3":
        text = "Patrick and Grace are studying hard to get a good score."
    elif selected_text == "text4":
        text = "Henry and Victoria are planning a cross-country road trip."
    elif selected_text == "text5":
        text = "Charlotte and Samuel are planning a surprise party for their parents."
    elif selected_text == "text6":
        text = "Greshmi and James organized a charity event to help the homeless."
    elif selected_text == "text7":
        text = "We are planning a surprise for Amanda and Christopher."
    recognized_text = text  # Initialize recognized text
    count = 0
    if method == "cfg":
        tokens = pos_tag(word_tokenize(text))
        grammar = r"""NAME: {<NNP>+} """
        parser = nltk.RegexpParser(grammar)
        result = parser.parse(tokens)

        for token in result:
            if isinstance(token, nltk.tree.Tree) and token.label() == "NAME":
                name = token.leaves()[0][0]
                recognized_text = recognized_text.replace(name, f'<span class="highlight">{name}</span>')
                count += 1

    if method == "spacy":
        custom_entities = []

        for ent in nlp(text).ents:
            if ent.label_ == "PERSON":
                name = ent.text
                custom_entities.append((name, "name"))
                recognized_text = recognized_text.replace(name, f'<span class="highlight">{name}</span>')
                count += 1

    return render_template("index.html", recognized_text=recognized_text, count=count, method=method)


