window.onload = function(){

  $.ajax(
    {
      url:'/online',
      type:'GET',
      success:function(result){
        if(!result['result'])
        {
          location.href = "/"
        }
      }
    }
  )

  if(location.href.includes('pass'))
  {
    swal.fire({
      "title": "認證成功"
    });
  }
};

function chatting(){
  $.ajax(
    {
      url:'/matching',
      type:'GET',
      success:function(response){location.href =  response;}
    }
  )
}
