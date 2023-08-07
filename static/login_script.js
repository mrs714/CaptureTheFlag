function showMessage(message) {
  document.getElementById('message').textContent = message;
}

flag = 0;
// Toggles the visibility of the Create User form and Login form
function toggleCreateUser() {
  const createUserForm = document.getElementById('createUserForm');
  const loginForm = document.getElementById('loginForm');

  // Toggle visibility of the Create User form and Login form
  if (createUserForm.style.display == 'none' || flag == 0) {
    createUserForm.style.display = 'block';
    loginForm.style.display = 'none';
    flag = 1;
  } else {
    createUserForm.style.display = 'none';
    loginForm.style.display = 'block';
  }

  // Clear the message
  showMessage('');
}

// A implementar: checkLogin(username, password)
function loginButton() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  // Check if the username, password are empty or include things other than letters and numbers
  if (!checkUsernameAndPassword(username, password)) {
    return;
  }

  // Check if the username and password match
  if (checkLogin(username, password)) {
    showMessage('Login successful! Redirecting to home page...');
    Redirecting();
  }
}

// A implementar: checkUsernameAvailable(username), createUser(username, password)
function createUserButton() {
  showMessage('showpls2');
  const newUsername = document.getElementById('newUsername').value;
  const newPassword = document.getElementById('newPassword').value;

  // Check if the username, password are empty or include things other than letters and numbers
  if (!checkUsernameAndPassword(newUsername, newPassword)) {
    return;
  }
  
  // Check if the username already exists
  if (checkUsernameAvailable(newUsername)){
    createUser(newUsername, newPassword);
    showMessage('User created successfully! Redirecting to login page...');
    Redirecting();
  }
  else {
    showMessage('Username already exists. Please try another name. ');
  }
}

function checkUsernameAndPassword(username, password){
  
  if (username == '' || password == '') {
    showMessage('Username or password cannot be empty. Please try again.');
    return false;
  }

  if (!(/^[A-Za-z0-9]*$/.test(username)) || (!/^[A-Za-z0-9]*$/.test(password))) {
    showMessage('Username or password can only contain letters and numbers. Please try again.');
    return false;
  }

  return true;
}

// A implementar: checkLogin(username, password)
function checkLogin(username, password){
  return true;
}

// A implementar: checkUsernameAvailable(username)
function checkUsernameAvailable(username){
  return true;
}

// A implementar: createUser(username, password)
function createUser(username, password){
  return true;
}

function Redirecting(){
  setTimeout(() => {
    window.location.href = 'main_menu.html';
  }, 2000);
}
