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
            <a href="/stats-dashboard" class="btn">📊 Dashboard</a>
            <a href="/products-catalog" class="btn">🛍️ Catálogo</a>
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
            <a href="/products-catalog" class="btn">🛍️ Catálogo</a>
                <a href="/ventas" class="btn">💸 Ventas</a>
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
                <a href="/ventas" class="btn">💸 Ventas</a>
        </div>
        
        <div class="search-section">
            <h3>🔍 Buscar Productos</h3>
            <input type="text" class="search-input" id="searchInput" 
                   placeholder="Buscar por nombre, categoría o descripción...">
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
            
            // Confirmar compra
            const total = (precio * cantidad).toFixed(2);
            if (!confirm(`¿Confirmar compra de ${{cantidad}} unidad(es) por $$${{total}}?`)) {{
                return;
            }}
            
            // Realizar petición al endpoint de compra
            fetch(`/api/productos/${{productId}}/comprar?cantidad=${{cantidad}}`, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }}
            }})
            .then(response => {{
                if (!response.ok) {{
                    return response.json().then(err => {{
                        throw new Error(err.detail || 'Error en la compra');
                    }});
                }}
                return response.json();
            }})
            .then(data => {{
                // Mostrar mensaje de éxito
                alert(`✅ ${{data.mensaje}}\\n\\n💰 Total pagado: $$${{data.total_pagado}}\\n📦 Stock restante: ${{data.stock_restante}} unidades`);
                
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
    </script>
</body>
</html>"""

def get_admin_html():
    """🔧 Panel de administración para gestionar productos (CRUD completo)"""
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
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Panel de Administración</h1>
        
        <div class="nav-buttons">
            <a href="/" class="btn">🏠 Inicio</a>
            <a href="/catalog" class="btn">🛍️ Catálogo</a>
            <a href="/docs" class="btn">📚 API Docs</a>
            <a href="/dashboard" class="btn">📊 Dashboard</a>
            <a href="/ventas" class="btn">💸 Ventas</a>
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
                            <button onclick="eliminarProducto(${{product.id}}, '${{product.nombre}}')" class="btn-danger">🗑️ Eliminar</button>
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
        
        // Crear producto
        function crearProducto(data) {{
            fetch('/api/productos', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(data)
            }})
            .then(response => response.json())
            .then(newProduct => {{
                alert(`✅ Producto "${{newProduct.nombre}}" creado exitosamente`);
                document.getElementById('productForm').reset();
                loadProducts();
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
        
        // Actualizar producto
        function actualizarProducto(id, data) {{
            fetch(`/api/productos/${{id}}`, {{
                method: 'PUT',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(data)
            }})
            .then(response => response.json())
            .then(updatedProduct => {{
                alert(`✅ Producto "${{updatedProduct.nombre}}" actualizado exitosamente`);
                cancelarEdicion();
                loadProducts();
            }})
            .catch(error => {{
                alert(`❌ Error: ${{error.message}}`);
            }});
        }}
        
        // Eliminar producto
        function eliminarProducto(id, nombre) {{
            if (!confirm(`¿Estás seguro de eliminar "${{nombre}}"?`)) {{
                return;
            }}
            
            fetch(`/api/productos/${{id}}`, {{
                method: 'DELETE'
            }})
            .then(response => response.json())
            .then(data => {{
                alert(`✅ ${{data.mensaje}}`);
                loadProducts();
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
        
        // Cargar productos al inicio
        loadProducts();
    </script>
</body>
</html>"""

def get_docs_css():
    """CSS personalizado para la documentación"""
    return DOCS_CSS


def get_sales_html():
    """💸 Página simple para ventas"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <title>💸 EcoMarket API - Ventas</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💸</text></svg>'>
    <style>{BASE_CSS}</style>
</head>
<body>
    <div class="container">
        <h1>💸 Ventas</h1>
        <p>Bienvenido a la sección de ventas de EcoMarket API. Aquí podrás revisar reportes y ventas recientes.</p>
        <div style="margin-top:20px;"><a href="/" class="btn">🏠 Volver al inicio</a></div>
    </div>
</body>
</html>"""