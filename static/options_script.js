setupOptions(); // No changes can be made from the login to here, so the data previously loaded is okay to use

/* Set the checkbox with the options previously loaded at the login */
function setupOptions() {
  checkbox = document.getElementById('themeCheckbox');
  checkbox.checked = (theme === 'dark' ? true : false);
}

function toggleTheme() {
  sessionStorage.setItem('theme', (theme === 'dark' ? 'light' : 'dark')); 
  triggerPythonFunction('/toggle_theme');
  setupOptions();
}