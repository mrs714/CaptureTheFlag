function showMessage(message) { // Success/error loging
  document.getElementById('message_area').innerHTML = message; 
}

// UPDATE CONFIG --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function update_code() {

  const inputValue = editor.getValue()
  
  const data = {
    code: inputValue
  };

  const response = await fetch('/save_code', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  }).then(response => response.json());

  if (response.ok) {
    // Successfully saved configuration
    showMessage('Code saved successfully!');
    return true;

  } else {
      showMessage("Your code isn't working. Here's the compiler's output: <br><br>" + response.error + "<br><br>Please make sure to compile your code before saving it.");
    return false;
  }
}

// CODE MIRROR --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// Initialize CodeMirror instance, can't be used in the script file because of imports ES6 syntax 
const codeTextarea = document.getElementById('code_zone');
    
// Initialize CodeMirror with the dark theme (dracula)
const editor = CodeMirror.fromTextArea(codeTextarea, {
  theme: 'dracula', // Use the 'dracula' theme
  mode: 'python',   // Set the mode to Python
  lineNumbers: true // Show line numbers
});

// Synchronize scrolling between CodeMirror and line numbers
const lineNumbers = document.getElementById('lineNumbers');
editor.on('scroll', function () {
  lineNumbers.scrollTop = editor.getScrollInfo().top;
});