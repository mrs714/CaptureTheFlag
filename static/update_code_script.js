// UPDATE CONFIG --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function update_code() {

  const textarea = document.getElementById('code_zone');
  const inputValue = textarea.value;

  console.log("Code: ");
  console.log(inputValue);
  
  const data = {
    code: inputValue
  };

  const response = await fetch('/save_code', {
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
      showMessage('Something went wrong. Please try again later.');
    }
    return false;
  }
}