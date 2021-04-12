let width = 320;
let height = 0;

let streaming = false;
let video = null;
let canvas = null;
let startbutton = null;
let photo = null;

let input_to_fill = null;

$( document ).ready(function() {
    startup()
    $("#capturebarcode").hide();
    $(".snap").click(function(){
        input_to_fill = $(this).prev("input");
        $("#capturebarcode").show();
    })

    $("#startbutton").click(read_barcode);

});

function read_barcode() {
    $("#capturebarcode").hide();

    let data = new FormData();

    data.append('image',$("#photo").attr("src"));

    $.ajax({
        type: "POST",
        url: "/BarcodeReader",
        contentType: false,
        processData: false,
        data: data,
        success: function(result) {
            write_barcode(result)
        }
    });
    
}


function write_barcode(code) {
    input_to_fill.val(code);
    input_to_fill = null;
}

function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');

    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function(stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function(err) {
        console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev){
        if (!streaming) {
          height = video.videoHeight / (video.videoWidth/width);
  
          video.setAttribute('width', width);
          video.setAttribute('height', height);
          canvas.setAttribute('width', width);
          canvas.setAttribute('height', height);
          streaming = true;
        }
      }, false);

    startbutton.addEventListener('click', function(ev){
    takepicture();
    ev.preventDefault();
    }, false);

    clearphoto();
}


function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
}

function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        var data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);
    } else {
        clearphoto();
    }
}

