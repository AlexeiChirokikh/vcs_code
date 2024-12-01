from textblob import TextBlob

blob = TextBlob("I havv a guud idea")

corrected_blob = blob.correct()

print(blob)

print(corrected_blob)