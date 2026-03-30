-- =========================
-- TABLA BARRIOS
-- =========================

CREATE TABLE barrios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    municipio_id INT NOT NULL,
    CONSTRAINT fk_barrio_municipio
        FOREIGN KEY (municipio_id)
        REFERENCES municipios(id)
        ON DELETE CASCADE
);

-- =========================
-- ACTUALIZAR TABLA LUGARES_VOTACION
-- =========================

ALTER TABLE lugares_votacion 
    ADD COLUMN barrio_id INT,
    ADD COLUMN numero_mesa INT,
    ADD CONSTRAINT fk_lugar_barrio
        FOREIGN KEY (barrio_id)
        REFERENCES barrios(id)
        ON DELETE SET NULL;

-- =========================
-- DATOS DE EJEMPLO
-- =========================

-- Insertar departamento
INSERT INTO departamentos (nombre) VALUES ('Antioquia');

-- Insertar municipio
INSERT INTO municipios (nombre, departamento_id) VALUES ('Medellín', 1);

-- Insertar barrios
INSERT INTO barrios (nombre, municipio_id) VALUES 
    ('El Poblado', 1),
    ('Centro', 1);

-- Insertar lugares de votación con mesas
INSERT INTO lugares_votacion (nombre, direccion, municipio_id, barrio_id, numero_mesa)
VALUES 
    ('Colegio INEM', 'Calle 50 # 48-50', 1, 1, 1),
    ('Colegio INEM', 'Calle 50 # 48-50', 1, 1, 2),
    ('Institución Educativa San Alonso', 'Carrera 48 # 48-50', 1, 2, 1);
