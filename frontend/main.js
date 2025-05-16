// Backend base URL
const BACKEND_BASE_URL = 'https://raresonalcloudresume-ahbdgehufwhzftfg.canadacentral-01.azurewebsites.net';

// Function to fetch and update the visitor count
export async function fetchVisitorCount() {
  try {
    const response = await fetch(`${BACKEND_BASE_URL}/api/visitor`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    document.getElementById('counter').textContent = data.count;
  } catch (error) {
    console.error('Error fetching visitor count:', error);
  }
}

// Function to download the resume
export async function downloadResume() {
  try {
    const response = await fetch(`${BACKEND_BASE_URL}/api/resume`);
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

// Register download button listener after DOM is ready
window.onload = () => {
  fetchVisitorCount();

  const resumeButton = document.getElementById('resumeDownload');
  if (resumeButton) {
    resumeButton.addEventListener('click', downloadResume);
  }
};
