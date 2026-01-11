class AdminController {
    constructor() {
        this.init();
    }

    async init() {
        // Auth Check
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user || user.role !== 'admin') {
            if (window.ui) window.ui.showModal('Erişim Reddedildi', 'Bu sayfaya erişim yetkiniz yok!');
            else alert('Bu sayfaya erişim yetkiniz yok!');

            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 2000);
            return;
        }

        document.getElementById('user-name-display').textContent = user.name;

        // Initialize State for Filtering
        this.currentStatusFilter = '';

        // Initial render
        await this.renderTable();
        await this.renderStats();

        // Search Listener
        const searchInput = document.getElementById('searchPlate');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.renderTable(e.target.value);
            });
        }
    }

    // New method for filtering by status
    filterByStatus(status) {
        this.currentStatusFilter = status;
        const searchVal = document.getElementById('searchPlate').value;
        this.renderTable(searchVal);
    }

    async renderStats() {
        try {
            const complaints = await window.api.getComplaints();
            const total = complaints.length;
            const pending = complaints.filter(c => c.status === 'İnceleniyor').length;
            const approved = complaints.filter(c => c.status === 'Onaylandı').length;
            const rejected = complaints.filter(c => c.status === 'Reddedildi').length;

            document.getElementById('stat-total').textContent = total;
            document.getElementById('stat-pending').textContent = pending;
            document.getElementById('stat-approved').textContent = approved;
            document.getElementById('stat-rejected').textContent = rejected;
        } catch (error) {
            console.error("Stats render error:", error);
        }
    }

    async renderTable(searchTerm = '') {
        const tbody = document.getElementById('admin-table-body');
        if (!tbody) return;

        tbody.innerHTML = '<tr><td colspan="6" class="px-6 py-4 text-center text-gray-400">Yükleniyor...</td></tr>';

        try {
            const complaints = await window.api.getComplaints();

            // Updated filtering logic
            const filtered = complaints.filter(c => {
                const matchesSearch = c.plate.toLowerCase().includes(searchTerm.toLowerCase()) ||
                    (c.description && c.description.toLowerCase().includes(searchTerm.toLowerCase()));

                const matchesStatus = this.currentStatusFilter === '' || c.status === this.currentStatusFilter;

                return matchesSearch && matchesStatus;
            });

            document.getElementById('showing-info').textContent = `Toplam ${filtered.length} kayıt gösteriliyor` +
                (this.currentStatusFilter ? ` (${this.currentStatusFilter})` : '');

            if (filtered.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="px-6 py-4 text-center text-gray-400">Kayıt bulunamadı.</td></tr>';
                return;
            }

            tbody.innerHTML = filtered.map(c => `
                <tr class="hover:bg-[#1E3A5F]/50 transition-colors">
                    <td class="px-6 py-4 whitespace-nowrap text-gray-300 font-mono text-xs">${c.date || new Date(c.created_at).toLocaleDateString()}</td>
                    <td class="px-6 py-4 whitespace-nowrap font-bold text-white font-mono">${c.plate}</td>
                    <td class="px-6 py-4 text-gray-300 truncate max-w-xs" title="${c.location || ''}">${c.location || '-'}</td>
                    <td class="px-6 py-4 text-gray-400 truncate max-w-xs">${c.description || '-'}</td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-1 rounded text-xs border ${this.getStatusColor(c.status)}">
                            ${c.status}
                        </span>
                    </td>
                    <td class="px-6 py-4 text-right whitespace-nowrap">
                        <div class="flex items-center justify-end space-x-2">
                            <button onclick="admin.openModal(${c.id})" class="text-xs bg-blue-900/50 border border-blue-700 hover:bg-blue-800 text-blue-100 px-3 py-1 rounded transition-colors">
                                İncele
                            </button>
                            ${c.status === 'İnceleniyor' ? `
                            <button onclick="admin.updateStatus(${c.id}, 'Onaylandı', 'Bildiriminiz sistem yöneticisi tarafından incelenmiş ve onaylanmıştır.')" class="text-xs bg-green-900 overflow-hidden border border-green-700 hover:bg-green-800 text-green-100 px-2 py-1 rounded transition-colors inline-flex items-center justify-center h-7 w-7" title="Otomatik Onayla">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                            </button>
                            <button onclick="admin.updateStatus(${c.id}, 'Reddedildi', 'Bildiriminiz sistem yöneticisi tarafından reddedilmiştir.')" class="text-xs bg-red-900 border border-red-700 hover:bg-red-800 text-red-100 px-2 py-1 rounded transition-colors inline-flex items-center justify-center h-7 w-7" title="Otomatik Reddet">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                            </button>
                            ` : ''}
                        </div>
                    </td>
                </tr>
            `).join('');
        } catch (error) {
            console.error("Table render error:", error);
            tbody.innerHTML = '<tr><td colspan="6" class="px-6 py-4 text-center text-red-400">Veri yüklenemedi.</td></tr>';
        }
    }

    // Modal Actions
    async openModal(id) {
        try {
            const complaint = await window.api.getComplaint(id);
            if (!complaint) return;

            this.currentId = id; // Store for actions

            document.getElementById('modal-plate').textContent = complaint.plate;
            document.getElementById('modal-date').textContent = complaint.date || new Date(complaint.created_at).toLocaleDateString();
            document.getElementById('modal-location').textContent = complaint.location || '-';
            document.getElementById('modal-description').textContent = complaint.description || 'Açıklama yok.';

            // Admin Note
            const noteInput = document.getElementById('modal-admin-note');
            // Backend sends snake_case
            noteInput.value = complaint.admin_note || complaint.adminNote || '';
            noteInput.disabled = false; // Always allow editing

            // Status Badge
            const statusBadge = document.getElementById('modal-status-badge');
            statusBadge.className = `px-3 py-1 rounded text-sm font-bold border ${this.getStatusColor(complaint.status)}`;
            statusBadge.textContent = complaint.status;

            // Actions (Always allow updating status)
            const actionsDiv = document.getElementById('modal-actions');
            actionsDiv.innerHTML = `
                <button onclick="admin.updateStatusFromModal('Onaylandı')" 
                    class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm font-bold shadow transition-colors ${complaint.status === 'Onaylandı' ? 'opacity-50 cursor-not-allowed' : ''}" 
                    ${complaint.status === 'Onaylandı' ? 'disabled' : ''}>
                    ONAYLA
                </button>
                <button onclick="admin.updateStatusFromModal('Reddedildi')" 
                    class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded text-sm font-bold shadow transition-colors ${complaint.status === 'Reddedildi' ? 'opacity-50 cursor-not-allowed' : ''}" 
                    ${complaint.status === 'Reddedildi' ? 'disabled' : ''}>
                    REDDET
                </button>
            `;

            document.getElementById('detailModal').classList.remove('hidden');
        } catch (error) {
            console.error(error);
            alert("Detaylar yüklenemedi.");
        }
    }

    closeModal() {
        document.getElementById('detailModal').classList.add('hidden');
    }

    updateStatusFromModal(newStatus) {
        if (this.currentId) {
            let note = document.getElementById('modal-admin-note').value.trim();

            // Auto-fill note if empty
            if (!note) {
                if (newStatus === 'Onaylandı') note = 'Bildiriminiz sistem yöneticisi tarafından incelenmiş ve onaylanmıştır.';
                if (newStatus === 'Reddedildi') note = 'Bildiriminiz sistem yöneticisi tarafından reddedilmiştir.';
            }

            this.updateStatus(this.currentId, newStatus, note);
            this.closeModal();
        }
    }

    getStatusColor(status) {
        switch (status) {
            case 'Onaylandı': return 'bg-green-900/30 border-green-700 text-green-400';
            case 'Reddedildi': return 'bg-red-900/30 border-red-700 text-red-400';
            default: return 'bg-yellow-900/30 border-yellow-700 text-yellow-400';
        }
    }

    updateStatus(id, newStatus, note = '') {
        const confirmMsg = note ?
            `Bu kaydı "<strong>${newStatus}</strong>" olarak işaretlemek üzeresiniz.<br><br>Not: ${note}<br><br>Onaylıyor musunuz?` :
            `Bu kaydı "<strong>${newStatus}</strong>" olarak işaretlemek istediğinize emin misiniz?`;

        if (window.ui) {
            window.ui.showConfirm('İşlem Onayı', confirmMsg, () => {
                this.performUpdate(id, newStatus, note);
            });
        } else {
            if (confirm(confirmMsg.replace(/<br>/g, '\n').replace(/<\/?strong>/g, ''))) {
                this.performUpdate(id, newStatus, note);
            }
        }
    }

    async performUpdate(id, newStatus, note) {
        try {
            await window.api.updateComplaint(id, newStatus, note);
            // Refresh
            const searchVal = document.getElementById('searchPlate').value;
            this.renderTable(searchVal);
            this.renderStats();

            if (window.ui) window.ui.showModal('Başarılı', 'İşlem başarıyla tamamlandı.');
        } catch (error) {
            if (window.ui) window.ui.showModal('Hata', error.message);
            else alert('Hata: ' + error.message);
        }
    }
}

// Init
if (typeof window !== 'undefined') {
    window.admin = new AdminController();
}
