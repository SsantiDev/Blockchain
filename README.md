# 🏛️ NotaryChain: Inmutable Digital Notary

**NotaryChain** is a commercial-grade blockchain-based system designed for document authentication and digital evidence preservation. Built with **Clean Architecture** and **SOLID** principles, it provides a robust, decentralized, and tamper-proof ledger for any digital asset.

## 🌟 Key Features
- **Premium Web Interface:** Modern, high-end dashboard with Dark/Light mode support.
- **Immutable Evidence:** Secure document fingerprints (SHA-256) stored on a private blockchain.
- **Digital Certificates:** Automatic generation of PDF authenticity certificates with verification QR codes.
- **Digital Identity:** SECP256K1 (ECDSA) signatures ensure non-repudiation and proof of ownership.
- **Clean Architecture:** Strict separation of concerns (Domain, Application, Infrastructure, API).
- **RESTful API:** Modern FastAPI interface for easy integration with web and mobile clients.

## 🏗️ Technical Architecture
The project follows **Clean Architecture** patterns to ensure maximum testability and maintainability:

- **Domain Layer:** Pure business logic (Blocks, Transactions, Blockchain).
- **Application Layer:** Use cases coordination (Notarization, Verification).
- **Infrastructure Layer:** Cryptography (ECDSA) and Persistence (JSON/Repository Pattern).
- **Interface Layer:** FastAPI controllers and a Premium Vanilla JS Frontend.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js (Optional, for advanced frontend dev)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/SsantiDev/Blockchain.git
cd Blockchain

# Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt # Or install fastapi uvicorn cryptography python-multipart
```

### 3. Running the System
To run the full commercial demo, you need two terminals:

**Terminal 1: Backend API**
```bash
python run_api.py
```
*API available at `http://localhost:8001`*

**Terminal 2: Frontend Web**
```bash
cd frontend
python3 -m http.server 8888
```
*Access the dashboard at `http://localhost:8888`*

## 📄 License
This project is licensed under the MIT License.
