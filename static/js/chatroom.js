

var socket;


$(document).ready(function () {
  console.log("in chatroom.html");

  if (location.port) {
    socket = io.connect('http://' + document.domain + ":" + location.port + '/chatroom');
    socket.emit('join', {});
    msg(socket);
  }
  else {
    socket = io.connect('https://' + document.domain + '/chatroom');
    socket.emit('join', {});
    msg(socket);
  }

  //  socket.on('connect', function () {
  //    socket.emit('join', {});
  //  });

  $('#text').keypress(function (e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      var text = $('#text').val();
      $('#text').val('');
      console.log("text: " + text);
      console.log("socket: ", socket);
      socket.emit('text', { 'msg': text });
    }
  });

  $('#send').click(function () {
    var text = $('#text').val();
    $('#text').val('');
    socket.emit('text', { 'msg': text });
  })
  function msg(socket) {
    socket.on('message', function (data) {
      var user_id = data['user_id'];
      var message = data['msg'];
      console.log(data);

      if (!message && getCookie("user_id") === user_id) {
        $('#chatbox').html($('#chatbox').html() + "<div class='d-flex justify-content-end'>"
          + "<div class='msg_container_send messagebox'>You just enter the room :D</div></div>"
          + "<div class='d-flex'><div class='msg_container messagebox'>Your bro just enter the room :D</div></div>");
      }

      if (message) {
        if (getCookie("user_id") === user_id)
          $('#chatbox').html($('#chatbox').html() + "<div class='d-flex justify-content-end'><div class='msg_container_send messagebox'>" + message + "</div></div>");
        else
          $('#chatbox').html($('#chatbox').html() + "<div class='d-flex'><div class='msg_container messagebox'>" + message + "</div></div>");

        $("#chatbox").scrollTop($("#chatbox").prop("scrollHeight"));
      }
    });
  }

  $("#leave").click(function () {
    socket.emit('leave', {}, function () {
      socket.disconnect();
      location.href = '/chat';
    });
  });

});
