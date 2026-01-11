const API_BASE_URL = 'http://127.0.0.1:8000';

class ApiService {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
            
            if (response.status === 401) {
                // Unauthorized - redirect to login
                window.location.href = '/pages/login.html';
                return;
            }

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || data.error || 'API Request Failed');
            }

            return data;

        } catch (error) {
            console.error(`API Error for ${endpoint}:`, error);
            throw error;
        }
    }

    // Auth
    async login(email, password) {
        // Mocking auth logic
        try {
            // Demo User Credentials
            const demoUser = { email: 'demo@plaka.gov.tr', password: '123', name: 'Demo Memur', role: 'officer' };
            const adminUser = { email: 'admin@plaka.gov.tr', password: '123', name: 'Sistem Yöneticisi', role: 'admin' };
            
            // Check for locally registered user (mock database)
            const storedUser = JSON.parse(localStorage.getItem('registered_user'));

            // 1. Check Demo User
            if (email === demoUser.email && password === demoUser.password) {
                localStorage.setItem('user', JSON.stringify({ email: demoUser.email, name: demoUser.name, role: demoUser.role }));
                localStorage.setItem('token', 'mock-jwt-demo-' + Date.now());
                return { success: true, role: demoUser.role };
            }

            // 2. Check Admin User
            if (email === adminUser.email && password === adminUser.password) {
                localStorage.setItem('user', JSON.stringify({ email: adminUser.email, name: adminUser.name, role: adminUser.role }));
                localStorage.setItem('token', 'mock-jwt-admin-' + Date.now());
                return { success: true, role: adminUser.role };
            }

            // 3. Check Registered User
            if (storedUser && email === storedUser.email && password === storedUser.password) {
                localStorage.setItem('user', JSON.stringify({ email: storedUser.email, name: storedUser.name, role: 'officer' }));
                localStorage.setItem('token', 'mock-jwt-stored-' + Date.now());
                return { success: true, role: 'officer' };
            }
            
            throw new Error('Hatalı e-posta veya parola!');
        } catch (e) {
            throw e;
        }
    }

    async register(name, email, password) {
        // Mock register - save to "database" so login works later
        const newUser = { name, email, password };
        localStorage.setItem('registered_user', JSON.stringify(newUser));

        // Auto login
        localStorage.setItem('user', JSON.stringify({ email, name }));
        localStorage.setItem('token', 'mock-jwt-token-' + Date.now());
        return { success: true };
    }

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/pages/login.html';
    }

    // Detection
    async detectImage(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        // Using raw fetch to avoid content-type issues with FormData
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });
        
        return await response.json();
    }

    async detectVideo(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/predict_video`, {
            method: 'POST',
            body: formData
        });

        return await response.json();
    }

    // Vehicle Query (using existing endpoint)
    async queryVehicle(plate) {
        return this.request('/api/vehicle/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plate })
        });
    }

    // Complaints (Mock implementation as backend likely doesn't have this table)
    getComplaints() {
        const complaints = localStorage.getItem('complaints');
        return complaints ? JSON.parse(complaints) : [];
    }
    
    getComplaint(id) {
        const complaints = this.getComplaints();
        return complaints.find(c => c.id.toString() === id.toString());
    }

    saveComplaint(complaint) {
        const complaints = this.getComplaints();
        const newComplaint = {
            id: Date.now(),
            date: new Date().toLocaleDateString('tr-TR'),
            status: 'İnceleniyor',
            ...complaint
        };
        complaints.unshift(newComplaint);
        localStorage.setItem('complaints', JSON.stringify(complaints));
        return newComplaint;
    }

    updateComplaint(id, updatedData) {
        let complaints = this.getComplaints();
        const index = complaints.findIndex(c => c.id.toString() === id.toString());
        
        if (index !== -1) {
            complaints[index] = { ...complaints[index], ...updatedData };
            localStorage.setItem('complaints', JSON.stringify(complaints));
            return complaints[index];
        }
        return null;
    }
}

// Make globally available
window.api = new ApiService();
