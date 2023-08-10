// Sample replays data (replace this with the actual data from the server)
const replaysData = [
  { number: 45, highscore: 300, time: "13:05/5:03" },
  { number: 44, highscore: 300, time: "13:05/5:03" },
  { number: 43, highscore: 295, time: "13:05/5:03" },
  // Add more highscores data here...
];
// Sample highscores data (replace this with the actual data from the server)
const highscoresData = [
  { rank: 1, username: 'Player1', score: 100 },
  { rank: 2, username: 'Player2', score: 90 },
  { rank: 3, username: 'Player3', score: 80 },
  // Add more highscores data here...
];

// Function to populate the highscores table
function populateReplaysTable() {
  const tableBody = document.getElementById('replaysTable');
  replaysData.forEach(entry => {
    const row = document.createElement('tr');
    row.innerHTML = `<td>${entry.number}</td><td>${entry.highscore}</td><td>${entry.time}</td>`;
    tableBody.appendChild(row);
  });
}

// Function to populate the highscores table
function populateHighscoresTable() {
  const tableBody = document.getElementById('highscoresTable');
  highscoresData.forEach(entry => {
    const row = document.createElement('tr');
    row.innerHTML = `<td>${entry.rank}</td><td>${entry.username}</td><td>${entry.score}</td>`;
    tableBody.appendChild(row);
  });
}