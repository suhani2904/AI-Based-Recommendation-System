import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    
    if not isinstance(text, str):
        return ""
    
    # lowercase
    text = text.lower()
    
    # remove unwanted characters but keep + # .
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)
    
    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    
    # tokenization
    tokens = word_tokenize(text)
    
    # remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    
    # lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # join back
    return " ".join(tokens)