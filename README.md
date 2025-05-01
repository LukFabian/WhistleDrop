# WhistleDrop: Anonymous File Exchange Over Tor

WhistleDrop is a secure platform for anonymous file submissions and retrievals between whistleblowers and journalists.
It enables encrypted file uploads over the Tor network, protecting the identities and privacy of both parties. The
system uses end-to-end encryption, JWT authentication for journalists, and is designed to operate as a Tor hidden
service.

A demonstration video showing the platform set up as an onion service is available here:  
[Documentation and Demo Video](./documentation/demo.mp4)

---

## Project Overview

WhistleDrop consists of several components working together:

- **FastAPI Backend**  
  Provides the API for uploads, downloads, authentication, and key management. Supports JWT-based session authentication
  and serves OpenAPI documentation at `/docs`.

- **Vue 3 Frontend (TypeScript)**  
  Offers a responsive user interface for both whistleblowers and journalists. Built with Vite and served via an Nginx
  server.

- **PostgreSQL Database**  
  Stores file metadata, encrypted keys, and user accounts. RSA key pairs are managed securely within the database.

- **Tor Hidden Service**  
  Exposes the entire platform over the Tor network as a `.onion` address, ensuring anonymity and resistance to network
  surveillance or censorship.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Usage](#usage)
3. [Demo](#demo)
4. [Contributing](#contributing)
5. [Security Notes](#security-notes)
6. [Architecture](#architecture)

## Core Features

- Anonymous file uploads secured by public-key encryption.
- AES-GCM symmetric encryption for file confidentiality.
- JWT-based authentication for journalist accounts.
- Download system decrypts files only upon journalist authorization.
- Tor hidden service hosting for anonymous access.
- OpenAPI documentation available via `/docs`.

---

## Getting Started

Follow these steps to get WhistleDrop running locally.

### 1. Clone the repository

```bash
git clone https://github.com/your-org/whistledrop.git
cd whistledrop
```

### 2. Edit `.env.example` and rename it to `.env`

- Especially change the following to secure values:
  - `POSTGRES_PASSWORD`
  - `SECRET_KEY`

```bash
cp .env.example .env
```

### 3. Start the entire stack

```bash
docker compose up -d
```

### 4. Access the service

- **Backend API (local testing):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Frontend (local web UI):** [http://127.0.0.1:8080](http://127.0.0.1:8080)

### 5. Configure the frontend for your `.onion` domain

Run this command to automatically replace placeholder addresses in your frontend code:

```bash
ONION_ADDR=$(sudo cat ./tor/hidden_service/service1/hostname) && \
sed -i "s|YOUR_ONION_ADDRESS\.onion|$ONION_ADDR|g" ./frontend/src/lib/http.ts ./frontend/src/plugins/index.ts
```

### 6. Restart the frontend container

```bash
docker compose up frontend -d --force-recreate
```

### 7. Navigate to your running onion service

Lookup your .onion domain:

```bash
sudo cat ./tor/hidden_service/service1/hostname
```

Copy the displayed address and open it in the Tor Browser.

## Usage

Once the stack is running:

- Journalists can register and log in through the frontend.
- Whistleblowers can securely upload encrypted files.
- Journalists can decrypt and download the submissions they receive.

Both the backend and frontend support CORS and JWT authentication. All API routes are documented under `/docs`.



## Demo

You can watch a short video showing the setup and operation of WhistleDrop as a Tor Onion Service:

**[View Demo (MP4)](./documentation/demo.mp4)**


## Contributing

Contributions are welcome. Please open an issue or submit a pull request to propose changes.

For development setup, ensure you have Docker and Docker Compose installed, and refer to the Getting Started guide above.



## Security Notes

- All files are encrypted with AES-GCM before storage.

- RSA public/private key pairs are rotated and marked as used upon file decryption.

- Backend API enforces JWT authentication for any sensitive routes.

- Tor ensures highly anonymous access. You can harden the setup even more by disabling the port forwardings in the
  docker-compose.yaml.

## Architecture

    Backend: Python 3.12 + FastAPI

    Frontend: Vue 3 + Vite + TypeScript

    Database: PostgreSQL 17

    Webserver: Latest stable Nginx

    Tor: goldy/tor-hidden-service:latest
