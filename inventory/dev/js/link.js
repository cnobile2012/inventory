window.onload = function() {
  var link = document.getElementById("edit");

  if(link) {
    link.onclick = function() {
      return !window.open(link.href);
    }
  }
}
