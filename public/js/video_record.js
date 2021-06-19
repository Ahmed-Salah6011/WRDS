const socket = io();
const start_button = document.querySelector("#btn-start-recording");
const myVideo = document.querySelector("#my-preview");
const recordedVideo = document.querySelector("#recorded-preview");
const state_text = document.querySelector("#state");
const timer_container = document.querySelector("#timer");
const next_step_button = document.querySelector("#next-step-btn");

const state1_refused =
    "Video Refused, Please Record The Video While You Are Smiling Again!",
  state2_request = "Please Record a Video While You Are NOT Smiling",
  state2_refused =
    "Video Refused, Please Record The Video While You Are NOT Smiling Again!",
  state3_request = "Please Record a Video While You Are Blinking (5 To 10 Times)",
  state3_refused =
    "Video Refused, Please Record the Video While You Are Blinking (5 To 10 Times) Again!",
  welldone_message = "Please Proceed To The Next Step";
// const recorded_video = document.querySelector("recorded_video");
let state = 1;
navigator.mediaDevices
  .getUserMedia({
    video: true,
    audio: false,
  })
  .then(async function (stream) {
    let recorder = RecordRTC(stream, {
      MimeType: "video/MKV",
      type: "video",
    });
    myVideo.srcObject = stream;
    myVideo.play();
    var stop_record = () => {
      recorder.stopRecording(function () {
        let blob = recorder.getBlob();
        // sending the video to the backend
        socket.emit("blob", {
          blobData: blob,
          video_state: state,
        });
        timer_container.innerText = "Loading...";
      });
    };
    ////////////////////////
    socket.on("state", (data) => {
      start_button.disabled = false;
      if (data == "accepted") {
        if (state == 1) {
          state_text.innerText = state2_request;
          alert(state2_request);
        } else if (state == 2) {
          state_text.innerText = state3_request;
          alert(state3_request);
        }
        state++;
        if (state == 4) {
          start_button.disabled = true;
          state_text.innerText = welldone_message;
          alert(welldone_message);
          next_step_button.disabled = false;
        }
      } else if (data == "error") {
        alert(
          "Your Face Must Be Visible During The Record, Only One Face Should Be Visible"
        );
      } else {
        if (state == 1) {
          state_text.innerText = state1_refused;
          alert(state1_refused);
        } else if (state == 2) {
          state_text.innerText = state2_refused;
          alert(state2_refused);
        } else if (state == 3) {
          state_text.innerText = state3_refused;
          alert(state3_refused);
        }
      }
      timer_container.innerText = "Not Recording";
      console.log(data);
    });
    ///////////////////////
    start_button.addEventListener("click", () => {
      start_button.disabled = true;
      recorder.startRecording();
      start_timer(8);
      setTimeout(stop_record, 8000);
    });
  });
function start_timer(i) {
  let time = i;
  let timer = `Record Ends In: 00:${time}`;
  timer_container.innerText = timer;
  let count = () => {
    time--;
    timer = `Record Ends In: 00:${time}`;
    timer_container.innerText = timer;
    console.log(time);
    if (time == 0) {
      clearInterval(counter_interval);
      timer = `Not Recording`;
      timer_container.innerText = timer;
    }
  };
  let counter_interval = setInterval(count, 1000);
}
next_step_button.addEventListener("click", () => {
  timer_container.innerText = "Comparing Your Face With The Face In Your ID...";
});
