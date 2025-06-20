# 🧱 Proyecto: Blockchain en Python / Blockchain in Python
````markdown
>  This document is also available in [English](#blockchain-in-python). 
>
>  Este documento está disponible en [Español](#blockchain-en-python).
````

---

# 🧱 Blockchain en Python

## 📄 Descripción

Este es un proyecto educativo que implementa una **blockchain desde cero** en Python. El objetivo es comprender cómo funciona la estructura, creación y validación de bloques, así como la minería básica basada en prueba de trabajo (Proof of Work).

## 🚀 Características

- Creación de bloques con minería basada en dificultad.
- Estructura de cadena enlazada mediante hashes SHA-256.
- Validación de integridad de la cadena.
- Simulación de ataques a la blockchain.
- Gestión de transacciones simuladas.
- Visualización de la cadena de bloques completa.
- Proyecto estructurado y modular.

## 🛠️ Tecnologías y Herramientas

- **Lenguaje:** Python 3.13+
- **Control de versiones:** Git + GitHub
- **Editor:** Visual Studio Code

## 📦 Estructura del Proyecto

```text
MBlockchain/
│
├── block.py          # Definición y minería de un bloque
├── blockchain.py     # Lógica de la blockchain
├── utils.py          # Utilidades para hashing y validación
├── main.py           # Punto de entrada del programa
├── .gitignore        # Archivos ignorados por Git
├── README.md         # Documentación
````

## ⚙️ Instalación

```bash
git clone https://github.com/SsantiDev/Blockchain
cd MBlockchain
```

(Opcional) Crear entorno virtual:

```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

## ▶️ Ejecución

```bash
python main.py
```

El programa:

* Inicializa la blockchain.
* Agrega bloques con transacciones simuladas.
* Muestra la cadena completa.
* Simula un ataque y valida la integridad.

## 🧩 Mejoras Futuras

* Transacciones formales con múltiples campos.
* Red de nodos distribuidos.
* Persistencia en base de datos.
* API REST o interfaz gráfica.

## 🤝 Contribuciones

1. Haz un fork.
2. Crea una rama (`git checkout -b feature-nueva`).
3. Realiza tus cambios.
4. Abre un Pull Request.

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

# 🧱 Blockchain in Python

## 📄 Description

This is an educational project that implements a **blockchain from scratch** in Python. The goal is to understand how block creation, structure, validation, and basic Proof of Work (PoW) mining work.

## 🚀 Features

* Block creation with difficulty-based mining.
* Chained structure using SHA-256 hashes.
* Full blockchain integrity validation.
* Blockchain attack simulation.
* Management of simulated transactions.
* Full blockchain visualization.
* Modular and structured project.

## 🛠️ Technologies and Tools

* **Language:** Python 3.13+
* **Version control:** Git + GitHub
* **Editor:** Visual Studio Code

## 📦 Project Structure

```text
MBlockchain/
│
├── block.py          # Block definition and mining
├── blockchain.py     # Blockchain logic
├── utils.py          # Hashing and validation utilities
├── main.py           # Program entry point
├── .gitignore        # Files ignored by Git
├── README.md         # Documentation
```

## ⚙️ Installation

```bash
git clone https://github.com/SsantiDev/Blockchain
cd MBlockchain
```

(Optional) Create virtual environment:

```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

## ▶️ Usage

```bash
python main.py
```

The program:

* Initializes the blockchain.
* Adds blocks with simulated transactions.
* Displays the entire blockchain.
* Simulates an attack and verifies chain integrity.

## 🧩 Future Improvements

* Formal transactions with multiple fields.
* Distributed network of nodes.
* Persistence in databases.
* API REST or graphical interface.

## 🤝 Contributions

1. Fork the project.
2. Create a branch (`git checkout -b new-feature`).
3. Make your changes.
4. Open a Pull Request.

## 📄 License

This project is under the MIT license.
