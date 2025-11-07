# 🚀 Landing Page de Servicios Integrados de Guaraníes (PYG)

## 🌟 Descripción del Proyecto

Este proyecto es una aplicación web (Landing Page) moderna y tipada, con fuerte enfoque en la experiencia de usuario. Su objetivo es integrar información crucial en tiempo real, incluyendo datos meteorológicos, conversiones de moneda y precios de criptomonedas, utilizando una API de *backend* desarrollada en **FastAPI (Python)**.

El frontend está construido con la *stack* moderna de **React/Vite** y TypeScript, asegurando robustez, agilidad y facilidad de mantenimiento.

## 🔗 Demos en Vivo

Explora la aplicación desplegada y la documentación de la API:

| Componente | Enlace de Demostración |
| :--- | :--- |
| **Frontend (React/Vite)** | [https://paraguay-hub-frontend.onrender.com/](https://paraguay-hub-frontend.onrender.com/) |
| **Backend (FastAPI Docs)** | [https://paraguay-hub-backend.onrender.com/docs](https://paraguay-hub-backend.onrender.com/docs) |

---

## 🏗️ Arquitectura y Tecnologías

El proyecto sigue una arquitectura **Frontend-Backend (API)**. El frontend se encarga de la presentación y la lógica de estado, y el *backend* provee los datos a través de *endpoints* RESTful.



### 💻 Frontend (React/Vite)

| Categoría | Tecnología | Uso Específico |
| :--- | :--- | :--- |
| **Framework** | **React & Vite** | Vite como *bundler* ultrarrápido y React para construir la interfaz de usuario. |
| **Lenguaje** | **TypeScript (TSX)** | Garantiza código robusto, detección temprana de errores y tipado estricto para las respuestas de la API. |
| **Diseño/Estilos** | **Tailwind CSS** | Framework CSS *utility-first* para un diseño responsivo y rápido. |
| **Componentes** | **Shadcn/ui** | Colección de componentes UI re-utilizables y accesibles. |
| **Networking** | **`useApiFetch.ts` (Custom Hook)** | Hook personalizado para encapsular la lógica de fetching de datos, manejo de carga y errores. |

### ⚙️ Backend (API & Datos)

| Categoría | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Framework API** | **FastAPI (Python)** | Proporciona la capa RESTful de alta velocidad. |
| **Base de Datos** | **MongoDB** | Base de datos NoSQL utilizada específicamente para **cachear** las respuestas de la API de clima (OpenWeatherMap). |
| **Servidor** | **Uvicorn** | Servidor ASGI para ejecutar la aplicación FastAPI de forma asíncrona. |

### 🌐 Servicios de Terceros (APIs Utilizadas)

El *backend* de FastAPI actúa como un *proxy* y una capa de abstracción para los siguientes servicios externos:

| Servicio | Tipo de Dato | Propósito |
| :--- | :--- | :--- |
| **Clima** | **OpenWeatherMap** | Obtención de datos meteorológicos actuales y pronósticos. |
| **Monedas** | **ExchangeRate-API** | Obtención de tasas de cambio en tiempo real (USD, EUR, BRL, etc.) frente al PYG. |
| **Cripto** | **CoinGecko** | Obtención de precios en tiempo real de Bitcoin (BTC) y datos de tendencia. |

### ☁️ Despliegue e Infraestructura

| Servicio | Propósito | Uso Específico |
| :--- | :--- | :--- |
| **Render** | **Hosting/Despliegue (Deploy)** | Plataforma utilizada para el despliegue continuo (Continuous Deployment) y el alojamiento de los servicios de Backend (FastAPI) y Frontend (React/Vite). |

---

## 🛠️ Módulos Implementados

El *landing page* se compone de tres secciones principales:

| Módulo | Endpoint de API Principal | Tipo de Petición | Funcionalidad |
| :--- | :--- | :--- | :--- |
| **Clima** | `/weather/current` | `GET` | Muestra el estado del tiempo, temperatura y humedad actual. |
| **Conversor de Moneda** | `/currency/convert` | `POST` | Convierte cantidades de monedas seleccionadas a Guaraníes (PYG). |
| **Bitcoin** | `/bitcoin/convert` | `POST` | Muestra la tasa de 1 BTC a PYG y calcula conversiones de BTC a PYG. |

## 🚀 Cómo Iniciar el Proyecto

Para una ejecución exitosa, es necesario levantar tanto el *backend* (API) como el *frontend* (aplicación React).

---

### A. 🐍 Inicio del Backend (FastAPI)

Asumiremos que tu proyecto de FastAPI tiene una estructura estándar.

1.  **Clonar y Acceder al Directorio del Backend** (Si está separado):
    ```bash
    git clone https://github.com/maxwellweb/paraguay-hub.git
    cd paraguay-hub/backend
    ```

2.  **Crear y Activar el Entorno Virtual** (Recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # o .\venv\Scripts\activate  # En Windows (CMD/PowerShell)
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    # (Asegúrate de que 'fastapi', 'uvicorn', y 'pydantic' estén instalados)
    ```

4.  **Ejecutar el Servidor FastAPI:**
    Utiliza `uvicorn` para correr tu aplicación (reemplaza `app.main:app` con el nombre de tu archivo y aplicación si es diferente).
    ```bash
    uvicorn app.main:app --reload
    ```
    El *backend* estará activo, por defecto, en `http://127.0.0.1:8000`.

---

### B. ⚛️ Inicio del Frontend (React/Vite)

1.  **Acceder al Directorio del Frontend:**
    ```bash
    cd paraguay-hub/frontend
    ```

2.  **Instalar Dependencias:**
    ```bash
    npm install
    # o yarn install
    ```

3.  **Configurar la URL de la API (Variable de Entorno):**
    Crea un archivo llamado `.env.local` en la raíz del proyecto *frontend* para apuntar a tu API de FastAPI:
    ```
    VITE_API_BASE_URL="[http://127.0.0.1:8000](http://127.0.0.1:8000)" 
    ```
    *Nota: Asegúrate de que tu `useApiFetch.ts` utilice esta variable (`import.meta.env.VITE_API_BASE_URL`).*

4.  **Ejecutar el Servidor de Desarrollo de Vite:**
    ```bash
    npm run dev
    # o yarn dev
    ```
    La aplicación estará disponible, por defecto, en `http://localhost:5173`.

---

## 💖 Soporte y Donaciones

Si este proyecto te ha sido útil, te ha ahorrado tiempo o simplemente aprecias el esfuerzo de código abierto, considera apoyarlo. Tu contribución ayuda a motivarme a desarrollar nuevas funcionalidades o proyectos de aprendizajes como este.

Puedes apoyar el proyecto invitándonos a un café:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/maxwellweb)

---