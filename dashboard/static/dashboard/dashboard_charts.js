// Chart.js rendering for dashboard home
// Requires: Chart.js loaded on the page

document.addEventListener('DOMContentLoaded', function() {
    // Recent activity chart
    if (window.dashboardActivityData) {
        const ctx = document.getElementById('activityChart').getContext('2d');
        new Chart(ctx, {
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
    // Alerts chart
    if (window.dashboardAlertData) {
        const ctx = document.getElementById('alertChart').getContext('2d');
        new Chart(ctx, {
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
    // Measurements chart
    if (window.dashboardMeasurementData) {
        const ctx = document.getElementById('measurementChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: window.dashboardMeasurementData.labels,
                datasets: window.dashboardMeasurementData.datasets
            },
            options: { responsive: true }
        });
    }
});
