import random
from collections import Counter

with open("static/words-huge") as wf:
    words = {line.strip("\n").replace("'s", "").lower() for line in wf}  # A set.
words = sorted(words)[1:]  # Ignore the empty word at the start of the list.

sourcewords = [w for w in words if len(w) >= 8]

def pick_sourceword():
    return random.choice(sourcewords)

def is_valid(sourceword, ans):
    # lowercase to ignore case
    # strip to remove extra punctuation/user errors
    # nested list comprehension because we want to sanitise before testing
    # only include answers that aren't empty strings or just spaces
    # https://stackoverflow.com/a/4071407
    answers = [a for a in [x.strip(",.").lower() for x in ans.split(" ")] if a and not a.isspace()]
    reasons = []
    # seven 4-or-more letter words
    if len(answers) != 7:
        reasons.append(f"only {len(answers)} words, not 7 words")

    # The words all have four letters or more
    for answer in answers:
        if len(answer) < 4:
            reasons.append(f"{answer} is less than 4 letters long")

    # Each word exists within the dictionary (i.e., it's a “real” word).
    for answer in answers:
        if answer not in words:
            reasons.append(f"{answer} is not a real word")

    for answer in answers:
        # Each word is only made up from the letters contained within the sourceword.
        # You haven't reused any letter more times that it appears in the sourceword.
        if c:= Counter(answer) - Counter(sourceword):
            reasons.append(f"{answer} uses these invalid letters: {", ".join(list(c))}")

    # There are no duplicate words
    for answer in answers:
        if answers.count(answer) > 1:
            reasons.append(f"{answer} is duplicated")

    # None of the seven words is the source word
    for answer in answers:
        if answer == sourceword:
            reasons.append(f"{answer} is the source word")

    return list(set(reasons))
