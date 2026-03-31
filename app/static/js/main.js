const sidebarToggle = document.getElementById('sidebar-toggle');
const sidebar = document.getElementById('sidebar');

if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768 && sidebar.classList.contains('open')) {
      const inside = sidebar.contains(e.target) || sidebarToggle.contains(e.target);
      if (!inside) sidebar.classList.remove('open');
    }
  });
}

const TOAST_ICONS = {
  success: '<i class="fas fa-check-circle text-sage"></i>',
  error: '<i class="fas fa-times-circle text-rust"></i>',
  warning: '<i class="fas fa-exclamation-triangle text-amber"></i>',
  info: '<i class="fas fa-info-circle text-blue-600"></i>',
};

function showToast(message, type = 'info', duration = 3500) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div class="toast-icon">${TOAST_ICONS[type] || TOAST_ICONS.info}</div>
    <div class="toast-msg">${message || ''}</div>
    <button class="toast-close" aria-label="close"><i class="fas fa-times"></i></button>
  `;
  container.appendChild(toast);

  const close = () => {
    toast.style.animation = 'fadeOut .25s ease forwards';
    setTimeout(() => toast.remove(), 250);
  };
  toast.querySelector('.toast-close')?.addEventListener('click', close);
  setTimeout(close, duration);
}

let _confirmHandler = null;
function openConfirm(title, message, onConfirm, subtitle) {
  const modal = document.getElementById('confirm-modal');
  const okBtn = document.getElementById('confirm-ok-btn');
  if (!modal || !okBtn) return;
  document.getElementById('confirm-title').textContent = title || 'Xác nhận';
  document.getElementById('confirm-message').textContent = message || '';
  const subEl = document.getElementById('confirm-subtitle');
  if (subtitle !== undefined && subEl) subEl.textContent = subtitle || '';

  _confirmHandler = async () => {
    try {
      await (onConfirm?.());
    } finally {
      closeConfirm();
    }
  };

  okBtn.onclick = _confirmHandler;
  modal.classList.add('open');
}

function closeConfirm() {
  const modal = document.getElementById('confirm-modal');
  if (!modal) return;
  modal.classList.remove('open');
  const okBtn = document.getElementById('confirm-ok-btn');
  if (okBtn) okBtn.onclick = null;
  _confirmHandler = null;
}

document.getElementById('confirm-modal')?.addEventListener('click', (e) => {
  if (e.target?.id === 'confirm-modal') closeConfirm();
});

async function ajaxPostJson(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : null,
  });
  const data = await res.json().catch(() => ({ success: false, message: 'Lỗi phản hồi server.' }));
  showToast(data.message || 'OK', data.success ? 'success' : 'error');
  return data;
}

async function ajaxDelete(url, rowSelector, message) {
  openConfirm('Xác nhận', message || 'Bạn chắc chắn?', async () => {
    const res = await fetch(url, { method: 'POST' });
    const data = await res.json().catch(() => ({ success: false, message: 'Lỗi phản hồi server.' }));
    showToast(data.message || 'OK', data.success ? 'success' : 'error');
    if (data.success && rowSelector) {
      const el = document.querySelector(rowSelector);
      if (el) el.remove();
    }
  });
}

function formatMoneyVND(value) {
  const digits = String(value || '').replace(/\D+/g, '');
  if (!digits) return '';
  const normalized = digits.replace(/^0+(?=\d)/, '');
  return normalized.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

function unformatMoneyVND(value) {
  return String(value || '').replace(/\D+/g, '');
}

function initMoneyInputs() {
  document.querySelectorAll('input[data-money="vnd"]').forEach((el) => {
    if (el.value) el.value = formatMoneyVND(el.value);
  });
}

document.addEventListener('input', (e) => {
  const el = e.target;
  if (!(el instanceof HTMLInputElement)) return;
  if (el.dataset.money !== 'vnd') return;
  const formatted = formatMoneyVND(el.value);
  el.value = formatted;
});

document.addEventListener(
  'submit',
  (e) => {
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;
    form.querySelectorAll('input[data-money="vnd"]').forEach((el) => {
      if (!el.value) return;
      el.value = unformatMoneyVND(el.value);
    });
  },
  true
);

initMoneyInputs();
