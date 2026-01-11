// Removed imports

class ComplaintsController {
    constructor() {
        // We need to wait for DOM to be ready, but this script is likely loaded at bottom body or defer
        this.renderSidebar();
    }

    async renderSidebar() {
        const listContainer = document.getElementById('complaints-list');
        if (!listContainer) return;

        listContainer.innerHTML = '<div class="text-gray-400 text-sm text-center p-4">Yükleniyor...</div>';

        try {
            // Use global api - await the promise
            const complaints = await window.api.getComplaints();

            if (!complaints || complaints.length === 0) {
                listContainer.innerHTML = '<div class="text-gray-400 text-sm text-center p-4">Henüz şikayet kaydınız yok.</div>';
                return;
            }

            listContainer.innerHTML = complaints.map(c => {
                // Determine badge style and text
                let badgeClass = 'bg-yellow-600';
                let badgeText = c.status;

                if (c.status === 'Onaylandı') {
                    badgeClass = 'bg-green-600';
                    badgeText = 'Onaylandı';
                } else if (c.status === 'Reddedildi') {
                    badgeClass = 'bg-red-600';
                    badgeText = 'Onaylanmadı';
                } else {
                    // Default / In Review
                    badgeText = 'İnceleniyor';
                }

                // Handle camelCase vs snake_case
                // Backend sends: admin_note. Frontend previously used adminNote.
                const note = c.admin_note || c.adminNote;
                const dateStr = c.date || new Date(c.created_at).toLocaleDateString();

                return `
                <div onclick="window.location.href='complaint.html?id=${c.id}'" class="bg-blue-800/50 p-3 rounded mb-2 border border-blue-900 hover:border-blue-600 transition-colors cursor-pointer group hover:bg-blue-800/80">
                    <div class="flex justify-between items-start">
                        <span class="font-mono font-bold text-white">${c.plate}</span>
                        <span class="text-xs text-white px-1.5 py-0.5 rounded ${badgeClass}">${badgeText}</span>
                    </div>
                    <div class="text-xs text-gray-400 mt-1">${dateStr}</div>
                    <div class="text-xs text-gray-400 mt-1 truncate group-hover:text-gray-300">
                         <span class="text-blue-400 font-bold mr-1">[Detay]</span>${c.description}
                    </div>
                     ${note ? `
                    <div class="mt-2 text-xs p-2 rounded italic border break-words ${c.status === 'Onaylandı' ? 'bg-green-900/20 border-green-700/30 text-green-200/80' :
                            c.status === 'Reddedildi' ? 'bg-red-900/20 border-red-700/30 text-red-200/80' :
                                'bg-yellow-900/20 border-yellow-700/30 text-yellow-200/80'
                        }">
                        <span class="font-bold not-italic ${c.status === 'Onaylandı' ? 'text-green-500' :
                            c.status === 'Reddedildi' ? 'text-red-500' :
                                'text-yellow-500'
                        }">${c.status === 'Onaylandı' ? 'Açıklama:' :
                            c.status === 'Reddedildi' ? 'Red Gerekçesi:' :
                                'Yönetici Notu:'
                        }</span> ${note}
                    </div>` : ''}
                </div>
            `}).join('');

        } catch (error) {
            console.error('Failed to load complaints:', error);
            listContainer.innerHTML = '<div class="text-red-400 text-sm text-center p-4">Şikayetler yüklenemedi.</div>';
        }
    }

    submitComplaint(plate) {
        // Store selected plate for complaint page
        localStorage.setItem('current_complaint_plate', plate);
        window.location.href = 'complaint.html';
    }
}

// Make globally available
window.complaints = new ComplaintsController();
