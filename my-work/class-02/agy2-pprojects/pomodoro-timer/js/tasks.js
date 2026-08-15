/**
 * AuraFocus Task Manager
 * Handles task CRUD, active task binding to timer, local storage sync.
 */
class AuraTasks {
  constructor() {
    this.tasks = [];
    this.activeTaskId = null;
    this.filter = 'all'; // 'all' | 'active' | 'completed'
  }

  init() {
    this.loadTasks();
    this.render();
  }

  loadTasks() {
    const saved = localStorage.getItem('aura_tasks');
    if (saved) {
      try {
        this.tasks = JSON.parse(saved);
      } catch (e) {
        this.tasks = [];
      }
    }
    const savedActiveId = localStorage.getItem('aura_active_task_id');
    if (savedActiveId) {
      this.activeTaskId = savedActiveId;
    }
  }

  saveTasks() {
    localStorage.setItem('aura_tasks', JSON.stringify(this.tasks));
    if (this.activeTaskId) {
      localStorage.setItem('aura_active_task_id', this.activeTaskId);
    } else {
      localStorage.removeItem('aura_active_task_id');
    }
  }

  addTask(title, estimatedPomos = 1) {
    if (!title.trim()) return;
    const newTask = {
      id: 'task_' + Date.now(),
      title: title.trim(),
      estimatedPomos: parseInt(estimatedPomos) || 1,
      completedPomos: 0,
      completed: false,
      createdAt: Date.now()
    };
    this.tasks.unshift(newTask);
    if (!this.activeTaskId) {
      this.activeTaskId = newTask.id;
    }
    this.saveTasks();
    this.render();
    this.updateActiveTaskBanner();
    if (window.auraStats) window.auraStats.updateStatsUI();
  }

  toggleTaskComplete(id) {
    const task = this.tasks.find(t => t.id === id);
    if (task) {
      task.completed = !task.completed;
      if (task.completed && this.activeTaskId === id) {
        this.activeTaskId = null;
      }
      this.saveTasks();
      this.render();
      this.updateActiveTaskBanner();
      if (window.auraStats) window.auraStats.updateStatsUI();
    }
  }

  deleteTask(id) {
    this.tasks = this.tasks.filter(t => t.id !== id);
    if (this.activeTaskId === id) {
      this.activeTaskId = null;
    }
    this.saveTasks();
    this.render();
    this.updateActiveTaskBanner();
    if (window.auraStats) window.auraStats.updateStatsUI();
  }

  setActiveTask(id) {
    this.activeTaskId = (this.activeTaskId === id) ? null : id;
    this.saveTasks();
    this.render();
    this.updateActiveTaskBanner();
  }

  clearActiveTask() {
    this.activeTaskId = null;
    this.saveTasks();
    this.render();
    this.updateActiveTaskBanner();
  }

  incrementActiveTaskPomo() {
    if (!this.activeTaskId) return;
    const task = this.tasks.find(t => t.id === this.activeTaskId);
    if (task) {
      task.completedPomos += 1;
      this.saveTasks();
      this.render();
      this.updateActiveTaskBanner();
    }
  }

  getActiveTask() {
    return this.tasks.find(t => t.id === this.activeTaskId);
  }

  setFilter(filterName) {
    this.filter = filterName;
    this.render();
  }

  updateActiveTaskBanner() {
    const banner = document.getElementById('activeTaskBanner');
    const titleEl = document.getElementById('activeTaskTitle');
    const clearBtn = document.getElementById('clearActiveTaskBtn');
    const activeTask = this.getActiveTask();

    if (activeTask) {
      titleEl.textContent = `Focusing on: ${activeTask.title} (${activeTask.completedPomos}/${activeTask.estimatedPomos} pomos)`;
      if (clearBtn) clearBtn.style.display = 'inline-flex';
    } else {
      titleEl.textContent = 'Select a task to focus on';
      if (clearBtn) clearBtn.style.display = 'none';
    }
  }

  render() {
    const listEl = document.getElementById('taskList');
    const countEl = document.getElementById('taskCompletedCount');
    if (!listEl) return;

    // Filter tasks
    const filteredTasks = this.tasks.filter(t => {
      if (this.filter === 'active') return !t.completed;
      if (this.filter === 'completed') return t.completed;
      return true;
    });

    // Update stats brief
    const completedCount = this.tasks.filter(t => t.completed).length;
    if (countEl) countEl.textContent = `${completedCount}/${this.tasks.length} Tasks`;

    if (filteredTasks.length === 0) {
      listEl.innerHTML = `<div class="empty-state" style="text-align: center; color: var(--text-muted); padding: 30px 0;">No tasks found. Add a new goal to get started!</div>`;
      return;
    }

    listEl.innerHTML = filteredTasks.map(task => {
      const isActive = task.id === this.activeTaskId;
      return `
        <div class="task-item ${task.completed ? 'completed' : ''} ${isActive ? 'active-target' : ''}" data-id="${task.id}">
          <div class="task-left">
            <div class="task-checkbox" onclick="window.auraTasks.toggleTaskComplete('${task.id}')">
              ${task.completed ? '<i data-lucide="check" style="width:14px; height:14px; color:#fff;"></i>' : ''}
            </div>
            <span class="task-text">${this.escapeHtml(task.title)}</span>
          </div>
          <div class="task-right">
            <span class="task-pomo-badge">${task.completedPomos}/${task.estimatedPomos} 🍅</span>
            ${!task.completed ? `
              <button class="task-select-btn" onclick="window.auraTasks.setActiveTask('${task.id}')" title="${isActive ? 'Deselect Target' : 'Set as Active Target'}">
                <i data-lucide="${isActive ? 'target-off' : 'target'}" style="width:18px; height:18px;"></i>
              </button>
            ` : ''}
            <button class="task-delete-btn" onclick="window.auraTasks.deleteTask('${task.id}')" title="Delete task">
              <i data-lucide="trash-2" style="width:18px; height:18px;"></i>
            </button>
          </div>
        </div>
      `;
    }).join('');

    if (window.lucide) window.lucide.createIcons();
  }

  escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  }
}

window.auraTasks = new AuraTasks();
