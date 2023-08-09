/* Set the checkbox with the saved options */
checkbox = document.getElementById('themeCheckbox');

checkbox.checked = (theme === 'dark' ? true : false);
console.log("theme: " + theme);

function toggleTheme() {
  triggerPythonFunction('/toggle_theme');
}