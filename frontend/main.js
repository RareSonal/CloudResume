// Function to fetch and update the visitor count
async function fetchVisitorCount() {
    try {
        const response = await fetch('/api/visitor');
        const data = await response.json();
        document.getElementById('counter').textContent = data.count;
    } catch (error) {
        console.error('Error fetching visitor count:', error);
    }
}

// Function to download the resume
async function downloadResume() {
    try {
        const response = await fetch('/api/resume');
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "SonaliMandrupkar_Resume.pdf";
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            console.error('Error fetching resume:', response.statusText);
        }
    } catch (error) {
        console.error('Error downloading resume:', error);
    }
}

window.onload = fetchVisitorCount;
