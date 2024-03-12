let express=require("express");
let app=express();
const { spawn } = require('child_process');
let port=8080;
let path=require('path');
app.set("view engine","ejs");
app.set(path.join(__dirname,"views"));
app.use(express.static(path.join(__dirname,"/public/css")));
app.use(express.static(path.join(__dirname,"/public/js")))
app.use(express.json());
app.use(express.urlencoded({extended:true}));
app.listen(port,()=>{console.log("Port is listening");});
app.get("/form",(req,res)=>{
    res.render("eu.ejs");
})
app.post("/detect", (req, res) => {
    try {
        const { url } = req.body;

        // Run Python script as a child process
        const pythonProcess = spawn('python', ['C:/Users/Admin/Desktop/urldetectionml/app.py', url]);

        // Handle stdout from the Python process
        pythonProcess.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
            res.send(data); // Send data back to client
        });

        // Handle stderr from the Python process
        pythonProcess.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
            res.status(500).send("Error occurred while running Python script");
        });
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send("Internal Server Error");
    }
})