// LABELS AND CONSTANTS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// Bot config
health_label = document.getElementById("healthConfig");
shield_label = document.getElementById("shieldConfig");
attack_label = document.getElementById("attackConfig");
health = 0;
shield = 0;
attack = 0;

// Error log
error_label = document.getElementById("error_span");
error = "No status. ";

// User info
position_label = document.getElementById("position_span");
error_status_label = document.getElementById("error_status_span");
date_label = document.getElementById("date_span");
position = -1;
error_status = false;
date = "00/00/0000 00:00:00";

// Load previous data from server and update labels and information
function load_data() {
  if (config_successful && error_log_successful && user_info_successful) {
    // If all data could be loaded successfully, update labels
    showMessage("Your information has been loaded successfully.", false);
  }
  else {
    // If not, show error message
    showMessage("Your information couldn't be loaded. Please refresh the page or input the information again. ", true);
  }
}

download_config() // Config calls error which in turn calls user info

setTimeout(load_data, 4000); // Wait 2 seconds before loading data to make sure that the data has been downloaded


// FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function update_config(successful_download) {
  if (successful_download) {
    health_label.innerHTML = health;
    shield_label.innerHTML = shield;
    attack_label.innerHTML = attack;
  }
  else {
    health_label.innerHTML = "?";
    shield_label.innerHTML = "?";
    attack_label.innerHTML = "?";
  }
}

function update_error_log(successful_download) {
  if (successful_download) {
    if (error_log == null) {
      error_log = "No errors.";
    }
    else {
      error_label.innerHTML = error_log;
      error_label.style.color = "red";
    }
  }
  else {
    error_label.innerHTML = "Couldn't load the log.";
    error_label.style.color = "red";
  }
}

function update_user_info(successful_download) {
  if (successful_download) {
    position_label.innerHTML = position;
    error_status_label.innerHTML = error_status;
    date_label.innerHTML = date;
  }
  else {
    position_label.innerHTML = "-1";
    error_status_label.innerHTML = "false";
    date_label.innerHTML = "00/00/0000 00:00:00";
  }
}
  

// BUTTONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function log_button() {
  expand_form('75%')
  button = document.getElementById("log_button");
  if (button.innerHTML !== "Hide log") {
    button.innerHTML = "Hide log";
  }
  else {
    button.innerHTML = "Show last error log";
  }
}

// DOWNLOAD CONFIG AND INFO --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function download_config() {

  const response = await fetch('/download_config').then(response => response);
  const responseData = await response.json();
        
  if (response.ok) {

    health = responseData.health;
    shield = responseData.shield;
    attack = responseData.attack;
    console.log(health, shield, attack);
    
    update_config(true);
  
    config_successful = true;

    download_error_log()

  }
  else {

    update_config(false);

    config_successful = false;

  }
}

async function download_error_log() {
  const response = await fetch('/download_error_log').then(response => response);
  const responseData = await response.json();
        
  if (response.ok) {
    // Load data
    error_log = responseData.error_log;
    console.log(error_log);

    update_error_log(true);

    error_log_successful = true;

    download_user_info()

  } 
  else {
    update_error_log(false);
    error_log_successful = false;
  }
}

async function download_user_info() {

  const response = await fetch('/download_user_info').then(response => response);
  const responseData = await response.json();
    
  if (response.ok) {

    console.log(responseData);

    // Load data
    position = responseData.position;
    date = responseData.date;

    error_status = position == -1 ? true : false;

    update_user_info(true);

    user_info_successful = true;

  } 
  else {
    update_user_info(false);
    user_info_successful = false;
  }
}