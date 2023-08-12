// Load the data from the server
health = 0;
shield = 0;
attack = 0;

download_config();


// FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function update_info() {
  document.getElementById("healthConfig").innerHTML = health;
  document.getElementById("shieldConfig").innerHTML = shield;
  document.getElementById("attackConfig").innerHTML = attack;
}

// BUTTONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*function help_button() {
  button = document.getElementById("help_button");
  if (button.innerHTML !== "Got it.") {
    button.innerHTML = "Got it.";
  }
  else {
    button.innerHTML = "Need some help?";
  }
}

// UPLOAD CONFIG --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function upload_config() {
  const data = {
    health: parseInt(health_slider.value),
    shield: parseInt(shield_slider.value),
    attack: parseInt(attack_slider.value)
  };

  const response = await fetch('/upload_config', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (response.ok) {
    // Successfully saved configuration
    showMessage('Configuration saved successfully.', false);
    return true;

  } else {
    if (response.status == 400) {
      showMessage('Incorrect ammount of points. Please try again.', true);
    }
    return false;
  }
}*/

// DOWNLOAD CONFIG --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function download_config() {

  const response = await fetch('/download_config').then(response => response);
  const responseData = await response.json();
      
  if (response.ok) {
    // Load data
    health = responseData.health;
    shield = responseData.shield;
    attack = responseData.attack;

    update_info();

    // Load previous code
    if (response.status == 200) {
      showMessage("Your information has been loaded successfully.", false);
    }
    if (response.status == 201){
      showMessage("Welcome to the configuration.", false);
    }
    return true;
  } else {
      showMessage("Your information couldn't be loaded. Please input it again. ", true);
    return false;
  }
}