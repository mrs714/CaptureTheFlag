/* All html files include this script. This means that the variables are mantained across the entire website.
This allows for easier access to the user data, and carrying information between pages. 
The first time this will be used will be at the login, wether to load the data for a previous user, 
or to reflect the newly created data from a new user. This will also be used with the options file. */

/* Obtention of data from the server, and saving to local html session storage */
username = sessionStorage.getItem('username') !== null ? sessionStorage.getItem('username') : '';
theme = sessionStorage.getItem('theme') !== null ? sessionStorage.getItem('theme') : 'light';
loggedIn = sessionStorage.getItem('loggedIn') !== null ? sessionStorage.getItem('loggedIn') : false;

function fetchSessionData(callback) {
  fetch('/get_session_data') 
    .then(response => response.json())
    .then(data => {
      callback(data);
    })
    .catch(error => {
      console.error('Error fetching session data:', error);
    });
}

/* Any script that requires an update on the server-stored data will call this function.
The changes made will persist to other html files. */
function getSessionData() { 
  fetchSessionData(data => { 
    if (data) {
      sessionStorage.setItem('username', data.username);
      sessionStorage.setItem('theme', data.theme);
      sessionStorage.setItem('loggedIn', data.loggedIn);
      console.log('username: ' + username);
      console.log('theme: ' + theme);
      console.log('loggedIn: ' + loggedIn);
    }
  });
}


/* Functions */
// Go to the previous page
function goBack() {
  window.location.href = '/main_menu';
}

// Call a certain python function
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
