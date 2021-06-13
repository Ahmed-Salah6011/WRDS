const express = require("express");
const http = require("http");
const app = express();
const fs = require("fs");
const multer = require("multer");
const FileReader = require("filereader");
const { spawn } = require("child_process");
const path = require("path");
const socketio = require("socket.io");
const server = http.createServer(app);
const io = socketio(server);

app.use(express.static("uploads"));
app.use(express.static("public"));
app.set("view engine", "ejs");
const port = 4000;
let baseDir = path.join(__dirname, "videos", "test.MKV");

const upload = multer({
  dest: path.join(__dirname, "uploads"),
  // you might also want to set some limits: https://github.com/expressjs/multer#limits
});

app.get("/", (req, res) => {
  res.render("upload_photo");
});

app.post("/upload", upload.single("img"), (req, res) => {
  const tempPath = req.file.path;
  const targetPath = path.join(__dirname, "./uploads/image.jpg");
  fs.rename(tempPath, targetPath, (err) => {
    if (err) console.log(err);
    res.render("test");
  });
});
server.listen(port, () => {
  console.log("listening on http://localhost:4000/");
});
io.on("connection", (socket) => {
  socket.on("blob", (data) => {
    let blob = data.blobData;
    //A Blob() is almost a File() - it's just missing the two properties below which we will add
    blob.lastModifiedDate = new Date();
    blob.name = "test.webm";
    console.log(blob);
    var reader = new FileReader();
    reader.onload = function () {
      var buffer = new Buffer(reader.result);
      fs.writeFile(baseDir, buffer, {}, (err, res) => {
        if (err) {
          console.error(err);
          return;
        }
        console.log("video saved");
        const python = spawn("python", ["main_anti.py", data.video_state]);
        python.stdout.on("data", (data) => {
          dataFromPython = data.toString();
          console.log(dataFromPython);
          if (dataFromPython.trim() === "1") socket.emit("state", "accepted");
          else socket.emit("state", "refused");
        });
      });
    };
    reader.readAsArrayBuffer(blob);
  });
});
