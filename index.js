let express = require('express')
let app = express()
const { spawn } = require('child_process')
let port = 8080
let path = require('path')
app.set('view engine', 'ejs')
app.set(path.join(__dirname, 'views'))
app.use(express.static(path.join(__dirname, '/public/css')))
app.use(express.static(path.join(__dirname, '/public/js')))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.listen(port, () => {
  console.log('Port is listening')
})
app.get('/form', (req, res) => {
  res.render('eu.ejs')
})
app.post('/detect', (req, res) => {
  try {
    const { url } = req.body

    // Run Python script as a child process
    const pythonProcess = spawn('python', ['app.py', url])

    let result = ''
    // Handle stdout from the Python process
    pythonProcess.stdout.on('data', (data) => {
      result += data.toString()
    })

    // Handle stderr from the Python process
    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`)
      res.status(500).send('Error occurred while running Python script')
    })

    // When the Python process exits
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        res.send(result)
      } else {
        res.status(500).send('Python script exited with an error')
      }
    })
  } catch (error) {
    console.error('Error:', error)
    res.status(500).send('Internal Server Error')
  }
})
