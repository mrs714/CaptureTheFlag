// SLIDERS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
health_slider = document.getElementById("health_slider");
shield_slider = document.getElementById("shield_slider");
attack_slider = document.getElementById("attack_slider");

health_slider.addEventListener('input', first_slider);
shield_slider.addEventListener('input', second_slider);
attack_slider.addEventListener('input', third_slider);

sliders = [health_slider, shield_slider, attack_slider];

update_info();

function first_slider() {
  var points_to_give = 300 - parseInt(total_value());
  if (parseInt(shield_slider.value) == 50 && points_to_give < 0){
    attack_slider.value = parseInt(attack_slider.value) + points_to_give;
  }
  else if (parseInt(shield_slider.value) == 150 && points_to_give > 0){
    attack_slider.value = parseInt(attack_slider.value) + points_to_give;
  }
  else if (parseInt(attack_slider.value) == 50 && points_to_give < 0){
    shield_slider.value = parseInt(shield_slider.value) + points_to_give;
  }
  else if (parseInt(attack_slider.value) == 150 && points_to_give > 0){
    shield_slider.value = parseInt(shield_slider.value) + points_to_give;
  }
  else {
    if (points_to_give %2 != 0) {
      shield_slider.value = parseInt(shield_slider.value) + parseInt(points_to_give/2);
      attack_slider.value = parseInt(attack_slider.value) + parseInt(points_to_give/2);
      if (parseInt(shield_slider.value) < parseInt(attack_slider.value)) {
        shield_slider.value = parseInt(shield_slider.value) + 1;
      }
      else {
        attack_slider.value = parseInt(attack_slider.value) + 1;
      }
    }
    else {
      shield_slider.value = parseInt(shield_slider.value) + parseInt(points_to_give/2);
      attack_slider.value = parseInt(attack_slider.value) + parseInt(points_to_give/2);
    }
  }
  

  update_info();
}

function second_slider() {

  var points_to_give = 300 - parseInt(total_value());
  if (parseInt(attack_slider.value) == 50 && points_to_give < 0){
    shield_slider.value = parseInt(shield_slider.value) + points_to_give;
  }
  else if (parseInt(attack_slider.value) == 150 && points_to_give > 0){
    shield_slider.value = parseInt(shield_slider.value) + points_to_give;
  }
  else {
    attack_slider.value = parseInt(attack_slider.value) + points_to_give;
  }

  update_info();
}

function third_slider() {
  var points_to_give = 300 - parseInt(total_value());
  if (parseInt(shield_slider.value) == 50 && points_to_give < 0){
    attack_slider.value = parseInt(attack_slider.value) + points_to_give;
  }
  else if (parseInt(shield_slider.value) == 150 && points_to_give > 0){
    attack_slider.value = parseInt(attack_slider.value) + points_to_give;
  }
  else {
    shield_slider.value = parseInt(shield_slider.value) + points_to_give;
  }

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

function fix_sliders() {
  if (total_value() > 300) {
    shield_slider.value = parseInt(shield_slider.value) - 1;
  }
  if (total_value() > 300) {
    attack_slider.value = parseInt(attack_slider.value) - 1;
  }
  if (total_value() < 300) {
    shield_slider.value = parseInt(shield_slider.value) + 1;
  }
  if (total_value() < 300) {
    attack_slider.value = parseInt(attack_slider.value) + 1;
  }
}

function update_info() {
  fix_sliders();
  document.getElementById("health_slider_info").innerHTML = "Health: " + health_slider.value;
  document.getElementById("shield_slider_info").innerHTML = "Shield: " + shield_slider.value;
  document.getElementById("attack_slider_info").innerHTML = "Attack: " + attack_slider.value;
}

// BUTTONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function help_button() {
  button = document.getElementById("help_button");
  if (button.innerHTML !== "Got it.") {
    button.innerHTML = "Got it.";
  }
  else {
    button.innerHTML = "Need some help?";
  }
}

// UPDATE CONFIG --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function save_config() {
  const data = {
    health: parseInt(health_slider.value),
    shield: parseInt(shield_slider.value),
    attack: parseInt(attack_slider.value)
  };

  const response = await fetch('/save_config', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (response.ok) {
    // Successfully logged in
    return true;

  } else {
    if (response.status == 400) {
      showMessage('Incorrect username or password. Please try again.');
    }
    else if (response.status == 401) {
      showMessage("The server found something that didn't check out in the user or password. Please try again.");
    }
    else if (response.status == 404) {
      showMessage('This username does not exist. Please try again.');
    }
    return false;
  }
}