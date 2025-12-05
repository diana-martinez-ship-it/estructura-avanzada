"""
Fuzzing Test Suite - Ejercicio 3: Validación Determinista
==========================================================

10 casos de prueba con entradas problemáticas para detectar 
vulnerabilidades en la validación.
"""

import json
from typing import Dict, Any, List
from validators import ProductValidator


class FuzzingTestCase:
    """Caso de prueba de fuzzing"""
    def __init__(self, name: str, description: str, input_data: Dict[str, Any], expected_result: str):
        self.name = name
        self.description = description
        self.input_data = input_data
        self.expected_result = expected_result


# ============== 10 CASOS DE FUZZING ==============

FUZZING_CASES = [
    FuzzingTestCase(
        name="FUZZ_1_SQL_INJECTION",
        description="Intento de inyección SQL en nombre",
        input_data={
            "name": "Product'; DROP TABLE products;--",
            "price": 100,
            "currency": "USD"
        },
        expected_result="REJECTED - Caracteres peligrosos en name (';--)"
    ),
    
    FuzzingTestCase(
        name="FUZZ_2_XSS_SCRIPT",
        description="Intento de XSS con <script>",
        input_data={
            "name": "<script>alert('XSS')</script>",
            "price": 100,
            "currency": "USD"
        },
        expected_result="REJECTED - Caracteres HTML no permitidos en name"
    ),
    
    FuzzingTestCase(
        name="FUZZ_3_UNICODE_OVERFLOW",
        description="Caracteres Unicode especiales (emoji, CJK)",
        input_data={
            "name": "Producto 日本語 🎉🎊 مرحبا",
            "price": 100,
            "currency": "USD"
        },
        expected_result="REJECTED - Solo alfanuméricos + puntuación básica permitidos"
    ),
    
    FuzzingTestCase(
        name="FUZZ_4_PRICE_PRECISION",
        description="Precio con más de 2 decimales",
        input_data={
            "name": "Product",
            "price": 99.999999999,
            "currency": "USD"
        },
        expected_result="ACCEPTED - Se redondea a 100.00 (2 decimales)"
    ),
    
    FuzzingTestCase(
        name="FUZZ_5_FLOAT_INFINITY",
        description="Valores especiales de float (Infinity, NaN)",
        input_data={
            "name": "Product",
            "price": float('inf'),
            "currency": "USD"
        },
        expected_result="REJECTED - Valor fuera de rango (> 999999999.99)"
    ),
    
    FuzzingTestCase(
        name="FUZZ_6_NULL_BYTE",
        description="Null byte en string (truncation attack)",
        input_data={
            "name": "Product\x00Hidden",
            "price": 100,
            "currency": "USD"
        },
        expected_result="ACCEPTED - Null byte eliminado por sanitización (result: 'ProductHidden')"
    ),
    
    FuzzingTestCase(
        name="FUZZ_7_MASSIVE_ARRAY",
        description="Array de tags muy grande (DoS)",
        input_data={
            "name": "Product",
            "price": 100,
            "currency": "USD",
            "tags": [f"tag{i}" for i in range(1000)]
        },
        expected_result="REJECTED - Máximo 10 tags, recibido 1000"
    ),
    
    FuzzingTestCase(
        name="FUZZ_8_DEEPLY_NESTED",
        description="Objeto profundamente anidado (stack overflow)",
        input_data={
            "name": "Product",
            "price": 100,
            "currency": "USD",
            "tags": [
                {"nested": {"very": {"deep": {"object": "value"}}}}
            ]
        },
        expected_result="REJECTED - tags[0]: Se esperaba string, recibido dict"
    ),
    
    FuzzingTestCase(
        name="FUZZ_9_REGEX_DOS",
        description="String que causa ReDoS (catastrophic backtracking)",
        input_data={
            "name": "A" * 100000,  # 100k caracteres
            "price": 100,
            "currency": "USD"
        },
        expected_result="REJECTED - name: Máximo 80 caracteres, recibido 100000"
    ),
    
    FuzzingTestCase(
        name="FUZZ_10_TYPE_JUGGLING",
        description="Type juggling: bool/null en campos numéricos",
        input_data={
            "name": "Product",
            "price": True,  # bool en vez de number
            "currency": "USD"
        },
        expected_result="ACCEPTED - Python convierte True → 1.0 (válido)"
    ),
]


# ============== EJECUTOR DE FUZZING ==============

def run_fuzzing_suite():
    """Ejecutar todos los casos de fuzzing"""
    print("="*80)
    print(" FUZZING TEST SUITE - Validación Determinista")
    print("="*80)
    
    results = {
        "passed": 0,
        "failed": 0,
        "unexpected": 0
    }
    
    for i, test_case in enumerate(FUZZING_CASES, 1):
        print(f"\n[{i}/10] {test_case.name}")
        print(f"📝 {test_case.description}")
        print(f"Input: {json.dumps(test_case.input_data, indent=2, default=str)}")
        print(f"Esperado: {test_case.expected_result}")
        
        try:
            validated = ProductValidator.validate_create_request(test_case.input_data)
            result = f"ACCEPTED - Datos validados: {json.dumps(validated, default=str)}"
            
            if "ACCEPTED" in test_case.expected_result:
                print(f"✅ {result}")
                results["passed"] += 1
            else:
                print(f"⚠️ INESPERADO: {result}")
                print(f"   Se esperaba rechazo: {test_case.expected_result}")
                results["unexpected"] += 1
                
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'details'):
                error_msg = f"REJECTED - {e.details[0]['field']}: {e.details[0]['issue']}"
                if 'received' in e.details[0]:
                    error_msg += f" (received: {e.details[0]['received']})"
            
            if "REJECTED" in test_case.expected_result:
                print(f"✅ {error_msg}")
                results["passed"] += 1
            else:
                print(f"❌ FALLÓ: {error_msg}")
                print(f"   Se esperaba aceptación: {test_case.expected_result}")
                results["failed"] += 1
    
    # Resumen
    print("\n" + "="*80)
    print(" RESUMEN DE FUZZING")
    print("="*80)
    print(f"✅ Pasados: {results['passed']}/10")
    print(f"❌ Fallados: {results['failed']}/10")
    print(f"⚠️ Inesperados: {results['unexpected']}/10")
    print("="*80)
    
    return results


# ============== CASOS ADICIONALES: PAYLOAD GRANDES ==============

def test_payload_size_limits():
    """Probar límites de tamaño de payload"""
    print("\n" + "="*80)
    print(" TEST: LÍMITES DE TAMAÑO DE PAYLOAD")
    print("="*80)
    
    # Test 1: Nombre muy largo (>80 chars)
    print("\n1. Nombre de 1000 caracteres")
    try:
        ProductValidator.validate_name("A" * 1000)
        print("❌ FALLÓ: Debería rechazar nombres > 80 chars")
    except Exception as e:
        print(f"✅ Rechazado correctamente: {e}")
    
    # Test 2: Precio con muchos decimales
    print("\n2. Precio con 10 decimales")
    try:
        validated_price = ProductValidator.validate_price(99.9999999999)
        print(f"✅ Redondeado a: {validated_price}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Tags con strings muy largos
    print("\n3. Tag de 100 caracteres")
    try:
        ProductValidator.validate_tags(["a" * 100])
        print("❌ FALLÓ: Debería rechazar tags > 30 chars")
    except Exception as e:
        print(f"✅ Rechazado correctamente: {e}")
    
    # Test 4: Payload completo de ~1MB
    print("\n4. Payload de ~1MB (muchos tags largos)")
    huge_tags = ["tag" + str(i) for i in range(10000)]
    payload = {
        "name": "Product",
        "price": 100,
        "currency": "USD",
        "tags": huge_tags
    }
    payload_size = len(json.dumps(payload))
    print(f"   Tamaño del payload: {payload_size:,} bytes (~{payload_size/1024/1024:.2f} MB)")
    
    try:
        ProductValidator.validate_create_request(payload)
        print("❌ FALLÓ: Debería rechazar payloads grandes")
    except Exception as e:
        print(f"✅ Rechazado correctamente: {e}")


# ============== CASOS ADICIONALES: CARACTERES ESPECIALES ==============

def test_special_characters():
    """Probar manejo de caracteres especiales"""
    print("\n" + "="*80)
    print(" TEST: CARACTERES ESPECIALES")
    print("="*80)
    
    test_cases = [
        ("Espacios múltiples", "Product    Name", "Product Name"),
        ("Tabs y newlines", "Product\t\nName", "Product Name"),
        ("Espacios inicio/fin", "  Product Name  ", "Product Name"),
        ("Puntuación permitida", "Product (2025)", "Product (2025)"),
        ("Guiones y guiones bajos", "Product-Name_v2", "Product-Name_v2"),
    ]
    
    for i, (desc, input_str, expected) in enumerate(test_cases, 1):
        print(f"\n{i}. {desc}")
        print(f"   Input: {repr(input_str)}")
        try:
            result = ProductValidator.validate_name(input_str)
            if result == expected:
                print(f"   ✅ Sanitizado correctamente: {repr(result)}")
            else:
                print(f"   ⚠️ Resultado: {repr(result)} (esperado: {repr(expected)})")
        except Exception as e:
            print(f"   ❌ Error: {e}")


# ============== CASOS ADICIONALES: BOUNDARY VALUES ==============

def test_boundary_values():
    """Probar valores en los límites exactos"""
    print("\n" + "="*80)
    print(" TEST: BOUNDARY VALUES")
    print("="*80)
    
    boundaries = [
        ("Nombre 2 chars (mínimo)", {"name": "AB", "price": 100, "currency": "USD"}, True),
        ("Nombre 1 char (< mínimo)", {"name": "A", "price": 100, "currency": "USD"}, False),
        ("Nombre 80 chars (máximo)", {"name": "A" * 80, "price": 100, "currency": "USD"}, True),
        ("Nombre 81 chars (> máximo)", {"name": "A" * 81, "price": 100, "currency": "USD"}, False),
        ("Precio 0 (mínimo)", {"name": "Product", "price": 0, "currency": "USD"}, True),
        ("Precio -0.01 (< mínimo)", {"name": "Product", "price": -0.01, "currency": "USD"}, False),
        ("10 tags (máximo)", {"name": "Product", "price": 100, "currency": "USD", "tags": [f"tag{i}" for i in range(10)]}, True),
        ("11 tags (> máximo)", {"name": "Product", "price": 100, "currency": "USD", "tags": [f"tag{i}" for i in range(11)]}, False),
    ]
    
    for i, (desc, input_data, should_pass) in enumerate(boundaries, 1):
        print(f"\n{i}. {desc}")
        try:
            validated = ProductValidator.validate_create_request(input_data)
            if should_pass:
                print(f"   ✅ Aceptado correctamente")
            else:
                print(f"   ⚠️ INESPERADO: Debería ser rechazado")
        except Exception as e:
            if not should_pass:
                print(f"   ✅ Rechazado correctamente")
            else:
                print(f"   ❌ INESPERADO: Debería ser aceptado. Error: {e}")


# ============== MAIN ==============

if __name__ == "__main__":
    # Ejecutar suite principal de fuzzing
    results = run_fuzzing_suite()
    
    # Tests adicionales
    test_payload_size_limits()
    test_special_characters()
    test_boundary_values()
    
    print("\n" + "="*80)
    print(" FUZZING COMPLETO")
    print("="*80)
    print("\n💡 Recomendaciones:")
    print("  1. Implementar límite de tamaño de payload (ej: 1MB)")
    print("  2. Timeout en validación de regex (prevenir ReDoS)")
    print("  3. Sanitización agresiva de HTML/SQL en strings")
    print("  4. Rate limiting en endpoints de creación")
    print("  5. Logging de intentos de fuzzing/ataques")
    print("="*80 + "\n")
