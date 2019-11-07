$(document).ready(function () {
  console.log("in chatroom.html");
  var socket = io.connect('http://' + document.domain +'/chatroom')  //' + document.domain + '
  socket.on('connect', function () {
    socket.emit('join', {});
  });

  $('#text').keypress(function (e) 
  {
    var code = e.keyCode || e.which;
    if (code == 13)
    {
      text = $('#text').val();
      $('#text').val('');
      socket.emit('text', 
      {
        'msg': text
      });
    }
  });

  socket.on('message', function (data) 
  {
    console.log(data);
    var user_id = data.msg.split(":")[0];
    var message = data.msg.split(":")[1];
  

    if (data.msg.includes("entered") && document.cookie.split("=")[1] === user_id)
    {
        $('#chatbox').html($('#chatbox').html() + "<div class='d-flex justify-content-end'>"
        + "<div class='msg_container_send'>You has entered the room :D</div></div>" 
        + "<div class='d-flex'><div class='msg_container'>Other has entered the room :D</div></div>");
    }
    
    if(!data.msg.includes("entered"))
    { 
      if (document.cookie.split("=")[1] === user_id)
      $('#chatbox').html($('#chatbox').html() + "<div class='d-flex justify-content-end'><div class='msg_container_send'>"   + message +  "</div></div>");
    else
      $('#chatbox').html($('#chatbox').html() + "<div class='d-flex'><div class='msg_container'>"   + message +  "</div></div>");
    }

  });


});

function leave_room() 
{
  socket.emit('leave', {}, function () 
  {
    socket.disconnect();
    window.location.herf = '/';
  });
}
