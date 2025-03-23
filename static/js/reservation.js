// reservations.js

document.addEventListener('DOMContentLoaded', function() {
    const reservationItems = document.querySelectorAll('.reservation-item');

    reservationItems.forEach(item => {
        item.addEventListener('click', function() {
            alert('Reservation details clicked!');
            // Add further interactivity or functionality as needed
        });
    });
});
