let userData = [];

function showMessage(message) {
  document.getElementById('message').textContent = message;
}

function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const user = userData.find(u => u.username === username && u.password === password);
  if (user) {
    showMessage('Login successful!');
    setTimeout(() => {
      // Redirect to another HTML page (e.g., dashboard.html) after a delay of 2 seconds (2000 milliseconds)
      window.location.href = 'mainMenu.html';
    }, 2000);
  } else {
    showMessage('Invalid credentials. Please try again.');
  }
}

function createUser() {
  const newUsername = document.getElementById('newUsername').value;
  const newPassword = document.getElementById('newPassword').value;

  // Check if the username already exists
  if (userData.some(u => u.username === newUsername)) {
    showMessage('Username already exists. Please choose a different username.');
  } else {
    // Add the new user to the userData array
    userData.push({ username: newUsername, password: newPassword });
    showMessage('User created successfully!');
    setTimeout(() => {
      // Redirect to another HTML page (e.g., dashboard.html) after a delay of 2 seconds (2000 milliseconds)
      window.location.href = 'mainMenu.html';
    }, 2000);
  }
}
