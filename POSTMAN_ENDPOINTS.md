# 📮 Endpoints Sivoter - Mesas de Votación

## Base URL
```
http://localhost:8000
```

---

## 📋 CRUD Mesas de Votación

### 1️⃣ CREAR MESA DE VOTACIÓN
**POST** `/mesas-votacion`

```json
{
  "nombre": "Colegio INEM",
  "direccion": "Calle 50 # 48-50",
  "barrio_id": 1
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "nombre": "Colegio INEM",
  "direccion": "Calle 50 # 48-50",
  "barrio_id": 1,
  "created_at": "2026-03-29T10:30:00",
  "updated_at": "2026-03-29T10:30:00"
}
```

---

### 2️⃣ LISTAR TODAS LAS MESAS
**GET** `/mesas-votacion?skip=0&limit=100`

**Parámetros:**
- `skip`: número de registros a saltar (default: 0)
- `limit`: máximo de registros a retornar (default: 100)

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "nombre": "Colegio INEM",
    "direccion": "Calle 50 # 48-50",
    "barrio_id": 1,
    "created_at": "2026-03-29T10:30:00",
    "updated_at": "2026-03-29T10:30:00"
  },
  {
    "id": 2,
    "nombre": "Institución Educativa San Alonso",
    "direccion": "Carrera 48 # 48-50",
    "barrio_id": 2,
    "created_at": "2026-03-29T10:32:00",
    "updated_at": "2026-03-29T10:32:00"
  }
]
```

---

### 3️⃣ OBTENER MESA POR ID
**GET** `/mesas-votacion/{mesa_id}`

**Ejemplo:** `/mesas-votacion/1`

**Respuesta (200):**
```json
{
  "id": 1,
  "nombre": "Colegio INEM",
  "direccion": "Calle 50 # 48-50",
  "barrio_id": 1,
  "created_at": "2026-03-29T10:30:00",
  "updated_at": "2026-03-29T10:30:00"
}
```

**Respuesta si no existe (404):**
```json
{
  "detail": "Mesa de votación con ID 999 no encontrada."
}
```

---

### 4️⃣ ACTUALIZAR MESA
**PUT** `/mesas-votacion/{mesa_id}`

**Ejemplo:** `/mesas-votacion/1`

```json
{
  "nombre": "Colegio INEM - Medellín",
  "direccion": "Calle 50 # 48-50, Piso 2",
  "barrio_id": 1
}
```

**Respuesta (200):**
```json
{
  "id": 1,
  "nombre": "Colegio INEM - Medellín",
  "direccion": "Calle 50 # 48-50, Piso 2",
  "barrio_id": 1,
  "created_at": "2026-03-29T10:30:00",
  "updated_at": "2026-03-29T14:45:00"
}
```

---

### 5️⃣ ELIMINAR MESA
**DELETE** `/mesas-votacion/{mesa_id}`

**Ejemplo:** `/mesas-votacion/1`

**Respuesta (204 No Content)** - Sin body

---

## ⚙️ Códigos de Respuesta

| Código | Significado |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 204 | No Content - Eliminado exitosamente |
| 400 | Bad Request - Datos inválidos o FK no existe |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error |

---

## 📝 Validaciones

### Campos Requeridos:
- `nombre`: string (1-150 caracteres) - **OBLIGATORIO**
- `barrio_id`: integer - **OBLIGATORIO**

### Campos Opcionales:
- `direccion`: string (máx 200 caracteres) - opcional

### Errores Comunes:

**Barrio no existe:**
```json
{
  "detail": "El valor 999 de 'barrio_id' no existe en 'barrios'."
}
```

**Campo requerido faltante:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "barrio_id"],
      "msg": "Field required"
    }
  ]
}
```

---

## 🧪 Ejemplos de Prueba

### Crear 3 mesas de ejemplo
```bash
# Mesa 1 - Colegio INEM, El Poblado
POST /mesas-votacion
{
  "nombre": "Colegio INEM",
  "direccion": "Calle 50 # 48-50",
  "barrio_id": 1
}

# Mesa 2 - Otro lugar en El Poblado
POST /mesas-votacion
{
  "nombre": "Biblioteca La Ladera",
  "direccion": "Carrera 43 # 7-50",
  "barrio_id": 1
}

# Mesa 3 - Centro
POST /mesas-votacion
{
  "nombre": "Institución Educativa San Alonso",
  "direccion": "Carrera 48 # 48-50",
  "barrio_id": 2
}
```

---

## 📊 Estructura de Barrios Disponibles (Según Sivoter2.sql)

**Antioquia - Medellín:**
- ID 1: El Poblado
- ID 2: Laureles
- ID 3: Belén
- ID 4: Manrique
- ID 5: Aranjuez

**Antioquia - Bello:**
- ID 6: Niquía
- ID 7: Cabañas
- ID 8: Bello Centro
- ID 9: Trapiche
- ID 10: Pérez

(Y muchos más en otros municipios...)

---

## 🔗 Relaciones

```
Departamento (Antioquia)
  └─ Municipio (Medellín)
      └─ Barrio (El Poblado)
          └─ Lugar de Votación / Mesa (Colegio INEM)
```

Para consultar barrios disponibles, necesitarías endpoints adicionales de barrios que podremos crear después.

