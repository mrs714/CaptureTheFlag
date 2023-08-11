health_slider = document.getElementById("health_slider");
shield_slider = document.getElementById("shield_slider");
attack_slider = document.getElementById("attack_slider");

function first_slider() {
  var points_to_give = 300 - total_value();
  if (points_to_give %2 != 0) {
    shield_slider.value += parseInt(points_to_give/2) + 1;
    attack_slider.value += parseInt(points_to_give/2);
  }
  shield_slider.value += parseInt(points_to_give/2);
  attack_slider.value += parseInt(points_to_give/2);
}

function second_slider() {
  var points_to_give = 300 - total_value();
  attack_slider.value += parseInt(points_to_give);
}

function third_slider() {
  var points_to_give = 300 - total_value();
  shield_slider.value += parseInt(points_to_give);
}

sliders.forEach(slider => {
  slider.addEventListener('input', () => {
    totalPoints = 300 - sliders.reduce((total, slider) => total + parseInt(slider.value), 0);
    totalPointsDisplay.textContent = `Total Points: ${totalPoints}`;
  });
});

function total_value() {
  let total_ammount = 0;
  sliders.forEach(slider => {
    total_ammount += parseInt(slider.value);
  });
}