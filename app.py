import joblib
import pandas as pd
from tld import get_tld
from urllib.parse import urlparse
import re
import sys
from flask import Flask, request

app = Flask(__name__)

RF_spamURL_classifier = 'RF_spamURL_classifier.pkl'
model = joblib.load(RF_spamURL_classifier)

def process_input(text):
    df={'url':[text]}
    data=pd.DataFrame(df,columns=['url','url_len','http','tld','tld_len','hostname_len','@','?','-','=','.','#','%','+','$','!','*',',','//','digits','letters','abnormal_url','short_url','ip_address'])
    data['url_len'] = data['url'].apply(lambda x: len(str(x)))
    data['http'] = data['url'].apply(lambda i : i.count('http'))
    data['tld'] = data['url'].apply(lambda i: get_tld(i,fail_silently=True))
    def tld_length(tld):
        try:
            return len(tld)
        except:
            return 0
    data['tld_len'] = data['tld'].apply(lambda i: tld_length(i))
    data['hostname_len'] = data['url'].apply(lambda i: len(urlparse(i).netloc))
    feature = ['@','?','-','=','.','#','%','+','$','!','*',',','//']
    data = data.drop("tld",1)
    for a in feature:
        data[a] = data['url'].apply(lambda i: i.count(a))
    def digit_count(url):
        digits = 0
        for i in url:
            if i.isnumeric():
                digits = digits + 1
        return digits
    data['digits']= data['url'].apply(lambda i: digit_count(i))

    def letter_count(url):
        letters = 0
        for i in url:
            if i.isalpha():
                letters = letters + 1
        return letters
    data['letters']= data['url'].apply(lambda i: letter_count(i))

    def abnormal_url(url):
        hostname = urlparse(url).hostname
        hostname = str(hostname)
        match = re.search(hostname, url)
        if match:
            return 1 
        else:
            return 0
    data['abnormal_url'] = data['url'].apply(lambda i: abnormal_url(i))    
    def short_url(url):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                        'tr\.im|link\.zip\.net',
                        url)
        if match:
            return 1
        else:
            return 0
    data['short_url'] = data['url'].apply(lambda x: short_url(x))    
    def ip_address(url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
            '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
            '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
        if match:
            return 1
        else:
            return 0
    data['ip_address'] = data['url'].apply(lambda i: ip_address(i))    
    return data

def predict_url(url):
    data=process_input(url)
    prediction=model.predict(data)
    return prediction[0]

@app.route('/detect', methods=['POST'])
def classify_url():
    url = request.json['url']
    prediction = predict_url(url)
    return {'prediction': prediction}

if __name__ == '__main__':
    app.run(debug=True)
