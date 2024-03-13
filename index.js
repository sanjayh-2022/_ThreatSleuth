// Example using Express.js
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 8080;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const cors = require('cors');
app.use(cors());

// Updated route handler to handle GET requests and retrieve parameters from the URL path
app.get('/endpoint/:id', (req, res) => {
    const receivedUrl= req.params.id; // Retrieve the parameter from the URL path
    console.log('Received URL:', receivedUrl);

    // Process the URL here

    // Send a response back to the extension if needed
    res.json({ message: `${receivedUrl}` });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
