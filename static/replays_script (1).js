// ON LOAD --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
replays_data = [{number: 0,  highscore: "NoOne: 0 points", time_start: "00/00/0000 00:00:00", time_elapsed: "00:00:00"}] // Only one replay for now, might be more in the future (placeholder)

//download_simulation_info();
populate_replays_table();



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

// FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function populate_replays_table() {
  const table_body = document.getElementById('replays_table');
  replays_data.forEach(entry => {
    const row = document.createElement('tr');
    row.innerHTML = `<td>${entry.number}</td><td>${entry.highscore}</td><td>${entry.time_start}</td><td>${entry.time_elapsed}</td>`;
    table_body.appendChild(row);
  });
}

// DOWNLOAD CONFIG AND INFO --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function download_config() {

  const response = await fetch('/download_config').then(response => response);
  const responseData = await response.json();
      
  if (response.ok) {

    health = responseData.health;
    shield = responseData.shield;
    attack = responseData.attack;
    
    update_config(true);
  
    return true;

  }
  else {

    update_config(false);

    return false;

  }
}