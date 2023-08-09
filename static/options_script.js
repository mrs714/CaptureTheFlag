/* Set the checkbox with the saved options */
checkbox = document.getElementById('themeCheckbox');
theme = checkbox.getAttribute('theme');

checkbox.checked = (theme === 'dark' ? true : false);
console.log(theme);

function toggleTheme() {
  window.location.href = '/toggle-theme';
}