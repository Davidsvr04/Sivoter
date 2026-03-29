-- =========================
-- TABLA MESAS DE VOTACIÓN
-- =========================

CREATE TABLE mesas_votacion (
    id SERIAL PRIMARY KEY,
    departamento VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    barrio VARCHAR(100) NOT NULL,
    nombre_lugar VARCHAR(150) NOT NULL,
    numero_mesa INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- DATOS DE EJEMPLO
-- =========================

INSERT INTO mesas_votacion (departamento, municipio, barrio, nombre_lugar, numero_mesa)
VALUES 
    ('Antioquia', 'Medellín', 'El Poblado', 'Colegio INEM', 1),
    ('Antioquia', 'Medellín', 'El Poblado', 'Colegio INEM', 2),
    ('Antioquia', 'Medellín', 'Centro', 'Institución Educativa San Alonso', 1);
