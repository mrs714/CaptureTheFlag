/* All html files include this script. This means that the variables are mantained across the entire website.
This allows for easier access to the user data, and carrying information between pages. 
The first time this will be used will be at the login, wether to load the data for a previous user, 
or to reflect the newly created data from a new user. This will also be used with the options file. */

/* Obtention of data from the server, and saving to local html session storage */
// Load the data from the html session storage when the script is first loaded in a page
// Data used by the scripts:
var username = ''; // The username of the user
var theme = ''; // The theme of the user (light or dark)
updateSessionData();

function updateSessionData() { // Update the data from the html session storage
  username = sessionStorage.getItem('username') !== null ? sessionStorage.getItem('username') : '';
  theme = sessionStorage.getItem('theme') !== null ? sessionStorage.getItem('theme') : 'light';
}

function updateSessionValue(key, value) { // Update a single value from the html session storage
  sessionStorage.setItem(key, value);
  updateSessionData();
}

function fetchSessionData(callback) { // Fetch the data from the server
  fetch('/get_session_data') 
    .then(response => response.json())
    .then(data => {
      callback(data);
    })
    .catch(error => {
      console.error('Error fetching session data:', error);
    });
}

/* This will only be called when logging in, when the data obtained from the server database is 
being relayed to the new html session */
function getSessionData() { // Pass the data from the server to the html session storage
  fetchSessionData(data => { 
    if (data) {
      // Save the data to html session storage (persists across pages)
      sessionStorage.setItem('username', data.username);
      sessionStorage.setItem('theme', data.theme);

      // Update the values
      updateSessionData();

      // Log the values (debugging purposes)
      console.log('username: ' + username);
      console.log('theme: ' + theme);
    }
  });
}

/* Functions */
// Go to the main menu
function goBack() {
  window.location.href = '/main_menu';
}

// Call a certain python function (Functions: /toggle_theme)
async function triggerPythonFunction(functionName) { 
  try {
      const response = await fetch(functionName);
      if (response.ok) {
          console.log(functionName + ' triggered successfully');
      } else {
          console.error('Error triggering ' + functionName);
      }
  } catch (error) {
      console.error('Error:', error);
  }
}
