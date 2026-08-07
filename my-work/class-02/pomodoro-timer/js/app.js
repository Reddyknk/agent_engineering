/**
 * AuraFocus Main Coordinator
 * Tab navigation, theme management, background particle canvas, ambient audio drawer, settings.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Sub-Systems
  if (window.auraTimer) window.auraTimer.init();
  if (window.auraTasks) window.auraTasks.init();
  if (window.auraStats) window.auraStats.init();
  if (window.auraBreathing) window.auraBreathing.init();

  initThemeEngine();
  initTabNavigation();
  initTimerControls();
  initTaskForms();
  initAmbientDrawer();
  initSettingsModal();
  initZenMode();
  initQuotes();
  initBackgroundCanvas();
  initKeyboardShortcuts();
});

/* --------------------------------------------------------------------------
   1. Theme Management
   -------------------------------------------------------------------------- */
function initThemeEngine() {
  const themeBtn = document.getElementById('themeBtn');
  const themeMenu = document.getElementById('themeMenu');
  const themeOptions = document.querySelectorAll('.theme-option');

  const savedTheme = localStorage.getItem('aura_theme') || 'sage';
  setTheme(savedTheme);

  if (themeBtn && themeMenu) {
    themeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      themeMenu.classList.toggle('show');
    });

    document.addEventListener('click', () => {
      themeMenu.classList.remove('show');
    });
  }

  themeOptions.forEach(opt => {
    opt.addEventListener('click', (e) => {
      const val = e.currentTarget.getAttribute('data-theme-val');
      setTheme(val);
      themeMenu.classList.remove('show');
    });
  });
}

function setTheme(themeName) {
  document.documentElement.setAttribute('data-theme', themeName);
  localStorage.setItem('aura_theme', themeName);

  document.querySelectorAll('.theme-option').forEach(opt => {
    opt.classList.toggle('active', opt.getAttribute('data-theme-val') === themeName);
  });

  // Trigger chart re-render with new theme colors
  if (window.auraStats) {
    setTimeout(() => window.auraStats.renderChart(), 100);
  }
}

/* --------------------------------------------------------------------------
   2. Tab Navigation
   -------------------------------------------------------------------------- */
function initTabNavigation() {
  const navBtns = document.querySelectorAll('.nav-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');

      navBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetContent = document.getElementById(`tab-${targetTab}`);
      if (targetContent) targetContent.classList.add('active');

      if (targetTab === 'stats' && window.auraStats) {
        window.auraStats.updateStatsUI();
        window.auraStats.renderChart();
      }
    });
  });
}

/* --------------------------------------------------------------------------
   3. Timer Controls & Modes
   -------------------------------------------------------------------------- */
function initTimerControls() {
  const startPauseBtn = document.getElementById('startPauseBtn');
  const resetBtn = document.getElementById('resetBtn');
  const skipBtn = document.getElementById('skipBtn');
  const modeBtns = document.querySelectorAll('.mode-btn');
  const clearTaskBtn = document.getElementById('clearActiveTaskBtn');

  if (startPauseBtn) {
    startPauseBtn.addEventListener('click', () => {
      if (window.auraAudio) window.auraAudio.init();
      window.auraTimer.toggle();
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', () => window.auraTimer.resetTimer());
  }

  if (skipBtn) {
    skipBtn.addEventListener('click', () => window.auraTimer.skip());
  }

  modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const mode = btn.getAttribute('data-mode');
      window.auraTimer.setMode(mode);
    });
  });

  if (clearTaskBtn) {
    clearTaskBtn.addEventListener('click', () => {
      if (window.auraTasks) window.auraTasks.clearActiveTask();
    });
  }
}

/* --------------------------------------------------------------------------
   4. Task Form Handlers
   -------------------------------------------------------------------------- */
function initTaskForms() {
  const taskForm = document.getElementById('taskForm');
  const filterBtns = document.querySelectorAll('.filter-btn');

  if (taskForm) {
    taskForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = document.getElementById('taskInput');
      const pomoInput = document.getElementById('pomoEstInput');

      if (input && input.value.trim()) {
        window.auraTasks.addTask(input.value.trim(), pomoInput ? pomoInput.value : 1);
        input.value = '';
        if (pomoInput) pomoInput.value = 1;
      }
    });
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      filterBtns.forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      const filter = e.target.getAttribute('data-filter');
      window.auraTasks.setFilter(filter);
    });
  });
}

/* --------------------------------------------------------------------------
   5. Ambient Sound Drawer
   -------------------------------------------------------------------------- */
function initAmbientDrawer() {
  const toggleBtn = document.getElementById('ambientToggleBtn');
  const closeBtn = document.getElementById('closeAmbientBtn');
  const drawer = document.getElementById('ambientDrawer');
  const sliders = document.querySelectorAll('.volume-slider');
  const badge = document.getElementById('ambientBadge');

  if (toggleBtn && drawer) {
    toggleBtn.addEventListener('click', () => {
      drawer.classList.add('open');
      if (window.auraAudio) window.auraAudio.init();
    });
  }

  if (closeBtn && drawer) {
    closeBtn.addEventListener('click', () => drawer.classList.remove('open'));
  }

  sliders.forEach(slider => {
    slider.addEventListener('input', (e) => {
      const soundKey = e.target.closest('.sound-item').getAttribute('data-sound');
      const val = parseInt(e.target.value);
      if (window.auraAudio) {
        window.auraAudio.setVolume(soundKey, val);
        const count = window.auraAudio.getActiveCount();
        if (badge) {
          badge.style.display = count > 0 ? 'block' : 'none';
        }
      }
    });
  });
}

/* --------------------------------------------------------------------------
   6. Settings Modal
   -------------------------------------------------------------------------- */
function initSettingsModal() {
  const settingsBtn = document.getElementById('settingsBtn');
  const closeBtn = document.getElementById('closeSettingsBtn');
  const cancelBtn = document.getElementById('cancelSettingsBtn');
  const saveBtn = document.getElementById('saveSettingsBtn');
  const modal = document.getElementById('settingsModal');

  const pomoInput = document.getElementById('pomoTimeInput');
  const shortInput = document.getElementById('shortBreakInput');
  const longInput = document.getElementById('longBreakInput');
  const autoBreakToggle = document.getElementById('autoStartBreaksToggle');
  const autoPomoToggle = document.getElementById('autoStartPomosToggle');
  const soundToggle = document.getElementById('soundEnabledToggle');

  const populateSettings = () => {
    if (!window.auraTimer) return;
    const s = window.auraTimer.settings;
    if (pomoInput) pomoInput.value = s.pomodoro;
    if (shortInput) shortInput.value = s.shortBreak;
    if (longInput) longInput.value = s.longBreak;
    if (autoBreakToggle) autoBreakToggle.checked = s.autoStartBreaks;
    if (autoPomoToggle) autoPomoToggle.checked = s.autoStartPomos;
    if (soundToggle) soundToggle.checked = s.soundEnabled;
  };

  if (settingsBtn && modal) {
    settingsBtn.addEventListener('click', () => {
      populateSettings();
      modal.classList.add('show');
    });
  }

  const closeModal = () => modal.classList.remove('show');

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      const newSettings = {
        pomodoro: Math.max(1, parseInt(pomoInput.value) || 25),
        shortBreak: Math.max(1, parseInt(shortInput.value) || 5),
        longBreak: Math.max(1, parseInt(longInput.value) || 15),
        autoStartBreaks: autoBreakToggle ? autoBreakToggle.checked : false,
        autoStartPomos: autoPomoToggle ? autoPomoToggle.checked : false,
        soundEnabled: soundToggle ? soundToggle.checked : true
      };
      window.auraTimer.saveSettings(newSettings);
      closeModal();
    });
  }
}

/* --------------------------------------------------------------------------
   7. Zen Focus Mode
   -------------------------------------------------------------------------- */
function initZenMode() {
  const zenBtn = document.getElementById('zenToggleBtn');
  if (zenBtn) {
    zenBtn.addEventListener('click', () => {
      document.body.classList.toggle('zen-mode');
    });
  }
}

/* --------------------------------------------------------------------------
   8. Quotes Carousel
   -------------------------------------------------------------------------- */
function initQuotes() {
  const quotes = [
    { text: "Focus on being productive instead of busy.", author: "Tim Ferriss" },
    { text: "Simplicity is about subtracting the obvious and adding the meaningful.", author: "John Maeda" },
    { text: "It is not enough to be busy. The question is: what are we busy about?", author: "Henry David Thoreau" },
    { text: "Do one thing at a time, and do it well.", author: "Zen Proverb" },
    { text: "Peace comes from within. Do not seek it without.", author: "Buddha" },
    { text: "Your future is created by what you do today, not tomorrow.", author: "Robert Kiyosaki" }
  ];

  const textEl = document.getElementById('quoteText');
  const authorEl = document.getElementById('quoteAuthor');

  let idx = 0;
  setInterval(() => {
    idx = (idx + 1) % quotes.length;
    if (textEl && authorEl) {
      textEl.style.opacity = 0;
      authorEl.style.opacity = 0;
      setTimeout(() => {
        textEl.textContent = `"${quotes[idx].text}"`;
        authorEl.textContent = `— ${quotes[idx].author}`;
        textEl.style.opacity = 1;
        authorEl.style.opacity = 1;
      }, 300);
    }
  }, 12000);
}

/* --------------------------------------------------------------------------
   9. Background Canvas Particles
   -------------------------------------------------------------------------- */
function initBackgroundCanvas() {
  const canvas = document.getElementById('bgCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width = canvas.width = window.innerWidth;
  let height = canvas.height = window.innerHeight;

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const particles = [];
  const particleCount = 28;

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 3 + 1,
      dx: (Math.random() - 0.5) * 0.4,
      dy: (Math.random() - 0.5) * 0.4,
      alpha: Math.random() * 0.5 + 0.1
    });
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    particles.forEach(p => {
      p.x += p.dx;
      p.y += p.dy;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${p.alpha})`;
      ctx.fill();
    });

    requestAnimationFrame(animate);
  }

  animate();
}

/* --------------------------------------------------------------------------
   10. Keyboard Shortcuts
   -------------------------------------------------------------------------- */
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Ignore keypresses if user is typing in an input field
    if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

    if (e.code === 'Space') {
      e.preventDefault();
      if (window.auraAudio) window.auraAudio.init();
      if (window.auraTimer) window.auraTimer.toggle();
    } else if (e.key === 'r' || e.key === 'R') {
      if (window.auraTimer) window.auraTimer.resetTimer();
    } else if (e.key === 's' || e.key === 'S') {
      if (window.auraTimer) window.auraTimer.skip();
    } else if (e.key === 'Escape') {
      document.body.classList.remove('zen-mode');
    }
  });
}
