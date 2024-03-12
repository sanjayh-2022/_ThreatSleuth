# app.py
def classify_url(url):
    # Process or classify the URL here
    return {'received_url': url}

if __name__ == '__main__':
    import sys
    import json
    url = sys.argv[1] if len(sys.argv) > 1 else ''
    result = classify_url(url)
    print(json.dumps(result))
