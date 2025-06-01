// Toggle sidebar
document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar
    document.querySelector('#sidebarCollapse').addEventListener('click', function() {
        document.querySelector('#sidebar').classList.toggle('active');
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});
