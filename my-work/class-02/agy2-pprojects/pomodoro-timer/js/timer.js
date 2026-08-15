/**
 * AuraFocus Timer Controller
 * Precision countdown timer, SVG progress rendering, phase transitions.
 */
class AuraTimer {
  constructor() {
    this.settings = {
      pomodoro: 25,
      shortBreak: 5,
      longBreak: 15,
      autoStartBreaks: false,
      autoStartPomos: false,
      soundEnabled: true
    };

    this.mode = 'pomodoro'; // 'pomodoro' | 'shortBreak' | 'longBreak'
    this.remainingSeconds = 25 * 60;
    this.totalSeconds = 25 * 60;
    this.isRunning = false;
    this.timerId = null;
    this.completedCycles = 0; // 0 to 4

    this.circleRadius = 130;
    this.circumference = 2 * Math.PI * this.circleRadius;

    this.onTick = null;
    this.onComplete = null;
  }

  init() {
    this.loadSettings();
    this.updateDisplay();
    this.requestNotificationPermission();
  }

  loadSettings() {
    const saved = localStorage.getItem('aura_timer_settings');
    if (saved) {
      try {
        this.settings = { ...this.settings, ...JSON.parse(saved) };
      } catch (e) {}
    }
    this.totalSeconds = this.settings[this.mode] * 60;
    this.remainingSeconds = this.totalSeconds;
  }

  saveSettings(newSettings) {
    this.settings = { ...this.settings, ...newSettings };
    localStorage.setItem('aura_timer_settings', JSON.stringify(this.settings));
    if (!this.isRunning) {
      this.resetTimer();
    }
  }

  requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }

  setMode(newMode) {
    if (this.mode === newMode) return;
    this.mode = newMode;
    this.resetTimer();
  }

  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    const startTime = Date.now();
    const initialRemaining = this.remainingSeconds;

    this.timerId = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      this.remainingSeconds = Math.max(0, initialRemaining - elapsed);
      
      this.updateDisplay();
      if (this.onTick) this.onTick(this.remainingSeconds);

      if (this.remainingSeconds <= 0) {
        this.completePhase();
      }
    }, 1000);

    this.updateDisplay();
  }

  pause() {
    if (!this.isRunning) return;
    this.isRunning = false;
    clearInterval(this.timerId);
    this.timerId = null;
    this.updateDisplay();
  }

  toggle() {
    if (this.isRunning) {
      this.pause();
    } else {
      this.start();
    }
  }

  resetTimer() {
    this.pause();
    this.totalSeconds = (this.settings[this.mode] || 25) * 60;
    this.remainingSeconds = this.totalSeconds;
    this.updateDisplay();
  }

  skip() {
    this.pause();
    this.completePhase(true); // skipped
  }

  completePhase(wasSkipped = false) {
    this.pause();

    if (!wasSkipped) {
      // Play chime sound
      if (this.settings.soundEnabled && window.auraAudio) {
        window.auraAudio.playChime();
      }

      // Show Desktop Notification
      if ('Notification' in window && Notification.permission === 'granted') {
        const title = this.mode === 'pomodoro' ? 'Focus Session Completed! 🌟' : 'Break Finished! 🔔';
        const body = this.mode === 'pomodoro' ? 'Time for a refreshing break.' : 'Ready to dive back into deep focus?';
        new Notification(title, { body, icon: 'https://cdn-icons-png.flaticon.com/512/3208/3208726.png' });
      }

      // Record Stats & Task Progress
      if (this.mode === 'pomodoro') {
        const minutesSpent = this.settings.pomodoro;
        if (window.auraStats) window.auraStats.logSession(minutesSpent);
        if (window.auraTasks) window.auraTasks.incrementActiveTaskPomo();

        this.completedCycles = (this.completedCycles + 1) % 4;
      }
    }

    // Determine Next Phase
    let nextMode = 'pomodoro';
    if (this.mode === 'pomodoro') {
      nextMode = (this.completedCycles === 0 && !wasSkipped) ? 'longBreak' : 'shortBreak';
    } else {
      nextMode = 'pomodoro';
    }

    this.mode = nextMode;
    this.resetTimer();

    // Auto-start handling
    const shouldAutoStart = (nextMode === 'pomodoro' && this.settings.autoStartPomos) ||
                            (nextMode !== 'pomodoro' && this.settings.autoStartBreaks);
    if (shouldAutoStart && !wasSkipped) {
      setTimeout(() => this.start(), 1000);
    }

    if (this.onComplete) this.onComplete(this.mode);
  }

  updateDisplay() {
    const mins = Math.floor(this.remainingSeconds / 60);
    const secs = this.remainingSeconds % 60;
    const timeStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

    // Update DOM element
    const timeEl = document.getElementById('timerTime');
    if (timeEl) timeEl.textContent = timeStr;

    // Update SVG progress ring
    const circle = document.getElementById('timerProgressCircle');
    if (circle) {
      const progress = this.remainingSeconds / this.totalSeconds;
      const offset = this.circumference * (1 - progress);
      circle.style.strokeDashoffset = offset;
    }

    // Update Document Title
    const phaseName = this.mode === 'pomodoro' ? 'Focus' : (this.mode === 'shortBreak' ? 'Short Break' : 'Long Break');
    document.title = `${timeStr} - ${phaseName} | AuraFocus`;

    // Update Start/Pause Button Icon & Text
    const startPauseText = document.getElementById('startPauseText');
    const startPauseIcon = document.getElementById('startPauseIcon');
    if (startPauseText) startPauseText.textContent = this.isRunning ? 'Pause' : 'Start';
    if (startPauseIcon) startPauseIcon.setAttribute('data-lucide', this.isRunning ? 'pause' : 'play');
    if (window.lucide) window.lucide.createIcons();

    // Update Cycle Dots
    const dotsContainer = document.getElementById('cycleDots');
    if (dotsContainer) {
      const dots = dotsContainer.querySelectorAll('.cycle-dot');
      dots.forEach((dot, idx) => {
        dot.classList.toggle('active', idx <= this.completedCycles && this.mode === 'pomodoro');
      });
    }

    // Phase Label
    const phaseLabel = document.getElementById('timerPhaseLabel');
    if (phaseLabel) {
      if (this.mode === 'pomodoro') phaseLabel.textContent = 'Time to Focus';
      else if (this.mode === 'shortBreak') phaseLabel.textContent = 'Short Refresh';
      else phaseLabel.textContent = 'Deep Rest Break';
    }
  }
}

window.auraTimer = new AuraTimer();
