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

var user_id;

$(document).ready(function () {
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
  var matching_socket = io.connect('https://' + document.domain + '/chat');
  console.log("user in chat " + user_id);
  matching_socket.on(user_id, function (data) {
    console.log('matching_socket in chat.js name ' + user_id)
    // console.log(data);
    if (data.target_room === 'None') {
      location.href = '/sorry';
    }
    else {
      var room = data.target_room
      var chatroom_socket = io.connect('https://' + document.domain + '/chatroom')
      chatroom_socket.emit('join', {});  //which room
      $.ajax({
        url: "/post_room",
        type: "POST",
        data: { 'target_room': room },
        success: function (response) {
          console.log(response);
          location.href = response['url'];
        }
      })
    }
  });
  Swal.fire({
    "title": "Loading",
    showConfirmButton: false,
    onBeforeOpen: () => {
      Swal.showLoading();
    }
  })
  $.ajax({
    url: '/match',
    type: 'GET',
    success: function (response) {
      console.log('/match success')
      console.log(response)
      if (response['url'] != 'waiting') // TODO reponse['result']
        location.href = response['url'];
      // console.log(" match response "+response['url']);
      // location.href = response['url'];
    }
  });
}
