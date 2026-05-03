# NotaryChain — Arquitectura Frontend

## Resumen

Reestructura completa del frontend de NotaryChain desde un archivo monolítico hacia una arquitectura modular basada en **Design Tokens + BEM + ES Modules nativos**.

---

## Motivación

El frontend original (`style.css` + `app.js`) presentaba estos problemas:

- Estilos inline dispersos en todo el HTML (`style=""`)
- Lógica mezclada en un solo archivo JS (tema, API, PDF, drag-drop juntos)
- Sin aislamiento de componentes — imposible añadir auth/dashboard sin romper lo existente
- Sin sistema de tokens — colores y espaciados hardcodeados en múltiples lugares

---

## Metodología

### CSS: Design Tokens + BEM

**BEM (Block Element Modifier)** — nomenclatura que previene colisiones y hace legible la jerarquía:

```
.card              → Bloque
.card__title       → Elemento
.card--featured    → Modificador

.btn               → Bloque
.btn--primary      → Modificador
.btn--loading      → Modificador de estado
```

**Design Tokens** — todas las variables viven en `tokens.css`. Ningún archivo CSS usa valores hardcodeados; todo referencia un token:

```css
/* MAL */
border-radius: 12px;
color: #00ffcc;

/* BIEN */
border-radius: var(--radius-md);
color: var(--accent-primary);
```

### JavaScript: ES Modules nativos

Cada archivo es un módulo con responsabilidad única. Las dependencias se declaran explícitamente con `import/export`. Sin variables globales.

```
api.js → no depende de nada
utils.js → no depende de nada
theme.js → no depende de nada
auth.js → importa api.js, utils.js
notarize.js → importa api.js, utils.js
dashboard.js → importa api.js
main.js → importa todo, orquesta
```

La comunicación entre módulos desacoplados (auth ↔ dashboard) usa **Custom Events**:

```js
// auth.js dispara el evento tras login exitoso
document.dispatchEvent(new CustomEvent('notarychain:login'));

// dashboard.js escucha sin conocer auth.js
document.addEventListener('notarychain:login', showDashboard);
```

---

## Estructura de archivos

```
frontend/
├── index.html                   ← HTML semántico, sin estilos inline
├── styles/
│   ├── tokens.css               ← Variables globales (colores, espaciado, radios)
│   ├── base.css                 ← Reset, body, tipografía, animaciones
│   ├── layout.css               ← Header, footer, .container, .section
│   ├── components.css           ← .btn, .card, .drop-zone, .modal, .form, .toast, .badge
│   └── pages/
│       ├── home.css             ← Hero, stats-bar, features-grid
│       ├── auth.css             ← Auth tabs del modal de login/registro
│       └── dashboard.css        ← Tabla de historial, dashboard del usuario
└── js/
    ├── api.js                   ← Todos los fetch() centralizados + JWT headers
    ├── utils.js                 ← Utilidades compartidas (showToast)
    ├── theme.js                 ← Toggle dark/light con persistencia
    ├── auth.js                  ← Login, registro, sesión JWT, custom events
    ├── notarize.js              ← Drag-drop, notarizar, verificar, generación PDF
    ├── dashboard.js             ← Historial del usuario, descarga de certificados
    └── main.js                  ← Punto de entrada, importa e inicializa todo
```

### Orden de carga CSS (importa)

```html
<link rel="stylesheet" href="styles/tokens.css">      <!-- 1. Variables -->
<link rel="stylesheet" href="styles/base.css">         <!-- 2. Reset -->
<link rel="stylesheet" href="styles/layout.css">       <!-- 3. Estructura -->
<link rel="stylesheet" href="styles/components.css">   <!-- 4. Componentes -->
<link rel="stylesheet" href="styles/pages/home.css">   <!-- 5. Página específica -->
<link rel="stylesheet" href="styles/pages/auth.css">
<link rel="stylesheet" href="styles/pages/dashboard.css">
```

---

## Tokens del sistema de diseño

### Colores

| Token | Oscuro | Claro |
|---|---|---|
| `--bg-primary` | `#0a0b10` | `#f1f5f9` |
| `--bg-secondary` | `#141620` | `#ffffff` |
| `--bg-glass` | `rgba(20,22,32,0.7)` | `rgba(255,255,255,0.7)` |
| `--text-primary` | `#f8fafc` | `#0f172a` |
| `--text-secondary` | `#94a3b8` | `#475569` |
| `--accent-primary` | `#00ffcc` | `#059669` |
| `--accent-secondary` | `#0ea5e9` | `#0284c7` |
| `--error` | `#ef4444` | `#ef4444` |

### Espaciado

| Token | Valor |
|---|---|
| `--space-xs` | `0.5rem` |
| `--space-sm` | `1rem` |
| `--space-md` | `1.5rem` |
| `--space-lg` | `2rem` |
| `--space-xl` | `3rem` |
| `--space-2xl` | `4rem` |
| `--space-3xl` | `8rem` |

### Radios

| Token | Valor | Uso |
|---|---|---|
| `--radius-sm` | `8px` | Inputs, botones pequeños |
| `--radius-md` | `12px` | Botones, cards pequeñas |
| `--radius-lg` | `24px` | Cards, modales, drop-zone |
| `--radius-full` | `50px` | Pills, badges |

---

## Componentes disponibles

### Botones

```html
<button class="btn btn--primary">Acción principal</button>
<button class="btn btn--ghost">Acción secundaria</button>
<button class="btn btn--outline">Terciario</button>
<button class="btn btn--primary btn--sm">Pequeño</button>
<button class="btn btn--primary btn--full">Ancho completo</button>
<button class="btn btn--primary btn--loading" disabled>Cargando</button>
```

### Card

```html
<div class="card">
  <i data-lucide="lock" class="card__icon"></i>
  <h3 class="card__title">Título</h3>
  <p class="card__body">Descripción del componente.</p>
</div>
```

### Badge

```html
<span class="badge badge--verified">Verificado</span>
<span class="badge badge--pending">Pendiente</span>
```

### Toast (programático)

```js
import { showToast } from './utils.js';
showToast('Mensaje de éxito');
showToast('Algo falló', 'error');
```

---

## Convenciones para nuevas funcionalidades

### Añadir una página nueva

1. Crear `styles/pages/nueva-pagina.css`
2. Agregar `<link rel="stylesheet" href="styles/pages/nueva-pagina.css">` en `index.html`
3. Crear `js/nueva-pagina.js` con `export const init = () => { ... }`
4. Importar e inicializar en `js/main.js`

### Añadir un endpoint nuevo a la API

Solo tocar `js/api.js`:

```js
export const nuevoEndpoint = (body) =>
  fetch(`${API_URL}/nuevo`, {
    method: 'POST',
    body: JSON.stringify(body),
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
  });
```

### Añadir un componente nuevo

1. Definir el bloque BEM en `styles/components.css`
2. Usar tokens, nunca valores hardcodeados
3. Documentar variantes con modificadores (`--variante`)

---

## Próximos pasos

- [ ] **Backend Auth** — endpoints `/auth/register`, `/auth/login`, `GET /users/me`
- [ ] **Backend Dashboard** — endpoint `GET /my-notarizations` con user_id
- [ ] **Backend Certificado** — endpoint `GET /notarizations/{tx_hash}/certificate`
- [ ] **Modelos SQL** — tablas `users`, `blocks`, `transactions` con SQLAlchemy
- [ ] **Migraciones** — configurar Alembic desde el inicio
- [ ] **Responsive** — media queries para mobile en `layout.css`
