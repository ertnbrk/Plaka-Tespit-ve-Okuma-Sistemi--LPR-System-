// Removed import, relying on global window.api

class AuthController {
    constructor() {
        this.bindEvents();
    }

    bindEvents() {
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }

        // Check auth status on protected pages
        if (!window.location.pathname.includes('login.html') && 
            !window.location.pathname.includes('register.html')) {
            this.checkAuth();
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const result = await window.api.login(email, password);
             if (result.role === 'admin') {
                window.location.href = 'admin.html';
            } else {
                window.location.href = 'dashboard.html';
            }
        } catch (error) {
            if(window.ui) window.ui.showModal('Giriş Başarısız', error.message);
            else alert('Giriş başarısız: ' + error.message);
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            await api.register(name, email, password);
            window.location.href = 'dashboard.html';
        } catch (error) {
            if(window.ui) window.ui.showModal('Kayıt Başarısız', error.message);
            else alert('Kayıt başarısız: ' + error.message);
        }
    }

    checkAuth() {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = 'login.html';
        } else {
            const user = JSON.parse(localStorage.getItem('user'));
            const userNameDisplay = document.getElementById('user-name-display');
            if (userNameDisplay && user) {
                userNameDisplay.textContent = user.name;
            }
        }
    }
}

// Initialize only if we are in browser environment
if (typeof window !== 'undefined') {
    new AuthController();
}
