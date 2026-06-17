CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL,
    clave_secreta VARCHAR(50) NOT NULL,
    rol VARCHAR(20) NOT NULL
);

INSERT INTO usuarios (nombre_usuario, clave_secreta, rol) VALUES
('fernando', 'fer_admin_2026', 'Administrador'),
('augusto', 'aug_medico_01', 'Medico'),
('andrea', 'and_recepcion_99', 'Recepcionista'),
('daniel', 'dan_paciente_x', 'Paciente'),
('juan_perez', 'juan1234', 'Paciente'),
('maria_gomez', 'maria_enf_77', 'Enfermera'),
('carlos_ruiz', 'carlos_pass', 'Paciente'),
('lucia_mtz', 'lucia_segura', 'Medico'),
('roberto_d', 'rob_admin_2', 'Administrador'),
('sofia_l', 'sofia_paciente', 'Paciente');