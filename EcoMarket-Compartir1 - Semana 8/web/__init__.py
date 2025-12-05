"""
🌱 EcoMarket API - Web Module
Módulo con interfaces web y estilos separados
"""

from .templates import get_homepage_html, get_dashboard_html, get_catalog_html, get_admin_html, get_sales_html, get_docs_css
from .styles import BASE_CSS, DASHBOARD_CSS, CATALOG_CSS, DOCS_CSS

__all__ = [
    'get_homepage_html',
    'get_dashboard_html', 
    'get_catalog_html',
    'get_admin_html',
    'get_sales_html',
    'get_docs_css',
    'BASE_CSS',
    'DASHBOARD_CSS',
    'CATALOG_CSS',
    'DOCS_CSS'
]