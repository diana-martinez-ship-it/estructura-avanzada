"""
Script para generar certificados SSL autofirmados para desarrollo local
Usa cryptography (pura Python) en lugar de openssl
"""
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta, timezone
import os

def generar_certificados():
    """Genera certificado y llave privada autofirmados"""
    
    # Crear directorio certs si no existe
    os.makedirs("certs", exist_ok=True)
    
    print("🔑 Generando par de llaves RSA (4096 bits)...")
    # Generar llave privada RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    
    print("📜 Creando certificado autofirmado...")
    # Crear certificado autofirmado
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "MX"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Estado"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Ciudad"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "EcoMarket Dev"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc)
    ).not_valid_after(
        # Válido por 365 días
        datetime.now(timezone.utc) + timedelta(days=365)
    ).add_extension(
        # Nombres alternativos del sujeto (para localhost y 127.0.0.1)
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.DNSName("ecomarket.local"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    print("💾 Guardando certificados en carpeta certs/...")
    # Guardar llave privada
    with open("certs/key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Guardar certificado
    with open("certs/cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print("✅ Certificados generados exitosamente:")
    print("   📄 certs/cert.pem - Certificado público")
    print("   🔐 certs/key.pem  - Llave privada")
    print("")
    print("⚠️  IMPORTANTE:")
    print("   - Estos certificados son SOLO para desarrollo local")
    print("   - NO usarlos en producción")
    print("   - Los navegadores mostrarán advertencia de seguridad (es normal)")
    print("   - Válidos por 365 días desde hoy")
    print("")
    print("🚀 Ahora puedes ejecutar el servidor con HTTPS:")
    print("   python main.py")

if __name__ == "__main__":
    import ipaddress
    generar_certificados()
