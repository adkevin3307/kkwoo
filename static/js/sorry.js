
Swal.fire({
    title:"Sorry , failed to connect with someone :(",
    type:"error",
    showConfirmButton:true
}).then(()=>{
    location.href = '/chat';
});

