// main.js
document.addEventListener("scenarioDataLoaded", () => {
  console.log("Scenario data is loaded, populating dropdown...");
  populateDropdown();
});

const scenarioSelect = document.getElementById("scenarioSelect");
const scenarioDescElem = document.getElementById("scenarioDescription");
const generateReportBtn = document.getElementById("generateReportBtn");

// Function to populate the dropdown
function populateDropdown() {
  const scenarioData = window.scenarioData; // Read from global variable

  if (!scenarioSelect) {
    console.error("Dropdown element not found!");
    return;
  }

  if (!scenarioData || Object.keys(scenarioData).length === 0) {
    console.error("Scenario data is empty or not loaded.");
    return;
  }

  console.log("Populating dropdown with scenarios:", Object.keys(scenarioData));

  scenarioSelect.innerHTML = "<option value=''>Select a scenario</option>"; // Default option

  Object.keys(scenarioData).forEach((scenario) => {
    const opt = document.createElement("option");
    opt.value = scenario;
    opt.textContent = scenario;
    scenarioSelect.appendChild(opt);
  });
}

// Handle dropdown selection
if (scenarioSelect && scenarioDescElem) {
  scenarioSelect.addEventListener("change", () => {
    const selected = scenarioSelect.value;
    const scenarioInfo = window.scenarioData[selected];

    scenarioDescElem.textContent =
      scenarioInfo?.description?.description?.story || "No description available.";

    clearReports();
  });
}

// Function to get scenario reports
function getScenarioReports(scenario) {
  return window.scenarioData[scenario]?.biased_reports || {};
}

// Handle "Generate Report" button click
if (generateReportBtn) {
  generateReportBtn.addEventListener("click", () => {
    const selectedScenario = scenarioSelect.value;
    if (!selectedScenario || !window.scenarioData[selectedScenario]) {
      alert("Please select a valid scenario first!");
      return;
    }
    const reports = getScenarioReports(selectedScenario);

    fillReport("villainizingAlex", reports.villainizing_alex);
    fillReport("villainizingJordan", reports.villainizing_jordan);
    fillReport("alexVillainJordanHero", reports.villainizing_alex_painting_jordan_as_hero);
    fillReport("jordanVillainAlexHero", reports.villainizing_jordan_painting_alex_as_hero);
  });
}

// Helper function to fill reports
function fillReport(elementId, data = { headline: "", report: "" }) {
  const box = document.getElementById(elementId);
  if (!box) return;

  const header = box.querySelector(".news-header");
  const content = box.querySelector("p");

  if (header && content) {
    header.textContent = data.headline || "";
    content.textContent = data.report || "";
  }
}

function clearReports() {
  fillReport("villainizingAlex");
  fillReport("villainizingJordan");
  fillReport("alexVillainJordanHero");
  fillReport("jordanVillainAlexHero");
}
