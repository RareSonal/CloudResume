// Function to fetch and update the visitor count
async function fetchVisitorCount() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/visitor');
        const data = await response.json();
        document.getElementById('counter').textContent = data.count; // Update visitor count on page
    } catch (error) {
        console.error('Error fetching visitor count:', error);
    }
}

// Function to download the resume
async function downloadResume() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/resume');
        
        // If resume fetch is successful, convert it to a blob
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob); // Create a URL for the blob
            const a = document.createElement('a');
            a.href = url;
            a.download = "SonaliMandrupkar_Resume.pdf"; // Specify the download file name
            a.click();
            window.URL.revokeObjectURL(url); // Clean up the URL object after download
        } else {
            console.error('Error fetching resume:', response.statusText);
        }
    } catch (error) {
        console.error('Error downloading resume:', error);
    }
}

// Fetch visitor count when the page loads
window.onload = fetchVisitorCount;
