/**
 * AuraFocus Guided Breathing Engine
 * Provides Box Breathing, 4-7-8 Relaxing, and Deep Calm breathing exercises.
 */
class AuraBreathing {
  constructor() {
    this.techniques = {
      box: [
        { phase: 'Inhale', duration: 4, scale: 1.4 },
        { phase: 'Hold', duration: 4, scale: 1.4 },
        { phase: 'Exhale', duration: 4, scale: 1.0 },
        { phase: 'Hold', duration: 4, scale: 1.0 }
      ],
      relax: [
        { phase: 'Inhale', duration: 4, scale: 1.4 },
        { phase: 'Hold', duration: 7, scale: 1.4 },
        { phase: 'Exhale', duration: 8, scale: 1.0 }
      ],
      calm: [
        { phase: 'Inhale', duration: 4, scale: 1.4 },
        { phase: 'Exhale', duration: 6, scale: 1.0 }
      ]
    };

    this.currentTechnique = 'box';
    this.isActive = false;
    this.stepIndex = 0;
    this.phaseRemaining = 0;
    this.intervalId = null;
  }

  init() {
    this.bindEvents();
  }

  bindEvents() {
    const btn = document.getElementById('startBreathingBtn');
    if (btn) {
      btn.addEventListener('click', () => this.toggle());
    }

    const techBtns = document.querySelectorAll('.technique-btn');
    techBtns.forEach(b => {
      b.addEventListener('click', (e) => {
        techBtns.forEach(t => t.classList.remove('active'));
        e.target.classList.add('active');
        this.currentTechnique = e.target.getAttribute('data-technique');
        if (this.isActive) this.stop();
        else this.resetUI();
      });
    });
  }

  toggle() {
    if (this.isActive) {
      this.stop();
    } else {
      this.start();
    }
  }

  start() {
    this.isActive = true;
    this.stepIndex = 0;

    const btn = document.getElementById('startBreathingBtn');
    if (btn) btn.textContent = 'End Exercise';

    this.runNextPhase();
  }

  stop() {
    this.isActive = false;
    if (this.intervalId) clearInterval(this.intervalId);
    this.intervalId = null;

    const btn = document.getElementById('startBreathingBtn');
    if (btn) btn.textContent = 'Start Exercise';

    this.resetUI();
  }

  resetUI() {
    const circle = document.getElementById('breathingCircle');
    const label = document.getElementById('breathingInstruction');
    const timer = document.getElementById('breathingPhaseTimer');

    if (circle) circle.style.transform = 'scale(1.0)';
    if (label) label.textContent = 'Press Start';
    if (timer) timer.textContent = '';
  }

  runNextPhase() {
    if (!this.isActive) return;

    const steps = this.techniques[this.currentTechnique];
    const currentStep = steps[this.stepIndex];

    const circle = document.getElementById('breathingCircle');
    const label = document.getElementById('breathingInstruction');
    const timer = document.getElementById('breathingPhaseTimer');

    if (circle) {
      circle.style.transition = `transform ${currentStep.duration}s ease-in-out`;
      circle.style.transform = `scale(${currentStep.scale})`;
    }
    if (label) label.textContent = currentStep.phase;

    this.phaseRemaining = currentStep.duration;
    if (timer) timer.textContent = `${this.phaseRemaining}s`;

    if (this.intervalId) clearInterval(this.intervalId);

    this.intervalId = setInterval(() => {
      this.phaseRemaining -= 1;
      if (timer) timer.textContent = `${this.phaseRemaining}s`;

      if (this.phaseRemaining <= 0) {
        clearInterval(this.intervalId);
        this.stepIndex = (this.stepIndex + 1) % steps.length;
        this.runNextPhase();
      }
    }, 1000);
  }
}

window.auraBreathing = new AuraBreathing();
