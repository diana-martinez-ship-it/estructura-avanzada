"""
🎨 Estilos CSS para EcoMarket API
Archivo centralizado con todos los estilos visuales
Este archivo contiene SOLO CSS - no tiene lógica, solo apariencia visual
"""

# 📱 CSS BASE - Estilos que se aplican a TODAS las páginas de la aplicación
BASE_CSS = """
    /* 🔧 CONFIGURACIÓN DEL CUERPO PRINCIPAL (body) */
    body { 
        /* 🔤 Define la fuente de texto - si no encuentra Segoe UI, usa Tahoma, etc. */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        
        /* 📏 Elimina márgenes predeterminados del navegador */
        margin: 0; 
        
        /* 📏 Elimina espaciado interno predeterminado */
        padding: 0; 
        
        /* 🌈 FONDO DEGRADADO: de azul claro (#667eea) a morado (#764ba2) en diagonal */
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        
        /* 📐 Altura mínima = 100% de la pantalla del usuario (vh = viewport height) */
        min-height: 100vh;
        
        /* 🎨 Color del texto por defecto = gris oscuro */
        color: #333;
    }
    
    /* 📦 CONTENEDOR PRINCIPAL - La "caja" donde va todo el contenido */
    .container { 
        /* 📏 Ancho máximo de 1200 píxeles - no se hace más ancho aunque la pantalla sea gigante */
        max-width: 1200px; 
        
        /* 🎯 CENTRADO AUTOMÁTICO: 0 arriba/abajo, auto izquierda/derecha = centrado */
        margin: 0 auto; 
        
        /* 📏 Espaciado INTERNO de 20px en todos los lados */
        padding: 20px; 
        
        /* 🎨 Fondo blanco sólido */
        background: white; 
        
        /* 📏 Margen SUPERIOR de 40px (separa del borde superior) */
        margin-top: 40px; 
        
        /* 🔘 Esquinas redondeadas con radio de 15px */
        border-radius: 15px; 
        
        /* ✨ SOMBRA: 0px horizontal, 8px vertical, 32px difuminado, color negro al 10% */
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        
        /* 🌫️ Efecto de cristal esmerilado (requiere navegador moderno) */
        backdrop-filter: blur(10px);
        
        /* 🖼️ Borde blanco semitransparente (20% de opacidad) */
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* 📢 TÍTULO PRINCIPAL (h1) - El texto más grande e importante */
    h1 { 
        /* 🎨 Color gris azulado oscuro para que resalte */
        color: #2d3748; 
        
        /* 🎯 Texto centrado horizontalmente en la página */
        text-align: center; 
        
        /* 📏 Espacio DEBAJO del título = 30px para separarlo del contenido */
        margin-bottom: 30px; 
        
        /* 📏 Tamaño de fuente grande = 2.5 veces el tamaño normal */
        font-size: 2.5em;
        
        /* ✨ SOMBRA DEL TEXTO: hace que se vea "flotando" sobre el fondo */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 📢 SUBTÍTULO (h2) - Secciones importantes con línea decorativa */
    h2 {
        /* 🎨 Color gris más suave que h1 */
        color: #4a5568;
        
        /* 📏 LÍNEA DECORATIVA: borde azul de 3px de grosor en la parte inferior */
        border-bottom: 3px solid #667eea;
        
        /* 📏 Espaciado INTERNO inferior = 10px entre el texto y la línea */
        padding-bottom: 10px;
        
        /* 📏 Margen SUPERIOR = 30px para separar de contenido previo */
        margin-top: 30px;
    }
    
    /* 🔘 CONTENEDOR DE BOTONES DE NAVEGACIÓN - Organiza los botones principales */
    .nav-buttons { 
        /* 📐 FLEXBOX: hace que los elementos se organicen en fila flexible */
        display: flex; 
        
        /* 🎯 CENTRADO: todos los botones se alinean al centro horizontalmente */
        justify-content: center;
        
        /* 🔄 RESPONSIVE: permite que los botones se envuelvan en pantallas pequeñas */
        flex-wrap: wrap;
        
        /* 📏 ESPACIADO: margen superior e inferior para separar de otros elementos */
        margin: 30px 0; 
        
        /* 📏 ESPACIO ENTRE BOTONES: 15px de separación entre cada botón */
        gap: 15px; 
        
        /* 📏 MÁRGENES: 30px arriba y abajo, 0px izquierda y derecha */
        margin: 30px 0; 
        
        /* 📱 RESPONSIVE: si no caben en una línea, se van a la siguiente (móviles) */
        flex-wrap: wrap;
    }
    
    .btn { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white; 
        padding: 12px 25px; 
        text-decoration: none; 
        border-radius: 25px; 
        font-weight: bold; 
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    
    .btn:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 6px 20px rgba(102,126,234,0.4);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        border: 1px solid rgba(102,126,234,0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .feature-card h3 {
        color: #2d3748;
        margin-bottom: 15px;
        font-size: 1.2em;
    }
    
    .feature-card p {
        color: #4a5568;
        line-height: 1.6;
        margin: 0;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    
    .stat-number {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .stat-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    
    @media (max-width: 768px) {
        .container { 
            margin: 10px; 
            padding: 15px; 
            border-radius: 10px;
        }
        
        h1 { 
            font-size: 2em; 
        }
        
        .nav-buttons { 
            flex-direction: column; 
            align-items: center;
        }
        
        .btn { 
            width: 200px; 
            text-align: center;
        }
        
        .feature-grid {
            grid-template-columns: 1fr;
        }
        
        .btn-ventas {
            width: 220px;
            text-align: center;
            padding: 16px 30px;
        }
    }
    
    /* 💸 BOTÓN DE VENTAS ESPECIAL - Diseño único y llamativo */
    .btn-ventas {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%, #2f855a 100%);
        color: white;
        padding: 14px 28px;
        text-decoration: none;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1.1em;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: none;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ✨ Efecto de brillo animado */
    .btn-ventas::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .btn-ventas:hover::before {
        left: 100%;
    }
    
    .btn-ventas:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(72, 187, 120, 0.6);
        background: linear-gradient(135deg, #38a169 0%, #2f855a 50%, #276749 100%);
    }
    
    .btn-ventas:active {
        transform: translateY(-1px) scale(1.02);
        transition: all 0.1s ease;
    }
    
    /* 💰 Efecto de pulso para llamar la atención */
    @keyframes pulse-ventas {
        0% { box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4); }
        50% { box-shadow: 0 6px 25px rgba(72, 187, 120, 0.6); }
        100% { box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4); }
    }
    
    .btn-ventas {
        animation: pulse-ventas 2s infinite;
    }
    
    .btn-ventas:hover {
        animation: none;
    }
    
    /* 💸 DROPDOWN DE VENTAS - Contenedor y estilos */
    .sales-dropdown-container {
        position: relative;
        display: inline-block;
    }
    
    .sales-dropdown {
        display: none !important;
        position: absolute;
        top: 100%;
        left: 0;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 2px solid rgba(72,187,120,0.1);
        min-width: 250px;
        z-index: 1000;
        overflow: hidden;
        animation: dropdownSlide 0.3s ease;
        opacity: 0;
        visibility: hidden;
        transform: translateY(-10px);
        transition: all 0.3s ease;
    }
    
    .sales-dropdown.show {
        display: block !important;
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }
    
    @keyframes dropdownSlide {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .dropdown-option {
        padding: 15px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    .dropdown-option:last-child {
        border-bottom: none;
    }
    
    .dropdown-option:hover {
        background: linear-gradient(135deg, #f0fff4, #e6fffa);
        color: #2d3748;
        transform: translateX(5px);
    }
    
    .mode-icon {
        font-size: 1.2em;
        width: 25px;
        text-align: center;
    }
    
    .mode-name {
        font-weight: 600;
        font-size: 0.95em;
    }
    
    /* 📱 Responsive para dropdown */
    @media (max-width: 768px) {
        .sales-dropdown {
            left: -50px;
            min-width: 200px;
        }
    }
"""

# CSS específico para Dashboard
DASHBOARD_CSS = """
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
        border: 1px solid rgba(102,126,234,0.1);
    }
    
    .chart-title {
        color: #2d3748;
        text-align: center;
        margin-bottom: 20px;
        font-size: 1.5em;
        font-weight: bold;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(102,126,234,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
    }
    
    .metric-value {
        font-size: 2.2em;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .metric-label {
        color: #4a5568;
        font-size: 1.1em;
        font-weight: 500;
    }
    
    /* 📊 CONTENEDOR DE GRÁFICOS - Layout fijo para evitar movimiento */
    .charts-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
        margin-top: 20px;
    }
    
    /* 📊 CONTENEDOR DE GRÁFICO - Espaciado mejorado para títulos y leyendas */
    .chart-container {
        position: relative;
        height: 450px; /* Más altura para títulos y leyendas */
        width: 100%;
        padding: 15px; /* Espaciado interno */
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    }
    
    .chart-title {
        margin-bottom: 20px !important; /* MÁS espacio entre título y gráfico */
        text-align: center;
        font-size: 1.1em; /* Tamaño más compacto */
        font-weight: 600;
        color: #2d3748;
        padding: 8px 15px;
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 8px;
        border-left: 4px solid #667eea;
        flex-shrink: 0; /* No se comprime */
        white-space: nowrap; /* Evita que el texto se corte */
        overflow: hidden;
        text-overflow: ellipsis; /* Si es muy largo, muestra ... */
    }
    
    .chart-wrapper {
        flex: 1; /* Toma el espacio restante */
        position: relative;
        min-height: 300px; /* Altura mínima para el gráfico */
    }
    
    .chart-container canvas {
        position: absolute !important;
        top: 0;
        left: 0;
        width: 100% !important;
        height: 100% !important;
        max-width: 100% !important;
        max-height: 100% !important;
    }
    
    /* 📱 RESPONSIVE - En pantallas pequeñas, gráficos en columna */
    @media (max-width: 768px) {
        .charts-grid {
            grid-template-columns: 1fr;
            gap: 15px;
        }
        
        .chart-container {
            height: 350px; /* Altura reducida pero suficiente */
            padding: 10px; /* Menos padding en móvil */
        }
        
        .chart-title {
            font-size: 1.1em; /* Título más pequeño en móvil */
            margin-bottom: 10px !important;
        }
        
        .chart-wrapper {
            min-height: 250px; /* Altura mínima menor */
        }
    }
    
    /* 📱 EXTRA SMALL - Para pantallas muy pequeñas */
    @media (max-width: 480px) {
        .chart-container {
            height: 320px;
            padding: 8px;
        }
        
        .chart-title {
            font-size: 1em;
        }
    }
"""

# CSS específico para Catálogo
CATALOG_CSS = """
    .products-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 25px;
        margin-top: 30px;
    }
    
    .product-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(102,126,234,0.1);
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .product-image {
        width: 100%;
        height: 200px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 3em;
    }
    
    .product-info {
        padding: 20px;
    }
    
    .product-name {
        color: #2d3748;
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .product-description {
        color: #4a5568;
        line-height: 1.5;
        margin-bottom: 15px;
        font-size: 0.9em;
    }
    
    .product-details {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .product-price {
        color: #667eea;
        font-size: 1.4em;
        font-weight: bold;
    }
    
    .product-category {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: 500;
    }
    
    .product-stock {
        color: #4a5568;
        font-size: 0.9em;
    }
    
    .product-badges {
        display: flex;
        gap: 8px;
        margin-top: 10px;
        flex-wrap: wrap;
    }
    
    .badge {
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 0.7em;
        font-weight: 500;
    }
    
    .badge-organic {
        background: #48bb78;
        color: white;
    }
    
    .badge-available {
        background: #38b2ac;
        color: white;
    }
    
    .search-section {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .search-input {
        width: 100%;
        padding: 12px 15px;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        font-size: 1em;
        transition: border-color 0.3s ease;
    }
    
    .search-input:focus {
        outline: none;
        border-color: #667eea;
    }
"""

# CSS específico para Documentación personalizada
DOCS_CSS = """
    /* Ocultar completamente el enlace openapi.json */
    .download-url-wrapper { display: none !important; }
    .info .url { display: none !important; }
    .topbar .download-url-wrapper { display: none !important; }
    .swagger-ui .info .main .link { display: none !important; }
    .swagger-ui .topbar .download-url-wrapper { display: none !important; }
    
    /* Mejorar apariencia */
    .swagger-ui .topbar { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-bottom: 2px solid #5a5a5a;
    }
    .swagger-ui .info .title {
        color: #2d3748 !important;
        font-weight: bold !important;
    }
    .swagger-ui .info .description {
        color: #4a5568 !important;
    }
    
    /* Personalizar botones de la documentación */
    .swagger-ui .btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 6px !important;
    }
    
    .swagger-ui .btn:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
    }
"""