CREATE TABLE Poniente (
    id SERIAL CONSTRAINT poniente_pk PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido1 VARCHAR(255),
    apellido2 VARCHAR(255),
    telefono VARCHAR(9) CHECK (char_length(telefono) = 9),
    correo VARCHAR(255) CHECK (position('@' in correo) > 0) UNIQUE NOT NULL ,
    dni VARCHAR(255) NOT NULL UNIQUE,
    empresa VARCHAR(255),
    reputacion INT
);

CREATE TABLE Taller
(
    id           SERIAL
        CONSTRAINT taller_pk PRIMARY KEY,
    idPoniente   BIGINT,
    nombre       VARCHAR(255) NOT NULL,
    especialidad SMALLINT,
--     Es unica la fecha porque no puede ser que dos eventos se den a la misma hora
--      empieza uno acaba otro ,(se podría hacer un check?)
    initFecha    DATE         NOT NULL UNIQUE,
    finFecha     DATE         NOT NULL UNIQUE check (initFecha < finFecha),
    precio       INT,
    CONSTRAINT taller_fk_poniente FOREIGN KEY (idPoniente) REFERENCES poniente (id) ON DELETE CASCADE
);
CREATE TABLE Asistente
(
    id           SERIAL
        CONSTRAINT asistente_pk PRIMARY KEY,
    nombre       VARCHAR(255) NOT NULL,
    apellido1    VARCHAR(255),
    apellido2    VARCHAR(255),
    telefono     VARCHAR(9) CHECK (char_length(telefono) = 9),
    correo       VARCHAR(255) CHECK (position('@' in correo) > 0) UNIQUE NOT NULL ,
    metodoDePago VARCHAR(255) NOT NULL,
    dni          VARCHAR(255) NOT NULL UNIQUE


);
CREATE TABLE TallerAsistente
(
    id       SERIAL
        CONSTRAINT tallerAsistente_pk PRIMARY KEY,
    idTaller BIGINT,
    idAsistente BIGINT,
    CONSTRAINT TallerAsitente_FK_Taller FOREIGN KEY (idTaller) REFERENCES Taller (id) ON DELETE CASCADE,
    CONSTRAINT TallerAsitente_FK_Asistente FOREIGN KEY (idAsistente) REFERENCES Asistente (id) ON DELETE CASCADE


)