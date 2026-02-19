/* ════════════════════════════════════
   NAVBAR — scroll behaviour
════════════════════════════════════ */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
}, { passive: true });

/* ════════════════════════════════════
   HAMBURGER MENU
════════════════════════════════════ */
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobile-menu');

hamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');
});

document.querySelectorAll('.mobile-menu a').forEach(link => {
  link.addEventListener('click', () => mobileMenu.classList.remove('open'));
});

/* ════════════════════════════════════
   SMOOTH SCROLL (offset for fixed nav)
════════════════════════════════════ */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const top = target.getBoundingClientRect().top + window.scrollY - 80;
    window.scrollTo({ top, behavior: 'smooth' });
  });
});

/* ════════════════════════════════════
   SCROLL REVEAL (Intersection Observer)
════════════════════════════════════ */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 75);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* ════════════════════════════════════
   COUNTER ANIMATION
════════════════════════════════════ */
function animateCount(el) {
  const target = parseInt(el.dataset.target, 10);
  if (isNaN(target)) return;
  const duration = 1800;
  const startTime = performance.now();
  const step = (now) => {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target).toLocaleString();
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target.toLocaleString();
  };
  requestAnimationFrame(step);
}

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('[data-target]').forEach(animateCount);
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.4 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) statsObserver.observe(heroStats);

/* ════════════════════════════════════
   CHAT
════════════════════════════════════ */
const chatMessages = document.getElementById('chat-messages');
const userInput    = document.getElementById('user-input');
const sendBtn      = document.getElementById('send-btn');

function nowTime() {
  return new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
}

function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function scrollBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

/* Add a message bubble */
function addMessage(content, isUser = false, sources = []) {
  const wrap = document.createElement('div');
  wrap.className = `msg ${isUser ? 'user-msg' : 'bot-msg'}`;

  const avatarIcon = isUser ? 'fa-user' : 'fa-robot';

  let sourcesHtml = '';
  if (!isUser && sources.length) {
    sourcesHtml = `<div class="msg-sources">
      ${sources.map(s => `<span class="src-badge"><i class="fas fa-file-alt"></i>${s}</span>`).join('')}
    </div>`;
  }

  const bodyHtml = isUser
    ? `<p>${escHtml(content)}</p>`
    : marked.parse(content);

  wrap.innerHTML = `
    <div class="msg-avatar"><i class="fas ${avatarIcon}"></i></div>
    <div class="msg-bubble">
      ${bodyHtml}
      ${sourcesHtml}
      <div class="msg-time">${nowTime()}</div>
    </div>`;

  chatMessages.appendChild(wrap);
  scrollBottom();
}

/* Typing indicator */
function showTyping() {
  removeTyping();
  const wrap = document.createElement('div');
  wrap.id = 'typing-ind';
  wrap.className = 'typing-msg';
  wrap.innerHTML = `
    <div class="msg-avatar"><i class="fas fa-robot"></i></div>
    <div class="typing-bubble"><span></span><span></span><span></span></div>`;
  chatMessages.appendChild(wrap);
  scrollBottom();
}
function removeTyping() {
  const el = document.getElementById('typing-ind');
  if (el) el.remove();
}

/* Toggle loading state */
function setLoading(on) {
  sendBtn.disabled  = on;
  userInput.disabled = on;
  sendBtn.innerHTML  = on
    ? '<i class="fas fa-spinner fa-spin"></i>'
    : '<i class="fas fa-paper-plane"></i>';
}

/* Main send function */
async function sendMessage() {
  const query = userInput.value.trim();
  if (!query) return;

  addMessage(query, true);
  userInput.value = '';
  showTyping();
  setLoading(true);

  try {
    const res  = await fetch('/chat', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ message: query }),
    });
    const data = await res.json();
    removeTyping();

    if (data.error) {
      addMessage(`⚠️ Error: ${data.error}\n\nPlease ensure your GROQ_API_KEY is valid in the \`.env\` file.`);
    } else {
      addMessage(data.answer, false, data.sources || []);
    }
  } catch {
    removeTyping();
    addMessage('⚠️ Could not reach the server. Please make sure `app.py` is running.');
  } finally {
    setLoading(false);
    userInput.focus();
  }
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

/* Suggestion chips */
function useSuggestion(btn) {
  userInput.value = btn.textContent.trim();
  const chatSection = document.getElementById('chat');
  chatSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  setTimeout(() => sendMessage(), 400);
}

/* Clear chat */
function clearChat() {
  chatMessages.innerHTML = `
    <div class="msg bot-msg">
      <div class="msg-avatar"><i class="fas fa-robot"></i></div>
      <div class="msg-bubble">
        <p>Chat cleared! How can I help you? 🌾</p>
        <div class="msg-time">${nowTime()}</div>
      </div>
    </div>`;
}
