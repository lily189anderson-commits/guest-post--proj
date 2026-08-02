// If already logged in, skip straight to the dashboard.
if (getToken()) {
  window.location.href = "/dashboard.html";
}

const loginForm = document.getElementById("loginForm");
const loginError = document.getElementById("loginError");
const loginBtn = document.getElementById("loginBtn");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  loginError.hidden = true;
  loginBtn.disabled = true;
  loginBtn.textContent = "Signing in…";

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  try {
    const result = await api.login(username, password);
    setToken(result.access_token);
    window.location.href = "/dashboard.html";
  } catch (err) {
    loginError.textContent = err.message || "Invalid username or password";
    loginError.hidden = false;
    loginBtn.disabled = false;
    loginBtn.textContent = "Sign In";
  }
});
