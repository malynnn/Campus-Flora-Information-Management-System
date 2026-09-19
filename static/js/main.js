/**
 * PUPQC CAMPUS PLANT DATABASE - MAIN JAVASCRIPT
 */

document.addEventListener("DOMContentLoaded", () => {
    // Initial load
    fetchCategories();
    fetchPlants();
    checkDatabaseStatus();
    setupEventListeners();
    initCookieNotice();
});

// State
let currentPlants = [];
let plantModal = null;
let addPlantModal = null;

function setupEventListeners() {
    // Search input live filtering
    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("input", debounce(() => {
            filterPlants();
        }, 300));
    }

    // Category select filter
    const categoryFilter = document.getElementById("categoryFilter");
    if (categoryFilter) {
        categoryFilter.addEventListener("change", () => {
            filterPlants();
        });
    }

    // Form submit for adding a plant
    const addPlantForm = document.getElementById("addPlantForm");
    if (addPlantForm) {
        addPlantForm.addEventListener("submit", handleAddPlantSubmit);
    }
}

/**
 * Fetch database status (MySQL vs SQLite fallback)
 */
async function checkDatabaseStatus() {
    try {
        const response = await fetch("/api/status");
        const data = await response.json();
        const badge = document.getElementById("dbStatusBadge");
        if (badge) {
            badge.textContent = data.database_engine;
            badge.className = data.database_engine.includes("MySQL") 
                ? "badge bg-success" 
                : "badge bg-warning text-dark";
        }
    } catch (err) {
        console.warn("Could not fetch DB status:", err);
    }
}

/**
 * Fetch Categories for filter dropdown & forms
 */
async function fetchCategories() {
    try {
        const response = await fetch("/api/categories");
        const data = await response.json();
        
        if (data.status === "success") {
            populateCategoryDropdowns(data.categories);
        }
    } catch (error) {
        console.error("Error fetching categories:", error);
    }
}

function populateCategoryDropdowns(categories) {
    const categoryFilter = document.getElementById("categoryFilter");
    const formCategorySelect = document.getElementById("plantCategorySelect");

    if (categoryFilter) {
        categoryFilter.innerHTML = '<option value="">All Categories</option>';
        categories.forEach(cat => {
            const opt = document.createElement("option");
            opt.value = cat.id;
            opt.textContent = cat.name;
            categoryFilter.appendChild(opt);
        });
    }

    if (formCategorySelect) {
        formCategorySelect.innerHTML = '<option value="">Select Category</option>';
        categories.forEach(cat => {
            const opt = document.createElement("option");
            opt.value = cat.id;
            opt.textContent = cat.name;
            formCategorySelect.appendChild(opt);
        });
    }
}

/**
 * Fetch Plants from API
 */
async function fetchPlants() {
    const container = document.getElementById("plantGridContainer");
    const countElement = document.getElementById("plantCount");

    if (container) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <div class="spinner-border text-danger" role="status">
                    <span class="visually-hidden">Loading flora data...</span>
                </div>
                <p class="mt-2 text-muted">Loading PUPQC Campus Plants...</p>
            </div>
        `;
    }

    try {
        const response = await fetch("/api/plants");
        const data = await response.json();

        if (data.status === "success") {
            currentPlants = data.plants;
            renderPlantGrid(currentPlants);
            if (countElement) {
                countElement.textContent = `Displaying ${currentPlants.length} Flora Entries`;
            }
        } else {
            showError("Failed to load plants data.");
        }
    } catch (error) {
        console.error("Error fetching plants:", error);
        showError("Unable to connect to the backend server.");
    }
}

/**
 * Filter plants locally by search query and category
 */
function filterPlants() {
    const searchVal = (document.getElementById("searchInput")?.value || "").toLowerCase().trim();
    const catVal = document.getElementById("categoryFilter")?.value || "";

    const filtered = currentPlants.filter(plant => {
        const matchesSearch = !searchVal || 
            (plant.common_name && plant.common_name.toLowerCase().includes(searchVal)) ||
            (plant.scientific_name && plant.scientific_name.toLowerCase().includes(searchVal)) ||
            (plant.local_name && plant.local_name.toLowerCase().includes(searchVal)) ||
            (plant.family && plant.family.toLowerCase().includes(searchVal)) ||
            (plant.location_in_campus && plant.location_in_campus.toLowerCase().includes(searchVal));

        const matchesCat = !catVal || String(plant.category_id) === String(catVal);

        return matchesSearch && matchesCat;
    });

    renderPlantGrid(filtered);

    const countElement = document.getElementById("plantCount");
    if (countElement) {
        countElement.textContent = `Displaying ${filtered.length} of ${currentPlants.length} Flora Entries`;
    }
}

/**
 * Render Plant Cards HTML
 */
function renderPlantGrid(plants) {
    const container = document.getElementById("plantGridContainer");
    if (!container) return;

    if (plants.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <div class="alert alert-warning d-inline-block px-4">
                    <i class="fas fa-seedling me-2"></i> No plants found matching your filter criteria.
                </div>
            </div>
        `;
        return;
    }

    let html = "";
    plants.forEach(plant => {
        const statusBadgeClass = plant.conservation_status === "Vulnerable" 
            ? "badge-vulnerable" 
            : "badge-least-concern";

        const categoryName = plant.category_name || "Campus Flora";
        const fallbackImg = "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?auto=format&fit=crop&w=600&q=80";
        const plantImg = plant.image_url || fallbackImg;

        html += `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="plant-card">
                    <div class="plant-card-img-wrapper">
                        <img src="${plantImg}" 
                             alt="${escapeHtml(plant.common_name)}" 
                             class="plant-card-img"
                             onerror="this.onerror=null; this.src='${fallbackImg}';">
                        <span class="badge-status ${statusBadgeClass}">
                            ${escapeHtml(plant.conservation_status || 'Least Concern')}
                        </span>
                    </div>
                    <div class="plant-card-body">
                        <div class="plant-scientific-name">${escapeHtml(plant.scientific_name)}</div>
                        <h3 class="plant-common-name">${escapeHtml(plant.common_name)}</h3>
                        <div class="plant-meta-info">
                            <div><i class="fas fa-layer-group"></i> <strong>Family:</strong> ${escapeHtml(plant.family)}</div>
                            <div><i class="fas fa-map-marker-alt"></i> <strong>Location:</strong> ${escapeHtml(plant.location_in_campus)}</div>
                            <div><i class="fas fa-tag"></i> <strong>Category:</strong> ${escapeHtml(categoryName)}</div>
                        </div>
                        <p class="card-text text-muted small flex-grow-1">
                            ${truncateText(plant.description || '', 90)}
                        </p>
                    </div>
                    <div class="plant-card-footer">
                        <button class="btn btn-pup-outline w-100 btn-sm" onclick="openPlantModal(${plant.id})">
                            <i class="fas fa-eye me-1"></i> View Full Details
                        </button>
                    </div>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}

/**
 * Open detail modal for a plant
 */
async function openPlantModal(plantId) {
    const plant = currentPlants.find(p => p.id === plantId);
    if (!plant) return;

    document.getElementById("modalCommonName").textContent = plant.common_name;
    document.getElementById("modalScientificName").textContent = plant.scientific_name;
    document.getElementById("modalLocalName").textContent = plant.local_name || plant.common_name;
    document.getElementById("modalFamily").textContent = plant.family;
    document.getElementById("modalLocation").textContent = plant.location_in_campus;
    document.getElementById("modalCategory").textContent = plant.category_name || "General Flora";
    document.getElementById("modalConservation").textContent = plant.conservation_status || "Least Concern";
    document.getElementById("modalDescription").textContent = plant.description || "No description provided.";
    document.getElementById("modalMedicinal").textContent = plant.medicinal_uses || "None specified.";
    document.getElementById("modalEcological").textContent = plant.ecological_role || "Provides campus greenery and urban microclimate moderation.";

    const fallbackImg = "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?auto=format&fit=crop&w=600&q=80";
    const imgEl = document.getElementById("modalPlantImg");
    if (imgEl) {
        imgEl.src = plant.image_url || fallbackImg;
        imgEl.onerror = () => { imgEl.src = fallbackImg; };
    }

    if (!plantModal) {
        plantModal = new bootstrap.Modal(document.getElementById("plantDetailModal"));
    }
    plantModal.show();
}

/**
 * Add New Plant Handler
 */
async function handleAddPlantSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    
    const payload = {
        common_name: formData.get("common_name"),
        scientific_name: formData.get("scientific_name"),
        local_name: formData.get("local_name"),
        family: formData.get("family"),
        category_id: formData.get("category_id"),
        conservation_status: formData.get("conservation_status"),
        location_in_campus: formData.get("location_in_campus"),
        description: formData.get("description"),
        medicinal_uses: formData.get("medicinal_uses"),
        ecological_role: formData.get("ecological_role"),
        image_url: formData.get("image_url")
    };

    try {
        const response = await fetch("/api/plants", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const resData = await response.json();
        if (response.ok && resData.status === "success") {
            alert("Plant added successfully to PUPQC Database!");
            form.reset();
            const modalEl = document.getElementById("addPlantModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            
            // Refresh plants grid
            fetchPlants();
        } else {
            alert("Error: " + (resData.message || "Failed to add plant."));
        }
    } catch (err) {
        console.error("Add plant error:", err);
        alert("Server error occurred while adding plant.");
    }
}

/**
 * Cookie banner notice handler
 */
function initCookieNotice() {
    const banner = document.getElementById("cookieBanner");
    if (!banner) return;

    if (localStorage.getItem("pupqc_cookie_accepted") === "true") {
        banner.style.display = "none";
    }
}

function acceptCookies() {
    localStorage.setItem("pupqc_cookie_accepted", "true");
    const banner = document.getElementById("cookieBanner");
    if (banner) banner.style.display = "none";
}

function declineCookies() {
    const banner = document.getElementById("cookieBanner");
    if (banner) banner.style.display = "none";
}

// Helpers
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function truncateText(text, length) {
    if (text.length <= length) return escapeHtml(text);
    return escapeHtml(text.substring(0, length)) + "...";
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showError(msg) {
    const container = document.getElementById("plantGridContainer");
    if (container) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <div class="alert alert-danger d-inline-block px-4">
                    <i class="fas fa-exclamation-triangle me-2"></i> ${escapeHtml(msg)}
                </div>
            </div>
        `;
    }
}
