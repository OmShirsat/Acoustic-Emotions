// Function to navigate between pages
function goToPage(pageId) {
    console.log(`Navigating to page: ${pageId}`);

    // Hide all pages
    const containers = document.querySelectorAll('.container');
    containers.forEach(container => {
        container.style.display = 'none';
    });

    // Show the selected page
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.style.display = 'block';
        console.log(`Page "${pageId}" displayed.`);
    } else {
        console.error(`Page with ID "${pageId}" not found.`);
    }
}

// Function to handle file selection (for "Select Audio from File")
function fileSelected(event) {
    const file = event.target.files[0];
    if (file) {
        console.log(`File selected: ${file.name}`);
        // Proceed with file analysis logic or navigation
        goToPage('analyze-page');
    } else {
        console.error('No file selected.');
    }
}

// Event listener for page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScript loaded and ready.');
});
