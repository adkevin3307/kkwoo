window.onload = function () {

  $.ajax(
    {
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
    }
  )

};

function chatting() {
  $.ajax(
    {
      url: '/matching',
      type: 'GET',
      success: function (response) { location.href = response; }
    }
  )
}
