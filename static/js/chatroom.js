$(document).ready(function() {
  // $('#text').keypress(function(e) {
  //     var code = e.keyCode || e.which;
  //     if (code == 13) {
  //         text = $('#text').val();
  //         $('#userText').val($('#userText').val()+text+'\n');
  //         $('#otherText').val($('#otherText').val()+text+'\n');
  //         $('#text').val('');
  //     }
  // });

  var socket = io.connect('https://' + document.domain + '/chat')
  socket.on('connect', function() {
    socket.emit('join', {});
  });

  $('#text').keypress(function(e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      text = $('#text').val();
      $('#text').val('');
      socket.emit('text', {
        'msg': text
      });
    }
  });

  socket.on('message', function(data) {
    console.log(data);
    $('#otherText').val($('#otherText').val() + data.msg + '\n');
  });


})

function leave_room() {
  socket.emit('leave', {}, function() {
    socket.disconnect();
    window.location.herf = '/';
  })
}


// function chat() {
//   text = $('#text').val();
//   $('#userText').val($('#userText').val() + text + '\n');
//   $('#otherText').val($('#otherText').val() + text + '\n');
//   $('#text').val('');
// }
