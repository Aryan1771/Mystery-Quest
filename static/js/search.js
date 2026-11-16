/**
 * Mystery Quest – Live AJAX Search
 * Uses native Fetch API with debouncing to search cases, clues, and suspects in real time.
 */

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('liveSearchInput');
    const categorySelect = document.getElementById('searchCategory');
    const resultsContainer = document.getElementById('searchResultsArea');
    const resultsCountBadge = document.getElementById('resultsCountBadge');
    const loadingSpinner = document.getElementById('searchSpinner');

    if (!searchInput) return;

    let debounceTimer;

    function performSearch() {
        const query = searchInput.value.trim();
        const category = categorySelect ? categorySelect.value : 'all';

        if (query.length === 0) {
            resultsContainer.innerHTML = `
                <div class="text-center py-5 text-muted">
                    <i class="bi bi-search fs-1 d-block mb-3 text-secondary"></i>
                    <h5>Enter a keyword to inspect case dockets, clues, or suspect profiles</h5>
                    <p class="small text-dim">Type at least 1 character to initiate search.</p>
                </div>
            `;
            if (resultsCountBadge) resultsCountBadge.textContent = '0 found';
            if (loadingSpinner) loadingSpinner.classList.add('d-none');
            return;
        }

        if (loadingSpinner) loadingSpinner.classList.remove('d-none');

        const url = `/api/search/?q=${encodeURIComponent(query)}&category=${encodeURIComponent(category)}`;

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Search network response was not ok');
            return response.json();
        })
        .then(data => {
            if (loadingSpinner) loadingSpinner.classList.add('d-none');
            renderSearchResults(data);
        })
        .catch(err => {
            if (loadingSpinner) loadingSpinner.classList.add('d-none');
            console.error('Search fetch error:', err);
            resultsContainer.innerHTML = `
                <div class="alert alert-danger my-3">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i> Error communicating with crime archive database. Please retry.
                </div>
            `;
        });
    }

    function renderSearchResults(data) {
        if (resultsCountBadge) {
            resultsCountBadge.textContent = `${data.total_count} record${data.total_count === 1 ? '' : 's'} found`;
        }

        if (data.total_count === 0) {
            resultsContainer.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-journal-x fs-1 text-warning d-block mb-3"></i>
                    <h5 class="text-light">No records matched your investigation query: "${escapeHtml(data.query)}"</h5>
                    <p class="text-muted">No cases, evidence clues, or suspects match this term. Try broadening your keywords, Detective.</p>
                </div>
            `;
            return;
        }

        let html = '';

        // 1. Cases
        if (data.cases && data.cases.length > 0) {
            html += `<h6 class="text-uppercase text-gold fw-bold mb-3"><i class="bi bi-briefcase-fill me-2"></i> Matching Investigation Cases (${data.cases.length})</h6>`;
            html += `<div class="row g-3 mb-4">`;
            data.cases.forEach(c => {
                const diffClass = c.difficulty === 'Easy' ? 'badge-diff-easy' : (c.difficulty === 'Medium' ? 'badge-diff-medium' : 'badge-diff-hard');
                html += `
                    <div class="col-md-6">
                        <div class="card-detective p-3 h-100">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h6 class="fw-bold mb-0"><a href="${c.url}" class="text-light">${escapeHtml(c.title)}</a></h6>
                                <span class="badge ${diffClass}">${c.difficulty}</span>
                            </div>
                            <p class="text-muted small mb-3">${escapeHtml(c.description)}</p>
                            <div class="mt-auto">
                                <a href="${c.url}" class="btn btn-sm btn-outline-gold"><i class="bi bi-folder2-open me-1"></i> Open Dossier</a>
                            </div>
                        </div>
                    </div>
                `;
            });
            html += `</div>`;
        }

        // 2. Clues
        if (data.clues && data.clues.length > 0) {
            html += `<h6 class="text-uppercase text-gold fw-bold mb-3"><i class="bi bi-search me-2"></i> Matching Investigation Clues (${data.clues.length})</h6>`;
            html += `<div class="row g-3 mb-4">`;
            data.clues.forEach(cl => {
                html += `
                    <div class="col-md-6">
                        <div class="card-detective p-3 h-100 border-secondary">
                            <div class="d-flex justify-content-between align-items-start mb-1">
                                <h6 class="text-gold fw-bold mb-0">${escapeHtml(cl.title)}</h6>
                                <span class="badge bg-secondary">${escapeHtml(cl.clue_type)}</span>
                            </div>
                            <div class="small text-dim mb-2"><i class="bi bi-link-45deg"></i> Case: ${escapeHtml(cl.case_title)}</div>
                            <p class="text-muted small mb-3">${escapeHtml(cl.description)}</p>
                            <div class="mt-auto">
                                <a href="${cl.url}" class="btn btn-sm btn-outline-light"><i class="bi bi-bullseye me-1"></i> View in Crime Room</a>
                            </div>
                        </div>
                    </div>
                `;
            });
            html += `</div>`;
        }

        // 3. Suspects
        if (data.suspects && data.suspects.length > 0) {
            html += `<h6 class="text-uppercase text-gold fw-bold mb-3"><i class="bi bi-person-bounding-box me-2"></i> Suspect Dossiers (${data.suspects.length})</h6>`;
            html += `<div class="row g-3 mb-4">`;
            data.suspects.forEach(s => {
                html += `
                    <div class="col-md-6">
                        <div class="card-detective p-3 h-100">
                            <div class="d-flex align-items-center gap-3 mb-2">
                                <div class="suspect-avatar" style="width:45px; height:45px; font-size:1.1rem;">
                                    <i class="bi bi-person-fill"></i>
                                </div>
                                <div>
                                    <h6 class="fw-bold mb-0 text-light">${escapeHtml(s.name)}</h6>
                                    <span class="small text-muted">${escapeHtml(s.profile)}</span>
                                </div>
                            </div>
                            <div class="small text-warning mb-1"><b>Motive:</b> ${escapeHtml(s.motive)}</div>
                        </div>
                    </div>
                `;
            });
            html += `</div>`;
        }

        resultsContainer.innerHTML = html;
    }

    function escapeHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(performSearch, 300);
    });

    if (categorySelect) {
        categorySelect.addEventListener('change', performSearch);
    }
});
