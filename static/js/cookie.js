function getCookie(data) {
  var mycookie = document.cookie.split(";");

  for (var i = 0; i < mycookie.length; i++) {
    if (mycookie[i].includes(data)) {
      return mycookie[i].split("=")[1];
    }
  }
}
