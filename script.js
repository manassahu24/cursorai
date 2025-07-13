// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeThemeToggle();
    initializeNavigation();
    initializeSearch();
    initializeChartControls();
    initializeWatchlist();
    initializePortfolio();
    initializeNewsSection();
    initializeRealTimeUpdates();
});

// Theme Toggle Functionality
function initializeThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // Check for saved theme preference or default to light mode
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = body.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });
    
    function setTheme(theme) {
        body.setAttribute('data-theme', theme);
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
}

// Navigation Functionality
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Scroll to section (if implementing single page navigation)
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
        });
    });
}

// Search Functionality
function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchIcon = document.querySelector('.search-icon');
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length > 0) {
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        }
    });
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch(this.value.trim());
        }
    });
    
    function performSearch(query) {
        if (query.length === 0) return;
        
        // Add loading state
        searchIcon.className = 'fas fa-spinner fa-spin';
        
        // Simulate API call
        setTimeout(() => {
            console.log('Searching for:', query);
            // In a real application, this would make an API call
            // and update the stock quote section with the results
            
            // Example: Update stock quote with search result
            if (query.length >= 2) {
                updateStockQuote(query.toUpperCase());
            }
            
            // Reset search icon
            searchIcon.className = 'fas fa-search';
        }, 500);
    }
}

// Chart Controls Functionality
function initializeChartControls() {
    const chartButtons = document.querySelectorAll('.chart-btn');
    
    chartButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            chartButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update chart based on selected time period
            const timeFrame = this.textContent;
            updateChart(timeFrame);
        });
    });
    
    function updateChart(timeFrame) {
        console.log('Updating chart for timeframe:', timeFrame);
        // In a real application, this would fetch new data and update the chart
        
        // Add loading animation
        const chartPlaceholder = document.querySelector('.chart-placeholder');
        chartPlaceholder.style.opacity = '0.5';
        
        setTimeout(() => {
            chartPlaceholder.style.opacity = '1';
            // Update chart data here
        }, 300);
    }
}

// Watchlist Functionality
function initializeWatchlist() {
    const watchlistItems = document.querySelectorAll('.watchlist-item');
    const addToWatchlistBtn = document.querySelector('.btn-secondary');
    
    watchlistItems.forEach(item => {
        item.addEventListener('click', function() {
            const symbol = this.querySelector('.watchlist-symbol').textContent;
            updateStockQuote(symbol);
        });
        
        // Add hover effect
        item.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'var(--bg-tertiary)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'transparent';
        });
    });
    
    if (addToWatchlistBtn) {
        addToWatchlistBtn.addEventListener('click', function() {
            // In a real application, this would open a modal or form
            // to add a new stock to the watchlist
            showNotification('Add to Watchlist clicked', 'info');
        });
    }
}

// Portfolio Functionality
function initializePortfolio() {
    const holdingItems = document.querySelectorAll('.holding-item');
    
    holdingItems.forEach(item => {
        item.addEventListener('click', function() {
            const symbol = this.querySelector('.holding-symbol').textContent;
            updateStockQuote(symbol);
        });
        
        // Add hover effect
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = 'var(--shadow-md)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
}

// News Section Functionality
function initializeNewsSection() {
    const newsItems = document.querySelectorAll('.news-item');
    
    newsItems.forEach(item => {
        item.addEventListener('click', function() {
            // In a real application, this would open the full article
            const title = this.querySelector('h4').textContent;
            showNotification(`Opening article: ${title}`, 'info');
        });
        
        // Add hover effect
        item.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'var(--bg-tertiary)';
            this.style.cursor = 'pointer';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'transparent';
        });
    });
}

// Real-time Updates Simulation
function initializeRealTimeUpdates() {
    // Simulate real-time price updates
    setInterval(() => {
        updateMarketCards();
        updateStockPrices();
        updatePortfolioValues();
    }, 5000); // Update every 5 seconds
}

// Helper Functions
function updateStockQuote(symbol) {
    const stockSymbol = document.querySelector('.stock-symbol');
    const stockName = document.querySelector('.stock-name');
    const stockPrice = document.querySelector('.stock-price');
    const stockChange = document.querySelector('.stock-change');
    
    if (stockSymbol) {
        stockSymbol.textContent = symbol;
        
        // Simulate stock data fetch
        const mockData = generateMockStockData(symbol);
        
        if (stockName) stockName.textContent = mockData.name;
        if (stockPrice) stockPrice.textContent = `$${mockData.price}`;
        if (stockChange) {
            stockChange.innerHTML = `
                <i class="fas fa-arrow-${mockData.change >= 0 ? 'up' : 'down'}"></i>
                <span>${mockData.change >= 0 ? '+' : ''}${mockData.change} (${mockData.changePercent}%)</span>
            `;
            stockChange.className = `stock-change ${mockData.change >= 0 ? 'positive' : 'negative'}`;
        }
    }
}

function generateMockStockData(symbol) {
    const companies = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc.',
        'TSLA': 'Tesla Inc.',
        'NVDA': 'NVIDIA Corporation',
        'AMZN': 'Amazon.com Inc.',
        'META': 'Meta Platforms Inc.',
        'SPY': 'SPDR S&P 500 ETF Trust'
    };
    
    const basePrice = Math.random() * 500 + 50;
    const change = (Math.random() - 0.5) * 20;
    const changePercent = (change / basePrice * 100).toFixed(2);
    
    return {
        name: companies[symbol] || `${symbol} Corp.`,
        price: basePrice.toFixed(2),
        change: change.toFixed(2),
        changePercent: changePercent
    };
}

function updateMarketCards() {
    const marketCards = document.querySelectorAll('.market-card');
    
    marketCards.forEach(card => {
        const priceElement = card.querySelector('.market-price');
        const changeElement = card.querySelector('.market-change span');
        
        if (priceElement && changeElement) {
            const currentPrice = parseFloat(priceElement.textContent.replace(/,/g, ''));
            const change = (Math.random() - 0.5) * 10;
            const newPrice = currentPrice + change;
            const changePercent = (change / currentPrice * 100).toFixed(2);
            
            priceElement.textContent = newPrice.toLocaleString('en-US', { 
                minimumFractionDigits: 2, 
                maximumFractionDigits: 2 
            });
            
            changeElement.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)} (${changePercent}%)`;
            
            const changeContainer = card.querySelector('.market-change');
            changeContainer.className = `market-change ${change >= 0 ? 'positive' : 'negative'}`;
            
            const icon = changeContainer.querySelector('i');
            icon.className = `fas fa-arrow-${change >= 0 ? 'up' : 'down'}`;
        }
    });
}

function updateStockPrices() {
    const watchlistItems = document.querySelectorAll('.watchlist-item');
    
    watchlistItems.forEach(item => {
        const priceElement = item.querySelector('.watchlist-price');
        const changeElement = item.querySelector('.watchlist-change');
        
        if (priceElement && changeElement) {
            const currentPrice = parseFloat(priceElement.textContent.replace('$', ''));
            const changePercent = (Math.random() - 0.5) * 10;
            const newPrice = currentPrice * (1 + changePercent / 100);
            
            priceElement.textContent = `$${newPrice.toFixed(2)}`;
            changeElement.textContent = `${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(1)}%`;
            changeElement.className = `watchlist-change ${changePercent >= 0 ? 'positive' : 'negative'}`;
        }
    });
}

function updatePortfolioValues() {
    const portfolioTotal = document.querySelector('.portfolio-total');
    const portfolioChange = document.querySelector('.portfolio-change span');
    
    if (portfolioTotal && portfolioChange) {
        const currentTotal = parseFloat(portfolioTotal.textContent.replace(/[\$,]/g, ''));
        const change = (Math.random() - 0.5) * 1000;
        const newTotal = currentTotal + change;
        const changePercent = (change / currentTotal * 100).toFixed(2);
        
        portfolioTotal.textContent = `$${newTotal.toLocaleString('en-US', { 
            minimumFractionDigits: 2, 
            maximumFractionDigits: 2 
        })}`;
        
        portfolioChange.textContent = `${change >= 0 ? '+' : ''}$${Math.abs(change).toFixed(2)} (${changePercent}%)`;
        
        const changeContainer = document.querySelector('.portfolio-change');
        changeContainer.className = `portfolio-change ${change >= 0 ? 'positive' : 'negative'}`;
        
        const icon = changeContainer.querySelector('i');
        icon.className = `fas fa-arrow-${change >= 0 ? 'up' : 'down'}`;
    }
}

function scrollToSection(sectionId) {
    // In a real application, this would scroll to the appropriate section
    console.log('Scrolling to section:', sectionId);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background-color: var(--accent-primary);
        color: white;
        border-radius: 0.5rem;
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

function formatPercentage(percentage) {
    return `${percentage >= 0 ? '+' : ''}${percentage.toFixed(2)}%`;
}

// Error Handling
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
});

// Responsive Navigation for Mobile
function initializeMobileMenu() {
    const navToggle = document.createElement('button');
    navToggle.className = 'nav-toggle';
    navToggle.innerHTML = '<i class="fas fa-bars"></i>';
    navToggle.style.cssText = `
        display: none;
        background: none;
        border: none;
        color: var(--text-primary);
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0.5rem;
    `;
    
    const nav = document.querySelector('.nav');
    const logo = document.querySelector('.logo');
    
    if (nav && logo) {
        logo.parentNode.insertBefore(navToggle, nav);
        
        navToggle.addEventListener('click', function() {
            nav.classList.toggle('nav-open');
        });
    }
    
    // Show toggle button on mobile
    const mediaQuery = window.matchMedia('(max-width: 768px)');
    function handleMediaQuery(e) {
        if (e.matches) {
            navToggle.style.display = 'block';
        } else {
            navToggle.style.display = 'none';
            nav.classList.remove('nav-open');
        }
    }
    
    mediaQuery.addListener(handleMediaQuery);
    handleMediaQuery(mediaQuery);
}

// Initialize mobile menu
initializeMobileMenu();