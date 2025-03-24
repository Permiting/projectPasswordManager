(function(){
  function runMyCode(){
    console.log("obfuscated.js loaded successfully.");
    var themeToggle = document.getElementById("themeToggle");
    if (!themeToggle) {
      console.error("Theme toggle button not found.");
      return;
    }
    themeToggle.addEventListener("click", function(){
      document.body.classList.toggle("dark-theme");
      console.log("Theme toggled. Current class:", document.body.className);
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runMyCode);
  } else {
    runMyCode();
  }
})();

