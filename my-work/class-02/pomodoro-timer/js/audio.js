/**
 * AuraFocus Audio Engine
 * Uses Web Audio API to synthesize ambient soundscapes & completion chimes offline.
 */
class AuraAudioEngine {
  constructor() {
    this.ctx = null;
    this.isInitialized = false;
    this.sounds = {
      rain: { active: false, volume: 0, node: null },
      ocean: { active: false, volume: 0, node: null },
      wind: { active: false, volume: 0, node: null },
      pinkNoise: { active: false, volume: 0, node: null },
      binaural: { active: false, volume: 0, node: null }
    };
    this.masterGain = null;
  }

  init() {
    if (this.isInitialized) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.setValueAtTime(0.8, this.ctx.currentTime);
      this.masterGain.connect(this.ctx.destination);
      this.isInitialized = true;
    } catch (e) {
      console.warn("Web Audio API not supported in this browser", e);
    }
  }

  resumeContext() {
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  /**
   * Generates a 5-second Pink Noise AudioBuffer
   */
  createPinkNoiseBuffer() {
    const bufferSize = this.ctx.sampleRate * 5;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;

    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      b3 = 0.86650 * b3 + white * 0.3104856;
      b4 = 0.55000 * b4 + white * 0.5329522;
      b5 = -0.7616 * b5 - white * 0.0168980;
      data[i] = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362;
      data[i] *= 0.11; // scale back
      b6 = white * 0.115926;
    }
    return buffer;
  }

  /**
   * Set volume for a specific sound (0 to 100)
   */
  setVolume(soundKey, val) {
    this.init();
    this.resumeContext();
    const volume = Math.max(0, Math.min(100, val)) / 100;
    this.sounds[soundKey].volume = volume;

    if (volume > 0 && !this.sounds[soundKey].active) {
      this.startSound(soundKey);
    } else if (volume === 0 && this.sounds[soundKey].active) {
      this.stopSound(soundKey);
    } else if (this.sounds[soundKey].gainNode) {
      this.sounds[soundKey].gainNode.gain.setTargetAtTime(volume * 0.5, this.ctx.currentTime, 0.1);
    }
  }

  startSound(key) {
    if (!this.ctx) return;
    this.sounds[key].active = true;

    const gainNode = this.ctx.createGain();
    gainNode.gain.setValueAtTime(this.sounds[key].volume * 0.5, this.ctx.currentTime);
    gainNode.connect(this.masterGain);
    this.sounds[key].gainNode = gainNode;

    const pinkBuffer = this.createPinkNoiseBuffer();

    if (key === 'pinkNoise') {
      const src = this.ctx.createBufferSource();
      src.buffer = pinkBuffer;
      src.loop = true;
      src.connect(gainNode);
      src.start();
      this.sounds[key].source = src;
    } 
    else if (key === 'rain') {
      const src = this.ctx.createBufferSource();
      src.buffer = pinkBuffer;
      src.loop = true;

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.value = 1000;

      src.connect(filter);
      filter.connect(gainNode);
      src.start();
      this.sounds[key].source = src;
    } 
    else if (key === 'ocean') {
      const src = this.ctx.createBufferSource();
      src.buffer = pinkBuffer;
      src.loop = true;

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.value = 400;

      // LFO for wave modulation
      const lfo = this.ctx.createOscillator();
      lfo.frequency.value = 0.12; // 8 second wave cycle
      const lfoGain = this.ctx.createGain();
      lfoGain.gain.value = 350;

      lfo.connect(lfoGain);
      lfoGain.connect(filter.frequency);

      src.connect(filter);
      filter.connect(gainNode);

      lfo.start();
      src.start();
      this.sounds[key].source = src;
      this.sounds[key].lfo = lfo;
    }
    else if (key === 'wind') {
      const src = this.ctx.createBufferSource();
      src.buffer = pinkBuffer;
      src.loop = true;

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.value = 500;
      filter.Q.value = 3.0;

      const lfo = this.ctx.createOscillator();
      lfo.frequency.value = 0.2;
      const lfoGain = this.ctx.createGain();
      lfoGain.gain.value = 300;

      lfo.connect(lfoGain);
      lfoGain.connect(filter.frequency);

      src.connect(filter);
      filter.connect(gainNode);

      lfo.start();
      src.start();
      this.sounds[key].source = src;
      this.sounds[key].lfo = lfo;
    }
    else if (key === 'binaural') {
      // Left 200Hz, Right 240Hz (40Hz Gamma differential)
      const oscL = this.ctx.createOscillator();
      const oscR = this.ctx.createOscillator();
      oscL.frequency.value = 200;
      oscR.frequency.value = 240;

      const merger = this.ctx.createChannelMerger(2);
      oscL.connect(merger, 0, 0); // left channel
      oscR.connect(merger, 0, 1); // right channel

      merger.connect(gainNode);

      oscL.start();
      oscR.start();
      this.sounds[key].oscL = oscL;
      this.sounds[key].oscR = oscR;
    }
  }

  stopSound(key) {
    if (!this.sounds[key].active) return;
    this.sounds[key].active = false;
    if (this.sounds[key].source) {
      try { this.sounds[key].source.stop(); } catch(e){}
    }
    if (this.sounds[key].lfo) {
      try { this.sounds[key].lfo.stop(); } catch(e){}
    }
    if (this.sounds[key].oscL) {
      try { this.sounds[key].oscL.stop(); this.sounds[key].oscR.stop(); } catch(e){}
    }
  }

  /**
   * Plays a tranquil Tibetan Singing Bowl chime upon timer completion
   */
  playChime() {
    this.init();
    this.resumeContext();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    const freqs = [432, 864, 1296]; // A=432Hz harmonic series
    const gains = [0.5, 0.2, 0.08];

    freqs.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gainNode = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now);

      gainNode.gain.setValueAtTime(0, now);
      gainNode.gain.linearRampToValueAtTime(gains[idx], now + 0.08);
      gainNode.gain.exponentialRampToValueAtTime(0.0001, now + 3.5);

      osc.connect(gainNode);
      gainNode.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 3.6);
    });
  }

  getActiveCount() {
    return Object.values(this.sounds).filter(s => s.volume > 0).length;
  }
}

window.auraAudio = new AuraAudioEngine();
