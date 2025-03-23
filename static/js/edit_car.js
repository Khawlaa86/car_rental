// edit_car.js

document.addEventListener('DOMContentLoaded', function() {
    const priceInput = document.querySelector('input[name="price"]');

    priceInput.addEventListener('input', function() {
        const priceValue = priceInput.value;
        if (priceValue < 0) {
            alert('Price must be a positive number.');
            priceInput.value = '';
        }
    });
});
