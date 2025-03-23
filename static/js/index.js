// index.js

document.addEventListener('DOMContentLoaded', function() {
    const cars = document.querySelectorAll('.car');

    cars.forEach(car => {
        car.addEventListener('mouseenter', function() {
            car.style.transform = 'scale(1.05)';
        });

        car.addEventListener('mouseleave', function() {
            car.style.transform = 'scale(1)';
        });
    });
});
