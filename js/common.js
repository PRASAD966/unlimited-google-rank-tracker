const $ = jQuery;

function toggleMenu() { jQuery('.mobinav').toggleClass('open'); }

// Dashboard sidebar toggle
// Dashboard sidebar toggle
function toggleDashboardSidebar() {
    const sidebar = document.querySelector('.dashboard-menu');
    const mainWrapper = document.querySelector('.dashboard-main-wrapper');
    const toggleButtons = document.querySelectorAll('.dashboard-toggle, .sidebar-toggle-btn');

    if (sidebar) {
        sidebar.classList.toggle('collapsed');
        const isCollapsed = sidebar.classList.contains('collapsed');

        // PERSIST STATE
        localStorage.setItem('sidebarCollapsed', isCollapsed);

        toggleButtons.forEach(btn => {
            if (isCollapsed) {
                // Show >> symbol
                btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="13 17 18 12 13 7"></polyline><polyline points="6 17 11 12 6 7"></polyline></svg>`;
            } else {
                // Show << symbol
                btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="11 17 6 12 11 7"></polyline><polyline points="18 17 13 12 18 7"></polyline></svg>`;
            }
        });
    }
    if (mainWrapper) {
        mainWrapper.classList.toggle('collapsed');
    }
}
function mobilesliders() {
    if (jQuery(window).width() <= 850) {
        jQuery('.rank-sec-btm-blk').addClass('owl-carousel').owlCarousel({
            loop: true,
            autoplay: true,
            autoplayTimeout: 3000,
            autoplayHoverPause: true,
            touchDrag: true,
            items: 1,
            mouseDrag: true,
            nav: false,
            dots: true,
            margin: 0,
            autoHeight: true
        });
    } else {
        jQuery('.rank-sec-btm-blk').trigger('destroy.owl.carousel').removeClass('owl-carousel');
    }
}
function login() {
    const username = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (username && password) {
        window.location.href = "/dashboard";
    } else {
        showAlert("Login Error", "Please fill in both username and password.");
    }
}

function togglePasswordVisibility(inputId, icon) {
    const input = document.getElementById(inputId);
    if (!input) return;

    if (input.type === "password") {
        input.type = "text";
        // Convert to 'eye-off' (slash) icon
        icon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
        `;
    } else {
        input.type = "password";
        // Convert back to 'eye' icon
        icon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
            </svg>
        `;
    }
}

jQuery(document).ready(function () {
    mobilesliders();
    jQuery(window).resize(mobilesliders);
    jQuery('.accordion-heading').on('click', function () {
        let parent = jQuery(this).parent();
        parent.children('.accordion-section-content').slideToggle(300);
        parent.siblings('.accordion-section').children('.accordion-section-content').slideUp(300);
        parent.toggleClass('accordien-active');
        parent.siblings('.accordion-section').removeClass('accordien-active');
    });
    /*
     * Tabs Section script
     */
    jQuery('.tab-btn-group .tab-btn').on('click', function () {
        const _t = jQuery(this);
        _t.addClass('tab-btn-active');
        _t.siblings('.tab-btn').removeClass('tab-btn-active');
        let index = _t.index();
        let tabcontent = _t.parent('.tab-btn-group').siblings('.tab-content-area').children('.tab-pane').eq(index);
        tabcontent.addClass('tab-pane-active');
        tabcontent.siblings('.tab-pane').removeClass('tab-pane-active');
    });
    jQuery('.logo-lst').owlCarousel({
        loop: true,
        touchDrag: true,
        mouseDrag: true,
        nav: false,
        dots: false,
        items: 4,
        margin: 0,
        autoplay: true,
        responsive: {
            0: {
                items: 1
            },
            850: {
                items: 4
            },
        }
    });
});

// Notifications Logic
function fetchNotifications() {
    fetch('/api/notifications')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('notificationList');
            const badge = document.getElementById('notificationBadge');
            if (!list || !badge) return;

            let unreadCount = data.filter(n => !n.is_read).length;
            if (unreadCount > 0) {
                badge.innerText = unreadCount > 9 ? '9+' : unreadCount;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
                badge.innerText = '';
            }

            if (data.length === 0) {
                list.innerHTML = '<div class="no-notifications">No notifications yet</div>';
                return;
            }

            list.innerHTML = data.map(n => `
                <div class="notification-item ${n.is_read ? '' : 'unread'}">
                    <div class="notification-item-text">${n.message}</div>
                    <div class="notification-item-time">${n.timestamp}</div>
                </div>
            `).join('');
        });
}

function markNotificationsAsRead() {
    fetch('/api/notifications/read', { method: 'POST' })
        .then(() => fetchNotifications());
}

function clearNotifications() {
    fetch('/api/notifications/delete-all', { method: 'POST' })
        .then(() => fetchNotifications());
}

function showToast(message) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.innerHTML = `
        <h6>New Notification</h6>
        <p>${message}</p>
    `;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Socket.IO Notifications
if (typeof socket !== 'undefined' || (typeof io !== 'undefined')) {
    const s = (typeof socket !== 'undefined') ? socket : io();
    s.on('new_notification', (data) => {
        showToast(data.message);
        fetchNotifications();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // RESTORE SIDEBAR STATE - RUN ASAP
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    const sidebar = document.querySelector('.dashboard-menu');
    const mainWrapper = document.querySelector('.dashboard-main-wrapper');
    const toggleButtons = document.querySelectorAll('.dashboard-toggle, .sidebar-toggle-btn');

    if (isCollapsed) {
        if (sidebar) sidebar.classList.add('collapsed');
        if (mainWrapper) mainWrapper.classList.add('collapsed');

        toggleButtons.forEach(btn => {
            btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="13 17 18 12 13 7"></polyline><polyline points="6 17 11 12 6 7"></polyline></svg>`;
        });
    }

    // Remove preload class to enable transitions AFTER state is restored
    setTimeout(() => {
        document.body.classList.remove('preload');
    }, 50);

    fetchNotifications();

    const bell = document.querySelector('.dashboard-notificaton-blk');
    const dropdown = document.getElementById('notificationDropdown');

    if (bell && dropdown) {
        bell.addEventListener('click', (e) => {
            e.stopPropagation();
            const isVisible = dropdown.style.display === 'flex';
            dropdown.style.display = isVisible ? 'none' : 'flex';
            if (!isVisible) markNotificationsAsRead();
        });
    }

    document.addEventListener('click', () => {
        if (dropdown) dropdown.style.display = 'none';
    });
});
// Custom Alert System
function showAlert(title, message, type = 'error') {
    // Create modal if it doesn't exist
    let modal = document.getElementById('customAlertModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'customAlertModal';
        modal.className = 'logout-overlay';
        modal.style.display = 'none';
        modal.style.zIndex = '10000';
        modal.innerHTML = `
            <div class="logout-modal" style="text-align: center; max-width: 400px;">
                <div id="alertIcon" style="margin-bottom: 20px;"></div>
                <h2 id="alertTitle" style="margin-bottom: 10px; font-size: 20px;"></h2>
                <p id="alertMessage" style="color: #666; margin-bottom: 25px; line-height: 1.5;"></p>
                <div class="logout-actions" style="justify-content: center;">
                    <button class="btn-logout" onclick="closeCustomAlert()" style="background: #00B29D; width: 156px; height: 36px; display: inline-flex; justify-content: center; align-items: center; padding: 0; font-family: 'Lexend Deca', sans-serif; font-size: 13px; font-weight: 500; line-height: 20px; border-radius: 8px;">OK</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    // Set content
    const titleEl = document.getElementById('alertTitle');
    const messageEl = document.getElementById('alertMessage');
    const iconEl = document.getElementById('alertIcon');

    titleEl.innerText = title;
    messageEl.innerText = message;

    // Set icon based on type
    if (type === 'error') {
        iconEl.innerHTML = `<svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;
    } else if (type === 'success') {
        iconEl.innerHTML = `<svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#00B29D" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
    } else {
        iconEl.innerHTML = `<svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#007bff" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`;
    }

    modal.style.display = 'flex';
}

function closeCustomAlert() {
    const modal = document.getElementById('customAlertModal');
    if (modal) modal.style.display = 'none';
}

// Custom Confirm System
let onConfirmCallback = null;
function showConfirm(title, message, onConfirm) {
    onConfirmCallback = onConfirm;
    let modal = document.getElementById('customConfirmModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'customConfirmModal';
        modal.className = 'logout-overlay';
        modal.style.display = 'none';
        modal.style.zIndex = '10000';
        modal.innerHTML = `
            <div class="logout-modal" style="text-align: center; max-width: 400px;">
                <div style="margin-bottom: 20px;">
                    <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                </div>
                <h2 id="confirmTitle" style="margin-bottom: 10px; font-size: 20px;"></h2>
                <p id="confirmMessage" style="color: #666; margin-bottom: 25px; line-height: 1.5;"></p>
                <div class="logout-actions" style="justify-content: center; gap: 15px;">
                    <button class="btn-cancel" onclick="closeCustomConfirm()" style="width: 156px; height: 36px; display: inline-flex; justify-content: center; align-items: center; padding: 0; font-family: 'Lexend Deca', sans-serif; font-size: 13px; font-weight: 500; line-height: 20px; border-radius: 8px;">Cancel</button>
                    <button class="btn-logout" onclick="handleConfirm()" style="background: #00B29D; width: 156px; height: 36px; display: inline-flex; justify-content: center; align-items: center; padding: 0; font-family: 'Lexend Deca', sans-serif; font-size: 13px; font-weight: 500; line-height: 20px; border-radius: 8px;">Confirm</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    document.getElementById('confirmTitle').innerText = title;
    document.getElementById('confirmMessage').innerText = message;
    modal.style.display = 'flex';
}

function closeCustomConfirm() {
    const modal = document.getElementById('customConfirmModal');
    if (modal) modal.style.display = 'none';
    onConfirmCallback = null;
}

function handleConfirm() {
    if (onConfirmCallback) onConfirmCallback();
    closeCustomConfirm();
}
