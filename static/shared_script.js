/* Obtention of data from the server */
var finishedLoadingData = false; // This variable is used to check if the data has been loaded from the server, it is used to prevent other scripts from running before the data is loaded
var username;
var theme;
var loggedIn = false; 

function getSessionData(callback) {
  fetch('/get_session_data') // await is needed here because the function is async, this way other scripts that rely on the information from the server don't run beofre the data is fetched
    .then(response => response.json())
    .then(data => {
      callback(data);
    })
    .catch(error => {
      console.error('Error fetching session data:', error);
    });
}

getSessionData(data => { // Callback from getSessionData
  if (data) {
    username = data.username;
    theme = data.theme;
    loggedIn = data.loggedIn;
    console.log('username: ' + username);
    console.log('theme: ' + theme);
    console.log('loggedIn: ' + loggedIn);
    finishedLoadingData = true;
  }
});

/* Updating server data */
const newData = {
  key1: 'value1',
  key2: 'value2',
  // ... add more data keys and values as needed
};

/*
fetch('/update_data', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(newData)
})
.then(response => response.json())
.then(data => {
  console.log(data.message);  // Output: Data updated successfully
})
.catch(error => {
  console.error('Error updating data:', error);
});*/









/* Functions */
// Go to the previous page
function goBack() {
  if (window == window.history.previous){
    window.history.back(); //quick fix, remove later
  }
  window.history.back();
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
