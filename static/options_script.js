setupOptions(); // No changes can be made from the login to here, so the data previously loaded is okay to use

/* Set the checkbox with the options previously loaded at the login */
function setupOptions() {
  checkbox = document.getElementById('themeCheckbox');
  checkbox.checked = (theme === 'dark' ? true : false);
  console.log('theme: ' + theme);
}

function toggleTheme() {
  triggerPythonFunction('/toggle_theme');
  setTimeout(() => { getSessionData(); }, 200); // Get the data from the server, and wait until it is loaded
  setTimeout(() => { setupOptions(); }, 400);
}