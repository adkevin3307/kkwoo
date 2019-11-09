var user_id;
var matchAjax;
$(document).ready(function () {

  $.ajax({
    url: '/online',
    type: 'GET',
    success: function (result) {
      console.log(result)
      if (result['result']) {
        user_id = result['user_id']
        document.cookie = "user_id =" + result['user_id'];
        document.cookie = "user_name =" + result['user_name'];
      }
    }
  }).then(() => {
    swal.fire({
      "title": "Hi "+ getCookie("user_name") + " :D !"
    });
  });

  // $("#bar").load("/bar");

  // $.ajax({
  //   url: "/get_user",
  //   type: "GET",
  //   async: false,
  //   success: function (result) {
  //     user_id = result['user_id']
  //     document.cookie = "user_id =" + result['user_id'];
  //   }
  // });
});


function chat() {
  var matching_socket;

  if (location.port)
    matching_socket = io.connect('http://' + document.domain + ":" +  location.port + '/chat');
  else
    matching_socket = io.connect('https://' + document.domain + '/chat');

  console.log("user in chat " + user_id);
  matching_socket.on(user_id, function (data) {
    console.log('matching_socket in chat.js name ' + user_id)
    if (data['target_room'] === 'None') {
      location.href = '/sorry';
    }
    else {
      var room = data["target_room"]
      // if (location.port)
      //   var chatroom_socket = io.connect('http://' + document.domain + location.port + '/chat');
      // else
      //   var chatroom_socket = io.connect('https://' + document.domain + '/chatroom');
      // chatroom_socket.emit('join', {});

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
    "title": "Finding someone to match",
    showConfirmButton: false,
    allowOutsideClick: false,
    showCancelButton:true,
    onBeforeOpen: () => {
      Swal.showLoading();
    }
  }).then((result)=>{
    if(!result.value)
    {
      matchAjax.abort();
      Swal.fire("Cancel!");
    }
  })

  matchAjax = $.ajax({
    url: '/match',
    async: true,
    type: 'GET',
    success: function (response) {
      console.log('frontend matching (chat.js)', response);
      if (response['url'] != 'waiting') { // TODO reponse['result']
        location.href = response['url'];
      }
    }
  });
}
