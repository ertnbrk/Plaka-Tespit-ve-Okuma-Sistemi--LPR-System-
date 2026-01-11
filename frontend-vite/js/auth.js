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

        // Logout button
        const logoutBtn = document.getElementById('btn-logout');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                window.api.logout();
            });
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const submitBtn = e.target.querySelector('button[type="submit"]');

        if (submitBtn) submitBtn.disabled = true;

        try {
            console.log(`[Auth] Attempting login for ${email}`);
            const result = await window.api.login(email, password);
            console.log("[Auth] Login successful:", result);

            if (result.role === 'admin') {
                window.location.href = 'admin.html';
            } else {
                window.location.href = 'dashboard.html';
            }
        } catch (error) {
            console.error("[Auth] Login failed:", error);
            if (submitBtn) submitBtn.disabled = false;

            let message = error.message;
            if (message.includes('422')) {
                message = 'Girdiğiniz bilgileri kontrol ediniz (Eksik veya hatalı veri).';
            }
            if (message.includes('401')) {
                message = 'Hatalı e-posta veya şifre.';
            }

            if (window.ui && window.ui.showModal) window.ui.showModal('Giriş Başarısız', message);
            else alert('Giriş başarısız: ' + message);
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const submitBtn = e.target.querySelector('button[type="submit"]');

        console.log(`[Auth] Attempting registration for ${email}`);

        if (submitBtn) submitBtn.disabled = true;

        try {
            // 1. Register
            console.log("[Auth] Calling register API...");
            const regResponse = await window.api.register(name, email, password);
            console.log("[Auth] Registration response:", regResponse);

            // 2. Auto Login after success
            console.log("[Auth] Auto-logging in...");
            const result = await window.api.login(email, password);
            console.log("[Auth] Auto-login successful:", result);

            // 3. Redirect
            console.log("[Auth] Redirecting to dashboard...");
            window.location.href = 'dashboard.html';

        } catch (error) {
            console.error("[Auth] Registration error:", error);
            if (submitBtn) submitBtn.disabled = false;

            let message = error.message;
            if (message.includes('422')) {
                message = 'Girdiğiniz bilgileri kontrol ediniz (Eksik veya hatalı veri).';
            }
            if (message.includes('400')) {
                message = 'Bu e-posta adresi ile daha önce kayıt olunmuş.';
            }

            if (window.ui && window.ui.showModal) window.ui.showModal('Kayıt Başarısız', message);
            else alert('Kayıt başarısız: ' + message);
        }
    }

    checkAuth() {
        const token = localStorage.getItem('token');
        if (!token) {
            // Store current URL to redirect back after login? 
            // For now just simpler redirect
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
