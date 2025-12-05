"""
🖥️ Templates HTML para EcoMarket API
Archivo centralizado con todas las interfaces web
Este archivo contiene FUNCIONES que devuelven HTML completo (estructura + contenido)
"""

# 📥 IMPORTACIÓN: Trae los estilos CSS desde el archivo styles.py
from .styles import BASE_CSS, DASHBOARD_CSS, CATALOG_CSS, DOCS_CSS

# 🏠 FUNCIÓN: Genera la página principal (homepage) completa
def get_homepage_html():
    """🏠 FUNCIÓN: Crea la página principal completa de EcoMarket API"""
    
    # 📄 RETURN: Devuelve una cadena de texto con TODO el HTML de la página
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <!-- 🏷️ TÍTULO que aparece en la pestaña del navegador -->
    <title>🌱 EcoMarket API - Sistema Profesional</title>
    
    <!-- 🔤 CODIFICACIÓN: UTF-8 permite emojis y caracteres especiales -->
    <meta charset="UTF-8">
    
    <!-- 📱 RESPONSIVE: hace que se vea bien en móviles y tablets -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- 🔍 SEO: descripción que aparece en Google cuando buscan la página -->
    <meta name="description" content="EcoMarket API - Sistema profesional de gestión de inventarios">
    
    <!-- 🌱 FAVICON: el iconito que aparece en la pestaña (emoji de planta) -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌱</text></svg>">
    
    <!-- 🎨 CSS: Inserta aquí TODOS los estilos importados desde styles.py -->
    <style>{BASE_CSS}</style>
</head>
<body>
    <div class="container">
        <h1>🌱 EcoMarket API</h1>
        <h2>Sistema Profesional de Gestión</h2>
        
        <div class="nav-buttons">
            <a href="/docs" class="btn">📚 Documentación API</a>
            <a href="/dashboard" class="btn">📊 Dashboard</a>
            <a href="/catalog" class="btn">🛍️ Catálogo</a>
            <a href="/admin" class="btn" style="background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);">🔧 Administración</a>
        </div>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h3>🚀 API REST Completa</h3>
                <p>Operaciones CRUD completas para gestión de productos con validaciones avanzadas y paginación optimizada.</p>
            </div>
            
            <div class="feature-card">
                <h3>📊 Analytics en Tiempo Real</h3>
                <p>Dashboard interactivo con métricas del inventario, gráficas dinámicas y reportes estadísticos.</p>
            </div>
            
            <div class="feature-card">
                <h3>🔍 Búsqueda Avanzada</h3>
                <p>Sistema de filtrado inteligente por nombre, categoría, precio, estado orgánico y disponibilidad.</p>
            </div>
            
            <div class="feature-card">
                <h3>📱 Interfaz Moderna</h3>
                <p>Diseño responsive y atractivo con gradientes profesionales y experiencia de usuario optimizada.</p>
            </div>
            
            <div class="feature-card">
                <h3>🔒 Validaciones Robustas</h3>
                <p>Validación automática de datos con Pydantic, manejo de errores y ejemplos interactivos.</p>
            </div>
            
            <div class="feature-card">
                <h3>📚 Documentación Interactiva</h3>
                <p>Swagger UI integrado con ejemplos en vivo, esquemas detallados y pruebas directas.</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px; padding: 20px; background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); border-radius: 15px;">
            <h3>💼 ¿Listo para comenzar?</h3>
            <p>Explora nuestra documentación interactiva y descubre todo el potencial de EcoMarket API</p>
            <a href="/docs" class="btn">🚀 Comenzar Ahora</a>
        </div>
    </div>

    <script>
        // Homepage - sin dropdown de ventas
    </script>
</body>
</html>"""

def get_dashboard_html():
    """📊 Dashboard de estadísticas con gráficas interactivas"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <title>📊 EcoMarket API - Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📊</text></svg>">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {BASE_CSS}
        {DASHBOARD_CSS}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dashboard de Estadísticas</h1>
        
        <div class="nav-buttons">
            <a href="/" class="btn">🏠 Inicio</a>
            <a href="/docs" class="btn">📚 API Docs</a>
            <a href="/catalog" class="btn">🛍️ Catálogo</a>
        </div>
        
        <div class="metrics-grid" id="metrics-container">
            <!-- Las métricas se cargarán dinámicamente -->
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title">📈 Distribución por Categorías</div>
                <div class="chart-wrapper">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">💰 Análisis de Precios</div>
                <div class="chart-wrapper">
                    <canvas id="priceChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">📦 Estado del Inventario</div>
                <div class="chart-wrapper">
                    <canvas id="inventoryChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">🕒 Ventas por Día</div>
                <div class="chart-wrapper">
                    <canvas id="timeChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 🎨 CONFIGURACIÓN MEJORADA - Con espaciado adecuado para textos
        const chartConfig = {{
            responsive: true,
            maintainAspectRatio: false,
            animation: {{ duration: 0 }}, // Sin animaciones
            layout: {{
                padding: {{
                    top: 10,
                    bottom: 20,
                    left: 20,
                    right: 20
                }}
            }},
            plugins: {{
                legend: {{
                    position: 'bottom',
                    align: 'center',
                    labels: {{
                        usePointStyle: true,
                        padding: 15,
                        font: {{ 
                            size: 12,
                            weight: 'normal'
                        }},
                        boxWidth: 12,
                        boxHeight: 12
                    }}
                }}
            }}
        }};

        // 🌈 Colores sólidos sin transparencia
        const colors = [
            '#667eea', '#764ba2', '#48bb78',
            '#38b2ac', '#f6ad55', '#ed64a6'
        ];

        // 📊 Gráfica de categorías (Doughnut) - Con espaciado optimizado
        const ctx1 = document.getElementById('categoryChart').getContext('2d');
        new Chart(ctx1, {{
            type: 'doughnut',
            data: {{
                labels: ['Frutas', 'Verduras', 'Lácteos', 'Carnes', 'Bebidas', 'Otros'],
                datasets: [{{
                    data: [45, 19, 15, 12, 6, 3],
                    backgroundColor: colors,
                    borderWidth: 3,
                    borderColor: '#fff',
                    hoverBorderWidth: 4
                }}]
            }},
            options: {{
                ...chartConfig,
                cutout: '50%', // Tamaño del agujero central
                plugins: {{
                    ...chartConfig.plugins,
                    title: {{
                        display: true,
                        text: 'Productos por Categoría (%)'
                    }}
                }}
            }}
        }});

        // 💰 Gráfica de precios (Bar) - Con ejes claramente etiquetados
        const ctx2 = document.getElementById('priceChart').getContext('2d');
        new Chart(ctx2, {{
            type: 'bar',
            data: {{
                labels: ['$0-10', '$10-25', '$25-50', '$50-100', '$100+'],
                datasets: [{{
                    label: 'Cantidad',
                    data: [28, 45, 32, 18, 7],
                    backgroundColor: colors[0],
                    borderColor: colors[1],
                    borderWidth: 2,
                    borderRadius: 6,
                    borderSkipped: false
                }}]
            }},
            options: {{
                ...chartConfig,
                plugins: {{
                    ...chartConfig.plugins
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            padding: 10,
                            font: {{ size: 11 }},
                            color: '#4a5568'
                        }},
                        grid: {{
                            color: 'rgba(102,126,234,0.1)',
                            drawBorder: false
                        }}
                    }},
                    x: {{
                        ticks: {{
                            padding: 8,
                            font: {{ size: 10 }},
                            color: '#4a5568',
                            maxRotation: 0 // Evita rotación de etiquetas
                        }},
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});

        // Gráfica de inventario (Line)
        const ctx3 = document.getElementById('inventoryChart').getContext('2d');
        new Chart(ctx3, {{
            type: 'line',
            data: {{
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [{{
                    label: 'Stock Total',
                    data: [1200, 1350, 1180, 1420, 1380, 1500],
                    borderColor: colors[0],
                    backgroundColor: colors[0].replace('0.8', '0.2'),
                    tension: 0.4,
                    fill: true,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }}, {{
                    label: 'Productos Orgánicos',
                    data: [450, 520, 480, 580, 560, 620],
                    borderColor: colors[2],
                    backgroundColor: colors[2].replace('0.8', '0.2'),
                    tension: 0.4,
                    fill: true,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }}]
            }},
            options: {{
                ...chartConfig,
                plugins: {{
                    ...chartConfig.plugins,
                    title: {{
                        display: true,
                        text: 'Evolución del Inventario (6 meses)'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{
                            color: 'rgba(0,0,0,0.1)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});

        // 🕒 Gráfica de productos por tiempo (Radar)
        const ctx4 = document.getElementById('timeChart').getContext('2d');
        new Chart(ctx4, {{
            type: 'radar',
            data: {{
                labels: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
                datasets: [{{
                    label: 'Ventas por Día',
                    data: [65, 59, 90, 81, 56, 85, 40],
                    borderColor: colors[1],
                    backgroundColor: colors[1] + '20',
                    pointBackgroundColor: colors[1],
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: colors[1]
                }}]
            }},
            options: {{
                ...chartConfig,
                scales: {{
                    r: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});

        // 📊 Cargar métricas dinámicamente desde la API correcta
        fetch('/api/estadisticas')
            .then(response => response.json())
            .then(data => {{
                console.log('📊 Datos recibidos de la API:', data);
                const container = document.getElementById('metrics-container');
                
                // 🧮 Calcular métricas derivadas
                const totalCategorias = Object.keys(data.categorias || {{}}).length;
                
                container.innerHTML = `
                    <div class="metric-card">
                        <div class="metric-value">${{data.total_productos || 0}}</div>
                        <div class="metric-label">📦 Total Productos</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${{data.productos_disponibles || 0}}</div>
                        <div class="metric-label">✅ Disponibles</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${{data.productos_agotados || 0}}</div>
                        <div class="metric-label">❌ Agotados</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${{totalCategorias}}</div>
                        <div class="metric-label">🏷️ Categorías</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">$$${{(data.precio_promedio || 0).toFixed(2)}}</div>
                        <div class="metric-label">📊 Precio Promedio</div>
                    </div>
                `;
            }})
            .catch(error => {{
                console.log('Mostrando datos de ejemplo');
                const container = document.getElementById('metrics-container');
                container.innerHTML = `
                    <div class="metric-card">
                        <div class="metric-value">156</div>
                        <div class="metric-label">📦 Total Productos</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">89</div>
                        <div class="metric-label">🌱 Productos Orgánicos</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">142</div>
                        <div class="metric-label">✅ Disponibles</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">12</div>
                        <div class="metric-label">🏷️ Categorías</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">$24,580</div>
                        <div class="metric-label">💰 Valor Total</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">$18.45</div>
                        <div class="metric-label">📊 Precio Promedio</div>
                    </div>
                `;
            }});
    </script>
</body>
</html>"""

def get_catalog_html():
    """🛍️ Catálogo de productos con diseño moderno"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <title>🛍️ EcoMarket API - Catálogo</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛍️</text></svg>">
    <style>
        {BASE_CSS}
        {CATALOG_CSS}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛍️ Catálogo de Productos</h1>
        
        <div class="nav-buttons">
            <a href="/" class="btn">🏠 Inicio</a>
            <a href="/docs" class="btn">📚 API Docs</a>
            <a href="/stats-dashboard" class="btn">📊 Dashboard</a>
            <div class="sales-dropdown-container">
                <button class="btn-ventas" onclick="toggleSalesDropdown()">💸 Ventas ▼</button>
                <div class="sales-dropdown" id="salesDropdown">
                    <div class="dropdown-option" onclick="selectSalesMode('http-directo')">
                        <span class="mode-icon">🔗</span>
                        <span class="mode-name">HTTP Directo</span>
                    </div>
                    <div class="dropdown-option" onclick="selectSalesMode('reintentos-simples')">
                        <span class="mode-icon">🔄</span>
                        <span class="mode-name">Reintentos Simples</span>
                    </div>
                    <div class="dropdown-option" onclick="selectSalesMode('backoff-exponencial')">
                        <span class="mode-icon">📈</span>
                        <span class="mode-name">Backoff Exponencial</span>
                    </div>
                    <div class="dropdown-option" onclick="selectSalesMode('reintentos-sofisticados')">
                        <span class="mode-icon">🎯</span>
                        <span class="mode-name">Reintentos Sofisticados</span>
                    </div>
                    <div class="dropdown-option" onclick="selectSalesMode('redis-queue')">
                        <span class="mode-icon">📦</span>
                        <span class="mode-name">Redis Queue (En Redis)</span>
                    </div>
                    <div class="dropdown-option" onclick="selectSalesMode('rabbitmq')">
                        <span class="mode-icon">�</span>
                        <span class="mode-name">RabbitMQ (Garantías)</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="search-section">
            <h3>🔍 Buscar Productos</h3>
            <input type="text" class="search-input" id="searchInput" 
                   placeholder="Buscar por nombre, categoría o descripción...">
        </div>
        
        <!-- 🧪 Panel de Simulación de Fallos -->
        <div class="testing-panel" style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); padding: 20px; border-radius: 12px; margin: 20px 0; border: 2px solid #fdcb6e;">
            <h3 style="margin: 0 0 15px 0; color: #2d3436;">🧪 Simulador de Fallos de Conexión</h3>
            <p style="margin: 0 0 15px 0; color: #636e72; font-size: 0.9em;">Simula problemas de conexión para probar la resistencia de los diferentes modos de venta:</p>
            
            <!-- Botones de control general -->
            <div style="margin-bottom: 15px; text-align: center;">
                <button onclick="sincronizarEstado()" style="background: #0984e3; color: white; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; margin: 0 5px; font-size: 0.85em;">
                    🔄 Sincronizar Estado
                </button>
                <button onclick="resetCompleto()" style="background: #6c5ce7; color: white; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; margin: 0 5px; font-size: 0.85em;">
                    🔥 Reset Completo
                </button>
                <button onclick="desactivarTodos()" style="background: #d63031; color: white; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; margin: 0 5px; font-size: 0.85em;">
                    🚫 Desactivar Todos
                </button>
                <button onclick="activarTodos()" style="background: #00b894; color: white; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; margin: 0 5px; font-size: 0.85em;">
                    ✅ Activar Todos
                </button>
                <button onclick="debugEstado()" style="background: #fd79a8; color: white; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; margin: 0 5px; font-size: 0.85em;">
                    🐛 Debug Estado
                </button>
            </div></div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin-bottom: 15px;">
                <div style="text-align: center;">
                    <button onclick="toggleConnection('http_directo')" class="btn-connection" id="btn-http_directo" 
                            style="background: #00b894; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em; width: 100%;">
                        🔗 HTTP Directo: ON
                    </button>
                    <small style="color: #636e72; display: block; margin-top: 4px;">Solo: HTTP Directo</small>
                </div>
                <div style="text-align: center;">
                    <button onclick="toggleConnection('reintentos_simples')" class="btn-connection" id="btn-reintentos_simples"
                            style="background: #00b894; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em; width: 100%;">
                        � Reintentos: ON
                    </button>
                    <small style="color: #636e72; display: block; margin-top: 4px;">Solo: Reintentos Simples</small>
                </div>
                <div style="text-align: center;">
                    <button onclick="toggleConnection('backoff_exponencial')" class="btn-connection" id="btn-backoff_exponencial"
                            style="background: #00b894; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em; width: 100%;">
                        📈 Backoff: ON
                    </button>
                    <small style="color: #636e72; display: block; margin-top: 4px;">Solo: Backoff Exponencial</small>
                </div>
                <div style="text-align: center;">
                    <button onclick="toggleConnection('reintentos_sofisticados')" class="btn-connection" id="btn-reintentos_sofisticados"
                            style="background: #00b894; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em; width: 100%;">
                        🎯 Sofisticados: ON
                    </button>
                    <small style="color: #636e72; display: block; margin-top: 4px;">Solo: Reintentos Sofisticados</small>
                </div>
                <div style="text-align: center;">
                    <button onclick="toggleConnection('redis')" class="btn-connection" id="btn-redis"
                            style="background: #00b894; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em; width: 100%;">
                        📦 Redis: ON
                    </button>
                    <small style="color: #636e72; display: block; margin-top: 4px;">Solo: Redis Queue</small>
                </div>
                <div style="text-align: center;">
                    <button onclick="toggleConnection('rabbitmq')" class="btn-connection" id="btn-rabbitmq" 
                            style="background: #00b894; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em; width: 100%;">
                        � RabbitMQ: ON
                    </button>
                    <small style="color: #636e72; display: block; margin-top: 4px;">Solo: RabbitMQ</small>
                </div>
                <div style="text-align: center;">
                    <button onclick="toggleConnection('general_network')" class="btn-connection" id="btn-general_network"
                            style="background: #fd79a8; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em; width: 100%;">
                        🌐 Red General: ON
                    </button>
                    <small style="color: #636e72; display: block; margin-top: 4px;">Afecta: TODOS</small>
                </div>
            </div>
            
            <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
                <button onclick="desactivarTodo()" 
                        style="background: #e17055; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em;">
                    🚨 Desactivar Todo
                </button>
                <button onclick="resetAllConnections()" 
                        style="background: #74b9ff; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em;">
                    ✅ Activar Todo
                </button>
                <button onclick="checkConnectionStatus()" 
                        style="background: #a29bfe; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em;">
                    ℹ️ Ver Estado
                </button>
                <button onclick="testRetryModes()" 
                        style="background: #fd79a8; color: white; padding: 8px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em;">
                    🧪 Test Reintentos
                </button>
            </div>
        </div>
        
        <div id="products-container" class="products-grid">
            <!-- Los productos se cargarán dinámicamente -->
        </div>
        
        <div id="loading" style="text-align: center; margin: 40px 0;">
            <p style="color: #4a5568; font-size: 1.2em;">🔄 Cargando productos...</p>
        </div>
    </div>

    <script>
        let allProducts = [];
        let selectedSalesMode = 'HTTP_DIRECTO'; // Modo por defecto

        // Función para alternar dropdown de ventas
        function toggleSalesDropdown() {{
            const dropdown = document.getElementById('salesDropdown');
            dropdown.classList.toggle('show');
        }}

        // Función para seleccionar modo de ventas
        function selectSalesMode(mode) {{
            const modeMap = {{
                'http-directo': 'HTTP_DIRECTO',
                'reintentos-simples': 'REINTENTOS_SIMPLES',
                'backoff-exponencial': 'BACKOFF_EXPONENCIAL',
                'reintentos-sofisticados': 'REINTENTOS_SOFISTICADOS',
                'redis-queue': 'REDIS_QUEUE',
                'rabbitmq': 'RABBITMQ'
            }};
            
            selectedSalesMode = modeMap[mode] || 'HTTP_DIRECTO';
            
            // Actualizar texto del botón
            const modeNames = {{
                'HTTP_DIRECTO': 'HTTP Directo',
                'REINTENTOS_SIMPLES': 'Reintentos Simples',
                'BACKOFF_EXPONENCIAL': 'Backoff Exponencial',
                'REINTENTOS_SOFISTICADOS': 'Reintentos Sofisticados',
                'REDIS_QUEUE': 'Redis Queue',
                'RABBITMQ': 'RabbitMQ'
            }};
            
            const btn = document.querySelector('.btn-ventas');
            btn.innerHTML = `💸 Ventas: ${{modeNames[selectedSalesMode]}} ▼`;
            
            // Cerrar dropdown
            document.getElementById('salesDropdown').classList.remove('show');
            
            console.log('Modo seleccionado:', selectedSalesMode);
        }}

        // Función para renderizar productos
        function renderProducts(products) {{
            const container = document.getElementById('products-container');
            
            if (products.length === 0) {{
                container.innerHTML = `
                    <div style="grid-column: 1/-1; text-align: center; padding: 40px;">
                        <h3 style="color: #4a5568;">📭 No se encontraron productos</h3>
                        <p style="color: #718096;">Intenta con otros términos de búsqueda</p>
                    </div>
                `;
                return;
            }}

            container.innerHTML = products.map(product => `
                <div class="product-card" id="product-${{product.id}}">
                    <div class="product-image">
                        ${{getProductEmoji(product.category)}}
                    </div>
                    <div class="product-info">
                        <div class="product-name">${{product.name}}</div>
                        <div class="product-description">${{product.description || 'Sin descripción'}}</div>
                        
                        <div class="product-details">
                            <div class="product-price">${{formatPrice(product.price)}}</div>
                            <div class="product-category">${{product.category}}</div>
                        </div>
                        
                        <div class="product-stock" id="stock-${{product.id}}">📦 Stock: ${{product.stock}} unidades</div>
                        
                        <div class="product-badges">
                            ${{product.is_organic ? '<span class="badge badge-organic">🌱 Orgánico</span>' : ''}}
                            ${{product.is_available ? '<span class="badge badge-available">✅ Disponible</span>' : '<span class="badge" style="background: #e53e3e;">❌ No Disponible</span>'}}
                        </div>
                        
                        ${{product.is_available && product.stock > 0 ? `
                            <div style="margin-top: 15px; display: flex; gap: 10px; align-items: center;">
                                <input type="number" id="qty-${{product.id}}" min="1" max="${{product.stock}}" value="1" 
                                       style="width: 60px; padding: 8px; border: 2px solid #667eea; border-radius: 8px; text-align: center; font-weight: bold;">
                                <button onclick="comprarProducto(${{product.id}}, ${{product.price}})" 
                                        class="btn" style="flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: transform 0.2s;">
                                    🛒 Comprar
                                </button>
                            </div>
                        ` : '<div style="margin-top: 15px; padding: 10px; background: #fed7d7; color: #c53030; border-radius: 8px; text-align: center; font-weight: bold;">😔 Agotado</div>'}}
                    </div>
                </div>
            `).join('');
        }}

        // Función para obtener emoji según categoría
        function getProductEmoji(category) {{
            const emojiMap = {{
                'Frutas': '🍎',
                'Verduras': '🥬',
                'Frutas y Verduras': '🥬',
                'Lácteos': '🥛',
                'Carnes': '🥩',
                'Panadería': '🥖',
                'Bebidas': '🥤',
                'Condimentos y Especias': '🌶️',
                'Cereales': '🌾',
                'Snacks': '🍿'
            }};
            return emojiMap[category] || '📦';
        }}

        // Función para formatear precio
        function formatPrice(price) {{
            return new Intl.NumberFormat('es-MX', {{
                style: 'currency',
                currency: 'MXN'
            }}).format(price);
        }}

        // Función de búsqueda
        function searchProducts(query) {{
            if (!query.trim()) {{
                renderProducts(allProducts);
                return;
            }}

            const filtered = allProducts.filter(product => 
                product.name.toLowerCase().includes(query.toLowerCase()) ||
                product.category.toLowerCase().includes(query.toLowerCase()) ||
                (product.description && product.description.toLowerCase().includes(query.toLowerCase()))
            );
            
            renderProducts(filtered);
        }}

        // 🛒 Función para comprar producto
        function comprarProducto(productId, precio) {{
            const qtyInput = document.getElementById(`qty-${{productId}}`);
            const cantidad = parseInt(qtyInput.value) || 1;
            
            if (cantidad <= 0) {{
                alert('❌ La cantidad debe ser mayor que 0');
                return;
            }}
            
            // Mostrar modo seleccionado en la confirmación
            const modeNames = {{
                'HTTP_DIRECTO': 'HTTP Directo',
                'REINTENTOS_SIMPLES': 'Reintentos Simples',
                'BACKOFF_EXPONENCIAL': 'Backoff Exponencial',
                'REINTENTOS_SOFISTICADOS': 'Reintentos Sofisticados',
                'REDIS_QUEUE': 'Redis Queue',
                'RABBITMQ': 'RabbitMQ'
            }};
            
            const total = (precio * cantidad).toFixed(2);
            const confirmMessage = `¿Confirmar compra?\\n\\n📦 Cantidad: ${{cantidad}} unidad(es)\\n💰 Total: $$${{total}}\\n🔧 Modo: ${{modeNames[selectedSalesMode]}}`;
            
            if (!confirm(confirmMessage)) {{
                return;
            }}
            
            // Realizar petición al nuevo endpoint de compra
            const compraData = {{
                producto_id: productId,
                cantidad: cantidad,
                modo: selectedSalesMode
            }};
            
            fetch('/api/compras', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(compraData)
            }})
            .then(response => {{
                if (!response.ok) {{
                    return response.json().then(err => {{
                        // Manejar errores estructurados del servidor
                        if (typeof err.detail === 'object' && err.detail.mensaje) {{
                            throw new Error(err.detail.mensaje);
                        }}
                        throw new Error(err.detail || 'Error en la compra');
                    }});
                }}
                return response.json();
            }})
            .then(data => {{
                // Verificar si la venta falló
                if (data.estado === 'fallida' || data.alerta) {{
                    // Crear mensaje de error detallado
                    let errorMessage = `${{data.alerta || '❌ VENTA FALLIDA'}}\\n\\n`;
                    errorMessage += `🔧 Modo utilizado: ${{data.modo_procesamiento}}\\n`;
                    errorMessage += `📋 Detalles: ${{data.detalles || 'Sin detalles adicionales'}}\\n`;
                    
                    if (data.procesamiento) {{
                        errorMessage += `\\n📊 Procesamiento: ${{data.procesamiento}}`;
                    }}
                    
                    if (data.recomendacion) {{
                        errorMessage += `\\n\\n💡 Recomendación: ${{data.recomendacion}}`;
                    }}
                    
                    if (data.errores && data.errores.length > 0) {{
                        errorMessage += `\\n\\n🔍 Errores detectados:\\n${{data.errores.join('\\n')}}`;
                    }}
                    
                    alert(errorMessage);
                    return; // No actualizar UI si falló la venta
                }}
                
                // Crear mensaje de éxito detallado
                let successMessage = `✅ ${{data.mensaje}}\\n\\n💰 Total pagado: $$${{data.total_pagado}}\\n📦 Stock restante: ${{data.stock_restante}} unidades\\n🔧 Modo: ${{data.modo_procesamiento}}`;
                
                // Agregar información específica del modo
                if (data.rabbitmq_status) {{
                    successMessage += `\\n\\n🐰 RabbitMQ: ${{data.rabbitmq_status}}`;
                    if (data.cola) {{
                        successMessage += `\\n📫 Cola: ${{data.cola}}`;
                    }}
                }}
                
                if (data.procesamiento) {{
                    successMessage += `\\n\\n📋 Procesamiento: ${{data.procesamiento}}`;
                }}
                
                if (data.tiempo_total) {{
                    successMessage += `\\n⏱️ Tiempo total de esperas: ${{data.tiempo_total}}`;
                }}
                
                // Información especial para reintentos sofisticados
                if (data.modo_especial) {{
                    successMessage += `\\n\\n${{data.modo_especial}}`;
                }}
                
                if (data.intento_exitoso && selectedSalesMode === 'REINTENTOS_SOFISTICADOS') {{
                    successMessage += `\\n🎯 Éxito en intento: ${{data.intento_exitoso}}/5`;
                }}
                
                alert(successMessage);
                
                // Actualizar el stock en la UI
                const stockElement = document.getElementById(`stock-${{productId}}`);
                if (stockElement) {{
                    stockElement.textContent = `📦 Stock: ${{data.stock_restante}} unidades`;
                }}
                
                // Actualizar el producto en la lista
                const productIndex = allProducts.findIndex(p => p.id === productId);
                if (productIndex !== -1) {{
                    allProducts[productIndex].stock = data.stock_restante;
                    allProducts[productIndex].is_available = data.disponible;
                }}
                
                // Re-renderizar para actualizar el estado visual
                renderProducts(allProducts);
            }})
            .catch(error => {{
                alert(`❌ Error: ${{error.message}}`);
            }});
        }}

        // Event listener para búsqueda
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            searchProducts(e.target.value);
        }});

        // Cargar productos
        fetch('/api/productos')
            .then(response => response.json())
            .then(data => {{
                // Mapear campos en español a inglés para compatibilidad
                allProducts = (data || []).map(product => ({{
                    id: product.id,
                    name: product.nombre,
                    description: product.descripcion,
                    category: product.categoria,
                    price: product.precio,
                    stock: product.stock, // Stock real del producto
                    is_organic: true, // Asumimos orgánico por defecto
                    is_available: product.disponible
                }}));
                renderProducts(allProducts);
                document.getElementById('loading').style.display = 'none';
            }})
            .catch(error => {{
                console.log('Mostrando productos de ejemplo');
                // Productos de ejemplo si no hay datos
                allProducts = [
                    {{
                        name: '🥑 Aguacate Hass Orgánico',
                        description: 'Aguacate fresco de cultivo orgánico, cremoso y nutritivo',
                        category: 'Frutas y Verduras',
                        price: 25.50,
                        stock: 150,
                        is_organic: true,
                        is_available: true
                    }},
                    {{
                        name: '🍅 Tomate Cherry',
                        description: 'Tomates cherry dulces y jugosos, perfectos para ensaladas',
                        category: 'Frutas y Verduras',
                        price: 18.75,
                        stock: 200,
                        is_organic: false,
                        is_available: true
                    }},
                    {{
                        name: '🥕 Zanahoria Premium',
                        description: 'Zanahorias baby tiernas y dulces, ricas en betacarotenos',
                        category: 'Frutas y Verduras',
                        price: 12.99,
                        stock: 300,
                        is_organic: true,
                        is_available: true
                    }},
                    {{
                        name: '🍇 Uvas Rojas',
                        description: 'Uvas rojas sin semilla, jugosas y refrescantes',
                        category: 'Frutas y Verduras',
                        price: 32.00,
                        stock: 80,
                        is_organic: false,
                        is_available: true
                    }},
                    {{
                        name: '🥬 Lechuga Romana',
                        description: 'Lechuga romana fresca de cultivo orgánico',
                        category: 'Frutas y Verduras',
                        price: 9.50,
                        stock: 120,
                        is_organic: true,
                        is_available: true
                    }},
                    {{
                        name: '🍌 Plátano Dominico',
                        description: 'Plátanos maduros, dulces y cremosos',
                        category: 'Frutas y Verduras',
                        price: 14.25,
                        stock: 250,
                        is_organic: false,
                        is_available: true
                    }}
                ];
                renderProducts(allProducts);
                document.getElementById('loading').style.display = 'none';
            }});
        
        // 🧪 FUNCIONES DE SIMULACIÓN DE FALLOS
        let connectionStatus = {{
            rabbitmq: true,
            redis: true,
            http_directo: true,
            reintentos_simples: true,
            backoff_exponencial: true,
            reintentos_sofisticados: true,
            general_network: true
        }};

        // Función para alternar estado de conexión
        function toggleConnection(service) {{
            const newState = !connectionStatus[service];
            
            fetch('/api/simular-fallo', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    servicio: service,
                    activo: newState  // CORREGIDO: enviar el estado correcto directamente
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.mensaje) {{
                    // CORREGIDO: Actualizar con TODOS los servicios del servidor
                    connectionStatus = data.estado_actual;
                    updateConnectionButtons();
                    
                    const status = newState ? 'ON' : 'OFF';
                    const emoji = newState ? '✅' : '❌';
                    console.log(`🔄 ${{service.toUpperCase()}} cambiado a: ${{status}}`);
                    // Comentado alert para mejor UX
                    // alert(`${{emoji}} ${{service.toUpperCase()}} ahora está: ${{status}}`);
                }} else {{
                    alert(`❌ Error: ${{data.error}}`);
                }}
            }})
            .catch(error => {{
                console.error('Error cambiando estado:', error);
                alert(`❌ Error cambiando estado: ${{error.message}}`);
            }});
        }}

        // Función para actualizar botones
        function updateConnectionButtons() {{
            const services = ['http_directo', 'reintentos_simples', 'backoff_exponencial', 'reintentos_sofisticados', 'redis', 'rabbitmq', 'general_network'];
            const names = {{
                'http_directo': '🔗 HTTP Directo',
                'reintentos_simples': '� Reintentos',
                'backoff_exponencial': '📈 Backoff',
                'reintentos_sofisticados': '🎯 Sofisticados',
                'redis': '📦 Redis',
                'rabbitmq': '� RabbitMQ',
                'general_network': '🌐 Red General'
            }};
            
            services.forEach(service => {{
                const btn = document.getElementById(`btn-${{service}}`);
                if (!btn) {{
                    console.warn(`⚠️ Botón no encontrado: btn-${{service}}`);
                    return;
                }}
                
                // Verificar si el servicio existe en connectionStatus
                const isOn = connectionStatus[service] !== undefined ? connectionStatus[service] : true;
                
                btn.textContent = `${{names[service]}}: ${{isOn ? 'ON' : 'OFF'}}`;
                if (service === 'general_network') {{
                    btn.style.background = isOn ? '#fd79a8' : '#e17055';
                }} else {{
                    btn.style.background = isOn ? '#00b894' : '#e17055';
                }}
            }});
            
            // Debug: mostrar estado actual completo
            console.log('📊 Estado completo de connectionStatus:', connectionStatus);
            
            const serviciosOff = Object.entries(connectionStatus)
                .filter(([service, status]) => !status)
                .map(([service, status]) => service);
            
            if (serviciosOff.length > 0) {{
                console.log('🚫 Servicios desactivados:', serviciosOff);
            }} else {{
                console.log('✅ Todos los servicios están activos');
            }}
        }}

        // Función para desactivar todas las conexiones
        function desactivarTodo() {{
            if (!confirm('🚨 ¿Desactivar TODOS los servicios? Esto bloqueará todas las compras.')) {{
                return;
            }}
            
            fetch('/api/desactivar-todo', {{ method: 'POST' }})
                .then(response => response.json())
                .then(data => {{
                    connectionStatus = data.estado_actual;
                    updateConnectionButtons();
                    alert('🚨 TODOS los servicios han sido DESACTIVADOS\\n\\nTodas las compras serán bloqueadas');
                }})
                .catch(error => {{
                    alert(`❌ Error desactivando servicios: ${{error.message}}`);
                }});
        }}

        // Función para restaurar todas las conexiones
        function resetAllConnections() {{
            fetch('/api/activar-todo', {{ method: 'POST' }})
                .then(response => response.json())
                .then(data => {{
                    connectionStatus = data.estado_actual;
                    updateConnectionButtons();
                    alert('✅ TODOS los servicios han sido ACTIVADOS');
                }})
                .catch(error => {{
                    alert(`❌ Error activando servicios: ${{error.message}}`);
                }});
        }}

        // Función para verificar estado actual
        function checkConnectionStatus() {{
            fetch('/api/estado-conexiones')
                .then(response => response.json())
                .then(data => {{
                    let message = '📊 Estado Actual de Conexiones:\\n\\n';
                    Object.entries(data.conexiones).forEach(([service, status]) => {{
                        const emoji = status ? '✅' : '❌';
                        const state = status ? 'ACTIVO' : 'DESACTIVADO';
                        message += `${{emoji}} ${{service.toUpperCase()}}: ${{state}}\\n`;
                    }});
                    
                    message += '\\n🎯 Impacto por Modo de Venta:\\n';
                    Object.entries(data.impacto_por_modo).forEach(([modo, servicios]) => {{
                        const serviciosAfectados = servicios.map(s => data.conexiones[s] ? '✅' : '❌').join(' ');
                        message += `${{modo}}: ${{serviciosAfectados}}\\n`;
                    }});
                    
                    alert(message);
                }})
                .catch(error => {{
                    alert(`❌ Error obteniendo estado: ${{error.message}}`);
                }});
        }}

        // Función para probar específicamente los modos de reintentos
        function testRetryModes() {{
            if (!confirm('🧪 ¿Probar los modos de reintentos con el estado actual de conexiones?')) {{
                return;
            }}
            
            fetch('/api/test-connection-retry', {{ 
                method: 'POST'
                // Sin timeout específico - usar el default del navegador (~60s)
            }})
                .then(response => response.json())
                .then(data => {{
                    let message = '🧪 RESULTADOS DE PRUEBA DE REINTENTOS:\\n\\n';
                    
                    message += '📊 Estado de Conexiones:\\n';
                    Object.entries(data.estado_conexiones).forEach(([service, status]) => {{
                        const emoji = status ? '✅' : '❌';
                        message += `${{emoji}} ${{service.toUpperCase()}}: ${{status ? 'ON' : 'OFF'}}\\n`;
                    }});
                    
                    message += '\\n🔄 REINTENTOS SIMPLES:\\n';
                    message += `Status: ${{data.reintentos_simples.status}}\\n`;
                    message += `Mensaje: ${{data.reintentos_simples.mensaje}}\\n`;
                    if (data.reintentos_simples.errores) {{
                        message += `Errores: ${{data.reintentos_simples.errores.length}} detectados\\n`;
                    }}
                    
                    message += '\\n📈 BACKOFF EXPONENCIAL:\\n';
                    message += `Status: ${{data.backoff_exponencial.status}}\\n`;
                    message += `Mensaje: ${{data.backoff_exponencial.mensaje}}\\n`;
                    if (data.backoff_exponencial.tiempo_total_esperas) {{
                        message += `Tiempo total: ${{data.backoff_exponencial.tiempo_total_esperas}}\\n`;
                    }}
                    
                    message += '\\n🎯 REINTENTOS SOFISTICADOS:\\n';
                    message += `Status: ${{data.reintentos_sofisticados.status}}\\n`;
                    message += `Mensaje: ${{data.reintentos_sofisticados.mensaje}}\\n`;
                    if (data.reintentos_sofisticados.tiempo_total_esperas) {{
                        message += `Tiempo total: ${{data.reintentos_sofisticados.tiempo_total_esperas}}\\n`;
                    }}
                    if (data.reintentos_sofisticados.intento) {{
                        message += `Intentos realizados: ${{data.reintentos_sofisticados.intento}}/5\\n`;
                    }}
                    
                    // Mostrar el mensaje principal primero
                    alert(message);
                    
                    // Mostrar detalles de reintentos sofisticados en una segunda alerta
                    if (data.reintentos_sofisticados.errores && data.reintentos_sofisticados.errores.length > 0) {{
                        let detalleMessage = '🎯 DETALLE DE REINTENTOS SOFISTICADOS:\\n\\n';
                        detalleMessage += `Intentos realizados: ${{data.reintentos_sofisticados.intento || data.reintentos_sofisticados.errores.length}}/5\\n`;
                        detalleMessage += `Tiempo total: ${{data.reintentos_sofisticados.tiempo_total_esperas}}\\n\\n`;
                        
                        data.reintentos_sofisticados.errores.forEach((error, index) => {{
                            const esperaTiempos = [1, 2, 4, 8, 16];
                            const tiempoEspera = esperaTiempos[index] || 'N/A';
                            detalleMessage += `Intento ${{index + 1}}: ${{error}}\\n`;
                            detalleMessage += `   └── Tiempo de espera: ${{tiempoEspera}} segundos\\n\\n`;
                        }});
                        
                        if (data.reintentos_sofisticados.recomendacion) {{
                            detalleMessage += `Recomendación:\\n${{data.reintentos_sofisticados.recomendacion}}`;
                        }}
                        
                        alert(detalleMessage);
                    }} else if (data.reintentos_sofisticados.status === 'success') {{
                        let successMessage = '🎯 REINTENTOS SOFISTICADOS - ÉXITO:\\n\\n';
                        successMessage += `Procesado exitosamente en intento ${{data.reintentos_sofisticados.intento}}/5\\n`;
                        successMessage += `Tiempo total: ${{data.reintentos_sofisticados.tiempo_total_esperas}}\\n\\n`;
                        successMessage += 'El sistema funcionó correctamente después de los reintentos programados.';
                        alert(successMessage);
                    }}
                }})
                .catch(error => {{
                    alert(`❌ Error en prueba: ${{error.message}}`);
                }});
        }}

        // Función para sincronizar estado con servidor
        function sincronizarEstado() {{
            fetch('/api/estado-conexiones')
                .then(response => response.json())
                .then(data => {{
                    console.log('🔄 Estado del servidor:', data.conexiones);
                    connectionStatus = data.conexiones;
                    updateConnectionButtons();
                    
                    // Mostrar estado actual en consola para debug
                    const serviciosOff = Object.entries(connectionStatus)
                        .filter(([service, status]) => !status)
                        .map(([service, status]) => service);
                    
                    if (serviciosOff.length > 0) {{
                        console.log('🚫 Servicios desactivados:', serviciosOff);
                        alert(`🔄 Estado sincronizado.\\n\\n🚫 Servicios desactivados: ${{serviciosOff.join(', ')}}`);
                    }} else {{
                        console.log('✅ Todos los servicios están activos');
                        alert('🔄 Estado sincronizado.\\n\\n✅ Todos los servicios están activos');
                    }}
                }})
                .catch(error => {{
                    console.error('❌ Error al cargar estado:', error);
                    alert('Error al sincronizar estado con servidor');
                }});
        }}

        // Función para desactivar todos los servicios
        function desactivarTodos() {{
            if (!confirm('¿Desactivar TODOS los servicios?\\n\\nEsto simulará fallos completos del sistema.')) {{
                return;
            }}
            
            const services = ['http_directo', 'reintentos_simples', 'backoff_exponencial', 'reintentos_sofisticados', 'redis', 'rabbitmq', 'general_network'];
            let promesas = services.map(service => 
                fetch('/api/simular-fallo', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ servicio: service, activo: false }})
                }})
            );
            
            Promise.all(promesas).then(() => {{
                sincronizarEstado();
            }});
        }}

        // Función para activar todos los servicios
        function activarTodos() {{
            const services = ['http_directo', 'reintentos_simples', 'backoff_exponencial', 'reintentos_sofisticados', 'redis', 'rabbitmq', 'general_network'];
            let promesas = services.map(service => 
                fetch('/api/simular-fallo', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ servicio: service, activo: true }})
                }})
            );
            
            Promise.all(promesas).then(() => {{
                sincronizarEstado();
            }});
        }}

        // Función para reset completo desde el servidor
        function resetCompleto() {{
            if (!confirm('¿Hacer RESET COMPLETO del sistema?\\n\\nEsto reactivará todos los servicios desde el servidor.')) {{
                return;
            }}
            
            fetch('/api/reset-conexiones', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }}
            }})
            .then(response => response.json())
            .then(data => {{
                console.log('🔥 Reset completo realizado:', data);
                sincronizarEstado();
                alert('🔥 RESET COMPLETO REALIZADO\\n\\n✅ Todos los servicios han sido reactivados');
            }})
            .catch(error => {{
                console.error('❌ Error en reset:', error);
                alert('Error al realizar reset completo');
            }});
        }}

        // Función de debug para verificar estado
        function debugEstado() {{
            console.log('=== DEBUG DE ESTADO ===');
            console.log('1. Estado local (connectionStatus):', connectionStatus);
            
            fetch('/api/estado-conexiones')
                .then(response => response.json())
                .then(data => {{
                    console.log('2. Estado del servidor:', data.conexiones);
                    
                    const diferencias = [];
                    Object.keys(data.conexiones).forEach(service => {{
                        const local = connectionStatus[service];
                        const servidor = data.conexiones[service];
                        if (local !== servidor) {{
                            diferencias.push(`${{service}}: local=${{local}}, servidor=${{servidor}}`);
                        }}
                    }});
                    
                    if (diferencias.length > 0) {{
                        console.warn('⚠️ DIFERENCIAS encontradas:', diferencias);
                        alert(`⚠️ ESTADO DESINCRONIZADO\\n\\nDiferencias:\\n${{diferencias.join('\\n')}}\\n\\n¿Sincronizar ahora?`) && sincronizarEstado();
                    }} else {{
                        console.log('✅ Estados sincronizados correctamente');
                        alert('✅ Estado local y servidor están sincronizados');
                    }}
                }})
                .catch(error => {{
                    console.error('❌ Error verificando servidor:', error);
                    alert('❌ Error al verificar estado del servidor');
                }});
        }}

        // Función para reset completo del servidor
        function resetCompleto() {{
            if (!confirm('🔥 ¿Hacer RESET COMPLETO del servidor?\\n\\nEsto reactivará todos los servicios en el servidor.')) {{
                return;
            }}
            
            fetch('/api/reset-conexiones', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }}
            }})
            .then(response => response.json())
            .then(data => {{
                console.log('🔥 Reset completo realizado:', data);
                sincronizarEstado();
                alert('🔥 RESET COMPLETO realizado\\n\\n✅ Todos los servicios han sido reactivados en el servidor');
            }})
            .catch(error => {{
                console.error('❌ Error en reset:', error);
                alert('Error al hacer reset completo');
            }});
        }}

        // Inicializar estado de botones al cargar
        setTimeout(() => {{
            sincronizarEstado();
        }}, 1000);

        // Cerrar dropdown si se hace clic fuera
        document.addEventListener('click', function(event) {{
            const container = document.querySelector('.sales-dropdown-container');
            const dropdown = document.getElementById('salesDropdown');
            
            if (container && !container.contains(event.target)) {{
                dropdown.classList.remove('show');
            }}
        }});
    </script>
</body>
</html>"""

def get_admin_html():
    """🔧 Panel de administración para gestionar productos (CRUD completo) con JWT"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <title>🔧 EcoMarket API - Administración</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔧</text></svg>">
    <style>
        {BASE_CSS}
        {CATALOG_CSS}
        
        .user-bar {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .user-info {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .user-role {{
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        
        .btn-logout {{
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid white;
            padding: 8px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .btn-logout:hover {{
            background: white;
            color: #667eea;
        }}
        
        .form-container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .form-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .form-group {{
            display: flex;
            flex-direction: column;
        }}
        
        .form-group label {{
            font-weight: 600;
            margin-bottom: 8px;
            color: #2d3748;
        }}
        
        .form-group input,
        .form-group textarea,
        .form-group select {{
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }}
        
        .form-group input:focus,
        .form-group textarea:focus,
        .form-group select:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            transition: transform 0.2s;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
        }}
        
        .btn-secondary {{
            background: linear-gradient(135deg, #48bb78 0%, #38b2ac 100%);
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 8px;
        }}
        
        .btn-danger {{
            background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }}
        
        .product-actions {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}
        
        .section-title {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 20px;
            color: #2d3748;
        }}
        
        .loading-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.95);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            flex-direction: column;
            gap: 20px;
        }}
        
        .spinner {{
            width: 50px;
            height: 50px;
            border: 5px solid #e2e8f0;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div id="loadingOverlay" class="loading-overlay">
        <div class="spinner"></div>
        <p style="color: #667eea; font-size: 1.2em; font-weight: bold;">🔐 Verificando autenticación...</p>
    </div>

    <div class="container" id="mainContent" style="display: none;">
        <h1>🔧 Panel de Administración</h1>
        
        <!-- Barra de usuario -->
        <div class="user-bar">
            <div class="user-info">
                <span style="font-size: 1.5em;">👤</span>
                <div>
                    <div style="font-weight: bold;" id="userName">Usuario</div>
                    <div style="font-size: 0.9em; opacity: 0.9;" id="userEmail">email</div>
                </div>
                <span class="user-role" id="userRole">ROLE</span>
            </div>
            <button onclick="logout()" class="btn-logout">🚪 Cerrar Sesión</button>
        </div>
        
        <div class="nav-buttons">
            <a href="/" class="btn">🏠 Inicio</a>
            <a href="/catalog" class="btn">🛍️ Catálogo</a>
            <a href="/docs" class="btn">📚 API Docs</a>
            <a href="/dashboard" class="btn">📊 Dashboard</a>
        </div>

        <!-- Formulario para crear/editar producto -->
        <div class="form-container">
            <div class="section-title" id="form-title">➕ Crear Nuevo Producto</div>
            <form id="productForm">
                <input type="hidden" id="productId">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="nombre">* Nombre:</label>
                        <input type="text" id="nombre" required>
                    </div>
                    <div class="form-group">
                        <label for="categoria">* Categoría:</label>
                        <select id="categoria" required>
                            <option value="">Seleccionar...</option>
                            <option value="Frutas">Frutas</option>
                            <option value="Verduras">Verduras</option>
                            <option value="Lácteos">Lácteos</option>
                            <option value="Carnes">Carnes</option>
                            <option value="Bebidas">Bebidas</option>
                            <option value="Panadería">Panadería</option>
                            <option value="Otros">Otros</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="precio">* Precio:</label>
                        <input type="number" id="precio" step="0.01" min="0.01" required>
                    </div>
                    <div class="form-group">
                        <label for="stock">* Stock:</label>
                        <input type="number" id="stock" min="0" value="0" required>
                    </div>
                    <div class="form-group">
                        <label for="disponible">Disponible:</label>
                        <select id="disponible">
                            <option value="true">Sí</option>
                            <option value="false">No</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <label for="descripcion">Descripción:</label>
                    <textarea id="descripcion" rows="3"></textarea>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button type="submit" class="btn-primary" id="submitBtn">➕ Crear Producto</button>
                    <button type="button" class="btn-secondary" onclick="cancelarEdicion()" id="cancelBtn" style="display: none;">❌ Cancelar</button>
                </div>
            </form>
        </div>
        
        <!-- Lista de productos existentes -->
        <div class="section-title">📦 Productos Existentes</div>
        <div id="products-container" class="products-grid">
            <!-- Los productos se cargarán dinámicamente -->
        </div>
        
        <div id="loading" style="text-align: center; margin: 40px 0;">
            <p style="color: #4a5568; font-size: 1.2em;">🔄 Cargando productos...</p>
        </div>
    </div>

    <script>
        let allProducts = [];
        let editingProductId = null;
        let accessToken = null;
        let userRole = null;
        
        // Verificar autenticación al cargar
        async function checkAuth() {{
            accessToken = localStorage.getItem('access_token');
            const userEmail = localStorage.getItem('user_email');
            userRole = localStorage.getItem('user_role');
            
            if (!accessToken) {{
                // No hay token, redirigir al login
                window.location.href = '/login';
                return false;
            }}
            
            try {{
                // Verificar que el token sea válido
                const response = await fetch('/api/auth/me', {{
                    headers: {{
                        'Authorization': `Bearer ${{accessToken}}`
                    }}
                }});
                
                if (!response.ok) {{
                    // Token inválido, limpiar y redirigir
                    localStorage.clear();
                    window.location.href = '/login';
                    return false;
                }}
                
                const userData = await response.json();
                
                // Actualizar UI con datos del usuario
                document.getElementById('userName').textContent = userData.nombre || 'Usuario';
                document.getElementById('userEmail').textContent = userData.email;
                document.getElementById('userRole').textContent = userData.role.toUpperCase();
                
                // Verificar permisos (solo admin y vendedor pueden administrar)
                if (userData.role === 'cliente') {{
                    // Limpiar sesión y redirigir a login con mensaje
                    localStorage.clear();
                    window.location.href = '/login?blocked=cliente';
                    return false;
                }}
                
                // Ocultar overlay y mostrar contenido
                document.getElementById('loadingOverlay').style.display = 'none';
                document.getElementById('mainContent').style.display = 'block';
                
                return true;
            }} catch (error) {{
                console.error('Error verificando autenticación:', error);
                localStorage.clear();
                window.location.href = '/login';
                return false;
            }}
        }}
        
        // Función para obtener headers con JWT
        function getAuthHeaders() {{
            return {{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${{accessToken}}`
            }};
        }}
        
        // Cerrar sesión
        async function logout() {{
            const refreshToken = localStorage.getItem('refresh_token');
            
            // Revocar refresh token
            if (refreshToken) {{
                try {{
                    await fetch('/api/auth/logout', {{
                        method: 'POST',
                        headers: getAuthHeaders(),
                        body: JSON.stringify({{ refresh_token: refreshToken }})
                    }});
                }} catch (error) {{
                    console.error('Error al cerrar sesión:', error);
                }}
            }}
            
            // Limpiar localStorage
            localStorage.clear();
            
            // Redirigir al login
            window.location.href = '/login';
        }}
        
        // Cargar productos
        function loadProducts() {{
            fetch('/api/productos')
                .then(response => response.json())
                .then(data => {{
                    allProducts = data || [];
                    renderAdminProducts(allProducts);
                    document.getElementById('loading').style.display = 'none';
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    document.getElementById('loading').innerHTML = '<p style="color: #e53e3e;">❌ Error al cargar productos</p>';
                }});
        }}
        
        // Renderizar productos con botones de administración
        function renderAdminProducts(products) {{
            const container = document.getElementById('products-container');
            
            if (products.length === 0) {{
                container.innerHTML = `
                    <div style="grid-column: 1/-1; text-align: center; padding: 40px;">
                        <h3 style="color: #4a5568;">📭 No hay productos</h3>
                        <p style="color: #718096;">Crea tu primer producto usando el formulario</p>
                    </div>
                `;
                return;
            }}

            container.innerHTML = products.map(product => `
                <div class="product-card" id="product-${{product.id}}">
                    <div class="product-info">
                        <div class="product-name">${{product.nombre}}</div>
                        <div class="product-description">${{product.descripcion || 'Sin descripción'}}</div>
                        
                        <div class="product-details">
                            <div class="product-price">$${{product.precio.toFixed(2)}}</div>
                            <div class="product-category">${{product.categoria}}</div>
                        </div>
                        
                        <div class="product-stock">📦 Stock: ${{product.stock}} unidades</div>
                        
                        <div class="product-badges">
                            ${{product.disponible ? '<span class="badge badge-available">✅ Disponible</span>' : '<span class="badge" style="background: #e53e3e;">❌ No Disponible</span>'}}
                        </div>
                        
                        <div class="product-actions">
                            <button onclick="editarProducto(${{product.id}})" class="btn-secondary">✏️ Editar</button>
                            ${{userRole === 'admin' ? `<button onclick="eliminarProducto(${{product.id}}, '${{product.nombre}}')" class="btn-danger">🗑️ Eliminar</button>` : ''}}
                        </div>
                    </div>
                </div>
            `).join('');
        }}
        
        // Manejar envío del formulario (crear o actualizar)
        document.getElementById('productForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const productData = {{
                nombre: document.getElementById('nombre').value,
                categoria: document.getElementById('categoria').value,
                precio: parseFloat(document.getElementById('precio').value),
                stock: parseInt(document.getElementById('stock').value),
                disponible: document.getElementById('disponible').value === 'true',
                descripcion: document.getElementById('descripcion').value || null
            }};
            
            if (editingProductId) {{
                // Actualizar producto existente
                actualizarProducto(editingProductId, productData);
            }} else {{
                // Crear nuevo producto
                crearProducto(productData);
            }}
        }});
        
        // Crear producto (CON JWT)
        function crearProducto(data) {{
            fetch('/api/productos', {{
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(data)
            }})
            .then(async response => {{
                if (response.status === 401) {{
                    alert('❌ Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
                    logout();
                    return;
                }}
                if (!response.ok) {{
                    const error = await response.json();
                    throw new Error(error.detail || 'Error al crear producto');
                }}
                return response.json();
            }})
            .then(newProduct => {{
                if (newProduct) {{
                    alert(`✅ Producto "${{newProduct.nombre}}" creado exitosamente`);
                    document.getElementById('productForm').reset();
                    loadProducts();
                }}
            }})
            .catch(error => {{
                alert(`❌ Error: ${{error.message}}`);
            }});
        }}
        
        // Editar producto
        function editarProducto(id) {{
            const product = allProducts.find(p => p.id === id);
            if (!product) return;
            
            editingProductId = id;
            document.getElementById('productId').value = id;
            document.getElementById('nombre').value = product.nombre;
            document.getElementById('categoria').value = product.categoria;
            document.getElementById('precio').value = product.precio;
            document.getElementById('stock').value = product.stock;
            document.getElementById('disponible').value = product.disponible.toString();
            document.getElementById('descripcion').value = product.descripcion || '';
            
            document.getElementById('form-title').textContent = '✏️ Editar Producto';
            document.getElementById('submitBtn').textContent = '💾 Guardar Cambios';
            document.getElementById('cancelBtn').style.display = 'inline-block';
            
            // Scroll al formulario
            document.getElementById('productForm').scrollIntoView({{ behavior: 'smooth' }});
        }}
        
        // Actualizar producto (CON JWT)
        function actualizarProducto(id, data) {{
            fetch(`/api/productos/${{id}}`, {{
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify(data)
            }})
            .then(async response => {{
                if (response.status === 401) {{
                    alert('❌ Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
                    logout();
                    return;
                }}
                if (!response.ok) {{
                    const error = await response.json();
                    throw new Error(error.detail || 'Error al actualizar producto');
                }}
                return response.json();
            }})
            .then(updatedProduct => {{
                if (updatedProduct) {{
                    alert(`✅ Producto "${{updatedProduct.nombre}}" actualizado exitosamente`);
                    cancelarEdicion();
                    loadProducts();
                }}
            }})
            .catch(error => {{
                alert(`❌ Error: ${{error.message}}`);
            }});
        }}
        
        // Eliminar producto (CON JWT, solo admin)
        function eliminarProducto(id, nombre) {{
            if (userRole !== 'admin') {{
                alert('❌ Solo los administradores pueden eliminar productos');
                return;
            }}
            
            if (!confirm(`¿Estás seguro de eliminar "${{nombre}}"?`)) {{
                return;
            }}
            
            fetch(`/api/productos/${{id}}`, {{
                method: 'DELETE',
                headers: getAuthHeaders()
            }})
            .then(async response => {{
                if (response.status === 401) {{
                    alert('❌ Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
                    logout();
                    return;
                }}
                if (!response.ok) {{
                    const error = await response.json();
                    throw new Error(error.detail || 'Error al eliminar producto');
                }}
                return response.json();
            }})
            .then(data => {{
                if (data) {{
                    alert(`✅ ${{data.mensaje}}`);
                    loadProducts();
                }}
            }})
            .catch(error => {{
                alert(`❌ Error: ${{error.message}}`);
            }});
        }}
        
        // Cancelar edición
        function cancelarEdicion() {{
            editingProductId = null;
            document.getElementById('productForm').reset();
            document.getElementById('form-title').textContent = '➕ Crear Nuevo Producto';
            document.getElementById('submitBtn').textContent = '➕ Crear Producto';
            document.getElementById('cancelBtn').style.display = 'none';
        }}
        
        // Inicializar al cargar la página
        checkAuth().then(isAuthenticated => {{
            if (isAuthenticated) {{
                loadProducts();
            }}
        }});
    </script>
</body>
</html>"""

def get_docs_css():
    """CSS personalizado para la documentación"""
    return DOCS_CSS


def get_sales_html():
    """💸 Página completa de ventas con funcionalidad"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <title>💸 EcoMarket API - Ventas</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <!-- VERSION ACTUALIZADA: 2025-10-27 -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💸</text></svg>'>
    <style>
        {BASE_CSS}
        
        .sales-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 30px;
        }}
        
        .sales-form {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #e2e8f0 100%);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            border: 2px solid rgba(72,187,120,0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .sales-form::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #48bb78, #38a169, #2f855a);
        }}
        
        .sales-form:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(72,187,120,0.2);
        }}
        
        .sales-list {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #e2e8f0 100%);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            border: 2px solid rgba(102,126,234,0.1);
            max-height: 500px;
            overflow-y: auto;
            transition: all 0.3s ease;
            position: relative;
            overflow-x: hidden;
        }}
        
        .sales-list::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2, #5a67d8);
        }}
        
        .sales-list:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(102,126,234,0.2);
        }}
        
        .form-group {{
            margin-bottom: 20px;
            position: relative;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2d3748;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .form-group input, .form-group select {{
            width: 100%;
            padding: 14px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .form-group input:focus, .form-group select:focus {{
            outline: none;
            border-color: #48bb78;
            box-shadow: 0 0 0 4px rgba(72,187,120,0.1), 0 4px 12px rgba(72,187,120,0.15);
            transform: translateY(-2px);
        }}
        
        .form-group input:hover, .form-group select:hover {{
            border-color: #cbd5e0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .sale-item {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 15px;
            border-left: 5px solid #48bb78;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .sale-item::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(72,187,120,0.02), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .sale-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 8px 25px rgba(72,187,120,0.15);
            border-left-color: #38a169;
        }}
        
        .sale-item:hover::before {{
            opacity: 1;
        }}
        
        .sale-info {{
            flex: 1;
        }}
        
        .sale-amount {{
            font-size: 1.2em;
            font-weight: bold;
            color: #48bb78;
        }}
        
        .metrics-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #48bb78 0%, #38a169 50%, #2f855a 100%);
            color: white;
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(72,187,120,0.3);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            border: 2px solid rgba(255,255,255,0.1);
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            transition: transform 0.6s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 15px 40px rgba(72,187,120,0.4);
        }}
        
        .metric-card:hover::before {{
            transform: rotate(45deg) translate(50%, 50%);
        }}
        
        .metric-number {{
            font-size: 2.5em;
            font-weight: 900;
            margin-bottom: 8px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            color: white;
        }}
        
        .metric-label {{
            font-size: 0.85em;
            opacity: 0.95;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        @media (max-width: 768px) {{
            .sales-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="background: linear-gradient(135deg, #48bb78, #38a169, #2f855a); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 3em; margin-bottom: 10px;">💸 Gestión de Ventas</h1>
            <p style="color: #718096; font-size: 1.2em; font-weight: 500;">Centro de control de ventas y transacciones</p>
        </div>
        
        <div class="nav-buttons">
            <a href="/" class="btn">🏠 Inicio</a>
            <a href="/docs" class="btn">📚 API Docs</a>
            <a href="/dashboard" class="btn">📊 Dashboard</a>
            <a href="/catalog" class="btn">🛍️ Catálogo</a>
            <a href="/admin" class="btn">🔧 Administración</a>
        </div>
        
        <div class="metrics-row" id="sales-metrics" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0;">
            <div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 50%, #2f855a 100%); color: white; padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0 8px 25px rgba(72,187,120,0.3);">
                <div class="metric-number" id="total-sales" style="font-size: 2.5em; font-weight: 900; margin-bottom: 8px;">$0</div>
                <div class="metric-label" style="font-size: 0.85em; opacity: 0.95; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Ventas Totales</div>
            </div>
            <div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 50%, #2f855a 100%); color: white; padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0 8px 25px rgba(72,187,120,0.3);">
                <div class="metric-number" id="daily-sales" style="font-size: 2.5em; font-weight: 900; margin-bottom: 8px;">$0</div>
                <div class="metric-label" style="font-size: 0.85em; opacity: 0.95; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Ventas Hoy</div>
            </div>
            <div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 50%, #2f855a 100%); color: white; padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0 8px 25px rgba(72,187,120,0.3);">
                <div class="metric-number" id="transactions-count" style="font-size: 2.5em; font-weight: 900; margin-bottom: 8px;">0</div>
                <div class="metric-label" style="font-size: 0.85em; opacity: 0.95; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Transacciones</div>
            </div>
            <div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 50%, #2f855a 100%); color: white; padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0 8px 25px rgba(72,187,120,0.3);">
                <div class="metric-number" id="avg-sale" style="font-size: 2.5em; font-weight: 900; margin-bottom: 8px;">$0</div>
                <div class="metric-label" style="font-size: 0.85em; opacity: 0.95; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Venta Promedio</div>
            </div>
        </div>
        
        <div class="sales-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 30px;">
            <div class="sales-form" style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #e2e8f0 100%); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 2px solid rgba(72,187,120,0.1);"
                <h2 style="color: #2d3748; margin-bottom: 25px; font-size: 1.5em; display: flex; align-items: center; gap: 10px;">
                    <span style="background: linear-gradient(135deg, #48bb78, #38a169); color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2em;">📝</span>
                    Nueva Venta
                </h2>
                <form id="sale-form">
                    <div class="form-group">
                        <label for="product-select">Producto:</label>
                        <select id="product-select" required>
                            <option value="">Seleccionar producto...</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="quantity">Cantidad:</label>
                        <input type="number" id="quantity" min="1" value="1" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="customer">Cliente:</label>
                        <input type="text" id="customer" placeholder="Nombre del cliente" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="total-display">Total:</label>
                        <input type="text" id="total-display" readonly style="background: #f7fafc; font-weight: bold;">
                    </div>
                    
                    <button type="submit" class="btn-ventas" style="width: 100%; margin-top: 15px; padding: 16px 25px; font-size: 1.1em;">
                        💰 Registrar Venta
                    </button>
                </form>
            </div>
            
            <div class="sales-list" style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #e2e8f0 100%); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 2px solid rgba(102,126,234,0.1); max-height: 500px; overflow-y: auto;"
                <h2 style="color: #2d3748; margin-bottom: 25px; font-size: 1.5em; display: flex; align-items: center; gap: 10px;">
                    <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2em;">📋</span>
                    Ventas Recientes
                </h2>
                <div id="recent-sales">
                    <p style="text-align: center; color: #718096;">No hay ventas registradas aún</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Variables globales para la gestión de ventas
        let products = [];
        let sales = JSON.parse(localStorage.getItem('sales') || '[]');
        
        // Cargar productos desde la API
        async function loadProducts() {{
            try {{
                const response = await fetch('/api/productos');
                products = await response.json();
                populateProductSelect();
            }} catch (error) {{
                console.error('Error cargando productos:', error);
                // Productos de ejemplo si falla la API
                products = [
                    {{id: 1, nombre: "Manzana Orgánica", precio: 2.5}},
                    {{id: 2, nombre: "Tomate Cherry", precio: 3.0}},
                    {{id: 3, nombre: "Lechuga Hidropónica", precio: 1.8}}
                ];
                populateProductSelect();
            }}
        }}
        
        // Llenar el select de productos
        function populateProductSelect() {{
            const select = document.getElementById('product-select');
            select.innerHTML = '<option value="">Seleccionar producto...</option>';
            
            products.filter(p => p.disponible).forEach(product => {{
                const option = document.createElement('option');
                option.value = product.id;
                option.textContent = `${{product.nombre}} - $${{product.precio}}`;
                option.dataset.price = product.precio;
                select.appendChild(option);
            }});
        }}
        
        // Calcular total cuando cambia el producto o cantidad
        function calculateTotal() {{
            const select = document.getElementById('product-select');
            const quantity = document.getElementById('quantity').value;
            const totalDisplay = document.getElementById('total-display');
            
            if (select.value && quantity) {{
                const price = parseFloat(select.options[select.selectedIndex].dataset.price || 0);
                const total = price * quantity;
                totalDisplay.value = `$${{total.toFixed(2)}}`;
            }} else {{
                totalDisplay.value = '';
            }}
        }}
        
        // Registrar nueva venta
        function registerSale(event) {{
            event.preventDefault();
            
            const select = document.getElementById('product-select');
            const quantity = parseInt(document.getElementById('quantity').value);
            const customer = document.getElementById('customer').value;
            
            if (!select.value || !quantity || !customer) {{
                alert('Por favor completa todos los campos');
                return;
            }}
            
            const product = products.find(p => p.id == select.value);
            const total = product.precio * quantity;
            
            const sale = {{
                id: Date.now(),
                product: product.nombre,
                quantity: quantity,
                customer: customer,
                total: total,
                date: new Date().toLocaleString('es-ES')
            }};
            
            sales.unshift(sale);
            localStorage.setItem('sales', JSON.stringify(sales));
            
            // Limpiar formulario
            document.getElementById('sale-form').reset();
            document.getElementById('total-display').value = '';
            
            // Actualizar visualización
            renderSales();
            updateMetrics();
            
            alert('¡Venta registrada exitosamente!');
        }}
        
        // Mostrar ventas recientes
        function renderSales() {{
            const container = document.getElementById('recent-sales');
            
            if (sales.length === 0) {{
                container.innerHTML = '<p style="text-align: center; color: #718096;">No hay ventas registradas aún</p>';
                return;
            }}
            
            container.innerHTML = sales.slice(0, 10).map(sale => `
                <div class="sale-item">
                    <div class="sale-info">
                        <strong>${{sale.product}}</strong><br>
                        <small>Cliente: ${{sale.customer}} | Cant: ${{sale.quantity}} | ${{sale.date}}</small>
                    </div>
                    <div class="sale-amount">$${{sale.total.toFixed(2)}}</div>
                </div>
            `).join('');
        }}
        
        // Actualizar métricas
        function updateMetrics() {{
            const totalSales = sales.reduce((sum, sale) => sum + sale.total, 0);
            const today = new Date().toDateString();
            const dailySales = sales.filter(sale => new Date(sale.date).toDateString() === today)
                                  .reduce((sum, sale) => sum + sale.total, 0);
            const avgSale = sales.length > 0 ? totalSales / sales.length : 0;
            
            document.getElementById('total-sales').textContent = `$${{totalSales.toFixed(2)}}`;
            document.getElementById('daily-sales').textContent = `$${{dailySales.toFixed(2)}}`;
            document.getElementById('transactions-count').textContent = sales.length;
            document.getElementById('avg-sale').textContent = `$${{avgSale.toFixed(2)}}`;
        }}
        
        // Event listeners
        document.getElementById('product-select').addEventListener('change', calculateTotal);
        document.getElementById('quantity').addEventListener('input', calculateTotal);
        document.getElementById('sale-form').addEventListener('submit', registerSale);
        
        // Inicialización
        document.addEventListener('DOMContentLoaded', function() {{
            loadProducts();
            renderSales();
            updateMetrics();
        }});
    </script>
</body>
</html>"""

def get_login_html():
    """🔐 Página de login con JWT"""
    return """<!DOCTYPE html>
<html lang="es">
<head>
    <title>🔐 EcoMarket - Iniciar Sesión</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔐</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            max-width: 450px;
            width: 90%;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .login-header h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #2d3748;
        }
        
        .form-group input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn-login {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .btn-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn-login:disabled {
            background: linear-gradient(135deg, #cbd5e0 0%, #a0aec0 100%);
            cursor: not-allowed;
            transform: none;
        }
        
        .error-message, .success-message {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
            text-align: center;
        }
        
        .error-message {
            background: #fed7d7;
            color: #c53030;
        }
        
        .success-message {
            background: #c6f6d5;
            color: #22543d;
        }
        
        .test-users {
            margin-top: 30px;
            padding: 20px;
            background: #f7fafc;
            border-radius: 10px;
            border: 2px dashed #cbd5e0;
        }
        
        .test-users h3 {
            margin-top: 0;
            color: #2d3748;
            font-size: 1em;
            margin-bottom: 10px;
        }
        
        .test-users ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .test-users li {
            padding: 8px;
            margin: 5px 0;
            background: white;
            border-radius: 6px;
            font-size: 0.9em;
            color: #4a5568;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .test-users li:hover {
            background: #edf2f7;
        }
        
        .back-link {
            display: block;
            text-align: center;
            margin-top: 20px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>🔐 Iniciar Sesión</h1>
            <p style="color: #718096; margin: 0;">Accede al panel de administración</p>
        </div>
        
        <div id="error-message" class="error-message"></div>
        <div id="success-message" class="success-message"></div>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="email">📧 Correo Electrónico</label>
                <input type="email" id="email" name="email" required 
                       placeholder="usuario@ejemplo.com"
                       autocomplete="email">
            </div>
            
            <div class="form-group">
                <label for="password">🔑 Contraseña</label>
                <input type="password" id="password" name="password" required
                       placeholder="••••••••"
                       autocomplete="current-password">
            </div>
            
            <button type="submit" class="btn-login" id="loginBtn">
                🚀 Iniciar Sesión
            </button>
        </form>
        
        <div class="test-users">
            <h3>👥 Usuarios de Prueba:</h3>
            <ul>
                <li onclick="fillCredentials('admin')"><strong>Admin:</strong> admin@ecomarket.com / admin123</li>
                <li onclick="fillCredentials('vendedor')"><strong>Vendedor:</strong> vendedor@ecomarket.com / vendedor123</li>
                <li onclick="fillCredentials('cliente')"><strong>Cliente:</strong> cliente@ecomarket.com / cliente123</li>
            </ul>
            <p style="font-size: 0.85em; color: #718096; margin-top: 10px; text-align: center;">
                💡 Haz clic en un usuario para auto-completar
            </p>
        </div>
        
        <a href="/" class="back-link">← Volver al inicio</a>
    </div>

    <script>
        // Limpiar localStorage SOLO si el usuario actual es cliente
        const currentRole = localStorage.getItem('user_role');
        if (currentRole === 'cliente') {
            localStorage.clear();
        }
        
        // Mostrar mensaje si venía bloqueado
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('blocked') === 'cliente') {
            const errorMsg = document.getElementById('error-message');
            errorMsg.textContent = '⚠️ Los clientes no tienen acceso al panel de administración. Inicia sesión con admin o vendedor.';
            errorMsg.style.display = 'block';
        }
        
        // Auto-completar credenciales
        function fillCredentials(role) {
            const credentials = {
                'admin': { email: 'admin@ecomarket.com', password: 'admin123' },
                'vendedor': { email: 'vendedor@ecomarket.com', password: 'vendedor123' },
                'cliente': { email: 'cliente@ecomarket.com', password: 'cliente123' }
            };
            
            if (credentials[role]) {
                document.getElementById('email').value = credentials[role].email;
                document.getElementById('password').value = credentials[role].password;
            }
        }
        
        // Manejar envío del formulario
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const loginBtn = document.getElementById('loginBtn');
            const errorMsg = document.getElementById('error-message');
            const successMsg = document.getElementById('success-message');
            
            errorMsg.style.display = 'none';
            successMsg.style.display = 'none';
            
            loginBtn.disabled = true;
            loginBtn.textContent = '🔄 Iniciando sesión...';
            
            console.log('Intentando login con:', email);
            console.log('URL completa:', window.location.origin + '/api/auth/login');
            
            try {
                console.log('Haciendo fetch...');
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });
                
                console.log('Response status:', response.status);
                console.log('Response ok:', response.ok);
                
                const data = await response.json();
                console.log('Response data:', data);
                
                if (response.ok) {
                    // LIMPIAR PRIMERO cualquier dato previo
                    localStorage.clear();
                    
                    // LUEGO guardar los nuevos datos
                    localStorage.setItem('access_token', data.access_token);
                    localStorage.setItem('refresh_token', data.refresh_token);
                    localStorage.setItem('user_email', data.user.email);
                    localStorage.setItem('user_role', data.user.role);
                    
                    console.log('Datos guardados en localStorage:', {
                        email: data.user.email,
                        role: data.user.role,
                        token: data.access_token.substring(0, 20) + '...'
                    });
                    
                    successMsg.textContent = `✅ ¡Bienvenido ${data.user.email}!`;
                    successMsg.style.display = 'block';
                    
                    setTimeout(() => {
                        window.location.href = '/admin';
                    }, 1000);
                } else {
                    console.error('Login fallido:', data);
                    errorMsg.textContent = data.detail || '❌ Credenciales incorrectas';
                    errorMsg.style.display = 'block';
                    
                    loginBtn.disabled = false;
                    loginBtn.textContent = '🚀 Iniciar Sesión';
                }
            } catch (error) {
                console.error('Error completo:', error);
                console.error('Tipo de error:', error.name);
                console.error('Mensaje:', error.message);
                console.error('Stack:', error.stack);
                errorMsg.textContent = `❌ Error de conexión: ${error.message}. Verifica que la API esté funcionando en http://127.0.0.1:8001`;
                errorMsg.style.display = 'block';
                
                loginBtn.disabled = false;
                loginBtn.textContent = '🚀 Iniciar Sesión';
            }
        });
    </script>
</body>
</html>"""