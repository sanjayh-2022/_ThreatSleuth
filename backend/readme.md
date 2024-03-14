<h1> AI-powered malicious/phishing URL detector</h1>
<h4>**It's a Chrome extension that detects phishing URLs when they are clicked on.**</h4>
<h5>Here is the step-by-step procedure of how the extension works: </h5>
<list><ol>1. When you click on the extension, the JavaScript file collects the URL of the current Chrome tab and sends a request to the backend server.</ol>
<ol>2. The backend server retrieves the URL and runs the Python file by sending that URL to the `app.py` Python file.</ol>
<ol>3. The Python file processes the URL based on the trained ML model and sends a safe or alert message to the server.</ol>
<ol>4. The server sends a response to the JavaScript file in the extension and prints whether the URL is safe or not.</ol></list><br>
<img src="./Screenshot (2504).png"><br><img src="./Screenshot (2502).png"><br><img src="./Screenshot (2503).png">
