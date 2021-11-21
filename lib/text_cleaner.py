import re

def remove_hashtags(text):
    regex = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)" # hash-tags
    text = re.sub(regex, ' ', text)
    return text

def remove_mentions(text):
    regex = r'@[^\s]+' #remove @-mentions
    text = re.sub(regex, ' ', text)
    return text

def remove_urls(text):
    regex = r'http\S+' #remove url
    text = re.sub(regex, ' ', text)
    return text

def remove_special_characters(text):
    #text_filtered = []
    # for segment in text_splitted:
    #     if len(segment < 20):
    #         continue
    #     text_filtered.append(segment)
    # text = "\n".join(text_filtered)
    text = text.replace("\t", " ") #.replace("\n", " ").replace("\r", " ")
    text = re.sub(' +', ' ', text)
    return text

def clean_text(raw_text):

    text = remove_urls(raw_text)
    text = remove_mentions(raw_text)
    text = remove_hashtags(raw_text)
    text = remove_special_characters(raw_text)

    return text
