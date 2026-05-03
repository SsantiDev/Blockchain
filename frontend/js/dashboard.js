import { getMyNotarizations, getCertificate } from './api.js';

export const initDashboard = () => {
  document.addEventListener('notarychain:login',  showDashboard);
  document.addEventListener('notarychain:logout', hideDashboard);
};

const showDashboard = async () => {
  const section = document.getElementById('section-dashboard');
  section.style.display = 'block';
  section.scrollIntoView({ behavior: 'smooth' });
  await loadTable();
};

const hideDashboard = () => {
  document.getElementById('section-dashboard').style.display = 'none';
};

const loadTable = async () => {
  const wrapper = document.getElementById('dashboard-table-wrapper');
  try {
    const res  = await getMyNotarizations();
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail);
    renderTable(data, wrapper);
  } catch {
    wrapper.innerHTML = '<p class="dashboard__empty">No se pudieron cargar tus notarizaciones.</p>';
  }
};

const renderTable = (records, wrapper) => {
  if (!records.length) {
    wrapper.innerHTML = '<p class="dashboard__empty">Aún no tienes notarizaciones. ¡Sube tu primer documento!</p>';
    return;
  }
  wrapper.innerHTML = `
    <table class="table">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Hash</th>
          <th>Bloque</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        ${records.map(r => `
          <tr>
            <td>${new Date(r.timestamp).toLocaleDateString('es')}</td>
            <td><span class="table__hash">${r.document_hash?.substring(0, 20)}…</span></td>
            <td>#${r.block_index}</td>
            <td><span class="badge badge--verified">Verificado</span></td>
            <td>
              <button class="btn btn--ghost btn--sm" data-hash="${r.document_hash}">
                Certificado
              </button>
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
  wrapper.querySelectorAll('[data-hash]').forEach(btn =>
    btn.addEventListener('click', () => downloadCert(btn.dataset.hash))
  );
};

const downloadCert = async (hash) => {
  const res = await getCertificate(hash);
  if (!res.ok) return;
  const blob = await res.blob();
  const url  = URL.createObjectURL(blob);
  const a    = Object.assign(document.createElement('a'), {
    href: url,
    download: `NotaryChain_${hash.substring(0, 8)}.pdf`,
  });
  a.click();
  URL.revokeObjectURL(url);
};
