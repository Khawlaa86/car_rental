// admin_dashboard.js

// Simple confirmation alert for deletion
document.querySelectorAll('a[href^="/admin/delete_car"]').forEach(link => {
    link.addEventListener('click', function(event) {
        if (!confirm('Are you sure you want to delete this car?')) {
            event.preventDefault();
        }
    });
});
