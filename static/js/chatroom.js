
$(document).ready(function () {
  console.log("in chatroom.html");

  var socket;

  if(location.port)
    socket = io.connect('http://' + document.domain + ":" +location.port + '/chatroom');
  else
    socket = io.connect('https://' + document.domain + '/chatroom');



  socket.on('connect', function () {
    socket.emit('join', {});
  });

  $('#text').keypress(function (e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      var text = $('#text').val();
      $('#text').val('');
      console.log("text: "+text);
      console.log("socket: "+socket);
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
    console.log(data);

    if (data.msg.includes("entered") && getCookie("user_id") === user_id) {
      $('#chatbox').html($('#chatbox').html() + "<div class='d-flex justify-content-end'>"
        + "<div class='msg_container_send messagebox'>You has entered the room :D</div></div>"
        + "<div class='d-flex'><div class='msg_container messagebox'>Other has entered the room :D</div></div>");
    }

    if (!data.msg.includes("entered") && message) {
      if (getCookie("user_id") === user_id)
        $('#chatbox').html($('#chatbox').html() + "<div class='d-flex justify-content-end'><div class='msg_container_send messagebox'>" + message + "</div></div>");
      else
        $('#chatbox').html($('#chatbox').html() + "<div class='d-flex'><div class='msg_container messagebox'>" + message + "</div></div>");

      $("#chatbox").scrollTop($("#chatbox").prop("scrollHeight"));
    }
  });

  // function leave_room(){
  //   socket.emit('leave', {}, function () {
  //     socket.disconnect();
  //     window.location.herf = '/';
  //   });
  // }

  $("#leave").click(function(){
    socket.emit('leave', {}, function (){
      socket.disconnect();
      location.href = 'index';
    });
  });

});
