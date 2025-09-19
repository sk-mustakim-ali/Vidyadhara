const roleButtons = document.querySelectorAll(".role-btn");
const roleInput   = document.getElementById("roleInput");
const errorMsg    = document.getElementById("errorMessage");

// ----- Role selection -----
roleButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    roleButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    roleInput.value = btn.dataset.role;
    errorMsg.style.display = "none";
  });
});

// ----- Form submission -----
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  if (!roleInput.value) {
    errorMsg.textContent = "⚠️ Please select your role before logging in!";
    errorMsg.style.display = "block";
    return;
  }

  const username = e.target.username.value.trim();
  const password = e.target.password.value.trim();
  const role     = roleInput.value;

  try {
    // Adjust URL/port if your FastAPI server differs
    const res = await fetch("http://127.0.0.1:8000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, role })
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    if (data.success) {
      // Redirect to the page specified by your backend
      window.location.href = data.redirect;
    } else {
      errorMsg.textContent = data.message || "❌ Login failed!";
      errorMsg.style.display = "block";
    }
  } catch (err) {
    console.error("Login error:", err);
    errorMsg.textContent = "⚠️ Unable to reach server!";
    errorMsg.style.display = "block";
  }
});
