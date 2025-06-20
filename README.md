
---

# 🧱 Proyecto: Blockchain en Python

Este es un proyecto educativo que implementa una **blockchain desde cero** en Python, diseñado para entender la estructura, creación y validación de bloques, así como la minería básica basada en la prueba de trabajo (Proof of Work).

## 🚀 Características

* Creación de bloques con minería basada en dificultad.
* Estructura de cadena enlazada mediante hashes SHA-256.
* Validación de integridad de la cadena.
* Simulación de ataques a la blockchain.
* Gestión de transacciones simuladas.
* Impresión y visualización completa de la cadena.
* Proyecto estructurado y modular.

---

## 🛠️ Tecnologías y Herramientas

* **Lenguaje:** Python 3.13+
* **Control de versiones:** Git + GitHub
* **Editor:** Visual Studio Code

---

## 📦 Estructura del Proyecto

```text
MBlockchain/
│
├── block.py          # Definición de la estructura y minería de un bloque
├── blockchain.py     # Lógica para gestionar la cadena de bloques
├── utils.py          # Funciones auxiliares para hashing y validaciones
├── main.py           # Punto de entrada para ejecutar la blockchain
├── .gitignore        # Archivos y carpetas ignorados por Git
├── README.md         # Este archivo de documentación
```

---

## ⚙️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd MBlockchain
```

2. (Opcional) Crea un entorno virtual:

```bash
python -m venv venv
# En Linux/Mac
source venv/bin/activate
# En Windows
venv\Scripts\activate
```

3. Instala dependencias si es necesario:

```bash
pip install -r requirements.txt
```

*(Actualmente no hay librerías externas, pero puedes agregar `pytest` para pruebas futuras.)*

---

## ▶️ Uso

Ejecuta el proyecto desde la terminal:

```bash
python main.py
```

El programa:

* Inicializa la blockchain.
* Agrega varios bloques con transacciones de ejemplo.
* Muestra la cadena completa.
* Simula un ataque modificando datos y verifica la integridad de la blockchain.

---

## 🧪 Ejemplo de Ejecución

```text
==== Initializing the blockchain ====
Blockchain initialized with 1 block(s).
Difficulty level set to 2.

==== Adding blocks to the blockchain ====
Mining block 1...
Block 1 mined successfully! With hash: 00a4f7c...
...

==== Complete String Blockchain ====
Block(index=0, timestamp=..., data=Genesis Block, previous_hash=0, nonce=..., hash=00abcd...)

==== Simulating a blockchain attack ====
Modifying the data of the Second block...
The blockchain is valid after the attack? False
The attack was detected because the stored hash does not match the recalculated hash.
```

---

## 🧩 Posibles Mejoras Futuras

* Implementación de transacciones formales con múltiples campos.
* Implementación de nodos distribuidos y sincronización en red.
* Persistencia en base de datos o archivos.
* Interfaz gráfica o API REST para interactuar con la blockchain.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature-nueva`).
3. Realiza tus cambios y haz commit (`git commit -m 'Agrega nueva característica'`).
4. Sube la rama (`git push origin feature-nueva`).
5. Abre un Pull Request.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Puedes consultar el archivo [LICENSE](LICENSE) para más detalles.

---