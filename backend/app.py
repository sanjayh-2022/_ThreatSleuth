import pandas as pd
import numpy as np
from tld import get_tld
from urllib.parse import urlparse
import re
import joblib 
import sys
import json

RF_spamURL_classifier = open('RF_malaciousURL.pkl','rb')
model = joblib.load(RF_spamURL_classifier)

def process_input(text):
    df={'url':[text]}
    data=pd.DataFrame(df,columns=['url','url_len','https','http','tld','tld_len','hostname_len','@','?','-','=','.','#','%','+','$','!','*',',','//','digits','letters','short_url','ip_address'])
    data['url_len'] = data['url'].apply(lambda x: len(str(x)))
    data['https'] = data['url'].apply(lambda i : i.count('https'))
    data['http'] = (data['url'].replace('https', '', regex=True)).apply(lambda i : i.count('http'))
    data['tld'] = data['url'].apply(lambda i: get_tld(i,fail_silently=True))
    def tld_length(tld):
        try:
            return len(tld)
        except:
            return 0
    data['tld_len'] = data['tld'].apply(lambda i: tld_length(i))
    data['hostname_len'] = data['url'].apply(lambda i: len(urlparse(i).netloc))
    feature = ['@','?','-','=','.','#','%','+','$','!','*',',','//']
    data = data.drop(["tld"],axis=1)
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

    def short_url(url):
        match = re.search(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                        r'tr\.im|link\.zip\.net',
                        url)
        if match:
            return 1
        else:
            return 0
    data['short_url'] = data['url'].apply(lambda x: short_url(x))
    def ip_address(url):
        match = re.search(
            r'(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            r'([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            r'(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            r'([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
            r'((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
            r'(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
            r'([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
            r'((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
        if match:
            return 1
        else:
            return 0
    data['ip_address'] = data['url'].apply(lambda i: ip_address(i))
    data=data.drop(['url'],axis=1)
    return data

def classify_url(url):
    data=process_input(url)
    pred=model.predict(data)
    return pred

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else ''
    result = classify_url(url)
    res=result.tolist()
    print(json.dumps(res))