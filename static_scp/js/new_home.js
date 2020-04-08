function hey(){
  console.log('hey')
}

var current_track





  function initAudioPlayer() {
    var audio, playbtn, mutebtn, volumeslider, currentTimeText, durationTimeText, playlist_status, beats, current_track;
    var playlist = [];
    var titles = [];
    var images = [];
    var playlist_index = 0;

    // slider variables

    ////cover art stuff
    var backdrop = document.getElementById('second');

    // Set object references
    playbtn = document.getElementById("play-pause-btn");
    var nextbtn = document.getElementById('fwd-btn')
     var prevbtn = document.getElementById('back-btn')
    // mutebtn = document.getElementById('mutebtn');

    // volumeslider = document.getElementById('volumeslider');
    currentTimeText = document.getElementById('currentTimeText');
    durationTimeText = document.getElementById('durationTimeText');
    playlist_status = document.getElementById("playlist-status");
    beats = document.getElementsByClassName("beat-item")

    // Seek slder stuff
    var slider, rect, ting, seeking, seekslider, seekto;
    seekslider = document.getElementById("slider");
    cont = document.getElementById('slide-container')
    rect = cont.getBoundingClientRect()
    contLength = rect.right - rect.left


    //// Volume slider stuff
    var volSlider, slot, volrect, bing, volSeeking, volBar, volBtn;
    volBar = document.getElementById('volume-bar')
    volBtn = document.getElementById('volume-btn')
    volLevel = document.getElementById("volume-level");
    slot = document.getElementById('volume-slot')
    volrect = slot.getBoundingClientRect()
    slotLength = volrect.bottom - volrect.top
    console.log(slotLength)


    ///// Build playlist array
    Array.prototype.forEach.call(beats, function(beat){
      playlist.push(beat.getAttribute('beat'));
      titles.push(beat.getAttribute('title'));
      images.push(beat.getAttribute('backdrop'))
    })



    //////////////////// Audio object
    audio = new Audio();
    audio.crossOrigin = 'anonymous';
    audio.src = playlist[playlist_index];
    audio.loop = false;
    audio.play();
    current_track = titles[playlist_index];
    playlist_status.innerHTML = titles[playlist_index];

    // Add Event Handling
    playbtn.addEventListener("click", playPause);
    nextbtn.addEventListener("click", nextTrack);
    prevbtn.addEventListener("click", previousTrack);
    volBtn.addEventListener("click", toggleVolumeDisplay);
  //  mutebtn.addEventListener("click", mute);
   cont.addEventListener("mousedown", function(event){ seeking=true; seek(event); });
   cont.addEventListener("mousemove", function(event){ seek(event); });
   cont.addEventListener("mouseup", function() {seeking=false});
   cont.addEventListener("mouseleave", function() {seeking=false});
   slot.addEventListener("mousedown", function(event){ volSeeking=true; setVolume(event); });
   slot.addEventListener("mousemove", function(event){ setVolume(event); });
   slot.addEventListener("mouseup", function(event){ volSeeking=false});
   slot.addEventListener("mouseleave", function(event){ volSeeking=false});
   audio.addEventListener("timeupdate", function(){ seekTimeUpdate(); });
   audio.addEventListener("ended", function() { nextTrack(); });
    // Functions
    //
    function setBackdrop(index){
      if (images[index] != 'none'){
      backdrop.style.backgroundImage = "url('" + images[index] + "')";
    } else {
      backdrop.style.removeProperty('background-image')
    }
    }
    ///////////////////////////// Switch Track function
    function nextTrack(){
      if (playlist_index == (playlist.length -1)){
        playlist_index = 0;
      } else {
        playlist_index++;
      }
      current_track = titles[playlist_index];
      playlist_status.innerHTML = titles[playlist_index];
      audio.src = playlist[playlist_index];
      setBackdrop(playlist_index);
      audio.play();
    }

    function previousTrack(){
      if (playlist_index == 0) {
        playlist_index = 0;
      } else {
        playlist_index--;
      }
      current_track = titles[playlist_index];
      playlist_status.innerHTML = titles[playlist_index];
      audio.src = playlist[playlist_index];
      setBackdrop(playlist_index);
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
        var beat = btn.getAttribute('beat');
        playlist_index = playlist.indexOf(beat);
        current_track = titles[playlist_index];
        playlist_status.innerHTML = titles[playlist_index];
        audio.src = beat;
        setBackdrop(playlist_index);
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
    function setVolume(event) {
      if (volSeeking){
        volrect = slot.getBoundingClientRect()
        slotLength = volrect.bottom - volrect.top
        console.log(slotLength)
        console.log('volume time')
        ting = event.clientY;
        yLength = volrect.bottom - ting
        yPercent = yLength / slotLength * 100
        console.log(ting);
        audio.volume = yPercent / 100;
        volLevel.style.height = (100 - yPercent).toString() + '%';
    }
    }

    function toggleVolumeDisplay(){
      if (volBar.style.display != 'block'){
        volBar.style.display = 'block';
        volBtn.style.color = 'orange';
      }
      else {
        volBar.style.display = 'none';
        volBtn.style.color = 'white';
      }
    }
    // //////////////////////////////////////////////////// Seek time update function
    function seekTimeUpdate(){
      var nt = audio.currentTime * (100 / audio.duration);
      seekslider.style.width = nt.toString() + '%';
      var curmins = Math.floor(audio.currentTime / 60);
      var cursecs = Math.floor(audio.currentTime - curmins * 60);
      var durmins = Math.floor(audio.duration / 60);
  	  var dursecs = Math.floor(audio.duration - durmins * 60);
  		if(cursecs < 10){ cursecs = "0"+cursecs; }
  	  if(dursecs < 10){ dursecs = "0"+dursecs; }
  	  if(curmins < 10){ curmins = "0"+curmins; }
  	  if(durmins < 10){ durmins = "0"+durmins; }
  		currentTimeText.innerHTML = curmins+":"+cursecs;
  	  durationTimeText.innerHTML = durmins+":"+dursecs;
    }

    function initMp3Player(){
      // console.log('squuuiiirrf')
      context = new AudioContext(); // AudioContext object instance  Look up how this works in chrome https://goo.gl/7K7WLu
      analyser = context.createAnalyser(); // AnalyserNode method
      canvas = document.getElementById('visualiser');
      ctx = canvas.getContext('2d');
      dpi = window.devicePixelRatio;



      // Re-route audio playback into the processing graph of the AudioContext
      source = context.createMediaElementSource(audio);
      source.connect(analyser);
      analyser.connect(context.destination);
      frameLooper();
      console.log('grrrrr')
    }

    function fix_dpi() {
      //get CSS height
      //the + prefix casts it to an integer
      //the slice method gets rid of "px"
      let style_height = +getComputedStyle(canvas).getPropertyValue("height").slice(0, -2);

      //get CSS width
      let style_width = +getComputedStyle(canvas).getPropertyValue("width").slice(0, -2);
      //scale the canvas
      canvas.setAttribute('height', style_height * dpi);
      canvas.setAttribute('width', style_width * dpi);
    }

    function frameLooper(){

      window.requestAnimationFrame(frameLooper);
      fbc_array = new Uint8Array(analyser.frequencyBinCount);
      analyser.getByteFrequencyData(fbc_array);
      fix_dpi();
      ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
      ctx.globalCompositeOperation = "source-over";
      ctx.fillStyle = 'rgba(255,255,255,0.25)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.globalCompositeOperation = 'destination-out'
      ctx.fillStyle = 'red'; // Color of the bars
      bars = 400;
      ctx.font = "800 6em Open Sans";
      ctx.fillStyle = "red";
      ctx.textAlign = "center";

      ctx.fillText(current_track.toUpperCase(), canvas.width/2, canvas.height/2);
      for (var i = 0; i < bars; i++) {
        bar_x = i * 3;
        bar_width = 8;
        bar_height = -(fbc_array[i]);
        //  fillRect( x, y, width, height ) // Explanation of the parameters below
        ctx.fillRect(bar_x, canvas.height, bar_width, bar_height);

        // console.log('wooop')
      }
    }

    initMp3Player();

  }





window.addEventListener("load", () => {
  hey();
  initAudioPlayer();
  cartStuff();








})





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
