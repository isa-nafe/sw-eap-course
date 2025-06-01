document.addEventListener('DOMContentLoaded', function() {
    // Disable right-click
    document.addEventListener('contextmenu', function(event) {
        // You can add a message to the user if you want, e.g., alert("Right-clicking is disabled.");
        event.preventDefault();
    });

    // Optional: Disable text selection
    // document.addEventListener('selectstart', function(event) {
    //     event.preventDefault();
    // });
    // For CSS-based text selection disabling (often more effective and less intrusive):
    // You would add this to your CSS: body { -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }
});
