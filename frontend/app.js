// Configuration
const API_URL = 'http://localhost:8001';

// Theme Management
const themeToggle = document.getElementById('theme-toggle');
const htmlElement = document.documentElement;
const toggleIcon = document.getElementById('toggle-icon');
const toggleText = document.getElementById('toggle-text');

themeToggle.addEventListener('click', () => {
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateToggleUI(newTheme);
});

function updateToggleUI(theme) {
    if (theme === 'light') {
        toggleIcon.setAttribute('data-lucide', 'sun');
        toggleText.innerText = 'Modo Claro';
    } else {
        toggleIcon.setAttribute('data-lucide', 'moon');
        toggleText.innerText = 'Modo Oscuro';
    }
    lucide.createIcons();
}

const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    htmlElement.setAttribute('data-theme', savedTheme);
    updateToggleUI(savedTheme);
}

// Stats Update
async function updateStats() {
    try {
        const response = await fetch(`${API_URL}/chain`);
        if (!response.ok) return;
        const data = await response.json();
        document.getElementById('stat-blocks').innerText = `#${data.length.toLocaleString()}`;
        document.getElementById('stat-nodes').innerText = Math.floor(150 + Math.random() * 10);
    } catch (error) {
        console.error('Error fetching chain stats:', error);
    }
}
setInterval(updateStats, 10000);
updateStats();

// Drag and Drop
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'var(--accent-primary)';
    dropZone.style.backgroundColor = 'rgba(0, 255, 204, 0.05)';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.borderColor = 'var(--border-color)';
    dropZone.style.backgroundColor = 'var(--bg-glass)';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'var(--border-color)';
    dropZone.style.backgroundColor = 'var(--bg-glass)';
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFile(files[0]);
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFile(e.target.files[0]);
});

function handleFile(file) {
    dropZone.innerHTML = `
        <i data-lucide="file-check" style="color: var(--accent-primary)"></i>
        <h3>${file.name}</h3>
        <p>Archivo listo para notarizar</p>
        <div style="margin-top: 1rem; display: flex; gap: 1rem;">
            <button class="btn-primary" id="notarize-btn">Notarizar Ahora</button>
            <button class="btn-primary" id="verify-btn" style="background: var(--bg-secondary); color: var(--text-primary); border: 1px solid var(--border-color);">Solo Verificar</button>
        </div>
    `;
    lucide.createIcons();
    
    document.getElementById('notarize-btn').addEventListener('click', () => notarizeFile(file));
    document.getElementById('verify-btn').addEventListener('click', () => verifyFile(file));
}

async function notarizeFile(file) {
    const btn = document.getElementById('notarize-btn');
    const originalText = btn.innerText;
    btn.innerText = 'Procesando...';
    btn.disabled = true;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('owner_address', '0x74a4e8b...f3c');
    formData.append('private_key_hex', 'mock_key');
    formData.append('description', 'Registro automático desde Web');

    try {
        const response = await fetch(`${API_URL}/notarize`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'Error interno del servidor');
        }
        
        showSuccess(result);
    } catch (error) {
        alert('❌ Error: ' + error.message);
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

async function verifyFile(file) {
    const btn = document.getElementById('verify-btn');
    const originalText = btn.innerText;
    btn.innerText = 'Verificando...';
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/verify`, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (!response.ok) throw new Error(result.detail);
        
        alert(`Estado: ${result.verified ? 'VERIFICADO ✅' : 'NO REGISTRADO ❌'}\n${result.message || ''}`);
    } catch (error) {
        alert('Error al verificar: ' + error.message);
    } finally {
        btn.innerText = originalText;
    }
}

function showSuccess(result) {
    dropZone.innerHTML = `
        <div style="text-align: center; animation: fadeIn 0.5s ease;">
            <i data-lucide="check-circle" style="color: var(--accent-primary); width: 64px; height: 64px; margin-bottom: 1rem;"></i>
            <h2 style="color: var(--accent-primary)">¡Notarización Exitosa!</h2>
            <p style="margin: 1rem 0;">Registrado permanentemente en el bloque #${result.block_index || '?'}.</p>
            <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem; font-family: monospace; font-size: 0.8rem; word-break: break-all;">
                Hash: ${result.document_hash || 'Sin Hash'}
            </div>
            <div style="display: flex; gap: 1rem; justify-content: center;">
                <button class="btn-primary" id="download-cert-btn">Descargar Certificado</button>
                <button class="btn-primary" style="background: var(--bg-secondary); color: var(--text-primary); border: 1px solid var(--border-color);" onclick="location.reload()">Nuevo Registro</button>
            </div>
            <div id="qrcode" style="display:none"></div>
        </div>
    `;
    lucide.createIcons();
    updateStats();

    document.getElementById('download-cert-btn').addEventListener('click', () => {
        generateCertificate(result);
    });
}

async function generateCertificate(result) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const primaryColor = [0, 255, 204];
    
    // Safety check for strings to avoid jsPDF errors
    const docHash = String(result.document_hash || 'N/A');
    const blockIdx = String(result.block_index || '0');
    const owner = String(result.owner || 'Anon');

    doc.setFillColor(10, 11, 16);
    doc.rect(0, 0, 210, 40, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(24);
    doc.setFont("helvetica", "bold");
    doc.text("NotaryChain", 20, 25);
    
    doc.setFontSize(10);
    doc.text("REGISTRO INMUTABLE BLOCKCHAIN", 140, 25);
    
    doc.setTextColor(10, 11, 16);
    doc.setFontSize(30);
    doc.text("CERTIFICADO DE", 20, 70);
    doc.text("AUTENTICIDAD", 20, 85);
    
    doc.setDrawColor(...primaryColor);
    doc.setLineWidth(2);
    doc.line(20, 95, 100, 95);
    
    doc.setFontSize(12);
    doc.setTextColor(100, 100, 100);
    doc.text("Por el presente se certifica que el activo digital ha sido registrado", 20, 115);
    doc.text("en la red descentralizada de NotaryChain.", 20, 122);
    
    doc.setFillColor(248, 250, 252);
    doc.rect(20, 135, 170, 80, 'F');
    doc.setDrawColor(226, 232, 240);
    doc.rect(20, 135, 170, 80, 'D');
    
    doc.setTextColor(10, 11, 16);
    doc.setFontSize(10);
    doc.setFont("helvetica", "bold");
    doc.text("HASH DEL DOCUMENTO (SHA-256):", 30, 150);
    doc.setFont("helvetica", "normal");
    doc.text(docHash, 30, 157);
    
    doc.setFont("helvetica", "bold");
    doc.text("ÍNDICE DE BLOQUE:", 30, 175);
    doc.setFont("helvetica", "normal");
    doc.text(`#${blockIdx}`, 30, 182);
    
    doc.setFont("helvetica", "bold");
    doc.text("FECHA DE REGISTRO:", 110, 175);
    doc.setFont("helvetica", "normal");
    doc.text(new Date().toLocaleString(), 110, 182);
    
    doc.setFont("helvetica", "bold");
    doc.text("DIRECCIÓN DEL PROPIETARIO:", 30, 200);
    doc.setFont("helvetica", "normal");
    doc.text(owner, 30, 207);

    const qrContainer = document.getElementById('qrcode');
    qrContainer.innerHTML = '';
    new QRCode(qrContainer, {
        text: `verify:${docHash}`,
        width: 100,
        height: 100
    });

    setTimeout(() => {
        const qrCanvas = qrContainer.querySelector('canvas');
        if (qrCanvas) {
            const qrImage = qrCanvas.toDataURL('image/png');
            doc.addImage(qrImage, 'PNG', 150, 60, 40, 40);
        }
        
        doc.save(`NotaryChain_Certificado_${blockIdx}.pdf`);
    }, 500);
}
