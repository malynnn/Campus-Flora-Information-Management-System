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
            // Update research section count
            const researchCount = document.getElementById("researchPlantCount");
            if (researchCount) researchCount.textContent = currentPlants.length;
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
            : plant.conservation_status === "Concerning"
            ? "badge-concerning"
            : "badge-least-concern";

        const categoryName = plant.category_name || "Campus Flora";

        const imgSection = plant.image_url
            ? `<img src="${plant.image_url}" 
                     alt="${escapeHtml(plant.common_name)}" 
                     class="plant-card-img"
                     onerror="this.style.display='none';this.nextElementSibling&&(this.nextElementSibling.style.display='flex');">` 
            : `<div class="plant-card-img d-flex flex-column align-items-center justify-content-center" 
                     style="background:linear-gradient(135deg,#e8f5e9,#c8e6c9);height:220px;">
                   <i class="fas fa-leaf" style="font-size:3rem;color:#4caf50;opacity:0.5;"></i>
                   <small class="text-muted mt-2" style="font-size:0.75rem;">No Photo Available</small>
               </div>`;

        html += `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="plant-card">
                    <div class="plant-card-img-wrapper">
                        ${imgSection}
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
                            <div><i class="fas fa-hashtag"></i> <strong>Quantity in PUPQC:</strong> ${plant.quantity ? plant.quantity + ' individual(s)' : 'Not recorded'}</div>
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
 * Open detail modal for a plant with photo gallery carousel
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

    const qtyEl = document.getElementById("modalQuantity");
    if (qtyEl) {
        qtyEl.textContent = plant.quantity ? `${plant.quantity} individual(s) recorded in PUPQC` : "Not recorded";
    }

    // Set conservation badge color
    const conservationBadge = document.getElementById("modalConservation");
    const statusColorMap = {
        "Least Concern": "bg-success",
        "Vulnerable": "bg-warning text-dark",
        "Concerning": "bg-orange text-white",
        "Endangered": "bg-orange text-white",
        "Critically Endangered": "bg-danger"
    };
    conservationBadge.className = "badge px-3 py-2 fs-6 " + (statusColorMap[plant.conservation_status] || "bg-success");

    // Build carousel
    const carouselInner = document.getElementById("carouselInner");
    const thumbnails = document.getElementById("photoThumbnails");
    const prevBtn = document.getElementById("carouselPrevBtn");
    const nextBtn = document.getElementById("carouselNextBtn");

    carouselInner.innerHTML = '<div class="carousel-item active"><div class="d-flex justify-content-center align-items-center" style="height:300px;background:#f0f0f0;"><div class="spinner-border text-danger"></div></div></div>';
    thumbnails.innerHTML = "";

    // Fetch gallery images
    let images = [];
    try {
        const res = await fetch(`/api/plants/${plantId}/images`);
        const data = await res.json();
        if (data.status === "success" && data.images.length > 0) {
            images = data.images;
        }
    } catch (e) {}

    // If no gallery images and plant has an image_url, use it; else show no-photo placeholder
    if (images.length === 0) {
        if (plant.image_url) {
            images = [{ image_url: plant.image_url, caption: plant.common_name, is_primary: 1 }];
        }
    }

    // Build carousel slides or no-photo placeholder
    if (images.length === 0) {
        carouselInner.innerHTML = `
            <div class="carousel-item active">
                <div class="d-flex flex-column align-items-center justify-content-center"
                     style="height:300px;background:linear-gradient(135deg,#e8f5e9,#c8e6c9);">
                    <i class="fas fa-leaf" style="font-size:4rem;color:#4caf50;opacity:0.45;"></i>
                    <p class="text-muted mt-3 mb-0" style="font-size:0.95rem;">No Photo Available</p>
                    <small class="text-muted">${escapeHtml(plant.common_name)}</small>
                </div>
            </div>`;
        prevBtn.style.display = "none";
        nextBtn.style.display = "none";
        thumbnails.innerHTML = "";
    } else {
        carouselInner.innerHTML = images.map((img, i) => `
            <div class="carousel-item ${i === 0 ? 'active' : ''}">
                <img src="${img.image_url}" 
                     alt="${escapeHtml(img.caption || plant.common_name)}"
                     class="d-block w-100"
                     style="max-height:300px; object-fit:cover;"
                     onerror="this.parentElement.innerHTML='<div class=\'d-flex flex-column align-items-center justify-content-center\' style=\'height:300px;background:linear-gradient(135deg,#e8f5e9,#c8e6c9);\'><i class=\'fas fa-leaf\' style=\'font-size:4rem;color:#4caf50;opacity:0.45;\'></i><p class=\'text-muted mt-3\'>No Photo Available</p></div>'">
                ${images.length > 1 ? `<div class="carousel-caption d-none d-md-block" style="background:rgba(0,0,0,0.4);border-radius:6px;bottom:8px;padding:4px 10px;">
                    <small>${escapeHtml(img.caption || '')}</small>
                </div>` : ''}
            </div>
        `).join('');

        if (images.length > 1) {
            prevBtn.style.display = "";
            nextBtn.style.display = "";
            thumbnails.innerHTML = images.map((img, i) => `
                <img src="${img.image_url}" 
                     alt="Photo ${i+1}"
                     class="rounded border ${i === 0 ? 'border-danger border-2' : 'border-secondary'}"
                     style="width:56px;height:56px;object-fit:cover;cursor:pointer;transition:opacity 0.2s;"
                     onclick="goToSlide(${i}, this)">
            `).join('');
        } else {
            prevBtn.style.display = "none";
            nextBtn.style.display = "none";
            thumbnails.innerHTML = "";
        }
    }

    if (!plantModal) {
        plantModal = new bootstrap.Modal(document.getElementById("plantDetailModal"));
    }
    plantModal.show();
}

/**
 * Navigate carousel to a specific slide and highlight the clicked thumbnail
 */
function goToSlide(index, thumbEl) {
    const carousel = bootstrap.Carousel.getOrCreateInstance(document.getElementById("plantPhotoCarousel"));
    carousel.to(index);
    // Highlight active thumbnail
    document.querySelectorAll("#photoThumbnails img").forEach(img => {
        img.classList.remove("border-danger", "border-2");
        img.classList.add("border-secondary");
        img.style.opacity = "0.7";
    });
    if (thumbEl) {
        thumbEl.classList.remove("border-secondary");
        thumbEl.classList.add("border-danger", "border-2");
        thumbEl.style.opacity = "1";
    }
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
