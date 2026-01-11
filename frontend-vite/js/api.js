const API_BASE_URL = 'http://127.0.0.1:8000';

class ApiService {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers
        };

        // Don't set Content-Type for FormData (browser sets it with boundary)
        if (options.body instanceof FormData) {
            delete headers['Content-Type'];
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

            if (response.status === 401) {
                // Unauthorized - redirect to login
                console.warn('Unauthorized access, redirecting to login...');
                this.logout();
                return;
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || data.message || data.error || 'API Request Failed');
            }

            return data;

        } catch (error) {
            console.error(`API Error for ${endpoint}:`, error);
            throw error;
        }
    }

    // --- Authentication ---

    async login(email, password) {
        try {
            const data = await this.request('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });

            // Backend returns: { token: "...", user: { ... } }
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));

            return { success: true, role: data.user.role, user: data.user };
        } catch (error) {
            throw error;
        }
    }

    async register(name, email, password, role = 'officer') {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password, role })
        });
    }

    async getProfile() {
        return this.request('/auth/me');
    }

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/pages/login.html';
    }

    // --- Complaints ---

    async getComplaints(skip = 0, limit = 100) {
        // Backend handles filtering by role automatically
        return this.request(`/complaints/?skip=${skip}&limit=${limit}`);
    }

    async getComplaint(id) {
        return this.request(`/complaints/${id}`);
    }

    async saveComplaint(complaintData) {
        // complaintData should match backend schema: 
        // { plate, description, date, location, city, district, neighborhood, address_detail }
        return this.request('/complaints/', {
            method: 'POST',
            body: JSON.stringify(complaintData)
        });
    }

    async updateComplaint(id, status, admin_note) {
        // Only admins can do this
        return this.request(`/complaints/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ status, admin_note })
        });
    }

    // --- Detection & Analysis ---

    async detectImage(file) {
        const formData = new FormData();
        formData.append('file', file);

        // request() handles FormData content-type automatically
        return this.request('/predict', {
            method: 'POST',
            body: formData
        });
    }

    async detectVideo(file) {
        const formData = new FormData();
        formData.append('file', file);

        return this.request('/predict_video', {
            method: 'POST',
            body: formData
        });
    }

    async queryVehicle(plate) {
        // Using backend endpoint that queries mock DB
        return this.request('/api/vehicle/query', {
            method: 'POST',
            body: JSON.stringify({ plate, source: 'web_client', timestamp: new Date().toISOString() })
        });
    }
}

// Make globally available
window.api = new ApiService();
