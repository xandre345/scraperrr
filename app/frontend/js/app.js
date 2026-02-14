// State
let allArticles = [];
let savedArticles = JSON.parse(localStorage.getItem('savedArticles') || '[]');
let currentFilter = 'all';

// DOM Elements
const articlesContainer = document.getElementById('articles-grid');
const loadingElement = document.getElementById('loading');
const lastUpdatedElement = document.getElementById('last-updated');
const filterBtns = document.querySelectorAll('.filter-btn');
const mobileToggle = document.getElementById('mobile-toggle');
const sidebar = document.querySelector('.sidebar');
const mainContent = document.querySelector('.main-content');
const navLinks = document.querySelectorAll('.nav-links a');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchArticles();
    setupFilters();
    setupMobileMenu();
    setupNavigation();
    updateTime();
});

// Fetch Articles
async function fetchArticles() {
    try {
        loadingElement.style.display = 'flex';
        articlesContainer.innerHTML = '';
        console.log('Fetching articles...');

        const response = await fetch('http://127.0.0.1:8000/api/articles');
        const data = await response.json();

        if (data.articles) {
            allArticles = data.articles;

            // Client-side sort as a double-layered safety measure to ensure strict interleaving
            allArticles.sort((a, b) => new Date(b.published) - new Date(a.published));

            // Re-render based on current view
            if (currentFilter === 'saved') {
                renderSavedArticles();
            } else {
                renderArticles(allArticles);
            }
        } else {
            articlesContainer.innerHTML = '<p>No articles found.</p>';
        }
    } catch (error) {
        console.error('Error fetching articles:', error);
        articlesContainer.innerHTML = '<p>Error loading articles. Please ensure backend is running.</p>';
    } finally {
        loadingElement.style.display = 'none';
        updateTime();
    }
}

// Render Articles
function renderArticles(articles) {
    articlesContainer.innerHTML = '';

    if (articles.length === 0) {
        articlesContainer.innerHTML = '<p>No articles match your filter.</p>';
        return;
    }

    articles.forEach((article, index) => {
        const card = createCard(article, index);
        articlesContainer.appendChild(card);
    });
}

function createCard(article, index) {
    const card = document.createElement('div');
    card.className = 'card';
    card.style.animationDelay = `${index * 0.05}s`;

    // Check if saved
    const isSaved = savedArticles.some(saved => saved.link === article.link);

    // Format date
    const date = new Date(article.published);
    const timeAgo = getTimeAgo(date);
    const sourceClass = article.source.toLowerCase().replace(/[^a-z0-9]/g, '-');

    card.innerHTML = `
        <div class="card-header">
            <span class="source-badge ${sourceClass}">${article.source}</span>
            <button class="save-btn ${isSaved ? 'saved' : ''}" 
                    title="${isSaved ? 'Remove from Saved' : 'Save for later'}"
                    onclick="toggleSave(this, '${article.link.replace(/'/g, "\\'")}')">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="${isSaved ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
                </svg>
            </button>
        </div>
        <h3 class="card-title">
            <a href="${article.link}" target="_blank">${article.title}</a>
        </h3>
        <div class="card-summary">
            ${article.summary || 'No summary available.'}
        </div>
        <div class="card-footer">
            <span class="date" title="${date.toLocaleString()}">${timeAgo}</span>
            <div class="tags">
                ${article.tags.slice(0, 2).map(tag => `<span class="tag">#${tag}</span>`).join('')}
            </div>
        </div>
    `;

    // Explicitly set color for saved state if CSS class isn't enough (redundancy)
    if (isSaved) {
        const btn = card.querySelector('.save-btn');
        btn.style.color = 'var(--accent-color)';
    }

    return card;
}


// Setup Filters (Source buttons)
function setupFilters() {
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Reset Nav Active State to Dashboard since we are filtering
            navLinks.forEach(l => l.classList.remove('active'));
            navLinks[0].classList.add('active'); // Assume first link is Dashboard

            // Update Filter UI
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Filter Data
            const filter = btn.dataset.filter;
            currentFilter = filter;

            if (filter === 'all') {
                renderArticles(allArticles);
            } else {
                const filtered = allArticles.filter(a => {
                    const source = a.source.toLowerCase();
                    if (filter === 'rundown') return source.includes('rundown');
                    if (filter === 'reddit') return source.includes('reddit') || source.includes('r/');
                    if (filter === 'bens') return source.includes('ben');
                    return true;
                });
                renderArticles(filtered);
            }
        });
    });
}

// Sidebar Navigation (Dashboard vs Saved)
function setupNavigation() {
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            // UI Update
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            const text = link.textContent.trim().toLowerCase();

            if (text.includes('saved')) {
                currentFilter = 'saved';
                renderSavedArticles();
                // Reset source filters visually
                filterBtns.forEach(b => b.classList.remove('active'));
                document.querySelector('h1').textContent = 'Saved Articles';
            } else if (text.includes('dashboard')) {
                currentFilter = 'all';
                // Reset to 'All Sources'
                filterBtns.forEach(b => b.classList.remove('active'));
                filterBtns[0].classList.add('active');
                renderArticles(allArticles);
                document.querySelector('h1').textContent = 'Latest AI News';
            }
        });
    });
}

function renderSavedArticles() {
    articlesContainer.innerHTML = '';

    if (savedArticles.length === 0) {
        articlesContainer.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-secondary);">
                <h3>No saved articles yet</h3>
                <p>Click the bookmark icon on any article to save it for later.</p>
            </div>
        `;
        return;
    }

    // Sort by date newest first
    const sortedSaved = [...savedArticles].sort((a, b) => new Date(b.published) - new Date(a.published));

    sortedSaved.forEach((article, index) => {
        const card = createCard(article, index);
        articlesContainer.appendChild(card);
    });
}

// Mobile Menu
function setupMobileMenu() {
    if (mobileToggle) {
        mobileToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('active');
        });

        // Close sidebar when clicking outside
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('active') &&
                !sidebar.contains(e.target) &&
                e.target !== mobileToggle) {
                sidebar.classList.remove('active');
            }
        });
    }
}

// Toggle Save
window.toggleSave = function (btn, link) {
    // Find the full article object
    let article = allArticles.find(a => a.link === link);

    // If not in allArticles (maybe we are in Saved view and it was filtered out of global list?), 
    // try finding it in savedArticles
    if (!article) {
        article = savedArticles.find(a => a.link === link);
    }

    if (!article) {
        console.error('Article not found:', link);
        return;
    }

    const index = savedArticles.findIndex(a => a.link === link);
    const isSaved = index > -1;

    if (isSaved) {
        // Remove
        savedArticles.splice(index, 1);
        btn.classList.remove('saved');
        btn.querySelector('svg').setAttribute('fill', 'none');
        btn.style.color = '';
        btn.title = 'Save for later';

        // If we represent this in the Saved view, remove the card immediately
        if (currentFilter === 'saved') {
            const card = btn.closest('.card');
            card.remove();
            if (savedArticles.length === 0) renderSavedArticles();
        }
    } else {
        // Add
        savedArticles.push(article);
        btn.classList.add('saved');
        btn.querySelector('svg').setAttribute('fill', 'currentColor');
        btn.style.color = 'var(--accent-color)';
        btn.title = 'Remove from Saved';
    }

    // Persist
    localStorage.setItem('savedArticles', JSON.stringify(savedArticles));
};

// Update Last Updated Time
function updateTime() {
    const now = new Date();
    lastUpdatedElement.textContent = `Last updated: ${now.toLocaleTimeString()}`;
}

function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);

    let interval = seconds / 31536000;
    if (interval > 1) {
        const value = Math.floor(interval);
        return value + (value === 1 ? " year ago" : " years ago");
    }

    interval = seconds / 2592000;
    if (interval > 1) {
        const value = Math.floor(interval);
        return value + (value === 1 ? " month ago" : " months ago");
    }

    interval = seconds / 86400;
    if (interval > 1) {
        const value = Math.floor(interval);
        return value + (value === 1 ? " day ago" : " days ago");
    }

    interval = seconds / 3600;
    if (interval > 1) {
        const value = Math.floor(interval);
        return value + (value === 1 ? " hour ago" : " hours ago");
    }

    interval = seconds / 60;
    if (interval > 1) {
        const value = Math.floor(interval);
        return value + (value === 1 ? " minute ago" : " minutes ago");
    }

    if (seconds <= 5) return "a second ago";
    return Math.floor(seconds) + " seconds ago";
}
