health_slider = document.getElementById("health_slider");
shield_slider = document.getElementById("shield_slider");
attack_slider = document.getElementById("attack_slider");

sliders = [health_slider, shield_slider, attack_slider];

update_info();

function first_slider() {
  var points_to_give = 300 - total_value();
  if (points_to_give %2 != 0) {
    shield_slider.value += parseInt(points_to_give/2) + 1;
    attack_slider.value += parseInt(points_to_give/2);
  }
  else {
    shield_slider.value += parseInt(points_to_give/2);
    attack_slider.value += parseInt(points_to_give/2);
  }
  

  update_info();
}

function second_slider() {

  var points_to_give = 300 - total_value();
  attack_slider.value += parseInt(points_to_give);

  update_info();
}

function third_slider() {
  var points_to_give = 300 - total_value();
  shield_slider.value += parseInt(points_to_give);

  update_info();
}

function total_value() {
  let total_ammount = 0;
  sliders.forEach(slider => {
    total_ammount += parseInt(slider.value);
  });
  console.log(total_ammount);
  return total_ammount;
}

function update_info() {
  document.getElementById("health_slider_info").innerHTML = "Health: " + health_slider.value;
  document.getElementById("shield_slider_info").innerHTML = "Shield: " + shield_slider.value;
  document.getElementById("attack_slider_info").innerHTML = "Attack: " + attack_slider.value;
}