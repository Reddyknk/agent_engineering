/**
 * AuraFocus Analytics & History Engine
 * Session logging, streak calculation, custom HTML5 canvas weekly bar chart.
 */
class AuraStats {
  constructor() {
    this.logs = [];
  }

  init() {
    this.loadLogs();
    this.updateStatsUI();
    this.renderChart();
  }

  loadLogs() {
    const saved = localStorage.getItem('aura_focus_logs');
    if (saved) {
      try {
        this.logs = JSON.parse(saved);
      } catch (e) {
        this.logs = [];
      }
    }
  }

  saveLogs() {
    localStorage.setItem('aura_focus_logs', JSON.stringify(this.logs));
  }

  logSession(minutes = 25) {
    const session = {
      id: 'sess_' + Date.now(),
      date: new Date().toISOString().split('T')[0],
      minutes: minutes,
      timestamp: Date.now()
    };
    this.logs.unshift(session);
    this.saveLogs();
    this.updateStatsUI();
    this.renderChart();
  }

  getTodayMinutes() {
    const todayStr = new Date().toISOString().split('T')[0];
    return this.logs
      .filter(log => log.date === todayStr)
      .reduce((sum, log) => sum + log.minutes, 0);
  }

  getTodayPomoCount() {
    const todayStr = new Date().toISOString().split('T')[0];
    return this.logs.filter(log => log.date === todayStr).length;
  }

  getStreakDays() {
    if (this.logs.length === 0) return 0;
    
    const dates = Array.from(new Set(this.logs.map(log => log.date))).sort().reverse();
    const todayStr = new Date().toISOString().split('T')[0];
    const yesterdayStr = new Date(Date.now() - 86400000).toISOString().split('T')[0];

    if (!dates.includes(todayStr) && !dates.includes(yesterdayStr)) {
      return 0;
    }

    let streak = 0;
    let currDate = new Date();
    if (!dates.includes(todayStr)) {
      currDate.setDate(currDate.getDate() - 1);
    }

    while (true) {
      const dateStr = currDate.toISOString().split('T')[0];
      if (dates.includes(dateStr)) {
        streak++;
        currDate.setDate(currDate.getDate() - 1);
      } else {
        break;
      }
    }
    return streak;
  }

  getTaskCompletionRate() {
    if (!window.auraTasks || window.auraTasks.tasks.length === 0) return 0;
    const total = window.auraTasks.tasks.length;
    const completed = window.auraTasks.tasks.filter(t => t.completed).length;
    return Math.round((completed / total) * 100);
  }

  getWeeklyData() {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const now = new Date();
    const result = [];

    for (let i = 6; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split('T')[0];
      const dayName = days[d.getDay()];

      const totalMins = this.logs
        .filter(log => log.date === dateStr)
        .reduce((sum, log) => sum + log.minutes, 0);

      result.push({
        day: dayName,
        date: dateStr,
        hours: parseFloat((totalMins / 60).toFixed(1))
      });
    }
    return result;
  }

  updateStatsUI() {
    // Stat values
    const todayTimeEl = document.getElementById('statTodayTime');
    const pomoCountEl = document.getElementById('statPomoCount');
    const streakEl = document.getElementById('statStreak');
    const taskRateEl = document.getElementById('statTaskRate');

    const totalMins = this.getTodayMinutes();
    const hours = Math.floor(totalMins / 60);
    const mins = totalMins % 60;

    if (todayTimeEl) todayTimeEl.textContent = `${hours}h ${mins}m`;
    if (pomoCountEl) pomoCountEl.textContent = this.getTodayPomoCount();
    if (streakEl) streakEl.textContent = `${this.getStreakDays()} Days`;
    if (taskRateEl) taskRateEl.textContent = `${this.getTaskCompletionRate()}%`;

    // History List
    const historyList = document.getElementById('historyList');
    if (historyList) {
      if (this.logs.length === 0) {
        historyList.innerHTML = `<div style="color: var(--text-muted); text-align: center; padding: 20px 0;">No sessions completed yet today.</div>`;
      } else {
        historyList.innerHTML = this.logs.slice(0, 8).map(log => {
          const timeStr = new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
          return `
            <div class="history-item">
              <span><i data-lucide="check" style="width:14px; height:14px; color: var(--accent-primary); display:inline; vertical-align:middle; margin-right:6px;"></i> Focus Session (${log.minutes} min)</span>
              <span>${log.date} at ${timeStr}</span>
            </div>
          `;
        }).join('');
        if (window.lucide) window.lucide.createIcons();
      }
    }
  }

  renderChart() {
    const canvas = document.getElementById('weeklyChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    
    const rect = canvas.getBoundingClientRect();
    canvas.width = (rect.width || 600) * dpr;
    canvas.height = 200 * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width || 600;
    const height = 200;

    ctx.clearRect(0, 0, width, height);

    const data = this.getWeeklyData();
    const maxHours = Math.max(4, ...data.map(d => d.hours));

    const paddingLeft = 35;
    const paddingBottom = 30;
    const chartWidth = width - paddingLeft - 20;
    const chartHeight = height - paddingBottom - 20;

    const barGap = 16;
    const barWidth = Math.max(12, (chartWidth - (data.length - 1) * barGap) / data.length);

    // Accent color from computed styles
    const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent-primary').trim() || '#639873';

    data.forEach((item, idx) => {
      const x = paddingLeft + idx * (barWidth + barGap);
      const barH = (item.hours / maxHours) * chartHeight;
      const y = height - paddingBottom - barH;

      // Draw Background Track Bar
      ctx.fillStyle = 'rgba(255, 255, 255, 0.04)';
      this.drawRoundedRect(ctx, x, 20, barWidth, chartHeight, 6);
      ctx.fill();

      // Draw Active Bar Gradient
      if (barH > 0) {
        const grad = ctx.createLinearGradient(x, y, x, y + barH);
        grad.addColorStop(0, accentColor);
        grad.addColorStop(1, 'rgba(255, 255, 255, 0.1)');

        ctx.fillStyle = grad;
        this.drawRoundedRect(ctx, x, y, barWidth, barH, 6);
        ctx.fill();
      }

      // Draw Day Label
      ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
      ctx.font = '12px "Plus Jakarta Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(item.day, x + barWidth / 2, height - 8);

      // Draw Hours Value Label above bar
      if (item.hours > 0) {
        ctx.fillStyle = '#ffffff';
        ctx.font = '10px "Outfit", sans-serif';
        ctx.fillText(`${item.hours}h`, x + barWidth / 2, y - 6);
      }
    });
  }

  drawRoundedRect(ctx, x, y, w, h, r) {
    if (w < 2 * r) r = w / 2;
    if (h < 2 * r) r = h / 2;
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }
}

window.auraStats = new AuraStats();
