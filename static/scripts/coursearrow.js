var arrow = document.getElementById('arrow');
var heading = document.getElementsByClassName('panel-heading')[0];
var details = document.getElementsByClassName('details')[0];

var arrowDownUrl = "/static/rsc/icons8-chevron-down-30.png";
var arrowUpUrl = "/static/rsc/icons8-chevron-up-30.png";

heading.addEventListener("click", function() {
  if (arrow.classList.contains("down")) {
    arrow.classList.remove("down");
    arrow.classList.add("up");
    details.style.display = "none";
    arrow.src = arrowUpUrl;
  } else {
    arrow.classList.remove("up");
    arrow.classList.add("down");
    details.style.display = "block";
    arrow.src = arrowDownUrl;
  }
});
