import { notarize, verify } from './api.js';
import { showToast }        from './utils.js';

export const initDropZone = () => {
  const zone  = document.getElementById('drop-zone');
  const input = document.getElementById('file-input');

  zone.addEventListener('click', () => input.click());
  zone.addEventListener('dragover',  (e) => { e.preventDefault(); zone.classList.add('drop-zone--active'); });
  zone.addEventListener('dragleave', ()  => zone.classList.remove('drop-zone--active'));
  zone.addEventListener('drop', (e) => {
    e.preventDefault();
    zone.classList.remove('drop-zone--active');
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  });
  input.addEventListener('change', (e) => {
    if (e.target.files[0]) handleFile(e.target.files[0]);
  });
};

const handleFile = (file) => {
  const zone = document.getElementById('drop-zone');
  zone.classList.add('drop-zone--success');
  zone.innerHTML = `
    <i data-lucide="file-check" class="drop-zone__icon"></i>
    <h3>${file.name}</h3>
    <p class="drop-zone__subtitle">Archivo listo para notarizar</p>
    <div class="drop-zone__actions">
      <button class="btn btn--primary" id="btn-notarize">Notarizar Ahora</button>
      <button class="btn btn--ghost"   id="btn-verify">Solo Verificar</button>
    </div>
  `;
  lucide.createIcons();
  document.getElementById('btn-notarize').addEventListener('click', () => doNotarize(file));
  document.getElementById('btn-verify').addEventListener('click',   () => doVerify(file));
};

const doNotarize = async (file) => {
  const btn = document.getElementById('btn-notarize');
  btn.disabled = true;
  btn.classList.add('btn--loading');
  btn.textContent = 'Procesando...';

  const formData = new FormData();
  formData.append('file',            file);
  formData.append('owner_address',   '0x74a4e8b...f3c');
  formData.append('private_key_hex', 'mock_key');
  formData.append('description',     'Registro automático desde Web');

  try {
    const res    = await notarize(formData);
    const result = await res.json();
    if (!res.ok) throw new Error(result.detail || 'Error del servidor');
    showSuccess(result);
  } catch (err) {
    showToast('Error: ' + err.message, 'error');
    btn.disabled = false;
    btn.classList.remove('btn--loading');
    btn.textContent = 'Notarizar Ahora';
  }
};

const doVerify = async (file) => {
  const btn = document.getElementById('btn-verify');
  btn.disabled = true;
  btn.textContent = 'Verificando...';
  const formData = new FormData();
  formData.append('file', file);
  try {
    const res    = await verify(formData);
    const result = await res.json();
    if (!res.ok) throw new Error(result.detail);
    showToast(
      result.verified ? 'Documento VERIFICADO ✅' : 'No registrado en cadena ❌',
      result.verified ? 'success' : 'error'
    );
  } catch (err) {
    showToast('Error al verificar: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Solo Verificar';
  }
};

const showSuccess = (result) => {
  const zone = document.getElementById('drop-zone');
  zone.innerHTML = `
    <i data-lucide="check-circle" class="drop-zone__icon" style="color:var(--accent-primary)"></i>
    <h2 style="color:var(--accent-primary)">¡Notarización Exitosa!</h2>
    <p>Registrado en el bloque <strong>#${result.block_index ?? '?'}</strong></p>
    <div class="hash-display">${result.document_hash ?? 'Sin hash'}</div>
    <div class="drop-zone__actions">
      <button class="btn btn--primary" id="btn-cert">Descargar Certificado</button>
      <button class="btn btn--ghost" onclick="location.reload()">Nuevo Registro</button>
    </div>
    <div id="qrcode" style="display:none"></div>
  `;
  lucide.createIcons();
  document.getElementById('btn-cert').addEventListener('click', () => generateCertificate(result));
};

const generateCertificate = (result) => {
  const { jsPDF } = window.jspdf;
  const doc       = new jsPDF();
  const docHash   = String(result.document_hash  ?? 'N/A');
  const blockIdx  = String(result.block_index     ?? '0');
  const owner     = String(result.owner           ?? 'Anon');

  doc.setFillColor(10, 11, 16);
  doc.rect(0, 0, 210, 40, 'F');
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(24);
  doc.setFont('helvetica', 'bold');
  doc.text('NotaryChain', 20, 25);
  doc.setFontSize(10);
  doc.text('REGISTRO INMUTABLE BLOCKCHAIN', 140, 25);

  doc.setTextColor(10, 11, 16);
  doc.setFontSize(30);
  doc.text('CERTIFICADO DE', 20, 70);
  doc.text('AUTENTICIDAD',   20, 85);

  doc.setDrawColor(0, 255, 204);
  doc.setLineWidth(2);
  doc.line(20, 95, 100, 95);

  doc.setFontSize(12);
  doc.setTextColor(100, 100, 100);
  doc.text('Por el presente se certifica que el activo digital ha sido registrado', 20, 115);
  doc.text('en la red descentralizada de NotaryChain.', 20, 122);

  doc.setFillColor(248, 250, 252);
  doc.rect(20, 135, 170, 80, 'F');
  doc.setDrawColor(226, 232, 240);
  doc.rect(20, 135, 170, 80, 'D');

  doc.setTextColor(10, 11, 16);
  doc.setFontSize(10);
  doc.setFont('helvetica', 'bold');
  doc.text('HASH DEL DOCUMENTO (SHA-256):', 30, 150);
  doc.setFont('helvetica', 'normal');
  doc.text(docHash, 30, 157);

  doc.setFont('helvetica', 'bold');
  doc.text('ÍNDICE DE BLOQUE:', 30, 175);
  doc.setFont('helvetica', 'normal');
  doc.text('#' + blockIdx, 30, 182);

  doc.setFont('helvetica', 'bold');
  doc.text('FECHA DE REGISTRO:', 110, 175);
  doc.setFont('helvetica', 'normal');
  doc.text(new Date().toLocaleString('es'), 110, 182);

  doc.setFont('helvetica', 'bold');
  doc.text('DIRECCIÓN DEL PROPIETARIO:', 30, 200);
  doc.setFont('helvetica', 'normal');
  doc.text(owner, 30, 207);

  const qrContainer = document.getElementById('qrcode');
  qrContainer.innerHTML = '';
  new QRCode(qrContainer, { text: `verify:${docHash}`, width: 100, height: 100 });

  setTimeout(() => {
    const qrCanvas = qrContainer.querySelector('canvas');
    if (qrCanvas) doc.addImage(qrCanvas.toDataURL('image/png'), 'PNG', 150, 60, 40, 40);
    doc.save(`NotaryChain_Certificado_${blockIdx}.pdf`);
  }, 500);
};
