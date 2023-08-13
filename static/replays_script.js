// BUTTONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function video_button() {
  button = document.getElementById("video_button");
  expand_form('75%');
  if (button.innerHTML !== "Hide last video") {
    button.innerHTML = "Hide last video";
  }
  else {
    button.innerHTML = "Show last video";
  }
}
