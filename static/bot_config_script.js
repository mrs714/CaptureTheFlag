const sliders = document.querySelectorAll('.form-control-range');
const totalPointsDisplay = document.getElementById('totalPoints');
let totalPoints = 300;

sliders.forEach(slider => {
  slider.addEventListener('input', () => {
    totalPoints = 300 - sliders.reduce((total, slider) => total + parseInt(slider.value), 0);
    totalPointsDisplay.textContent = `Total Points: ${totalPoints}`;
  });
});
</script>