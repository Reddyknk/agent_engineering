/**
 * GCP Tech Summit 2026 - Interactive Application JS
 */

document.addEventListener('DOMContentLoaded', () => {
    // State management
    let state = {
        talks: [],
        categories: [],
        speakers: [],
        lunchBreak: null,
        selectedCategory: '',
        selectedSpeaker: '',
        searchQuery: ''
    };

    // DOM Elements
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const speakerSelect = document.getElementById('speakerSelect');
    const categoryChips = document.getElementById('categoryChips');
    const scheduleTimeline = document.getElementById('scheduleTimeline');
    const resultsCount = document.getElementById('resultsCount');
    const resetAllFiltersBtn = document.getElementById('resetAllFilters');
    const noResultsMessage = document.getElementById('noResultsMessage');

    // Modal Elements
    const talkModal = document.getElementById('talkModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const modalTime = document.getElementById('modalTime');
    const modalCategories = document.getElementById('modalCategories');
    const modalTitle = document.getElementById('modalTitle');
    const modalDescription = document.getElementById('modalDescription');
    const modalSpeakers = document.getElementById('modalSpeakers');

    // Initialize App
    init();

    async function init() {
        await fetchCategories();
        await fetchSpeakers();
        await fetchTalks();

        setupEventListeners();
    }

    // Fetch Categories
    async function fetchCategories() {
        try {
            const res = await fetch('/api/categories');
            state.categories = await res.json();
            renderCategoryChips();
        } catch (err) {
            console.error('Failed to load categories:', err);
        }
    }

    // Fetch Speakers
    async function fetchSpeakers() {
        try {
            const res = await fetch('/api/speakers');
            state.speakers = await res.json();
            renderSpeakerDropdown();
        } catch (err) {
            console.error('Failed to load speakers:', err);
        }
    }

    // Fetch Talks based on current state filters
    async function fetchTalks() {
        try {
            scheduleTimeline.innerHTML = `
                <div class="loading-spinner">
                    <i class="fa-solid fa-circle-notch fa-spin"></i> Loading schedule...
                </div>`;

            const queryParams = new URLSearchParams();
            if (state.selectedCategory) queryParams.append('category', state.selectedCategory);
            if (state.selectedSpeaker) queryParams.append('speaker', state.selectedSpeaker);
            if (state.searchQuery) queryParams.append('q', state.searchQuery);

            const res = await fetch(`/api/talks?${queryParams.toString()}`);
            const data = await res.json();

            state.talks = data.talks;
            state.lunchBreak = data.lunch_break;

            renderSchedule();
            updateFilterSummary(data.total);
        } catch (err) {
            console.error('Failed to load talks:', err);
            scheduleTimeline.innerHTML = `<div class="loading-spinner text-red">Failed to load schedule. Please refresh.</div>`;
        }
    }

    // Render Category Chips
    function renderCategoryChips() {
        categoryChips.innerHTML = `<button class="chip ${state.selectedCategory === '' ? 'active' : ''}" data-category="">All Categories</button>`;
        state.categories.forEach(cat => {
            const chip = document.createElement('button');
            chip.className = `chip ${state.selectedCategory === cat ? 'active' : ''}`;
            chip.dataset.category = cat;
            chip.textContent = cat;
            categoryChips.appendChild(chip);
        });
    }

    // Render Speaker Dropdown
    function renderSpeakerDropdown() {
        speakerSelect.innerHTML = `<option value="">All Speakers</option>`;
        state.speakers.forEach(spk => {
            const opt = document.createElement('option');
            opt.value = spk.id;
            opt.textContent = `${spk.first_name} ${spk.last_name} (${spk.company})`;
            if (state.selectedSpeaker === spk.id) opt.selected = true;
            speakerSelect.appendChild(opt);
        });
    }

    // Render Schedule Timeline
    function renderSchedule() {
        scheduleTimeline.innerHTML = '';

        if (state.talks.length === 0) {
            noResultsMessage.style.display = 'block';
            return;
        } else {
            noResultsMessage.style.display = 'none';
        }

        // Combine talks and lunch break ordered chronologically by start minutes
        // Morning talks (start_minutes < 720) -> Lunch (720 = 12:00 PM) -> Afternoon talks
        const morningTalks = state.talks.filter(t => t.start_minutes < 720);
        const afternoonTalks = state.talks.filter(t => t.start_minutes >= 720);

        // Render morning talks
        morningTalks.forEach(talk => {
            scheduleTimeline.appendChild(createTalkCard(talk));
        });

        // Always show Lunch Break unless specifically filtering out and zero morning/afternoon overlap,
        // but if no search filters active or morning/afternoon talks present, insert Lunch Break at 12:00 PM slot
        if (state.lunchBreak) {
            scheduleTimeline.appendChild(createLunchBreakCard(state.lunchBreak));
        }

        // Render afternoon talks
        afternoonTalks.forEach(talk => {
            scheduleTimeline.appendChild(createTalkCard(talk));
        });
    }

    // Create Talk Card DOM Element
    function createTalkCard(talk) {
        const card = document.createElement('div');
        card.className = 'timeline-card';
        
        const categoriesHTML = talk.categories.map(cat => `<span class="category-tag">${escapeHTML(cat)}</span>`).join('');
        
        const speakersHTML = talk.speakers.map(spk => `
            <div class="speaker-pill">
                <div class="speaker-avatar">${spk.first_name[0]}${spk.last_name[0]}</div>
                <div class="speaker-info">
                    <span class="speaker-name">${escapeHTML(spk.first_name)} ${escapeHTML(spk.last_name)}</span>
                    <span class="speaker-company">${escapeHTML(spk.company)}</span>
                </div>
                <a href="${spk.linkedin}" target="_blank" rel="noopener noreferrer" class="linkedin-link" title="LinkedIn Profile">
                    <i class="fa-brands fa-linkedin"></i>
                </a>
            </div>
        `).join('');

        card.innerHTML = `
            <div class="timeline-time-col">
                <div class="talk-time"><i class="fa-regular fa-clock"></i> ${escapeHTML(talk.time)}</div>
                <div class="talk-duration">Session #${talk.id} • 45 Mins</div>
            </div>
            <div class="timeline-content-col">
                <div class="talk-header">
                    <h3 class="talk-title" data-talk-id="${talk.id}">${escapeHTML(talk.title)}</h3>
                    <div class="categories-list">${categoriesHTML}</div>
                </div>
                <p class="talk-description">${escapeHTML(talk.description)}</p>
                <div class="talk-footer">
                    <div class="speakers-list">${speakersHTML}</div>
                    <button class="details-btn" data-talk-id="${talk.id}">View Details <i class="fa-solid fa-chevron-right"></i></button>
                </div>
            </div>
        `;

        // Event delegation for opening modal
        card.querySelector('.talk-title').addEventListener('click', () => openModal(talk));
        card.querySelector('.details-btn').addEventListener('click', () => openModal(talk));

        return card;
    }

    // Create Lunch Break Banner Card DOM Element
    function createLunchBreakCard(lunch) {
        const card = document.createElement('div');
        card.className = 'timeline-card lunch-card';

        card.innerHTML = `
            <div class="timeline-time-col">
                <div class="talk-time"><i class="fa-solid fa-utensils"></i> ${escapeHTML(lunch.time)}</div>
                <div class="talk-duration">${lunch.duration_minutes} Minutes Break</div>
            </div>
            <div class="timeline-content-col">
                <div class="talk-header">
                    <h3 class="talk-title" style="cursor: default;">${escapeHTML(lunch.title)}</h3>
                    <span class="lunch-badge"><i class="fa-solid fa-mug-hot"></i> Food & Networking</span>
                </div>
                <p class="talk-description" style="-webkit-line-clamp: initial;">${escapeHTML(lunch.description)}</p>
            </div>
        `;

        return card;
    }

    // Modal Operations
    function openModal(talk) {
        modalTime.textContent = talk.time;
        modalCategories.innerHTML = talk.categories.map(c => `<span class="category-tag">${escapeHTML(c)}</span>`).join(' ');
        modalTitle.textContent = talk.title;
        modalDescription.textContent = talk.description;

        modalSpeakers.innerHTML = talk.speakers.map(spk => `
            <div class="modal-speaker-card">
                <div class="speaker-avatar">${spk.first_name[0]}${spk.last_name[0]}</div>
                <div class="speaker-details">
                    <div class="speaker-name">${escapeHTML(spk.first_name)} ${escapeHTML(spk.last_name)}</div>
                    <div class="speaker-company" style="font-size: 0.8rem; margin-bottom: 0.25rem;">${escapeHTML(spk.role)} @ ${escapeHTML(spk.company)}</div>
                    <a href="${spk.linkedin}" target="_blank" rel="noopener noreferrer" class="btn-text" style="padding: 0.2rem 0.6rem; font-size: 0.75rem;">
                        <i class="fa-brands fa-linkedin text-blue"></i> Connect on LinkedIn
                    </a>
                </div>
            </div>
        `).join('');

        talkModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        talkModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Event Listeners
    function setupEventListeners() {
        // Search Input Event
        let debounceTimer;
        searchInput.addEventListener('input', (e) => {
            state.searchQuery = e.target.value;
            clearSearchBtn.style.display = state.searchQuery ? 'block' : 'none';
            
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                fetchTalks();
            }, 300);
        });

        clearSearchBtn.addEventListener('click', () => {
            searchInput.value = '';
            state.searchQuery = '';
            clearSearchBtn.style.display = 'none';
            fetchTalks();
        });

        // Speaker Dropdown Event
        speakerSelect.addEventListener('change', (e) => {
            state.selectedSpeaker = e.target.value;
            fetchTalks();
        });

        // Category Chips Event
        categoryChips.addEventListener('click', (e) => {
            if (e.target.classList.contains('chip')) {
                state.selectedCategory = e.target.dataset.category;
                renderCategoryChips();
                fetchTalks();
            }
        });

        // Reset Filters Button Event
        resetAllFiltersBtn.addEventListener('click', resetFilters);

        // Modal Close Events
        modalCloseBtn.addEventListener('click', closeModal);
        talkModal.addEventListener('click', (e) => {
            if (e.target === talkModal) closeModal();
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && talkModal.style.display === 'flex') closeModal();
        });
    }

    // Update Filter Summary Bar
    function updateFilterSummary(totalCount) {
        resultsCount.textContent = `Showing ${totalCount} technical session${totalCount === 1 ? '' : 's'}`;
        
        const isFiltered = state.selectedCategory || state.selectedSpeaker || state.searchQuery;
        resetAllFiltersBtn.style.display = isFiltered ? 'inline-flex' : 'none';
    }

    // Reset All Filters Helper
    window.resetFilters = function() {
        state.selectedCategory = '';
        state.selectedSpeaker = '';
        state.searchQuery = '';
        searchInput.value = '';
        clearSearchBtn.style.display = 'none';
        renderCategoryChips();
        renderSpeakerDropdown();
        fetchTalks();
    };

    // Helper: Security escape for text
    function escapeHTML(str) {
        if (!str) return '';
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }
});
