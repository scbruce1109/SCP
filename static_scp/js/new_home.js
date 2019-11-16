function hey(){
  console.log('hey')
}






  function initAudioPlayer() {
    var audio, playbtn, mutebtn, volumeslider, currentTimeText, durationTimeText, playlist_status, beats;
    var playlist = [];
    var titles = [];
    var playlist_index = 0;

    // slider variables


    // Set object references
    playbtn = document.getElementById("play-pause-btn");
    var nextbtn = document.getElementById('fwd-btn')
     var prevbtn = document.getElementById('back-btn')
    // mutebtn = document.getElementById('mutebtn');

    // volumeslider = document.getElementById('volumeslider');
    // currentTimeText = document.getElementById('currentTimeText');
    // durationTimeText = document.getElementById('durationTimeText');
    playlist_status = document.getElementById("playlist-status");
    beats = document.getElementsByClassName("beat-item")

    // Seek slder stuff
    var slider, rect, ting, seeking, seekslider, seekto;
    seekslider = document.getElementById("slider");
    cont = document.getElementById('slide-container')
    rect = cont.getBoundingClientRect()
    contLength = rect.right - rect.left


    ///// Build playlist array
    Array.prototype.forEach.call(beats, function(beat){
      playlist.push(beat.getAttribute('beat'));
      titles.push(beat.getAttribute('title'));
    })



    //////////////////// Audio object
    audio = new Audio();
    audio.src = playlist[playlist_index];
    audio.loop = false;
    audio.play();
    playlist_status.innerHTML = titles[playlist_index];

    // Add Event Handling
    playbtn.addEventListener("click", playPause);
    nextbtn.addEventListener("click", nextTrack);
    prevbtn.addEventListener("click", previousTrack);
  //  mutebtn.addEventListener("click", mute);
   cont.addEventListener("mousedown", function(event){ seeking=true; seek(event); });
   cont.addEventListener("mousemove", function(event){ seek(event); });
   cont.addEventListener("mouseup", function() {seeking=false});
  //  volumeslider.addEventListener("mousemove", setVolume);
   audio.addEventListener("timeupdate", function(){ seekTimeUpdate(); });
   audio.addEventListener("ended", function() { nextTrack(); });
    // Functions
    //
    ///////////////////////////// Switch Track function
    function nextTrack(){
      if (playlist_index == (playlist.length -1)){
        playlist_index = 0;
      } else {
        playlist_index++;
      }
      playlist_status.innerHTML = titles[playlist_index];
      audio.src = playlist[playlist_index];
      audio.play();
    }

    function previousTrack(){
      if (playlist_index == 0) {
        playlist_index = 0;
      } else {
        playlist_index--;
      }
      playlist_status.innerHTML = titles[playlist_index];
      audio.src = playlist[playlist_index];
      audio.play();
    }

    //////////////////////////////////////////////// Play / Pause function


    function playPause() {
      if (audio.paused) {
        audio.play();
        console.log('agghgh')
      } else {
        audio.pause();
        console.log('blurrp')
      }
    }

    var trackBtnArray = document.getElementsByClassName("play-track-btn")

    Array.prototype.forEach.call(trackBtnArray, function(btn) {
    btn.addEventListener("click", function() {
        audio.src = btn.getAttribute('beat');
        audio.play();
    });
});

    // function mute() {
    //   if (audio.muted) {
    //     audio.muted = false;
    //   } else {
    //     audio.muted = true;
    //   }
    // }
    // /////////////////////////////////////////// Seek Function
    function seek(event) {
      if (seeking){

        ting = event.clientX;
        xLength = ting - rect.left
        xPercent = xLength / contLength * 100
        seekto = audio.duration * (xPercent / 100);
        console.log(seekto, audio.currentTime);
        audio.currentTime = seekto;
        console.log(seekto, audio.currentTime);
        seekslider.style.width = xPercent.toString() + '%';
      }
    }
    // //////////////////////////////////////////// Volume adjust function
    //
    // function setVolume() {
    //   audio.volume = volumeslider.value / 100;
    // }
    // //////////////////////////////////////////////////// Seek time update function
    function seekTimeUpdate(){
      var nt = audio.currentTime * (100 / audio.duration);
      seekslider.style.width = nt.toString() + '%';
    //   var curmins = Math.floor(audio.currentTime / 60);
    //   var cursecs = Math.floor(audio.currentTime - curmins * 60);
    //   var durmins = Math.floor(audio.duration / 60);
  	//   var dursecs = Math.floor(audio.duration - durmins * 60);
  	// 	if(cursecs < 10){ cursecs = "0"+cursecs; }
  	//   if(dursecs < 10){ dursecs = "0"+dursecs; }
  	//   if(curmins < 10){ curmins = "0"+curmins; }
  	//   if(durmins < 10){ durmins = "0"+durmins; }
  	// 	currentTimeText.innerHTML = curmins+":"+cursecs;
  	//   durationTimeText.innerHTML = durmins+":"+dursecs;
    }

    function initMp3Player(){
      // console.log('squuuiiirrf')
      context = new AudioContext(); // AudioContext object instance  Look up how this works in chrome https://goo.gl/7K7WLu
      analyser = context.createAnalyser(); // AnalyserNode method
      canvas = document.getElementById('visualiser');
      ctx = canvas.getContext('2d');
      // Re-route audio playback into the processing graph of the AudioContext
      source = context.createMediaElementSource(audio);
      source.connect(analyser);
      analyser.connect(context.destination);
      frameLooper();
      console.log('grrrrr')
    }

    initMp3Player();

  }





window.addEventListener("load", () => {
  hey();
  initAudioPlayer();
  cartStuff();








})


function frameLooper(){
  window.requestAnimationFrame(frameLooper);
  fbc_array = new Uint8Array(analyser.frequencyBinCount);
  analyser.getByteFrequencyData(fbc_array);
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
  ctx.fillStyle = 'red'; // Color of the bars
  bars = 100;
  for (var i = 0; i < bars; i++) {
    bar_x = i * 3;
    bar_width = 2;
    bar_height = -(fbc_array[i] / 2);
    //  fillRect( x, y, width, height ) // Explanation of the parameters below
    ctx.fillRect(bar_x, canvas.height, bar_width, bar_height);
    // console.log('wooop')
  }
}


// Cart stuff
function cartStuff() {
console.log('spewww');
var cartBtnArray = document.getElementsByClassName("beat-modal-btn");
console.log(cartBtnArray);
var modal = document.getElementById("product-modal");
var span = document.getElementById("close");

Array.prototype.forEach.call(cartBtnArray, function(btn) {
btn.addEventListener("click", function() {
    // audio.src = btn.getAttribute('beat');
    var stdInput = document.getElementById('standard').getElementsByClassName('product-form-input')[0]
    var trackoutInput = document.getElementById('trackout').getElementsByClassName('product-form-input')[0]
    var premiumInput = document.getElementById('premium').getElementsByClassName('product-form-input')[0]
    stdInput.setAttribute('value', btn.getAttribute('standard'));
    trackoutInput.setAttribute('value', btn.getAttribute('trackout'));
    premiumInput.setAttribute('value', btn.getAttribute('unlimited'));
    modal.style.display = "block";
});
});

span.onclick = function() {
  modal.style.display = "none";
}
}
