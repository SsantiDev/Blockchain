import { login, register } from './api.js';
import { showToast }       from './utils.js';

const TOKEN_KEY = 'nc_token';
const USER_KEY  = 'nc_user';

export const getToken   = ()  => localStorage.getItem(TOKEN_KEY);
export const getUser    = ()  => JSON.parse(localStorage.getItem(USER_KEY) || 'null');
export const isLoggedIn = ()  => !!getToken();

export const saveSession = (token, user) => {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

export const clearSession = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

export const initAuth = () => {
  renderAuthState();

  document.getElementById('btn-login').addEventListener('click', () => openModal('login'));
  document.getElementById('btn-logout').addEventListener('click', logout);
  document.getElementById('modal-close').addEventListener('click', closeModal);
  document.getElementById('modal-overlay').addEventListener('click', (e) => {
    if (e.target.id === 'modal-overlay') closeModal();
  });

  document.getElementById('tab-login').addEventListener('click',    () => switchTab('login'));
  document.getElementById('tab-register').addEventListener('click', () => switchTab('register'));
  document.getElementById('go-register').addEventListener('click',  () => switchTab('register'));
  document.getElementById('go-login').addEventListener('click',     () => switchTab('login'));

  document.getElementById('form-login').addEventListener('submit',    handleLogin);
  document.getElementById('form-register').addEventListener('submit', handleRegister);
};

export const renderAuthState = () => {
  const loggedIn = isLoggedIn();
  document.getElementById('btn-login').style.display      = loggedIn ? 'none'        : 'inline-flex';
  document.getElementById('btn-logout').style.display     = loggedIn ? 'inline-flex' : 'none';
  document.getElementById('nav-dashboard').style.display  = loggedIn ? 'block'       : 'none';
  if (loggedIn) {
    const user = getUser();
    const label = user?.email?.split('@')[0] || 'usuario';
    document.getElementById('btn-logout').textContent = `Salir (${label})`;
  }
};

const openModal = (tab = 'login') => {
  switchTab(tab);
  document.getElementById('modal-overlay').classList.remove('modal-overlay--hidden');
};

const closeModal = () => {
  document.getElementById('modal-overlay').classList.add('modal-overlay--hidden');
  document.getElementById('form-login').reset();
  document.getElementById('form-register').reset();
  document.getElementById('login-error').textContent = '';
  document.getElementById('reg-error').textContent   = '';
};

const switchTab = (tab) => {
  document.getElementById('form-login').style.display    = tab === 'login'    ? 'block' : 'none';
  document.getElementById('form-register').style.display = tab === 'register' ? 'block' : 'none';
  document.getElementById('tab-login').classList.toggle('auth-tab--active',    tab === 'login');
  document.getElementById('tab-register').classList.toggle('auth-tab--active', tab === 'register');
};

const handleLogin = async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('button[type=submit]');
  btn.disabled = true;
  document.getElementById('login-error').textContent = '';
  try {
    const res  = await login({
      email:    document.getElementById('login-email').value,
      password: document.getElementById('login-password').value,
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Error al iniciar sesión');
    saveSession(data.access_token, data.user);
    closeModal();
    renderAuthState();
    document.dispatchEvent(new CustomEvent('notarychain:login'));
    showToast('Sesión iniciada correctamente');
  } catch (err) {
    document.getElementById('login-error').textContent = err.message;
  } finally {
    btn.disabled = false;
  }
};

const handleRegister = async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('button[type=submit]');
  btn.disabled = true;
  document.getElementById('reg-error').textContent = '';
  try {
    const res  = await register({
      full_name: document.getElementById('reg-name').value,
      email:     document.getElementById('reg-email').value,
      password:  document.getElementById('reg-password').value,
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Error al registrarse');
    saveSession(data.access_token, data.user);
    closeModal();
    renderAuthState();
    document.dispatchEvent(new CustomEvent('notarychain:login'));
    showToast('Cuenta creada correctamente');
  } catch (err) {
    document.getElementById('reg-error').textContent = err.message;
  } finally {
    btn.disabled = false;
  }
};

const logout = () => {
  clearSession();
  renderAuthState();
  document.dispatchEvent(new CustomEvent('notarychain:logout'));
  showToast('Sesión cerrada');
};
