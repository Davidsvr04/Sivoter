-- =========================
-- ENUMS
-- =========================
CREATE TYPE rol_enum AS ENUM ('admin', 'votante');
CREATE TYPE estado_enum AS ENUM ('activa', 'cerrada');
CREATE TYPE nivel_enum AS ENUM ('nacional', 'departamental', 'municipal');

-- =========================
-- TABLAS BASE
-- =========================

CREATE TABLE partidos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    sigla VARCHAR(20)
);

CREATE TABLE tipo_cargo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nivel nivel_enum NOT NULL
);

CREATE TABLE departamentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE municipios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    departamento_id INT,
    CONSTRAINT fk_municipio_departamento
        FOREIGN KEY (departamento_id)
        REFERENCES departamentos(id)
        ON DELETE SET NULL
);

CREATE TABLE lugares_votacion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150),
    direccion VARCHAR(200),
    municipio_id INT,
    CONSTRAINT fk_lugar_municipio
        FOREIGN KEY (municipio_id)
        REFERENCES municipios(id)
        ON DELETE SET NULL
);

-- =========================
-- USUARIOS Y VOTANTES
-- =========================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(150),
    password VARCHAR(255),
    rol rol_enum,
    lugar_votacion_id INT,
    estado BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_lugar
        FOREIGN KEY (lugar_votacion_id)
        REFERENCES lugares_votacion(id)
        ON DELETE SET NULL
);

CREATE TABLE votantes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    documento VARCHAR(50),
    email VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- VOTACIONES Y CANDIDATOS
-- =========================

CREATE TABLE votaciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150),
    tipo_cargo_id INT,
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP,
    estado estado_enum,
    CONSTRAINT fk_votacion_tipo_cargo
        FOREIGN KEY (tipo_cargo_id)
        REFERENCES tipo_cargo(id)
        ON DELETE SET NULL
);

CREATE TABLE candidatos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    partido_id INT,
    votacion_id INT,
    tipo_cargo_id INT,
    departamento_id INT,
    municipio_id INT,
    votos INT DEFAULT 0,

    CONSTRAINT fk_candidato_partido
        FOREIGN KEY (partido_id)
        REFERENCES partidos(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_candidato_votacion
        FOREIGN KEY (votacion_id)
        REFERENCES votaciones(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_candidato_tipo_cargo
        FOREIGN KEY (tipo_cargo_id)
        REFERENCES tipo_cargo(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_candidato_departamento
        FOREIGN KEY (departamento_id)
        REFERENCES departamentos(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_candidato_municipio
        FOREIGN KEY (municipio_id)
        REFERENCES municipios(id)
        ON DELETE SET NULL
);

-- =========================
-- VOTOS
-- =========================

CREATE TABLE votos (
    id SERIAL PRIMARY KEY,
    votante_id INT,
    candidato_id INT,
    votacion_id INT,
    fecha_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_voto_votante
        FOREIGN KEY (votante_id)
        REFERENCES votantes(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_voto_candidato
        FOREIGN KEY (candidato_id)
        REFERENCES candidatos(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_voto_votacion
        FOREIGN KEY (votacion_id)
        REFERENCES votaciones(id)
        ON DELETE CASCADE
);