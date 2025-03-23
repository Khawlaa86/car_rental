// car_details.js

// You can add any dynamic functionality you need for this page here.
// For example, date validation, form interaction, etc.

document.addEventListener('DOMContentLoaded', function() {
    const startDateInput = document.querySelector('input[name="start_date"]');
    const endDateInput = document.querySelector('input[name="end_date"]');

    // Ensure that the end date is after the start date
    endDateInput.addEventListener('focus', function() {
        const startDate = startDateInput.value;
        if (!startDate) {
            alert('Please select a start date first.');
        }
    });
});
