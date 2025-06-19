// header-system.js - Erstelle diese Datei in /static/js/
class HeaderSystem {
    constructor() {
        this.currentUser = null;
        this.initialized = false;
    }

    async init() {
        if (this.initialized) return;
        
        try {
            await this.loadCurrentUser();
            this.renderHeader();
            this.initialized = true;
        } catch (error) {
            console.error('Header System Error:', error);
            this.renderGuestHeader();
        }
    }

    async loadCurrentUser() {
        const response = await fetch('/api/current-user');
        if (response.ok) {
            this.currentUser = await response.json();
        } else {
            throw new Error('Not authenticated');
        }
    }

    renderHeader() {
        const headerElement = document.getElementById('dynamic-header');
        if (!headerElement) return;

        if (this.currentUser && this.currentUser.authenticated) {
            if (this.currentUser.role === 'admin') {
                headerElement.innerHTML = this.getAdminHeader();
            } else {
                headerElement.innerHTML = this.getUserHeader();
            }
        } else {
            headerElement.innerHTML = this.getGuestHeader();
        }

        // Event Listeners hinzufügen
        this.attachEventListeners();
    }

    getAdminHeader() {
        return `
            <nav class="navbar">
                <div class="navbar-container">
                    <div class="navbar-brand">
                        <a href="/static/index.html">StudiLiving</a>
                        <span class="admin-badge">Admin</span>
                    </div>
                    <div class="navbar-menu">
                        <a href="/static/index.html" class="navbar-item">Start</a>
                        <a href="/static/admin_users.html" class="navbar-item admin-item">Nutzer verwalten</a>
                        <a href="/static/profil.html" class="navbar-item">Profil</a>
                        <a href="/static/my_properties.html" class="navbar-item">Meine Immobilien</a>
                        <a href="/static/create_property.html" class="navbar-item">Neue Immobilie</a>
                        <a href="/static/map.html" class="navbar-item">Karte</a>
                        <button onclick="headerSystem.logout()" class="navbar-item logout-btn">Logout (${this.currentUser.username})</button>
                    </div>
                </div>
            </nav>
        `;
    }

    getUserHeader() {
        return `
            <nav class="navbar">
                <div class="navbar-container">
                    <div class="navbar-brand">
                        <a href="/static/index.html">StudiLiving</a>
                    </div>
                    <div class="navbar-menu">
                        <a href="/static/index.html" class="navbar-item">Start</a>
                        <a href="/static/map.html" class="navbar-item">Karte</a>
                        <a href="/static/profil.html" class="navbar-item">Profil</a>
                        <button onclick="headerSystem.logout()" class="navbar-item logout-btn">Logout (${this.currentUser.username})</button>
                    </div>
                </div>
            </nav>
        `;
    }

    getGuestHeader() {
        return `
            <nav class="navbar">
                <div class="navbar-container">
                    <div class="navbar-brand">
                        <a href="/static/index.html">StudiLiving</a>
                    </div>
                    <div class="navbar-menu">
                        <a href="/static/index.html" class="navbar-item">Start</a>
                        <a href="/static/login.html" class="navbar-item">Login</a>
                        <a href="/static/register.html" class="navbar-item">Registrieren</a>
                    </div>
                </div>
            </nav>
        `;
    }

    renderGuestHeader() {
        const headerElement = document.getElementById('dynamic-header');
        if (headerElement) {
            headerElement.innerHTML = this.getGuestHeader();
        }
    }

    attachEventListeners() {
        // Hier können zusätzliche Event Listeners hinzugefügt werden
        // z.B. für Mobile Menu Toggle
    }

    async logout() {
        try {
            await fetch('/logout');
            window.location.href = '/static/index.html';
        } catch (error) {
            console.error('Logout error:', error);
            window.location.href = '/static/index.html';
        }
    }
}

// Globale Instanz erstellen
const headerSystem = new HeaderSystem();

// Automatisch initialisieren wenn DOM geladen ist
document.addEventListener('DOMContentLoaded', () => {
    headerSystem.init();
});