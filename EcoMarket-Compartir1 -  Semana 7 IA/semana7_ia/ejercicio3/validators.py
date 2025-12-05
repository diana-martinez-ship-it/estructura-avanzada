"""
Validadores Deterministas para Product API
==========================================

Implementación de validadores con:
- Orden de propiedades consistente
- Sin valores null en salida
- Mensajes de error estandarizados
- Sanitización de entrada
"""

from typing import Any, Dict, List, Optional, Tuple
import re
from datetime import datetime
from uuid import UUID
import json


class ValidationError(Exception):
    """Error de validación con detalles estructurados"""
    def __init__(self, field: str, issue: str, received: Any = None):
        self.field = field
        self.issue = issue
        self.received = received
        super().__init__(f"{field}: {issue}")


class ProductValidator:
    """Validador principal con orden de campos determinista"""
    
    # Orden fijo de propiedades en serialización
    PROPERTY_ORDER = ["id", "name", "price", "currency", "tags", "createdAt"]
    
    # Reglas de validación
    RULES = {
        "name": {
            "minLength": 2,
            "maxLength": 80,
            "pattern": r"^[\p{L}\p{N}\s\-_.,()]+$",  # Alfanumérico + puntuación básica
        },
        "price": {
            "minimum": 0,
            "maximum": 999999999.99,
            "decimals": 2,
        },
        "currency": {
            "enum": ["MXN", "USD", "EUR"],
        },
        "tags": {
            "minItems": 0,
            "maxItems": 10,
            "uniqueItems": True,
            "itemPattern": r"^[a-z0-9-]+$",
            "itemMinLength": 1,
            "itemMaxLength": 30,
        },
        "createdAt": {
            "format": "iso8601",
            "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$",
        },
    }
    
    @classmethod
    def validate_id(cls, value: Any) -> UUID:
        """Validar UUID v4"""
        if not value:
            raise ValidationError("id", "Campo requerido no proporcionado")
        
        if not isinstance(value, (str, UUID)):
            raise ValidationError("id", f"Se esperaba string o UUID, recibido {type(value).__name__}", value)
        
        try:
            uuid_obj = UUID(str(value), version=4)
            return uuid_obj
        except ValueError as e:
            raise ValidationError("id", f"UUID inválido: {e}", value)
    
    @classmethod
    def validate_name(cls, value: Any) -> str:
        """Validar nombre"""
        if value is None:
            raise ValidationError("name", "Campo requerido no proporcionado")
        
        if not isinstance(value, str):
            raise ValidationError("name", f"Se esperaba string, recibido {type(value).__name__}", value)
        
        # Sanitizar: eliminar espacios extras y caracteres peligrosos
        sanitized = cls._sanitize_string(value)
        
        rules = cls.RULES["name"]
        
        if len(sanitized) < rules["minLength"]:
            raise ValidationError(
                "name",
                f"Mínimo {rules['minLength']} caracteres, recibido {len(sanitized)}",
                sanitized
            )
        
        if len(sanitized) > rules["maxLength"]:
            raise ValidationError(
                "name",
                f"Máximo {rules['maxLength']} caracteres, recibido {len(sanitized)}",
                sanitized
            )
        
        # Validar patrón (simplificado para Python)
        if not re.match(r"^[a-zA-Z0-9\s\-_.,()]+$", sanitized):
            raise ValidationError(
                "name",
                "Solo se permiten letras, números, espacios y puntuación básica (-_.,())",
                sanitized
            )
        
        return sanitized
    
    @classmethod
    def validate_price(cls, value: Any) -> float:
        """Validar precio"""
        if value is None:
            raise ValidationError("price", "Campo requerido no proporcionado")
        
        if not isinstance(value, (int, float)):
            raise ValidationError("price", f"Se esperaba number, recibido {type(value).__name__}", value)
        
        rules = cls.RULES["price"]
        
        if value < rules["minimum"]:
            raise ValidationError("price", f"Debe ser >= {rules['minimum']}", value)
        
        if value > rules["maximum"]:
            raise ValidationError("price", f"Debe ser <= {rules['maximum']}", value)
        
        # Redondear a 2 decimales
        rounded = round(float(value), rules["decimals"])
        return rounded
    
    @classmethod
    def validate_currency(cls, value: Any) -> str:
        """Validar código de moneda"""
        if value is None:
            raise ValidationError("currency", "Campo requerido no proporcionado")
        
        if not isinstance(value, str):
            raise ValidationError("currency", f"Se esperaba string, recibido {type(value).__name__}", value)
        
        value_upper = value.upper().strip()
        rules = cls.RULES["currency"]
        
        if value_upper not in rules["enum"]:
            raise ValidationError(
                "currency",
                f"Debe ser uno de: {', '.join(rules['enum'])}",
                value
            )
        
        return value_upper
    
    @classmethod
    def validate_tags(cls, value: Any) -> List[str]:
        """Validar array de tags"""
        if value is None:
            return []  # Tags es opcional
        
        if not isinstance(value, list):
            raise ValidationError("tags", f"Se esperaba array, recibido {type(value).__name__}", value)
        
        rules = cls.RULES["tags"]
        
        if len(value) < rules["minItems"]:
            raise ValidationError("tags", f"Mínimo {rules['minItems']} elementos", len(value))
        
        if len(value) > rules["maxItems"]:
            raise ValidationError("tags", f"Máximo {rules['maxItems']} elementos, recibido {len(value)}", len(value))
        
        # Verificar unicidad
        if rules["uniqueItems"] and len(value) != len(set(value)):
            raise ValidationError("tags", "Todos los elementos deben ser únicos", value)
        
        # Validar cada tag
        validated_tags = []
        for i, tag in enumerate(value):
            if not isinstance(tag, str):
                raise ValidationError(f"tags[{i}]", f"Se esperaba string, recibido {type(tag).__name__}", tag)
            
            tag = tag.strip()
            
            if len(tag) < rules["itemMinLength"]:
                raise ValidationError(f"tags[{i}]", f"Mínimo {rules['itemMinLength']} caracteres", tag)
            
            if len(tag) > rules["itemMaxLength"]:
                raise ValidationError(f"tags[{i}]", f"Máximo {rules['itemMaxLength']} caracteres", tag)
            
            if not re.match(rules["itemPattern"], tag):
                raise ValidationError(
                    f"tags[{i}]",
                    "Solo se permiten minúsculas y guiones (a-z0-9-)",
                    tag
                )
            
            validated_tags.append(tag)
        
        return validated_tags
    
    @classmethod
    def validate_created_at(cls, value: Any) -> str:
        """Validar timestamp ISO-8601"""
        if value is None:
            raise ValidationError("createdAt", "Campo requerido no proporcionado")
        
        if not isinstance(value, str):
            raise ValidationError("createdAt", f"Se esperaba string, recibido {type(value).__name__}", value)
        
        rules = cls.RULES["createdAt"]
        
        # Verificar patrón
        if not re.match(rules["pattern"], value):
            raise ValidationError(
                "createdAt",
                "Debe estar en formato ISO-8601: YYYY-MM-DDTHH:mm:ss.sssZ",
                value
            )
        
        # Verificar que sea parseable
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as e:
            raise ValidationError("createdAt", f"Fecha inválida: {e}", value)
        
        return value
    
    @classmethod
    def _sanitize_string(cls, value: str) -> str:
        """Sanitizar string: eliminar espacios extras y caracteres peligrosos"""
        # Eliminar espacios al inicio/fin
        sanitized = value.strip()
        
        # Colapsar múltiples espacios en uno
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        # Eliminar caracteres de control (excepto espacios)
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char == '\n')
        
        return sanitized
    
    @classmethod
    def validate_create_request(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar request de creación"""
        errors = []
        
        # Verificar campos requeridos
        required = ["name", "price", "currency"]
        for field in required:
            if field not in data:
                errors.append(ValidationError(field, "Campo requerido no proporcionado"))
        
        if errors:
            raise cls._create_validation_exception(errors)
        
        # Validar cada campo
        validated = {}
        
        try:
            validated["name"] = cls.validate_name(data.get("name"))
        except ValidationError as e:
            errors.append(e)
        
        try:
            validated["price"] = cls.validate_price(data.get("price"))
        except ValidationError as e:
            errors.append(e)
        
        try:
            validated["currency"] = cls.validate_currency(data.get("currency"))
        except ValidationError as e:
            errors.append(e)
        
        try:
            validated["tags"] = cls.validate_tags(data.get("tags"))
        except ValidationError as e:
            errors.append(e)
        
        if errors:
            raise cls._create_validation_exception(errors)
        
        return validated
    
    @classmethod
    def validate_update_request(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar request de actualización"""
        if not data or not any(key in data for key in ["name", "price", "currency", "tags"]):
            raise cls._create_validation_exception([
                ValidationError("body", "Debe proporcionar al menos un campo para actualizar")
            ])
        
        errors = []
        validated = {}
        
        if "name" in data:
            try:
                validated["name"] = cls.validate_name(data["name"])
            except ValidationError as e:
                errors.append(e)
        
        if "price" in data:
            try:
                validated["price"] = cls.validate_price(data["price"])
            except ValidationError as e:
                errors.append(e)
        
        if "currency" in data:
            try:
                validated["currency"] = cls.validate_currency(data["currency"])
            except ValidationError as e:
                errors.append(e)
        
        if "tags" in data:
            try:
                validated["tags"] = cls.validate_tags(data["tags"])
            except ValidationError as e:
                errors.append(e)
        
        if errors:
            raise cls._create_validation_exception(errors)
        
        return validated
    
    @classmethod
    def serialize_product(cls, product: Dict[str, Any]) -> Dict[str, Any]:
        """Serializar producto con orden determinista"""
        # Orden fijo de propiedades
        ordered = {}
        for prop in cls.PROPERTY_ORDER:
            if prop in product:
                value = product[prop]
                # No incluir valores null
                if value is not None:
                    ordered[prop] = value
        
        return ordered
    
    @classmethod
    def _create_validation_exception(cls, errors: List[ValidationError]) -> Exception:
        """Crear excepción con múltiples errores"""
        details = [
            {
                "field": e.field,
                "issue": e.issue,
                **{"received": e.received} if e.received is not None else {}
            }
            for e in errors
        ]
        
        exc = Exception("Validation failed")
        exc.code = "VALIDATION_ERROR"
        exc.details = details
        return exc


# ============== TABLA DE ERRORES ==============

ERROR_MESSAGES = {
    "MISSING_REQUIRED": {
        "code": "VALIDATION_ERROR",
        "msgTemplate": "Campo requerido no proporcionado: {field}",
        "example": {
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "msg": "Campos requeridos faltantes",
                "details": [
                    {"field": "name", "issue": "Campo requerido no proporcionado"}
                ]
            }
        }
    },
    
    "INVALID_TYPE": {
        "code": "VALIDATION_ERROR",
        "msgTemplate": "Tipo de dato inválido en {field}: esperado {expected}, recibido {received}",
        "example": {
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "msg": "Tipo de dato inválido",
                "details": [
                    {"field": "price", "issue": "Se esperaba number, recibido string", "received": "not-a-number"}
                ]
            }
        }
    },
    
    "OUT_OF_RANGE": {
        "code": "VALIDATION_ERROR",
        "msgTemplate": "Valor fuera de rango en {field}: {constraint}",
        "example": {
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "msg": "Violación de restricción",
                "details": [
                    {"field": "price", "issue": "Debe ser >= 0", "received": -10.50}
                ]
            }
        }
    },
    
    "INVALID_LENGTH": {
        "code": "VALIDATION_ERROR",
        "msgTemplate": "Longitud inválida en {field}: {constraint}",
        "example": {
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "msg": "Longitud inválida",
                "details": [
                    {"field": "name", "issue": "Mínimo 2 caracteres, recibido 1", "received": "A"}
                ]
            }
        }
    },
    
    "INVALID_ENUM": {
        "code": "VALIDATION_ERROR",
        "msgTemplate": "Valor no permitido en {field}: debe ser uno de {allowed}",
        "example": {
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "msg": "Valor no permitido",
                "details": [
                    {"field": "currency", "issue": "Debe ser uno de: MXN, USD, EUR", "received": "JPY"}
                ]
            }
        }
    },
    
    "INVALID_FORMAT": {
        "code": "VALIDATION_ERROR",
        "msgTemplate": "Formato inválido en {field}: {constraint}",
        "example": {
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "msg": "Formato inválido",
                "details": [
                    {"field": "createdAt", "issue": "Debe estar en formato ISO-8601: YYYY-MM-DDTHH:mm:ss.sssZ", "received": "2025-11-26 10:30:00"}
                ]
            }
        }
    },
    
    "DUPLICATE_VALUES": {
        "code": "VALIDATION_ERROR",
        "msgTemplate": "Valores duplicados en {field}: todos los elementos deben ser únicos",
        "example": {
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "msg": "Elementos duplicados no permitidos",
                "details": [
                    {"field": "tags", "issue": "Todos los elementos deben ser únicos", "received": ["electronics", "sale", "electronics"]}
                ]
            }
        }
    },
    
    "ADDITIONAL_PROPERTIES": {
        "code": "VALIDATION_ERROR",
        "msgTemplate": "Propiedades adicionales no permitidas: {fields}",
        "example": {
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "msg": "Propiedades adicionales no permitidas",
                "details": [
                    {"field": "extraField", "issue": "Propiedad no definida en el schema"}
                ]
            }
        }
    },
}


if __name__ == "__main__":
    print("="*70)
    print("DEMO: Validadores Deterministas")
    print("="*70)
    
    # Caso 1: Validación exitosa
    print("\n✅ Caso 1: Validación exitosa")
    valid_data = {
        "name": "Laptop ThinkPad X1",
        "price": 1299.99,
        "currency": "usd",  # Se normalizará a USD
        "tags": ["electronics", "computers", "lenovo"]
    }
    try:
        validated = ProductValidator.validate_create_request(valid_data)
        print(f"Datos validados: {json.dumps(validated, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Caso 2: Precio negativo
    print("\n❌ Caso 2: Precio negativo")
    invalid_data = {
        "name": "Product",
        "price": -10.50,
        "currency": "MXN"
    }
    try:
        ProductValidator.validate_create_request(invalid_data)
    except Exception as e:
        print(f"Error capturado: {e}")
        print(f"Detalles: {json.dumps(e.details, indent=2)}")
    
    # Caso 3: Tags duplicados
    print("\n❌ Caso 3: Tags duplicados")
    invalid_data = {
        "name": "Product",
        "price": 100,
        "currency": "USD",
        "tags": ["electronics", "sale", "electronics"]
    }
    try:
        ProductValidator.validate_create_request(invalid_data)
    except Exception as e:
        print(f"Error capturado: {e}")
        print(f"Detalles: {json.dumps(e.details, indent=2)}")
    
    print("\n" + "="*70)
