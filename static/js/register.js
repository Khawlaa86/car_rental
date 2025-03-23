// register.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(e) {
        const username = document.querySelector('input[name="username"]').value;
        const password = document.querySelector('input[name="password"]').value;
        
        // Basic form validation
        if (!username || !password) {
            e.preventDefault();
            alert("Both fields are required!");
        }
    });
});
