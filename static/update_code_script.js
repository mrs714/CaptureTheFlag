code = document.getElementById('code').value;
// obtain text
code = code.value;

// UPDATE CONFIG --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function update_code() {
  console.log("Code: ");
  console.log(code);
  const data = {
    code: code
  };

  const response = await fetch('/save_config', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (response.ok) {
    // Successfully saved configuration
    return true;

  } else {
    if (response.status == 400) {
      showMessage('Incorrect ammount of points. Please try again.');
    }
    return false;
  }
}