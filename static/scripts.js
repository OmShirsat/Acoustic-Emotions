function goToPage(pageId) {
    // Hide all pages
    document.getElementById('welcome-page').style.display = 'none';
    document.getElementById('record-page').style.display = 'none';
    document.getElementById('recording-page').style.display = 'none';
    document.getElementById('analyze-page').style.display = 'none';
    
    // Show the selected page
    document.getElementById(pageId).style.display = 'block';
}

function fileSelected(event) {
    const file = event.target.files[0];
    if (file) {
        console.log(`File selected: ${file.name}, Size: ${file.size} bytes`);
    } else {
        console.log("No file selected");
    }
}

// Functions to handle page navigation (if necessary)
