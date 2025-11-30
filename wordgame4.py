import random
from collections import Counter

with open("static/words-huge") as wf:
    words = {line.strip("\n").replace("'s", "").lower() for line in wf}  # A set.
words = sorted(words)[1:]  # Ignore the empty word at the start of the list.

sourcewords = [w for w in words if len(w) >= 8]

def pick_sourceword():
    # return random.choice(sourcewords)
    return "overthrowers"

def is_valid(sourceword, ans):
    answers = ans.lower().split(" ")  # lowercase to ignore case
    reasons = []
    # seven 4-or-more letter words
    if len(answers) != 7:
        reasons.append("not seven words")

    # The words all have four letters or more
    for answer in answers:
        if len(answer) < 4:
            reasons.append(answer + " is less than 4 characters long")

    # Each word exists within the dictionary (i.e., it's a “real” word).
    for answer in answers:
        if answer not in words:
            reasons.append(answer + " is not a real word")

    for answer in answers:
        # Each word is only made up from the letters contained within the sourceword.
        # You haven't reused any letter more times that it appears in the sourceword.
        if Counter(answer) > Counter(sourceword):
            reasons.append(answer + " uses letters not in the sourceword or uses too many letters")

    # There are no duplicate words
    for answer in answers:
        if answers.count(answer) > 1:
            reasons.append(answer + " is duplicated")

    # None of the seven words is the source word
    for answer in answers:
        if answer == sourceword:
            reasons.append(answer + " is the source word")

    return reasons
