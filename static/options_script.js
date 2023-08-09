function toggleDarkMode() {
    if (document.body.classList.contains('dark-mode-body')) {

        document.body.classList.remove('dark-mode-body');
        document.body.classList.add('light-mode-body');
        modifyContainerStyleDark();
    } 
    
    else if (document.body.classList.contains('light-mode-body')) {

        document.body.classList.remove('light-mode-body');
        document.body.classList.add('dark-mode-body');
        modifyContainerStyleLight();
    }

    else { 
        document.body.classList.add('dark-mode-body');
        document.container.classList.add('dark-mode-container');
        modifyContainerStyleDark();
    }
}

function modifyContainerStyleDark() {
    const containerElements = document.querySelectorAll('.container');
    
    containerElements.forEach(element => {
      element.style.backgroundColor = 'lightblue';
    });
  }

function modifyContainerStyleLight() {
    const containerElements = document.querySelectorAll('.container');
    
    containerElements.forEach(element => {
      element.style.backgroundColor = 'darkblue';
    });
  }