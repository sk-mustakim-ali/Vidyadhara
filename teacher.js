// Sidebar navigation
const buttons = [...document.querySelectorAll(".menu button,[data-target]")];
const sections = [...document.querySelectorAll(".section")];
function show(id) {
  sections.forEach((s) => s.classList.toggle("active", s.id === id));
  document
    .querySelectorAll(".menu button")
    .forEach((b) => b.classList.toggle("active", b.dataset.target === id));
  document.body.classList.remove("sidebar-open");
  if (location.hash !== "#" + id) history.replaceState({}, "", "#" + id);
}
buttons.forEach((b) =>
  b.addEventListener("click", () => {
    const id = b.dataset.target;
    if (id) show(id);
  })
);
if (location.hash) {
  const id = location.hash.slice(1);
  if (document.getElementById(id)) show(id);
}

// Mobile menu
const menuToggle = document.getElementById("menuToggle");
if (menuToggle) {
  menuToggle.addEventListener("click", () => {
    document.body.classList.toggle("sidebar-open");
  });
}

// Study Material interactions
const pdfInput = document.getElementById("pdfInput");
const pdfSelected = document.getElementById("pdfSelected");
if (pdfInput)
  pdfInput.addEventListener("change", () => {
    pdfSelected.style.display = pdfInput.files.length ? "block" : "none";
    if (pdfInput.files[0])
      pdfSelected.textContent = "Selected: " + pdfInput.files[0].name;
  });
const videoUrl = document.getElementById("videoUrl");
const videoFrame = document.getElementById("videoFrame");
const iframe = document.getElementById("iframe");
if (videoUrl)
  videoUrl.addEventListener("change", () => {
    const url = computeEmbedUrl(videoUrl.value);
    iframe.src = url;
    videoFrame.style.display = "block";
  });
function computeEmbedUrl(url) {
  try {
    const u = new URL(url);
    if (u.hostname.includes("youtube.com")) {
      const v = u.searchParams.get("v");
      if (v) return "https://www.youtube.com/embed/" + v;
    }
    if (u.hostname.includes("youtu.be")) {
      const id = u.pathname.slice(1);
      if (id) return "https://www.youtube.com/embed/" + id;
    }
    return url;
  } catch {
    return url;
  }
}

// Quizzes – dynamic MCQs
const quizList = document.getElementById("quizList");
const addQ = document.getElementById("addQ");
let qCount = 0;
function addQuestion() {
  qCount++;
  const wrap = document.createElement("div");
  wrap.className = "card";
  wrap.innerHTML = `<div class="hd" style="display:flex;justify-content:space-between;align-items:center"><div><div class="title">Question ${qCount}</div><div class="desc">Provide the question and options</div></div><div><button class="btn" data-add="1">➕</button> <button class="btn" data-remove="1">🗑</button></div></div>
  <div class="bd grid" style="gap:10px"><div class="field"><label>Question</label><input placeholder="Type your question"></div>
  <div class="grid" style="display:grid;gap:10px;grid-template-columns:1fr 1fr"><div class="field"><label>Option A</label><input></div><div class="field"><label>Option B</label><input></div><div class="field"><label>Option C</label><input></div><div class="field"><label>Option D</label><input></div></div>
  <div class="field" style="max-width:220px"><label>Correct Answer</label><select><option value="0">Option A</option><option value="1">Option B</option><option value="2">Option C</option><option value="3">Option D</option></select></div></div>`;
  wrap.querySelector("[data-add]")?.addEventListener("click", addQuestion);
  wrap
    .querySelector("[data-remove]")
    ?.addEventListener("click", () => wrap.remove());
  quizList.appendChild(wrap);
}
if (addQ) {
  addQ.addEventListener("click", addQuestion);
  addQuestion();
}

// Challenges lobby
const codeInput = document.getElementById("invite");
const regen = document.getElementById("regen");
const copy = document.getElementById("copyCode");
const playersEl = document.getElementById("players");
const addPlayer = document.getElementById("addPlayer");
function randomCode() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  return Array.from(
    { length: 6 },
    () => chars[Math.floor(Math.random() * chars.length)]
  ).join("");
}
function chip(name) {
  const el = document.createElement("span");
  el.textContent = name;
  el.style.cssText =
    "padding:6px 10px;border-radius:999px;background:rgba(37,99,235,.12);color:var(--brand);font-size:13px";
  return el;
}
if (codeInput) {
  codeInput.value = randomCode();
}
if (regen) {
  regen.addEventListener("click", () => {
    codeInput.value = randomCode();
  });
}
if (copy) {
  copy.addEventListener("click", () => {
    navigator.clipboard.writeText(codeInput.value);
  });
}
if (playersEl) {
  ["Rahul", "Isha", "Karan"].forEach((n) => playersEl.appendChild(chip(n)));
}
if (addPlayer) {
  addPlayer.addEventListener("click", () =>
    playersEl.appendChild(chip("Guest-" + (playersEl.children.length + 1)))
  );
}

// Settings – dark mode
const darkToggle = document.getElementById("darkToggle");
if (darkToggle) {
  darkToggle.addEventListener("change", (e) => {
    document.documentElement.classList.toggle("dark", e.target.checked);
  });
}
const chatButton = document.getElementById("chatbot-button");
const chatPopup = document.getElementById("chatbot-popup");
const closeChat = document.getElementById("close-chat");
const sendBtn = document.getElementById("sendBtn");
const chatInput = document.getElementById("chatInput");
const chatBody = document.getElementById("chatBody");

chatButton.addEventListener("click", () => {
  chatPopup.style.display = "flex";
  chatButton.style.display = "none";
});

closeChat.addEventListener("click", () => {
  chatPopup.style.display = "none";
  chatButton.style.display = "flex";
});

sendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  let msg = chatInput.value.trim();
  if (msg === "") return;
  let userMsg = document.createElement("p");
  userMsg.className = "user";
  userMsg.textContent = msg;
  chatBody.appendChild(userMsg);

  chatInput.value = "";
  chatBody.scrollTop = chatBody.scrollHeight;

  // Dummy bot response
  setTimeout(() => {
    let botMsg = document.createElement("p");
    botMsg.className = "bot";
    botMsg.textContent = "🤖 This is a bot reply!";
    chatBody.appendChild(botMsg);
    chatBody.scrollTop = chatBody.scrollHeight;
  }, 600);
}