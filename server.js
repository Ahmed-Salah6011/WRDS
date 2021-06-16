const express = require("express");
const http = require("http");
const app = express();
const fs = require("fs");
const multer = require("multer");
const FileReader = require("filereader");
const { spawn } = require("child_process");
const path = require("path");
const socketio = require("socket.io");
const { parse } = require("path");
const server = http.createServer(app);
const io = socketio(server);
///////////////////////////////////////
app.use(express.static("uploads"));
app.use(express.static("public"));
app.set("view engine", "ejs");
const port = 4000;
let baseDir = path.join(__dirname, "videos", "test.MKV");
/////////////////////////////////////////
var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, "uploads"));
  },
  filename: function (req, file, cb) {
    cb(null, file.fieldname + ".jpg");
  },
});
const upload = multer({
  dest: path.join(__dirname, "uploads"),
  storage: storage,
  // you might also want to set some limits: https://github.com/expressjs/multer#limits
});
///////////////////////////////////////
app.get("/", (req, res) => {
  res.render("index");
});
app.get("/uploadfile", (req, res) => {
  res.render("upload_photo");
});
var uploadMultiple = upload.fields([
  { name: "ID_front", maxCount: 10 },
  { name: "ID_back", maxCount: 10 },
  { name: "cert", maxCount: 10 },
]);

app.post("/uploadfile", uploadMultiple, function (req, res, next) {
  if (req.files) {
    console.log(req.files);
    console.log("files uploaded");
  }
  const python = spawn("python", ["ocr/ocr.py"]);
  python.stdout.on("data", (data) => {
    dataFromPython = data.toString();
    console.log(dataFromPython);
  });
  res.redirect("/video");
});

app.get("/ocr", (req, res) => {
  let raw_id = fs.readFileSync("ID.json",encoding="utf-8");
  let raw_cert = fs.readFileSync("CERT.json",encoding="utf-8");
  let id_data = parse(raw_id);
  let cert_data = parse(raw_cert);
   console.log(id_data)
   console.log(cert_data)
  res.render("ocr", { 'cert': cert_data,'id':id_data });
   
});

app.get("/video", (req, res) => {
  res.render("video_record");
});
////////////////////////////////////
app.post("/upload", upload.single("img"), (req, res) => {
  const tempPath = req.file.path;
  const targetPath = path.join(__dirname, "./uploads/image.jpg");
  fs.rename(tempPath, targetPath, (err) => {
    if (err) console.log(err);
    res.render("video_record");
  });
});
//////////////////////////////////
server.listen(port, () => {
  console.log("listening on http://localhost:4000/");
});
///////////////////////////////////
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
