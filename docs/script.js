function toggleDarkMode() {
  var element = document.body;
  var button = document.getElementById("mode-toggle");
  element.classList.toggle("dark-mode");
  var theme = element.classList.contains("dark-mode") ? "dark" : "light";
  localStorage.setItem("theme", theme);
  button.textContent = theme === "dark" ? "Enable Light Mode" : "Enable Dark Mode";
}

// Apply the saved theme and button label on page load
window.onload = function () {
  var theme = localStorage.getItem("theme");
  var button = document.getElementById("mode-toggle");
  if (theme === "dark") {
    document.body.classList.add("dark-mode");
    button.textContent = "Enable Light Mode";
  }
};
