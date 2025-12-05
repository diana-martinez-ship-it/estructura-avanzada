# 🌱 EcoMarket API

# 🌱 EcoMarket API Enterprise

Sistema profesional de gestión de productos orgánicos con inventario en tiempo real.

![Version](https://img.shields.io/badge/version-2.1.0-green.svg)

## 📋 Características![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

- ✅ **API REST completa** con FastAPI![License](https://img.shields.io/badge/license-MIT-blue.svg)

- ✅ **Sistema de inventario** con control de stock

- ✅ **Compras en línea** con actualización automática> **Sistema de Gestión Empresarial de Inventarios**  

- ✅ **Panel de administración** (CRUD completo)> La solución completa para la gestión moderna de inventarios en el sector retail con tecnología de vanguardia.

- ✅ **Catálogo de productos** interactivo

- ✅ **Dashboard con estadísticas** en tiempo real## 🚀 Características Principales

- ✅ **Documentación interactiva** con Swagger UI

### ✨ **API REST Completa**

## 🚀 Instalación- 📊 **CRUD Completo** - Gestión completa de productos con validaciones avanzadas

- 🔍 **Búsqueda Inteligente** - Sistema de filtrado por nombre, categoría, precio y más

### Requisitos previos:- 📈 **Paginación Optimizada** - Rendimiento superior para grandes volúmenes de datos

- Python 3.8 o superior- 📱 **Documentación Interactiva** - Swagger UI integrado para pruebas en tiempo real

- pip (gestor de paquetes de Python)

### 🎨 **Interfaz Web Moderna**

### Pasos:- 📊 **Dashboard Ejecutivo** - Métricas en tiempo real con gráficos interactivos

- 🛍️ **Gestión Visual** - Formularios intuitivos para administrar productos

1. **Clonar o descargar el proyecto**- 📱 **Diseño Responsivo** - Optimizado para desktop, tablet y móvil

```powershell- 🎯 **Experiencia de Usuario** - Interfaz moderna con animaciones fluidas

cd EcoMarket-Compartir

```### 📈 **Analytics y Estadísticas**

- 💰 **Valor Total del Inventario** - Cálculos automáticos en tiempo real

2. **Crear entorno virtual** (si no existe)- ⚠️ **Alertas de Stock Bajo** - Notificaciones para reabastecimiento

```powershell- 🏷️ **Análisis por Categorías** - Distribución visual con gráficos de donut

python -m venv .venv- 🌱 **Productos Orgánicos** - Seguimiento de certificaciones especiales

```

## 🛠️ Tecnologías Utilizadas

3. **Activar entorno virtual**

```powershell### Backend

.\.venv\Scripts\Activate.ps1- **FastAPI** - Framework web moderno y de alto rendimiento

```- **Pydantic** - Validación de datos y serialización

- **Uvicorn** - Servidor ASGI de producción

4. **Instalar dependencias**

```powershell### Frontend

pip install -r requirements.txt- **HTML5** - Estructura semántica moderna

```- **CSS3** - Diseño responsivo con variables CSS y animaciones

- **Bootstrap 5** - Framework de componentes UI

## ▶️ Ejecutar la API- **JavaScript ES6+** - Interactividad y comunicación con API

- **Chart.js** - Visualización de datos con gráficos interactivos

```powershell- **Font Awesome** - Iconografía profesional

# Activar entorno virtual

.\.venv\Scripts\Activate.ps1## 📦 Instalación y Uso



# Iniciar servidor### Prerrequisitos

python main.py- Python 3.8 o superior

```- pip (gestor de paquetes de Python)



O con uvicorn directamente:### Instalación Rápida

```powershell```bash

uvicorn main:app --host 127.0.0.1 --port 8000 --reload# 1. Navega al directorio del proyecto

```cd api-ecomarket



El servidor estará disponible en: **http://127.0.0.1:8000**# 2. Instalar dependencias

pip install fastapi uvicorn python-multipart

## 🌐 URLs Disponibles

# 3. Ejecutar la aplicación

| URL | Descripción |uvicorn main:app --reload

|-----|-------------|```

| http://127.0.0.1:8000/ | 🏠 Página principal |

| http://127.0.0.1:8000/docs | 📚 Documentación API (Swagger) |### Acceder a la Aplicación

| http://127.0.0.1:8000/catalog | 🛍️ Catálogo con compras |- **🎨 Interfaz Web:** http://127.0.0.1:8000

| http://127.0.0.1:8000/admin | 🔧 Panel de administración |- **📚 Documentación API:** http://127.0.0.1:8000/docs

| http://127.0.0.1:8000/dashboard | 📊 Dashboard de estadísticas |- **📖 Redoc:** http://127.0.0.1:8000/redoc



## 🔌 Endpoints API## 🎯 Cómo Usar la Aplicación



### Productos### 1. **Dashboard Principal**

Al acceder a http://127.0.0.1:8000 verás:

| Método | Endpoint | Descripción |- 📊 Estadísticas en tiempo real del inventario

|--------|----------|-------------|- 💰 Valor total de productos

| `GET` | `/api/productos` | Lista todos los productos |- ⚠️ Alertas de stock bajo

| `GET` | `/api/productos/{id}` | Obtiene un producto específico |- 🏷️ Gráfico de distribución por categorías

| `POST` | `/api/productos` | Crea un nuevo producto |

| `PUT` | `/api/productos/{id}` | Actualiza un producto |### 2. **Gestión de Productos**

| `DELETE` | `/api/productos/{id}` | Elimina un producto |- **Agregar:** Completa el formulario con los datos del producto

| `POST` | `/api/productos/{id}/comprar?cantidad=X` | Realiza una compra |- **Buscar:** Usa la barra de búsqueda para filtrar productos

- **Filtrar:** Selecciona categorías específicas

### Estadísticas- **Ordenar:** Por nombre o precio (ascendente/descendente)



| Método | Endpoint | Descripción |### 3. **API REST**

|--------|----------|-------------|Usa los endpoints para integrar con otras aplicaciones:

| `GET` | `/api/estadisticas` | Obtiene estadísticas del inventario |

```bash

## 📦 Estructura del Proyecto# Listar productos

GET /products

```

EcoMarket-Compartir/# Crear producto

├── main.py              # Servidor FastAPI principalPOST /products

├── requirements.txt     # Dependencias del proyecto{

├── README.md           # Este archivo  "name": "🍎 Manzana Orgánica",

├── .venv/              # Entorno virtual de Python  "category": "Frutas y Verduras",

├── __pycache__/        # Cache de Python (auto-generado)  "price": 15.99,

└── web/                # Módulo de templates web  "stock": 150

    ├── __init__.py     # Inicializador del módulo}

    ├── templates.py    # Templates HTML

    └── styles.py       # Estilos CSS# Obtener estadísticas

```GET /stats

```

## 💻 Uso

## 📊 Funcionalidades Destacadas

### 1. Comprar Productos (Catálogo)

1. Ve a http://127.0.0.1:8000/catalog### ✨ **Productos Enriquecidos**

2. Selecciona la cantidad deseada- Nombre y descripción detallada

3. Click en "🛒 Comprar"- Categorización por tipo de producto

4. El stock se actualiza automáticamente- Precios y gestión de stock

- URLs de imágenes para catálogo visual

### 2. Administrar Productos- Códigos de barras para identificación

1. Ve a http://127.0.0.1:8000/admin- Información de proveedores

2. **Crear**: Llena el formulario y click "➕ Crear Producto"- Certificación orgánica

3. **Editar**: Click en "✏️ Editar" en cualquier producto- Control de disponibilidad

4. **Eliminar**: Click en "🗑️ Eliminar" (con confirmación)- Fechas de creación y actualización



### 3. Usar la API directamente### 📈 **Estadísticas Avanzadas**

1. Ve a http://127.0.0.1:8000/docs- Total de productos registrados

2. Explora y prueba los endpoints desde Swagger UI- Valor monetario del inventario

3. Todos los endpoints tienen documentación detallada- Identificación de productos con stock bajo

- Distribución por categorías

## 🔧 Dependencias- Conteo de productos orgánicos

- Precio promedio por producto

- **FastAPI**: Framework web moderno y rápido

- **Uvicorn**: Servidor ASGI de alto rendimiento### 🔍 **Búsqueda y Filtrado**

- **Pydantic**: Validación de datos- Búsqueda por nombre de producto

- **Requests**: Cliente HTTP (para pruebas)- Filtrado por categoría

- Filtrado por productos orgánicos

## 📝 Modelo de Datos- Rango de precios personalizable

- Solo productos disponibles

### Producto- Ordenamiento múltiple

```json

{## 🎨 Interfaz Visual Profesional

  "id": 1,

  "nombre": "Manzana Orgánica",La interfaz incluye:

  "categoria": "Frutas",- **Design System Moderno:** Colores corporativos y tipografía profesional

  "precio": 2.5,- **Componentes Interactivos:** Botones, formularios y tarjetas con hover effects

  "stock": 150,- **Gráficos Dinámicos:** Chart.js para visualización de datos

  "disponible": true,- **Responsive Design:** Adaptable a todos los dispositivos

  "descripcion": "Manzanas orgánicas frescas",- **Animaciones Fluidas:** Transiciones suaves y feedback visual

  "fecha_agregado": "2025-10-15T10:30:00"- **Notificaciones:** Alertas de éxito, error y advertencia

}

```## 🚀 Casos de Uso Comercial



## 🎯 Productos de Demostración### 🏪 **Retail y Tiendas**

- Gestión completa del catálogo

La API viene con 5 productos precargados:- Control de inventario en tiempo real

- Alertas de reabastecimiento

1. 🍎 **Manzana Orgánica** - Stock: 150- Análisis de productos más valiosos

2. 🍅 **Tomate Cherry** - Stock: 200

3. 🥬 **Lechuga Hidropónica** - Stock: 0 (Agotado)### 📦 **Almacenes y Distribución**

4. 🥕 **Zanahoria Orgánica** - Stock: 300- Seguimiento de stock por categorías

5. 🥑 **Palta Hass** - Stock: 80- Identificación de productos de alta rotación

- Gestión de proveedores

## 🛡️ Validaciones- Control de productos orgánicos/especiales



- ✅ Precio debe ser mayor que 0### 🛒 **E-commerce**

- ✅ Stock no puede ser negativo- API para integración con tiendas online

- ✅ Nombre y categoría obligatorios- Catálogo con imágenes y descripciones

- ✅ Validación de stock suficiente en compras- Gestión de disponibilidad

- ✅ Actualización automática de disponibilidad- Sincronización de precios y stock



## 🌟 Características Técnicas## 📞 Soporte y Contacto



- **Arquitectura REST**: Endpoints bien estructurados### 🌟 **Contacto Comercial**

- **Validación con Pydantic**: Datos siempre válidos- **Email:** ventas@ecomarket.com

- **Documentación automática**: Swagger UI integrado- **Teléfono:** +52 (55) 1234-5678

- **CORS habilitado**: Accesible desde cualquier origen- **Website:** www.ecomarket.com

- **Interfaz responsive**: Funciona en móviles y desktop

- **Actualización en tiempo real**: UI actualizada después de cada operación### 🛠️ **Soporte Técnico**

- **Email:** soporte@ecomarket.com

## 📄 Licencia- **API Docs:** http://127.0.0.1:8000/docs



Proyecto educativo - Uso libre---



## 👨‍💻 Autor<div align="center">

  <h2>🌟 ¡Transforma tu Inventario Hoy! 🌟</h2>

Desarrollado como proyecto de gestión de inventarios con FastAPI  <p><strong>EcoMarket API Enterprise - La tecnología que tu negocio necesita</strong></p>

  

---  **[🚀 Iniciar Aplicación](http://127.0.0.1:8000) | [📚 Ver Documentación](http://127.0.0.1:8000/docs)**

</div>

¿Necesitas ayuda? Visita la documentación interactiva en `/docs` 🚀

---

© 2024 EcoMarket Enterprise Solutions. Todos los derechos reservados.



