welcome_text = document.getElementById('welcome_text');
welcome_text.innerHTML = 'Welcome to the Game, ' + username + '!';

// Function to redirect to the "Update Code" page
function redirectToUpdateCode() {
  window.location.href = '/update_code';
}

// Function to redirect to the "Replays" page
function redirectToReplays() {
  window.location.href = '/replays';
}

// Function to redirect to the "Highscores" page
function redirectToHighscores() {
  window.location.href = '/highscores';
}

// Function to redirect to the "Player Info" page
function redirectToPlayerInfo() {
  window.location.href = '/player_info';
}

// Function to redirect to the "Bot Config" page
function redirectToBotConfig() {
  window.location.href = '/bot_config';
}