# NotaryChain — Manifiesto de Arquitectura y Calidad

Este documento define las reglas de oro para cualquier cambio o adición al código de NotaryChain. Todo nuevo desarrollo debe cumplir con estos principios.

## 1. Clean Architecture (Estructura de Carpetas)

### Backend (Python/FastAPI)
Seguimos el patrón de capas para aislar la lógica de negocio de la tecnología:
-   **Domain**: Entidades puras e interfaces (Repositories). No importa nada externo.
-   **Application**: Casos de uso (servicios). Coordina entidades y repositorios.
-   **Infrastructure**: Implementaciones reales (SQLAlchemy, Criptografía, APIs externas).
-   **API**: Controladores FastAPI que exponen la funcionalidad.

### Frontend (Vanilla JS)
Seguimos una arquitectura modular basada en el documento `FRONTEND_ARCHITECTURE.md`:
-   **Design Tokens**: Estilos definidos por variables, nunca valores fijos.
-   **BEM**: Nomenclatura CSS para evitar colisiones.
-   **ES Modules**: Cada archivo JS tiene una única responsabilidad.
-   **Events**: Comunicación desacoplada entre módulos.

---

## 2. Principios SOLID

1.  **Single Responsibility (SRP)**: Cada clase o función hace una sola cosa. Si `auth.js` maneja el login, no debe manejar el diseño de la tabla de documentos.
2.  **Open/Closed (OCP)**: El código debe ser abierto para extensión pero cerrado para modificación. Usamos interfaces (como `BlockchainRepository`) para cambiar el almacenamiento (JSON a SQL) sin tocar la lógica de la Blockchain.
3.  **Liskov Substitution (LSP)**: Cualquier implementación de un repositorio debe funcionar igual si se intercambia.
4.  **Interface Segregation (ISP)**: No obligar a una clase a implementar métodos que no usa.
5.  **Dependency Inversion (DIP)**: Los niveles superiores (Application) no dependen de niveles inferiores (Infrastructure). Dependen de abstracciones (Domain Interfaces).

---

## 3. Clean Code (Reglas de Estilo)

-   **Nombres Descriptivos**: `handleDocumentUpload` en lugar de `doUp`.
-   **Funciones Pequeñas**: Máximo 20-30 líneas. Si es más larga, se divide.
-   **Evitar Comentarios Obvios**: El código debe leerse como prosa. Comentar solo el "por qué", no el "qué".
-   **Sin "Magic Numbers"**: Usar constantes o tokens.
-   **DRY (Don't Repeat Yourself)**: Si el código se repite 2 veces, se extrae a una función o componente.

---

## 4. Flujo de Trabajo (Checklist)

Antes de hacer un `git push`, el desarrollador debe verificar:
-   [ ] ¿El cambio respeta la capa de Clean Architecture correspondiente?
-   [ ] ¿Se han usado tokens en el CSS?
-   [ ] ¿La lógica de negocio está aislada de los detalles de la base de datos o API?
-   [ ] ¿El código es legible y sigue las convenciones del proyecto?
