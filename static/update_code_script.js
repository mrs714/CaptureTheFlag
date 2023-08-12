function showMessage(message) { // Success/error loging
  document.getElementById('message_area').innerHTML = message; 
}

// UPDATE CONFIG --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function update_code() {

  const textarea = document.getElementById('code_zone');
  const inputValue = textarea.value;
  
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
