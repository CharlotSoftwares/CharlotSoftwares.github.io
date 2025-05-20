// script.js
function toggleDarkMode() {
var element = document.body;
element.classList.toggle("dark-mode");
var theme = element.classList.contains("dark-mode") ? "dark" : "light";
localStorage.setItem("theme", theme);
}

// Apply the saved theme on page load
window.onload = function() {
var theme = localStorage.getItem("theme");
if (theme === "dark") {
document.body.classList.add("dark-mode");
}
}
