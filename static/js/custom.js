/**
 * Custom JavaScript for App Granja
 * This file contains all the custom JavaScript functionality for the application
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize popovers
    initializePopovers();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize data tables if they exist
    initializeDataTables();
    
    // Initialize datepickers
    initializeDatepickers();
    
    // Initialize any charts if they exist
    initializeCharts();
    
    // Add active class to current nav item
    setActiveNavItem();
    
    // Handle flash messages
    handleFlashMessages();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap popovers
 */
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Initialize Bootstrap form validation
 */
function initializeFormValidation() {
    'use strict';
    
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');
    
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Initialize DataTables if they exist on the page
 */
function initializeDataTables() {
    if (typeof $ !== 'undefined' && $.fn.DataTable) {
        $('.datatable').DataTable({
            responsive: true,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
            },
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                 "<'row'<'col-sm-12'tr>>" +
                 "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            pageLength: 10,
            lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, 'Todos']]
        });
    }
}

/**
 * Initialize datepickers if they exist on the page
 */
function initializeDatepickers() {
    if (typeof $ !== 'undefined' && $.fn.datepicker) {
        $('.datepicker').datepicker({
            format: 'dd/mm/yyyy',
            autoclose: true,
            language: 'es',
            todayHighlight: true
        });
    }
}

/**
 * Initialize charts if they exist on the page
 */
function initializeCharts() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        return;
    }
    
    // Find all canvas elements with data-chart attribute
    const chartElements = document.querySelectorAll('canvas[data-chart]');
    
    chartElements.forEach(function(element) {
        const chartType = element.getAttribute('data-chart-type') || 'line';
        const chartData = JSON.parse(element.getAttribute('data-chart'));
        
        new Chart(element, {
            type: chartType,
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
}

/**
 * Set active class on current navigation item
 */
function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') && currentPath.startsWith(link.getAttribute('href'))) {
            link.classList.add('active');
            
            // If it's a dropdown item, also activate the parent
            const parent = link.closest('.dropdown-menu');
            if (parent) {
                const dropdownToggle = parent.previousElementSibling;
                if (dropdownToggle && dropdownToggle.classList.contains('dropdown-toggle')) {
                    dropdownToggle.classList.add('active');
                }
            }
        }
    });
}

/**
 * Handle flash messages
 */
function handleFlashMessages() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Format currency
 * @param {number} amount - The amount to format
 * @param {string} currency - The currency symbol (default: '$')
 * @param {number} decimals - Number of decimal places (default: 2)
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount, currency = '$', decimals = 2) {
    return `${currency}${parseFloat(amount).toFixed(decimals).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`;
}

/**
 * Format date
 * @param {string|Date} date - The date to format
 * @param {string} format - The format string (default: 'dd/mm/yyyy')
 * @returns {string} Formatted date string
 */
function formatDate(date, format = 'dd/mm/yyyy') {
    const d = new Date(date);
    if (isNaN(d.getTime())) return '';
    
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    
    return format
        .replace('dd', day)
        .replace('mm', month)
        .replace('yyyy', year);
}

/**
 * Toggle password visibility
 * @param {HTMLElement} button - The button element that was clicked
 */
function togglePassword(button) {
    const input = button.previousElementSibling;
    const icon = button.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

/**
 * Copy text to clipboard
 * @param {string} text - The text to copy
 * @param {HTMLElement} element - The element to show feedback in
 */
function copyToClipboard(text, element = null) {
    navigator.clipboard.writeText(text).then(function() {
        if (element) {
            const originalText = element.innerHTML;
            element.innerHTML = '<i class="fas fa-check"></i> Copiado!';
            setTimeout(() => {
                element.innerHTML = originalText;
            }, 2000);
        }
    }).catch(function(err) {
        console.error('Error al copiar al portapapeles: ', err);
        if (element) {
            const originalText = element.innerHTML;
            element.innerHTML = '<i class="fas fa-times"></i> Error';
            setTimeout(() => {
                element.innerHTML = originalText;
            }, 2000);
        }
    });
}

// Make functions available globally
window.AppGranja = {
    formatCurrency,
    formatDate,
    togglePassword,
    copyToClipboard
};
