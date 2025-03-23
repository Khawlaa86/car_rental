import os

# List of JavaScript files to create
js_files = [
    "script.js",           # Main script
    "admin_dashboard.js",  # Admin dashboard specific script
    "car_details.js",      # Car details page script
    "user_reservations.js" # User reservations page script
]

# Create the static/js/ directory if it doesn't exist
js_dir = "static/js"
if not os.path.exists(js_dir):
    os.makedirs(js_dir)

# Default content for each JS file (simple structure for now)
js_content = {
    "script.js": """
// Main JavaScript file for Car Rental App
document.addEventListener('DOMContentLoaded', () => {
    console.log('Car Rental App Loaded');
});
""",
    "admin_dashboard.js": """
// JavaScript for Admin Dashboard
document.addEventListener('DOMContentLoaded', () => {
    console.log('Admin Dashboard Loaded');
});
""",
    "car_details.js": """
// JavaScript for Car Details Page
document.addEventListener('DOMContentLoaded', () => {
    console.log('Car Details Page Loaded');
});
""",
    "user_reservations.js": """
// JavaScript for User Reservations Page
document.addEventListener('DOMContentLoaded', () => {
    console.log('User Reservations Page Loaded');
});
"""
}

# Create each JS file with its respective content
for js_file in js_files:
    file_path = os.path.join(js_dir, js_file)
    with open(file_path, 'w') as f:
        f.write(js_content[js_file])

    print(f"{js_file} has been created in {js_dir}")
