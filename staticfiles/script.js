// JavaScript to toggle colorblind-friendly mode
const toggle = document.getElementById('colorblindToggle');
toggle.addEventListener('change', function() {
  if (this.checked) {
    document.body.classList.add('colorblind');
  } else {
    document.body.classList.remove('colorblind');
  }
});
