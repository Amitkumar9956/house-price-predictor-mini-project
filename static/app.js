/**
 * HousePrice.AI — Client-side Interactivity and Validation Controller
 */

const PRESETS = {
  family: {
    Neighborhood: "CollgCr",
    OverallQual: 6,
    OverallCond: 5,
    GrLivArea: 1600,
    LotArea: 8500,
    TotalBsmtSF: 900,
    BedroomAbvGr: 3,
    TotRmsAbvGrd: 6,
    FullBath: 2,
    HalfBath: 1,
    YearBuilt: 1995,
    YearRemodAdd: 2005,
    GarageCars: 2,
    GarageArea: 480
  },
  luxury: {
    Neighborhood: "NridgHt",
    OverallQual: 9,
    OverallCond: 5,
    GrLivArea: 2800,
    LotArea: 13000,
    TotalBsmtSF: 1800,
    BedroomAbvGr: 4,
    TotRmsAbvGrd: 9,
    FullBath: 3,
    HalfBath: 1,
    YearBuilt: 2018,
    YearRemodAdd: 2020,
    GarageCars: 3,
    GarageArea: 780
  },
  starter: {
    Neighborhood: "OldTown",
    OverallQual: 4,
    OverallCond: 4,
    GrLivArea: 950,
    LotArea: 5000,
    TotalBsmtSF: 600,
    BedroomAbvGr: 2,
    TotRmsAbvGrd: 4,
    FullBath: 1,
    HalfBath: 0,
    YearBuilt: 1950,
    YearRemodAdd: 1970,
    GarageCars: 1,
    GarageArea: 240
  }
};

function updateSliderBadge(badgeId, value, suffix = "") {
  const badge = document.getElementById(badgeId);
  if (badge) {
    badge.textContent = `${value} ${suffix}`.trim();
  }
}

function autoFillGarageArea(cars) {
  const areaInput = document.getElementById("garageArea");
  if (!areaInput) return;
  const numCars = parseInt(cars, 10);
  const defaults = { 0: 0, 1: 240, 2: 480, 3: 750, 4: 950 };
  areaInput.value = defaults[numCars] !== undefined ? defaults[numCars] : numCars * 240;
}

function applyPreset(name) {
  const data = PRESETS[name];
  if (!data) return;

  for (const [key, val] of Object.entries(data)) {
    const input = document.querySelector(`[name="${key}"]`);
    if (input) {
      input.value = val;
    }
  }

  updateSliderBadge("qualBadge", data.OverallQual, "/ 10");
  updateSliderBadge("condBadge", data.OverallCond, "/ 10");
  clearAlert();
}

function showAlert(message) {
  const alertEl = document.getElementById("clientAlert");
  const textEl = document.getElementById("clientAlertText");
  if (alertEl && textEl) {
    textEl.textContent = message;
    alertEl.classList.remove("hidden");
    alertEl.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

function clearAlert() {
  const alertEl = document.getElementById("clientAlert");
  if (alertEl) {
    alertEl.classList.add("hidden");
  }
}

function handleFormSubmit(event) {
  clearAlert();

  const form = document.getElementById("valuationForm");
  const grLivArea = parseFloat(form.GrLivArea.value);
  const lotArea = parseFloat(form.LotArea.value);
  const yearBuilt = parseInt(form.YearBuilt.value, 10);
  const yearRemod = parseInt(form.YearRemodAdd.value, 10);
  const qual = parseInt(form.OverallQual.value, 10);

  // Client-side validations
  if (isNaN(grLivArea) || grLivArea < 300 || grLivArea > 15000) {
    event.preventDefault();
    showAlert("Please enter a valid ground living area between 300 and 15,000 sq ft.");
    return false;
  }

  if (isNaN(lotArea) || lotArea < 500) {
    event.preventDefault();
    showAlert("Please enter a valid lot area of at least 500 sq ft.");
    return false;
  }

  if (yearRemod < yearBuilt) {
    event.preventDefault();
    showAlert(`Year Remodeled (${yearRemod}) cannot be earlier than Year Built (${yearBuilt}).`);
    return false;
  }

  if (isNaN(qual) || qual < 1 || qual > 10) {
    event.preventDefault();
    showAlert("Overall Quality rating must be between 1 and 10.");
    return false;
  }

  // Activate full-screen loading screen
  const overlay = document.getElementById("processingOverlay");
  const submitBtn = document.getElementById("submitBtn");
  if (overlay) {
    overlay.classList.remove("hidden");
  }
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.querySelector(".btn-text").textContent = "Calculating Valuation...";
  }

  // Allow standard form POST to continue to /calculate and redirect to /result
  return true;
}
