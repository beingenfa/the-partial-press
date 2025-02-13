// data.js - Load JSON dynamically
async function loadScenarioData() {
  try {
    console.log("Fetching data.json...");

    const response = await fetch("data/data.json"); // Ensure correct path
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status} - ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Loaded scenario data:", data);

    // Store in global variable so other scripts can access it
    window.scenarioData = data;

    // Dispatch an event to let other scripts know the data is ready
    document.dispatchEvent(new Event("scenarioDataLoaded"));
  } catch (error) {
    console.error("Error loading scenario data:", error);
    alert("Failed to load scenario data. Check console for details.");
  }
}

// Call the function to load JSON when this script runs
loadScenarioData();
