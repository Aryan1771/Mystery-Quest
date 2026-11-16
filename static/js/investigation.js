/**
 * Mystery Quest – Investigation Room Interactivity
 * Handles AJAX Clue Collection and AJAX Rule-Based AI Hint Generation
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. AJAX Clue Collection
    const collectButtons = document.querySelectorAll('.btn-collect-clue');

    collectButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const url = btn.getAttribute('data-url');
            const clueId = btn.getAttribute('data-clue-id');
            const card = document.getElementById(`clue-card-${clueId}`);

            btn.disabled = true;
            btn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> Cataloging...`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Update Button & Card State
                    btn.className = "btn btn-sm btn-success disabled";
                    btn.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i> Cataloged`;
                    if (card) {
                        card.classList.add('collected');
                        const statusBadge = card.querySelector('.clue-status-badge');
                        if (statusBadge) {
                            statusBadge.className = "badge bg-success-subtle text-success border border-success clue-status-badge";
                            statusBadge.innerHTML = `<i class="bi bi-check2"></i> Cataloged`;
                        }
                    }

                    // Update Progress Bar
                    const progressBar = document.getElementById('caseProgressBar');
                    const progressText = document.getElementById('caseProgressText');
                    const clueCountText = document.getElementById('clueCountText');

                    if (progressBar) {
                        progressBar.style.width = `${data.progress_percent}%`;
                        progressBar.setAttribute('aria-valuenow', data.progress_percent);
                    }
                    if (progressText) {
                        progressText.textContent = `${data.progress_percent}%`;
                    }
                    if (clueCountText) {
                        clueCountText.textContent = `${data.collected_count} / ${data.total_count}`;
                    }

                    // Show transient alert
                    showToastNotification(data.message, 'success');
                } else {
                    btn.disabled = false;
                    btn.innerHTML = `<i class="bi bi-hand-index me-1"></i> Inspect & Catalog`;
                    showToastNotification('Could not catalog clue.', 'danger');
                }
            })
            .catch(err => {
                console.error('Clue collection error:', err);
                btn.disabled = false;
                btn.innerHTML = `<i class="bi bi-hand-index me-1"></i> Inspect & Catalog`;
            });
        });
    });

    // 2. AJAX Rule-Based AI Hint Generator
    const hintBtn = document.getElementById('requestHintBtn');
    const hintDisplay = document.getElementById('hintDisplayBox');

    if (hintBtn && hintDisplay) {
        hintBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const url = hintBtn.getAttribute('data-url');

            hintBtn.disabled = true;
            hintBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> Analyzing Deductions...`;

            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(res => res.json())
            .then(data => {
                hintBtn.disabled = false;
                hintBtn.innerHTML = `<i class="bi bi-lightbulb-fill text-warning me-1"></i> Request Another AI Hint (-15 pts)`;

                if (data.success) {
                    hintDisplay.classList.remove('d-none');
                    hintDisplay.innerHTML = `
                        <div class="alert alert-warning border-warning d-flex align-items-start gap-3 shadow-sm">
                            <i class="bi bi-robot fs-2 text-warning"></i>
                            <div>
                                <h6 class="alert-heading fw-bold mb-1"><i class="bi bi-cpu me-1"></i> AI Detective Hint (${data.level})</h6>
                                <p class="mb-1 text-light">${data.hint}</p>
                                <div class="small text-muted mt-2">
                                    <span class="badge bg-dark border border-secondary text-warning me-2">Focus: ${data.focus_area}</span>
                                    <span>Total hints consulted: <b>${data.hints_used}</b> (Score adjustment applied)</span>
                                </div>
                            </div>
                        </div>
                    `;
                    showToastNotification("AI Detective Hint retrieved!", 'info');
                }
            })
            .catch(err => {
                console.error('Hint fetch error:', err);
                hintBtn.disabled = false;
                hintBtn.innerHTML = `<i class="bi bi-lightbulb-fill text-warning me-1"></i> Request AI Clue Hint`;
            });
        });
    }

    // Helper: CSRF Cookie reader
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Helper: Toast message
    function showToastNotification(message, type='info') {
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
            toastContainer.style.zIndex = '1100';
            document.body.appendChild(toastContainer);
        }

        const toastEl = document.createElement('div');
        toastEl.className = `alert alert-${type} alert-dismissible fade show shadow-lg mb-2`;
        toastEl.role = 'alert';
        toastEl.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        toastContainer.appendChild(toastEl);

        setTimeout(() => {
            toastEl.classList.remove('show');
            setTimeout(() => toastEl.remove(), 200);
        }, 4000);
    }
});
