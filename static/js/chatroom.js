$(document).ready(function () {
  console.log("in chatroom.html");
  var socket = io.connect('https://' + document.domain + '/chatroom');  //' + document.domain + '
  socket.on('connect', function () {
    socket.emit('join', {});
  });

  $('#text').keypress(function (e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      var text = $('#text').val();
      $('#text').val('');
      socket.emit('text', { 'msg': text });
    }
  });

  $('#send').click(function () {
    var text = $('#text').val();
    $('#text').val('');
    socket.emit('text', { 'msg': text });
  })


  socket.on('message', function (data) {
	var user_id = data['user_id'];
	var message = data['msg'];
	console.log(data['msg']);

    if (data.msg.includes("entered") && document.cookie.split("=")[1] === user_id) {
      $('#chatbox').html($('#chatbox').html() + "<div class='d-flex justify-content-end'>"
        + "<div class='msg_container_send messagebox'>You has entered the room :D</div></div>"
        + "<div class='d-flex'><div class='msg_container messagebox'>Other has entered the room :D</div></div>");
    }

    if (!data.msg.includes("entered") && message) {
      if (document.cookie.split("=")[1] === user_id)
        $('#chatbox').html($('#chatbox').html() + "<div class='d-flex justify-content-end'><div class='msg_container_send messagebox'>" + message + "</div></div>");
      else
        $('#chatbox').html($('#chatbox').html() + "<div class='d-flex'><div class='msg_container messagebox'>" + message + "</div></div>");

      $("#chatbox").scrollTop($("#chatbox").prop("scrollHeight"));
    }
  });
});

function leave_room() {
  socket.emit('leave', {}, function () {
    socket.disconnect();
    window.location.herf = '/';
  });
}
