import spacy
from spacy.matcher import Matcher


nlp = spacy.load('en_core_web_lg')

with open('news.txt', 'r', encoding='utf-8') as f:
    data = f.read()

features = data.split('. ')

text = nlp(features[1])

print(text)
names = []
events = []
dates = []
money = []


for ent in text.ents:
    print(ent.text, ent.label_)
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
                print(word)
                events.append(word)
                iterator = 1
            else:
                events.append(token.text)
        except:
            print("End of text")

match = [{"POS" : "NOUN"}, {"POS" : "VERB"}]

print(names)
print(events)
print(dates)
print(money)
