// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Device status updates
    updateDeviceStatus();
    setInterval(updateDeviceStatus, 30000); // Update every 30 seconds

    // Initialize charts
    initializeCharts();
});

// Update device status function
function updateDeviceStatus() {
    const deviceStatusElements = document.querySelectorAll('.device-status');
    deviceStatusElements.forEach(element => {
        const deviceId = element.dataset.deviceId;
        fetch(`/api/devices/${deviceId}/status/`)
            .then(response => response.json())
            .then(data => {
                element.classList.remove('online', 'offline');
                element.classList.add(data.status);
                element.textContent = data.status.toUpperCase();
            })
            .catch(error => console.error('Error updating device status:', error));
    });
}

// Initialize charts
function initializeCharts() {
    // --- Stats Page Charts ---
    // Temperature & Humidity Chart
    var tempCanvas = document.getElementById('temperatureChart');
    if (tempCanvas && window.temperatureChartData) {
        var ctxTemp = tempCanvas.getContext('2d');
        new Chart(ctxTemp, {
            type: 'line',
            data: window.temperatureChartData,
            options: {
                responsive: true,
                plugins: { legend: { display: true } },
                scales: { y: { beginAtZero: false } }
            }
        });
    }
    // Measurements Evolution Chart
    var measurementsCanvas = document.getElementById('measurements-chart');
    if (measurementsCanvas && window.measurementsChartData) {
        var ctxMeas = measurementsCanvas.getContext('2d');
        new Chart(ctxMeas, {
            type: 'line',
            data: window.measurementsChartData,
            options: {
                responsive: true,
                plugins: { legend: { display: true } },
                scales: { y: { beginAtZero: false } }
            }
        });
    }

    // --- Dashboard Home Charts ---
    // Activity Chart (bar)
    var activityCanvas = document.getElementById('activityChart');
    if (activityCanvas && window.dashboardActivityData) {
        var ctx1 = activityCanvas.getContext('2d');
        new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: window.dashboardActivityData.labels,
                datasets: [{
                    label: 'Activités',
                    data: window.dashboardActivityData.counts,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }
    // Alert Chart (doughnut)
    var alertCanvas = document.getElementById('alertChart');
    if (alertCanvas && window.dashboardAlertData) {
        var ctx2 = alertCanvas.getContext('2d');
        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: window.dashboardAlertData.labels,
                datasets: [{
                    label: 'Alertes',
                    data: window.dashboardAlertData.counts,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(255, 206, 86, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: { responsive: true }
        });
    }
    // Measurement Chart (line)
    var measurementCanvas = document.getElementById('measurementChart');
    if (measurementCanvas && window.dashboardMeasurementData) {
        var ctx3 = measurementCanvas.getContext('2d');
        new Chart(ctx3, {
            type: 'line',
            data: {
                labels: window.dashboardMeasurementData.labels,
                datasets: window.dashboardMeasurementData.datasets
            },
            options: { responsive: true }
        });
    }
    // --- Stats Page Charts ---
    // Temperature Chart
    var tempCanvas = document.getElementById('temperatureChart');
    if (tempCanvas && window.temperatureChartData) {
        var ctxTemp = tempCanvas.getContext('2d');
        new Chart(ctxTemp, {
            type: 'line',
            data: window.temperatureChartData,
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } }
            }
        });
    }
    // Measurements Evolution Chart (stats)
    var measurementsChartDiv = document.getElementById('measurements-chart');
    if (measurementsChartDiv && window.measurementsChartData) {
        // Remove previous canvas if exists
        var oldCanvas = measurementsChartDiv.querySelector('canvas');
        if (oldCanvas) oldCanvas.remove();
        var newCanvas = document.createElement('canvas');
        newCanvas.height = 350;
        measurementsChartDiv.appendChild(newCanvas);
        var ctx4 = newCanvas.getContext('2d');
        new Chart(ctx4, {
            type: 'line',
            data: window.measurementsChartData,
            options: { responsive: true }
        });
    }
}


// Form handling
function handleFormSubmit(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            fetch(form.action, {
                method: form.method,
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showSuccessAlert(data.message);
                    form.reset();
                } else {
                    showErrorAlert(data.message);
                }
            })
            .catch(error => {
                showErrorAlert('An error occurred. Please try again.');
                console.error('Error:', error);
            });
        });
    }
}

// Alert handling
function showSuccessAlert(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show';
    alert.innerHTML = `${message} <button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

function showErrorAlert(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show';
    alert.innerHTML = `${message} <button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}
