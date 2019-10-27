$(document).ready(function () {
  var socket = io.connect('https://' + document.domain + '/chat')
  socket.on('connect', function () {
    socket.emit('join', {});
  });

  $('#text').keypress(function (e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      text = $('#text').val();
      $('#text').val('');
      socket.emit('text', {
        'msg': text
      });
    }
  });

  socket.on('message', function (data) {
    console.log(data);
    $('#otherText').val($('#otherText').val() + data.msg + '\n');
  });


});

function leave_room() {
  socket.emit('leave', {}, function () {
    socket.disconnect();
    window.location.herf = '/';
  })
}
