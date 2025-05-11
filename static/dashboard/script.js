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
    // Example chart initialization
    const ctx = document.getElementById('temperatureChart').getContext('2d');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Temperature (°C)',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
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
