window.onload = function () {
  $.ajax({
    url: '/online',
    type: 'GET',
    success: function (result) {
      console.log(result)
      if (result['result']) {
        swal.fire({
          "title": "認證成功"
        });
      }
    }
  });

};

var socket;
var user_id;

$(document).ready(function () {
   socket = io.connect('https://' + document.domain + '/chat');
  $.ajax({
    url: "/get_user",
    type: "GET",
    async: false,
    success: function (result) {
      user_id = result['user_id']
      console.log(user_id);
    }
  });

});


function chat() {
  console.log( "user in chat " + user_id);
  socket.on(user_id, function (data) {
    console.log('socket in chat.js name ' + user_id)
    // console.log(data);
    if (data.target_room === 'None') {
      location.href = '/sorry';
    }
    else {
      var room = data.target_room
      socket.emit('join', {});  //which room
      $.ajax({
        url:"/post_room",
        type:"POST",
        data:{'target_room':room},
        success: function(response) {
          console.log(response);
          location.href = response['url'];
        }
      })
    }
  });
  Swal.fire({
    "title":"Loading",
    showConfirmButton:false,
    onBeforeOpen:()=>{
      Swal.showLoading();
    }
  })
  $.ajax({
      url: '/match',
      type: 'GET',
      success: function (response) {
        if(!response['result']==='waiting')
             location.href = response['url'];
        // console.log(" match response "+response['url']);
        // location.href = response['url'];
      }
    });
}
