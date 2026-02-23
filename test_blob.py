from textblob import TextBlob

blob = TextBlob("I havv a very guud interestin idea")

corrected_blob = blob.correct()

print(blob)

print(corrected_blob)