// ----- Subject data -----
const subjects = {
  math: {
    title: '🧮 Math Village Shop',
    description: 'Learn math through village marketplace activities! Count coins, measure grains, and solve real-world problems.',
    activities: [
      { name: 'Coin Counting', icon: '🪙', description: 'Practice addition with village shop transactions' },
      { name: 'Weight & Measures', icon: '⚖', description: 'Learn measurement using traditional scales' },
      { name: 'Market Problems', icon: '🛒', description: 'Solve real marketplace math challenges' },
      { name: 'Pattern Games', icon: '🔢', description: 'Discover patterns in nature and village life' }
    ]
  },
  science: {
    title: '🔬 Science Farm Hut',
    description: 'Discover science through farming and nature! Explore plants, water, weather, and animal care.',
    activities: [
      { name: 'Plant Growth', icon: '🌱', description: 'Study how plants grow and what they need' },
      { name: 'Water Cycle', icon: '💧', description: 'Explore water in village wells and rain' },
      { name: 'Animal Care', icon: '🐄', description: 'Learn about farm animals and their needs' },
      { name: 'Weather Watch', icon: '🌤', description: 'Observe and predict weather patterns' }
    ]
  },
  tech: {
    title: '💻 Tech Community Center',
    description: 'Learn technology and coding through fun games and problem-solving activities!',
    activities: [
      { name: 'Basic Coding', icon: '📱', description: 'Start coding with simple, fun commands' },
      { name: 'Logic Puzzles', icon: '🧩', description: 'Solve problems using logical thinking' },
      { name: 'Digital Stories', icon: '📺', description: 'Create digital stories and presentations' },
      { name: 'Tech Tools', icon: '🔧', description: 'Learn about useful technology tools' }
    ]
  },
  engineering: {
    title: '⚙ Engineering Workshop',
    description: 'Build and create! Learn engineering through pulleys, levers, and building challenges.',
    activities: [
      { name: 'Simple Machines', icon: '🔩', description: 'Explore pulleys, levers, and wheels' },
      { name: 'Bridge Building', icon: '🌉', description: 'Design and build strong structures' },
      { name: 'Water Systems', icon: '🚰', description: 'Learn about village water supply systems' },
      { name: 'Solar Energy', icon: '☀', description: 'Discover renewable energy sources' }
    ]
  },
  language: {
    title: '📖 Storytelling Tree',
    description: 'Master languages through stories, grammar games, and regional tales!',
    activities: [
      { name: 'Folk Tales', icon: '📚', description: 'Read and listen to local folk stories' },
      { name: 'Grammar Games', icon: '✏', description: 'Learn grammar through fun activities' },
      { name: 'Word Puzzles', icon: '🔤', description: 'Build vocabulary with word games' },
      { name: 'Story Writing', icon: '📝', description: 'Create your own stories and poems' }
    ]
  }
};

let selectedActivity = null;

// ----- Modal handling -----
function openSubject(subjectKey) {
  const subject = subjects[subjectKey];
  document.getElementById('modal-title').textContent = subject.title;
  document.getElementById('modal-description').textContent = subject.description;
  const activityGrid = document.getElementById('activity-grid');
  activityGrid.innerHTML = '';

  subject.activities.forEach(activity => {
    const card = document.createElement('div');
    card.className = 'activity-card';
    card.innerHTML = `
      <div style="font-size:2rem;margin-bottom:0.5rem;">${activity.icon}</div>
      <div style="font-weight:bold;margin-bottom:0.5rem;">${activity.name}</div>
      <div style="font-size:0.8rem;color:#666;">${activity.description}</div>`;
    card.onclick = (e) => selectActivity(activity.name, e);
    activityGrid.appendChild(card);
  });

  document.getElementById('subjectModal').style.display = 'block';
  updateStars(5);
}

function closeModal() {
  document.getElementById('subjectModal').style.display = 'none';
  selectedActivity = null;
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('.close').onclick = closeModal;
  window.onclick = function(e){
    if (e.target === document.getElementById('subjectModal')) closeModal();
  };
});

// ----- Buttons -----
function startLearning() {
  showNotification('🎉 Welcome to Village Learning! Choose a subject hub to begin your adventure!','success');
  document.querySelector('.village-scene').scrollIntoView({behavior:'smooth'});
  updateStars(3);
}

function downloadPacks(event) {
  const loadingBtn = event.target;
  const originalText = loadingBtn.innerHTML;
  loadingBtn.innerHTML = '<span class="loading"></span> Downloading...';
  loadingBtn.disabled = true;

  let progress = 0;
  const downloadInterval = setInterval(() => {
    progress += 10;
    if (progress >= 100) {
      clearInterval(downloadInterval);
      showNotification('📥 Offline packs downloaded successfully!\n\n📦 Downloaded:\n• Math Challenge Pack\n• Science Experiment Pack\n• Language Story Pack\n• Engineering Building Pack\n• Tech Coding Pack','success');
      loadingBtn.innerHTML = originalText;
      loadingBtn.disabled = false;
      updateStars(10);
    }
  }, 200);
}

function selectActivity(activityName, e) {
  selectedActivity = activityName;
  document.querySelectorAll('.activity-card').forEach(card => {
    card.style.background = 'linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,215,0,0.3))';
    card.style.transform = 'scale(1)';
  });
  e.currentTarget.style.background = 'linear-gradient(135deg, #FFD700, #FFA500)';
  e.currentTarget.style.transform = 'scale(1.05)';
  showMiniCelebration(e.currentTarget);
}

function startActivity() {
  if (selectedActivity) {
    showNotification(`🚀 Starting "${selectedActivity}"!\n\nGet ready for an exciting learning adventure!\n\n⭐ Earn stars by completing challenges\n🏅 Unlock badges for achievements\n📊 Track your progress on the road to Village Science Fair!`, 'success');
    closeModal();
    updateStars(15);
    simulateActivityProgress();
  } else {
    showNotification('Please select an activity first! 🎯','warning');
  }
}

// ----- Stars & Progress -----
function updateStars(gained) {
  const starsElement = document.getElementById('stars-count');
  const currentStars = parseInt(starsElement.textContent);
  const newStars = currentStars + gained;

  let current = currentStars;
  const increment = gained / 20;
  const interval = setInterval(() => {
    current += increment;
    starsElement.textContent = Math.floor(current);
    if (current >= newStars) {
      starsElement.textContent = newStars;
      clearInterval(interval);
      if (gained >= 10) showCelebration();
      updateProgressBar();
      saveProgress();
    }
  }, 50);
}

function updateProgressBar() {
  const starsCount = parseInt(document.getElementById('stars-count').textContent);
  const progressFill = document.querySelector('.progress-fill');
  const progressPercentage = Math.min((starsCount/1000)*100,100);
  progressFill.style.width = progressPercentage + '%';
}

// ----- Notifications -----
function showNotification(message,type='info'){
  const notification = document.createElement('div');
  const bgColors = {
    success:'linear-gradient(45deg,#2E8B57,#32CD32)',
    warning:'linear-gradient(45deg,#FF8C00,#FFD700)',
    info:'linear-gradient(45deg,#4169E1,#87CEEB)',
    error:'linear-gradient(45deg,#DC143C,#FF6347)'
  };
  notification.innerHTML = message;
  notification.style.cssText = `
    position:fixed;top:20px;right:20px;
    background:${bgColors[type]};
    color:white;padding:1rem 2rem;border-radius:15px;
    font-weight:bold;z-index:3000;
    animation:slideInRight 0.5s ease-out;
    box-shadow:0 8px 16px rgba(0,0,0,0.3);
    border:2px solid white;
    max-width:400px;white-space:pre-line;text-align:center;`;
  document.body.appendChild(notification);

  setTimeout(()=>{
    notification.style.animation='slideOutRight 0.5s ease-out';
    setTimeout(()=>notification.remove(),500);
  },4000);
}

// ----- Mini effects -----
function showCelebration(){
  const celebration=document.createElement('div');
  celebration.innerHTML='🎉 Excellent work! +⭐ Stars earned! 🌟';
  celebration.style.cssText=`
    position:fixed;top:50%;left:50%;
    transform:translate(-50%,-50%);
    background:linear-gradient(45deg,#FFD700,#FFA500);
    color:white;padding:1.5rem 2.5rem;border-radius:25px;
    font-size:1.5rem;font-weight:bold;z-index:2000;
    animation:celebrationPulse 2.5s ease-in-out;
    box-shadow:0 12px 24px rgba(0,0,0,0.4);
    border:3px solid white;text-align:center;`;
  document.body.appendChild(celebration);
  createFloatingStars();
  setTimeout(()=>celebration.remove(),2500);
}

function showMiniCelebration(element){
  const rect = element.getBoundingClientRect();
  const mini=document.createElement('div');
  mini.innerHTML='✨';
  mini.style.cssText=`
    position:fixed;top:${rect.top + 10}px;
    left:${rect.left + rect.width/2}px;
    transform:translateX(-50%);
    font-size:1.5rem;z-index:1000;
    animation:miniPop 1s ease-out forwards;
    pointer-events:none;`;
  document.body.appendChild(mini);
  setTimeout(()=>mini.remove(),1000);
}

function createFloatingStars(){
  for (let i=0;i<12;i++){
    const star=document.createElement('div');
    star.innerHTML=['⭐','🌟','✨','💫'][Math.floor(Math.random()*4)];
    star.style.cssText=`
      position:fixed;top:50%;left:50%;
      font-size:2rem;z-index:1999;
      animation:floatStar 3s ease-out forwards;
      animation-delay:${i*0.1}s;pointer-events:none;`;
    const angle=(i/12)*360;
    star.style.setProperty('--angle', angle + 'deg');
    document.body.appendChild(star);
    setTimeout(()=>star.remove(),3000);
  }
}

// ----- Progress & Badges -----
function simulateActivityProgress(){
  let progress=0;
  const interval=setInterval(()=>{
    progress+=20;
    if(progress<=100){
      showNotification(`Activity Progress: ${progress}%`,'info');
      if(progress===100){
        clearInterval(interval);
        showNotification('🎊 Activity Completed! Great job! 🏆','success');
        updateStars(20);
        updateBadges();
      }
    }
  },1000);
}

function updateBadges(){
  const badgesElement=document.getElementById('badges-count');
  const currentBadges=parseInt(badgesElement.textContent);
  const starsCount=parseInt(document.getElementById('stars-count').textContent);
  if(starsCount>=300 && currentBadges<10){
    const newBadges=Math.min(10,currentBadges+1);
    badgesElement.textContent=newBadges;
    showNotification(`🏅 New Badge Earned! You now have ${newBadges} badges!`,'success');
  }
}

function saveProgress(){
  const progress={
    stars:parseInt(document.getElementById('stars-count').textContent),
    badges:parseInt(document.getElementById('badges-count').textContent),
    level:5,
    lastActivity:selectedActivity,
    timestamp:new Date().toISOString()
  };
  localStorage.setItem('villagelearning_progress', JSON.stringify(progress));
}

function loadProgress(){
  const saved = localStorage.getItem('villagelearning_progress');
  if(saved){
    const progress = JSON.parse(saved);
    document.getElementById('stars-count').textContent = progress.stars || 247;
    document.getElementById('badges-count').textContent = progress.badges || 8;
    updateProgressBar();
  }
}

document.addEventListener('DOMContentLoaded',()=>{
  loadProgress();
  document.querySelectorAll('.subject-hub').forEach(hub=>{
    hub.addEventListener('mouseenter',()=>hub.style.transform='scale(1.05) translateY(-2px)');
    hub.addEventListener('mouseleave',()=>hub.style.transform='scale(1) translateY(0)');
  });
  window.addEventListener('online',()=>showNotification('🌐 Online! Syncing progress...','success'));
  window.addEventListener('offline',()=>showNotification('📱 Offline mode active. Progress saved locally.','info'));
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape' && document.getElementById('subjectModal').style.display==='block') closeModal();
  });
  setTimeout(()=>showNotification('🎪 Welcome to Village Learning Mela! Start your educational journey! 🌟','success'),2000);
});

// ----- Animations CSS -----
const styleSheet = document.createElement('style');
styleSheet.textContent = `
@keyframes celebrationPulse {
  0%{transform:translate(-50%,-50%) scale(0) rotate(0deg);opacity:0;}
  30%{transform:translate(-50%,-50%) scale(1.3) rotate(10deg);opacity:1;}
  70%{transform:translate(-50%,-50%) scale(1.1) rotate(-5deg);opacity:1;}
  100%{transform:translate(-50%,-50%) scale(1) rotate(0deg);opacity:0;}
}
@keyframes miniPop {
  0%{transform:translateX(-50%) translateY(0) scale(0);opacity:0;}
  50%{transform:translateX(-50%) translateY(-20px) scale(1.5);opacity:1;}
  100%{transform:translateX(-50%) translateY(-40px) scale(0);opacity:0;}
}
@keyframes floatStar {
  0%{transform:translate(-50%,-50%) rotate(0deg) translateX(0) rotate(0deg);opacity:1;}
  100%{transform:translate(-50%,-50%) rotate(var(--angle)) translateX(150px) rotate(360deg);opacity:0;}
}
@keyframes slideInRight {from{transform:translateX(100%);opacity:0;}to{transform:translateX(0);opacity:1;}}
@keyframes slideOutRight {from{transform:translateX(0);opacity:1;}to{transform:translateX(100%);opacity:0;}}
`;
document.head.appendChild(styleSheet);

// ----- Chatbot -----
const chatButton=document.getElementById("chatbot-button");
const chatPopup=document.getElementById("chatbot-popup");
const closeChat=document.getElementById("close-chat");
const sendBtn=document.getElementById("sendBtn");
const chatInput=document.getElementById("chatInput");
const chatBody=document.getElementById("chatBody");

chatButton.addEventListener("click",()=>{
  chatPopup.style.display="flex";
  chatButton.style.display="none";
});
closeChat.addEventListener("click",()=>{
  chatPopup.style.display="none";
  chatButton.style.display="flex";
});
sendBtn.addEventListener("click",sendMessage);
chatInput.addEventListener("keypress",e=>{if(e.key==="Enter") sendMessage();});

async function sendMessage(){
  let msg = chatInput.value.trim();
  if(msg==="") return;

  // Show user message
  let userMsg=document.createElement("p");
  userMsg.className="user";
  userMsg.textContent=msg;
  chatBody.appendChild(userMsg);
  chatInput.value="";
  chatBody.scrollTop=chatBody.scrollHeight;

  try {
    // 🔗 Send to Flask backend
    const res = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: msg, user_id: "student123" })
    });

    const data = await res.json();

    let botMsg=document.createElement("p");
    botMsg.className="bot";
    botMsg.textContent=data.data?.response_text || "⚠️ No reply from AI";
    chatBody.appendChild(botMsg);
    chatBody.scrollTop=chatBody.scrollHeight;

  } catch (err) {
    let botMsg=document.createElement("p");
    botMsg.className="bot";
    botMsg.textContent="❌ Error connecting to server";
    chatBody.appendChild(botMsg);
    chatBody.scrollTop=chatBody.scrollHeight;
  }
}
