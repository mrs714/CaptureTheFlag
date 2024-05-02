// Load the code from the server
download_code();
// Set width
expand_form('75%');

// FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// none for the moment

// CODE MIRROR --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// Initialize CodeMirror instance
const codeTextArea = document.getElementById('code_zone');
    
// Initialize CodeMirror with the dark theme (dracula)
const editor = CodeMirror.fromTextArea(codeTextArea, {
  theme: 'dracula', // Use the 'dracula' theme
  mode: 'python',   // Set the mode to Python
  lineNumbers: true, // Show line numbers
});

// Synchronize scrolling between CodeMirror and line numbers
const lineNumbers = document.getElementById('lineNumbers');
editor.on('scroll', function () {
  lineNumbers.scrollTop = editor.getScrollInfo().top;
});

// UPDATE CODE --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function upload_code() {

  const inputValue = editor.getValue()
  
  const data = {
    code: inputValue
  };

  const response = await fetch('/upload_code', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  }).then(response => response.json());

  if (response.ok) {
    // Successfully saved configuration
    showMessage('Code saved successfully!', false);
    return true;

  } else {
      showMessage("Your code isn't working. Here's the compiler's output: <br><br>" + response.error + "<br><br>Please make sure to compile your code before saving it.", true);
    return false;
  }
}

// DOWNLOAD CODE --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function download_code() {

  const response = await fetch('/download_code').then(response => response);
  const responseData = await response.json();
    
  if (response.ok) {
    text = responseData.code;

    // Load previous code
    showMessage('Code time!', false);
    editor.setValue(text);
    return true;
  } else {
      showMessage("Your last code couldn't be loaded correctly. Please input it again, and don't use this as your default editor.", true);
    return false;
  }
}