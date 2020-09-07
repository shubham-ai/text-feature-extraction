import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_lg')

with open('news.txt', 'r', encoding='utf-8') as f:
    data = f.read()

features = data.split('. ')

text = nlp(features[16])

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

names = []
persons = []
organisations = []
events = []
references = []
dates = []
money = []
proper_nouns = []

for ent in text.ents:
    if ent.label_ == "MONEY" :
        money.append(ent.text)
    if ent.label_ == "DATE":
        dates.append(ent.text)
    if ent.label_ == "PERSON":
        persons.append(ent.text)
    if ent.label_ == "ORG" and ent.label_.lower() != 'rs':
        organisations.append(ent.text)

iterator = 0


print(text)

# for token in text:
#     print(token.text, token.pos_)

# for ent in text.ents:
#     print(ent.text, ent.label_)

for token in text:
    if iterator > 0:
        iterator -= 1
        continue

    if token.pos_ == "PROPN" and token.text.lower() not in months and token.text.lower() != "rs":
        proper_nouns.append(token.text)
        b = [i for i in dates if i.find(token.text) > -1]
        c = [i for i in money if i.find(token.text) > -1]
        if (len(b) == 0 and len(dates) != 0 or (len(c) == 0 and len(money) != 0)):
            try:
                if(text[token.i + 1].pos_ == "NOUN"):
                    if(text[token.i + 2].pos_ == "NOUN"):
                        word = token.text + " " + text[token.i + 1].text + " " + text[token.i + 2].text
                        references.append(word)
                        iterator = 2
                    else:
                        word = token.text + " " + text[token.i + 1].text
                        references.append(word)
                        iterator = 1
                else:
                    names.append(token.text)
            except:
                print("End of text")

        continue

    if token.pos_ == "NOUN" and token.text.lower() != "rs":
        try:
            if text[token.i+1].pos_ == "VERB":
                word = token.text + " " + text[token.i + 1].text
                references.append(word)
                iterator = 1
            else:
                references.append(token.text)
        except:
            print("End of text")


match = [{"POS":"PROPN"},
        {"POS":"ADP", "OP":"+"},
        {"POS":"PROPN", "OP":"?"},
        {"POS":"VERB", "OP":"?"}]

action = [{"POS":"VERB"},
            {"POS":"ADJ", "OP":"?"},
            {"POS":"ADP", "OP":"?"},
            {"POS":"DET", "OP":"?"},
            {"POS":"NOUN", "OP":"?"}]
        
money_lakh_pattern = [{"TEXT":"rs", "OP":"?"},
                {"POS":"NUM"}, 
                {"lower":"lakh"}]

money_crore_pattern = [{"lower":"rs", "OP":"?"},
                {"POS":"NUM"}, 
                {"lower":"crore"}]

money_lc_pattern = [{"lower":"rs", "OP":"?"},
                {"POS":"NUM"}, 
                {"lower":"lakh"},
                {"lower":"crore"}]

matcher = Matcher(nlp.vocab)
matcher.add("Context", None, match)
matcher.add("Action", None, action)
matcher.add("Lakh", None, money_lakh_pattern)
matcher.add("Crore", None, money_crore_pattern)
matches = matcher(text)

money_matcher = Matcher(nlp.vocab)
money_matcher.add("Lakh", None, money_lakh_pattern)
money_matcher.add("Crore", None, money_crore_pattern)
money_matcher.add("Lakh Crore", None, money_lc_pattern)
money_matches = money_matcher(text)

money_duplicates = [text[start:end] for _, start, end in money_matches]
money = spacy.util.filter_spans(money_duplicates)

remove_duplicates = [text[start:end] for _, start, end in matches]
span = spacy.util.filter_spans(remove_duplicates)


for i in span:
    events.append(i)

persons = list(dict.fromkeys(persons))
organisations = list(dict.fromkeys(organisations))
names= list(dict.fromkeys(names))
references = list(dict.fromkeys(references))
events = list(dict.fromkeys(events))
dates = list(dict.fromkeys(dates))
money = list(dict.fromkeys(money))

print("Persons : ", persons)
print("Organisations : ", organisations)
# print("Key names : ", names)
print("References : ", references)
print("Key actions : ", events)
print("Dates mentioned : ", dates)
print("Money : ", money)
