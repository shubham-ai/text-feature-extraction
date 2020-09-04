import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_lg')
matcher = Matcher(nlp.vocab)

with open('news.txt', 'r', encoding='utf-8') as f:
    data = f.read()

features = data.split('. ')

text = nlp(features[2])

print(text)
names = []
events = []
references = []
dates = []
money = []
proper_nouns = []

for ent in text.ents:
    if ent.label_ == "MONEY":
        money.append(ent.text)

    if ent.label_ == "DATE":
        dates.append(ent.text)
    

iterator = 0

for token in text:
    print(token.text, token.pos_)

for token in text:
    if iterator > 0:
        iterator -= 1
        continue

    if token.pos_ == "PROPN":
        proper_nouns.append(token.text)
        b = [i for i in dates if i.find(token.text) > -1]
        c = [i for i in money if i.find(token.text) > -1]
        if (len(b) == 0 and len(dates) != 0 or (len(c) == 0 and len(money) != 0)):
            try:
                if(text[token.i + 1].pos_ == "NOUN"):
                    if(text[token.i + 2].pos_ == "NOUN"):
                        word = token.text + " " + text[token.i + 1].text + " " + text[token.i + 2].text
                        events.append(word)
                        iterator = 2
                    else:
                        word = token.text + " " + text[token.i + 1].text
                        events.append(word)
                        iterator = 1
                else:
                    names.append(token.text)
            except:
                print("End of text")

        continue

    if token.pos_ == "NOUN":
        try:
            if text[token.i+1].pos_ == "VERB":
                word = token.text + " " + text[token.i + 1].text
                events.append(word)
                iterator = 1
            else:
                events.append(token.text)
        except:
            print("End of text")


match = [{"POS":"PROPN"},
        {"POS":"ADP", "OP":"?"},
        {"POS":"PROPN", "OP":"?"},
        {"POS":"VERB", "OP":"?"}]

action = [{"POS":"VERB"},
            {"POS":"ADJ", "OP":"?"},
            {"POS":"ADP", "OP":"?"},
            {"POS":"DET", "OP":"?"},
            {"POS":"NOUN", "OP":"?"}]

matcher.add("Context", None, match)
matcher.add("action", None, action)
matches = matcher(text)

remove_duplicates = [text[start:end] for _, start, end in matches]
span = spacy.util.filter_spans(remove_duplicates)


for i in span:
    references.append(i)


print(names)
print(events)
print(references)
print(dates)
print(money)
