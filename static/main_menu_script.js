welcome_text = document.getElementById('welcome_text');
welcome_text.innerHTML = 'Welcome to the Game, ' + username + '!';

// Function to redirect to the "Update Code" page
function update_code() {
  window.location.href = '/update_code';
}

// Function to redirect to the "Bot Config" page
function bot_config() {
  window.location.href = '/bot_config';
}

// Function to redirect to the "Player Info" page
function player_info() {
  window.location.href = '/player_info';
}

// Function to redirect to the "Replays" page
function replays() {
  window.location.href = '/replays';
}

// Function to redirect to the "Highscores" page
function highscores() {
  window.location.href = '/highscores';
}

// Function to redirect to the "Help" page
function help() {
  window.location.href = '/help';
}

// Log off user:
function logout() {
  window.location.href = '/logout';
}