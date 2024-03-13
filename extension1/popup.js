chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    // Get the URL of the active tab
    const tabUrl = tabs[0].url;
    
    // Print the URL in the console
    console.log("URL of the active tab:", tabUrl);
    // Define the URL of your Node.js server endpoint
const url = `http://localhost:8080/endpoint/${encodeURIComponent(tabUrl)}`; // Replace with your server endpoint
console.log(url);

// Send a GET request to the server
fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Assuming the server returns JSON data
    })
    .then(data => {
        console.log('Response from server:', data);
        console.log(data.message);
        let lt=document.querySelector(".loading-paragraph");
        lt.innerHTML=data.message;
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
    });

});
