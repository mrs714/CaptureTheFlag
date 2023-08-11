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

// LOGIN --------------------------------------------------------------------------------------------
function loginButton() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  // Check if the username, password are empty or include things other than letters and numbers
  if (!checkUsernameAndPassword(username, password)) {
    return;
  }

  // Check if the username and password match (request to server)
  login(username, password).then(success => {
    if (success) {
      saveSessionData(username); // Saves the username in the session storage
      showMessage('Login successful! Redirecting to home page...');
      Redirecting();
    }
  });
}

async function login(username, password) {
  const data = {
    username: username,
    password: password,
  };

  const response = await fetch('/login_function', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (response.ok) {
    // Successfully logged in
    return true;

  } else {
    if (response.status == 400) {
      showMessage('Incorrect username or password. Please try again.');
    }
    else if (response.status == 401) {
      showMessage("The server found something that didn't check out in the user or password. Please try again.");
    }
    else if (response.status == 404) {
      showMessage('This username does not exist. Please try again.');
    }
    return false;
  }
}

// CREATE USER -------------------------------------------------------------------------------------
// A implementar: checkUsernameAvailable(username), createUser(username, password)
function createUserButton() {
  const newUsername = document.getElementById('newUsername').value;
  const newPassword = document.getElementById('newPassword').value;

  // Check if the username, password are empty or include things other than letters and numbers
  if (!checkUsernameAndPassword(newUsername, newPassword)) {
    return;
  }
  
  // Check if the username already exists
  check_user(newUsername).then(user_exists => {
    if (!user_exists) {
      create_user(newUsername, newPassword).then(success => {
        if (create_user(newUsername, newPassword)){
          saveSessionData(newUsername); // Saves the username in the session storage
          showMessage('User created successfully! Redirecting to login page...');
          Redirecting();
        }
      });
    }
    else {
      showMessage('Username already exists. Please try another name. ');
    }
  });
}

async function check_user(username) {
  const data = {
    username: username,
  };

  const response = await fetch('/user_exists', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (response.ok) {
    const responseData = await response.json();
    return responseData.user_exists;
  } else {
    if (response.status == 400) {
      showMessage('Something went wrong with the server. Please try again.');
    }
  }
  return true;
}

async function create_user(username, password) {
  const data = {
    username: username,
    password: password,
  };

  const response = await fetch('/create_user', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    if (response.status == 400) {
      showMessage('Something went wrong with the server. Please try again.');
    }
    return false;
  }
  return true;
}


// OTHER FUNCTIONS ---------------------------------------------------------------------------------
function checkUsernameAndPassword(username, password){
  
  if (username == '' || password == '') {
    showMessage('Username or password cannot be empty. Please try again.');
    return false;
  }

  if (!(/^[A-Za-z0-9]*$/.test(username)) || (!/^[A-Za-z0-9]*$/.test(password))) {
    showMessage('Username or password can only contain letters and numbers. Please try again.');
    return false;
  }

  if (password.length > 20 || username.length > 20) {
    showMessage('Username or password cannot be longer than 20 characters. Please try again.');
    return false;
  }
 
  return true;
}

function Redirecting(){
  getSessionData(); // Updates the data from the server for the other html files, like the username
  setTimeout(() => {
    window.location.href = '/main_menu';
  }, 2000);
}
