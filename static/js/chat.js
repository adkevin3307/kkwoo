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
      document.cookie = "user_id =" + result['user_id'];
    }
  });
});


function chat() {
  var matching_socket = io.connect('https://' + document.domain + '/chat');
  console.log("user in chat " + user_id);
  matching_socket.on(user_id, function (data) {
    console.log('matching_socket in chat.js name ' + user_id)
    if (data.target_room === 'None') {
      location.href = '/sorry';
    }
    else {
      var room = data.target_room
      var chatroom_socket = io.connect('https://' + document.domain + '/chatroom');
      chatroom_socket.emit('join', {});
      $.ajax({
        url: "/post_room",
        type: "POST",
        async: true,
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
    async: true,
    type: 'GET',
    success: function (response) {
      console.log('frontend matching (chat.js)', response);
      if (response['url'] != 'waiting') // TODO reponse['result']
        location.href = response['url'];

    }
  });
}
