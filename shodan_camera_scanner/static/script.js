document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('search-btn');
    const demoBtn = document.getElementById('demo-btn');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const resultsSection = document.getElementById('results-section');
    const results = document.getElementById('results');
    const totalResults = document.getElementById('total-results');

    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.dataset.tab;
            
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });

    // Demo button click handler
    demoBtn.addEventListener('click', async function() {
        await performSearch(null, true);
    });

    // Search button click handler
    searchBtn.addEventListener('click', async function() {
        const activeTab = document.querySelector('.tab-btn.active').dataset.tab;
        const cameraType = document.querySelector('input[name="camera-type"]:checked').value;

        let query = buildCameraQuery(activeTab, cameraType);

        if (!query) {
            showError('Please fill in at least one search field');
            return;
        }

        await performSearch(query, false);
    });

    function buildCameraQuery(activeTab, cameraType) {
        let queryParts = [];
        
        // Base camera query based on type
        switch(cameraType) {
            case 'all':
                queryParts.push('(product:"IP Camera" OR product:"webcam" OR product:"camera" OR port:554)');
                break;
            case 'webcam':
                queryParts.push('product:"webcam"');
                break;
            case 'surveillance':
                queryParts.push('(product:"IP Camera" OR product:"surveillance")');
                break;
            case 'rtsp':
                queryParts.push('port:554');
                break;
        }

        // Add location-specific filters based on active tab
        if (activeTab === 'location') {
            const city = document.getElementById('city-input').value.trim();
            const country = document.getElementById('country-input').value.trim();
            const state = document.getElementById('state-input').value.trim();

            if (!city && !country && !state) {
                return null;
            }

            if (city) queryParts.push(`city:"${city}"`);
            if (country) queryParts.push(`country:${country.toUpperCase()}`);
            if (state) queryParts.push(`state:"${state}"`);
        } 
        else if (activeTab === 'coordinates') {
            const lat = document.getElementById('latitude-input').value.trim();
            const lon = document.getElementById('longitude-input').value.trim();

            if (!lat || !lon) {
                return null;
            }

            queryParts.push(`geo:"${lat},${lon}"`);
        }
        else if (activeTab === 'network') {
            const network = document.getElementById('network-input').value.trim();

            if (!network) {
                return null;
            }

            queryParts.push(`net:${network}`);
        }

        return queryParts.join(' ');
    }

    async function performSearch(query, useDemoMode = false) {
        // Hide previous results and errors
        error.style.display = 'none';
        resultsSection.style.display = 'none';
        document.getElementById('ml-results-section').style.display = 'none';
        loading.style.display = 'block';
        searchBtn.disabled = true;
        demoBtn.disabled = true;

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    query: query,
                    use_demo: useDemoMode
                })
            });

            const data = await response.json();

            if (!response.ok) {
                // Show suggestion to try demo mode if API fails
                let errorMsg = data.error || 'Search failed';
                if (data.suggest_demo) {
                    errorMsg += ' Click "Try Demo Mode" below to see how the app works!';
                }
                throw new Error(errorMsg);
            }

            // Show demo mode indicator if applicable
            if (data.demo_mode) {
                const demoAlert = document.createElement('div');
                demoAlert.className = 'demo-alert';
                demoAlert.innerHTML = '🎮 <strong>Demo Mode:</strong> Showing results from sample data (shodan_results.csv)';
                document.querySelector('.container').insertBefore(demoAlert, document.getElementById('ml-results-section'));
            }

            displayMLResults(data.ml_results);
            displayResults(data, query || 'Demo Data');
        } catch (err) {
            showError(err.message);
        } finally {
            loading.style.display = 'none';
            searchBtn.disabled = false;
            demoBtn.disabled = false;
        }
    }

    function displayMLResults(mlResults) {
        if (!mlResults) return;

        // Update ML statistics
        document.getElementById('ml-accuracy').textContent = mlResults.accuracy + '%';
        document.getElementById('exposed-count').textContent = mlResults.exposed_count;
        document.getElementById('benign-count').textContent = mlResults.benign_count;
        document.getElementById('total-analyzed').textContent = mlResults.total_devices;

        // Display visualization
        const visualization = document.getElementById('ml-visualization');
        visualization.src = 'data:image/png;base64,' + mlResults.visualization;

        // Show ML results section
        document.getElementById('ml-results-section').style.display = 'block';
    }

    function displayResults(data, query) {
        results.innerHTML = '';
        totalResults.textContent = `${data.total} devices found`;

        // Display the query that was used
        const queryDisplay = document.createElement('div');
        queryDisplay.className = 'query-display';
        queryDisplay.innerHTML = `<strong>Query:</strong> ${escapeHtml(query)}`;
        
        const resultsHeader = document.querySelector('.results-header');
        const existingQueryDisplay = document.querySelector('.query-display');
        if (existingQueryDisplay) {
            existingQueryDisplay.remove();
        }
        resultsHeader.appendChild(queryDisplay);

        if (data.devices.length === 0) {
            results.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No devices found for this search.</p>';
        } else {
            data.devices.forEach(device => {
                const riskClass = device.risk_level.toLowerCase();
                const card = document.createElement('div');
                card.className = `device-card ${riskClass}`;
                card.innerHTML = `
                    <span class="risk-badge ${riskClass}">${device.risk_level}</span>
                    <h3>🌐 ${device.ip}:${device.port}</h3>
                    <div class="device-info">
                        <strong>Location:</strong> ${device.location}, ${device.country}
                    </div>
                    <div class="device-info">
                        <strong>Organization:</strong> ${device.org}
                    </div>
                    ${device.product !== 'Unknown' ? `<div class="device-info"><strong>Product:</strong> ${device.product}</div>` : ''}
                    <div class="device-info">
                        <strong>AI Classification:</strong> <span style="font-weight: bold; color: ${riskClass === 'exposed' ? '#F44336' : '#4CAF50'}">${device.risk_level}</span>
                    </div>
                    <div class="device-data">
                        ${escapeHtml(device.data.substring(0, 300))}
                    </div>
                `;
                results.appendChild(card);
            });
        }

        resultsSection.style.display = 'block';
    }

    function showError(message) {
        error.textContent = message;
        error.style.display = 'block';
        setTimeout(() => {
            error.style.display = 'none';
        }, 5000);
    }

    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
});
