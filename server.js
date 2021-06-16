const express = require("express");
const http = require("http");
const app = express();
const fs = require("fs");
const multer = require("multer");
const FileReader = require("filereader");
const { spawn } = require("child_process");
const path = require("path");
const bodyparser = require("body-parser");
const socketio = require("socket.io");
const server = http.createServer(app);
const io = socketio(server);
///////////////////////////////////////
app.use(express.static("uploads"));
app.use(express.static("public"));
app.use(bodyparser.urlencoded({ extended: true }));
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

var check_for_id = (id) => {
  let raw_data;
  try {
    raw_data = fs.readFileSync("db.json", (encoding = "utf-8"));
  } catch {
    return "not found";
  }
  console.log(raw_data);
  let db_data = JSON.parse(raw_data);
  for (let index = 0; index < db_data.table.length; index++) {
    if (db_data.table[index].id == id) return db_data.table[index];
  }
  return "not found";
};

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
  let raw_id = fs.readFileSync("ID.json", (encoding = "utf-8"));
  let raw_cert = fs.readFileSync("CERT.json", (encoding = "utf-8"));
  let id_data = JSON.parse(raw_id);
  let cert_data = JSON.parse(raw_cert);
  res.render("ocr", { cert: cert_data, id: id_data });
});

app.get("/video", (req, res) => {
  res.render("video_record");
});
////////////////////////////////////
// app.post("/upload", upload.single("img"), (req, res) => {
//   const tempPath = req.file.path;
//   const targetPath = path.join(__dirname, "./uploads/image.jpg");
//   fs.rename(tempPath, targetPath, (err) => {
//     if (err) console.log(err);
//     res.render("video_record");
//   });
// });

app.post("/show_data", (req, res) => {
  let test = check_for_id(req.body.id);
  if (test == "not found") {
    res.send("id not found");
  } else {
    res.render("show_data", { data: test });
  }
});

app.post("/ocr", (req, res) => {
  fs.readFile("db.json", "utf8", function readFileCallback(err, data) {
    var obj;
    let test = check_for_id(req.body.id);
    if (test == "not found") {
      if (err) {
        obj = {
          table: [],
        };
        console.log(req.body);
        obj.table.push(req.body);
        let json = JSON.stringify(obj); //convert it to json
        fs.writeFile("db.json", json, "utf8", () => {
          res.send("done");
        }); // write it
      } else {
        obj = JSON.parse(data); //now it an object
        obj.table.push(req.body); //add some data
        let json = JSON.stringify(obj); //convert it back to json
        fs.writeFile("db.json", json, "utf8", () => {
          res.send("done");
        }); // write it back
      }
    } else {
      res.render("show_data", { data: test });
    }
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
