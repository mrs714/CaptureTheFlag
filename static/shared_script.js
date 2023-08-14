/* All html files include this script. This means that the variables are mantained across the entire website.
This allows for easier access to the user data, and carrying information between pages. 
The first time this will be used will be at the login, wether to load the data for a previous user, 
or to reflect the newly created data from a new user. This will also be used with the options file. */


// SESSION DATA ---------------------------------------------------------------
// Load the data from the html session storage when the script is first loaded in a page
// Data used by the scripts:
var username = ''; // The username of the user
updateSessionData(); // Update the data from the html session storage

// Update the data from the html session storage
function updateSessionData() { // Update the data from the html session storage
  username = sessionStorage.getItem('username') !== null ? sessionStorage.getItem('username') : '';
}

// Save the data to the html session storage
function saveSessionData(user) { // Save the data to the html session storage
  sessionStorage.setItem('username', user);
}

// FUNCTIONS ------------------------------------------------------------------- 
// Go to the main menu
function goBack() {
  window.location.href = '/main_menu';
}

function showMessage(message, error) {
  /* Pre: the html contains the message and message_span */
  document.getElementById('message').innerHTML = message;
  span = document.getElementById('message_span');
  if (error) {
    span.style.color = "red";
  }
  else {
    span.style.color = "#66ff00";
  }
}

function add_event_listener(element, funct){
  element.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      // Call function given when the event happens
      funct();
    }
  });
}

function expand_form(width) {
  const container = document.getElementById("container");
  container.style.maxWidth != width ? container.style.maxWidth = width : container.style.maxWidth = '35%';
}

// Call a certain python function (Functions: none for the moment)
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


// SERVER DATA -----------------------------------------------------------------

/* Obtention of data from the server, and saving to local html session storage 
For now, this functions WILL NOT be used, as the data is obtained from the html session storage,
and there is no need to fetch other data from the server to be used across the website.
Pages that need specific data from the server will fetch it through dedicated functions.
*/

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

      // Update the values
      updateSessionData();

      // Log the values (debugging purposes)
      console.log('username: ' + username);
    }
  });
}
