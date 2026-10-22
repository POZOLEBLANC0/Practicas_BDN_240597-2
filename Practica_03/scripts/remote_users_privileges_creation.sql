USE `db_test_7b`;

-- =========================================================
-- 1. CREACIÓN / LIMPIEZA DE USUARIOS
-- =========================================================
DROP USER IF EXISTS 'marco.ramirez'@'%';
CREATE USER 'marco.ramirez'@'%' IDENTIFIED BY 'qwerty123';

DROP USER IF EXISTS 'mario.banda'@'%';
CREATE USER 'mario.banda'@'%' IDENTIFIED BY '240597';

DROP USER IF EXISTS 'aaron.ali'@'%';
CREATE USER 'aaron.ali'@'%' IDENTIFIED BY '240045';

DROP USER IF EXISTS 'alfonso.garcia'@'%';
CREATE USER 'alfonso.garcia'@'%' IDENTIFIED BY '240904';

DROP USER IF EXISTS 'jona.papu'@'%';
CREATE USER 'jona.papu'@'%' IDENTIFIED BY '240080';

-- Usuarios Middleware / Apps
CREATE USER IF NOT EXISTS 'app_web'@'%' IDENTIFIED BY 'Web123';
CREATE USER IF NOT EXISTS 'app_mobile'@'%' IDENTIFIED BY 'Mobile890';


-- =========================================================
-- 2. CREACIÓN DE ROLES
-- =========================================================
CREATE ROLE IF NOT EXISTS 'superadmin';
CREATE ROLE IF NOT EXISTS 'admin';
CREATE ROLE IF NOT EXISTS 'seller';
CREATE ROLE IF NOT EXISTS 'buyer';
CREATE ROLE IF NOT EXISTS 'support';
CREATE ROLE IF NOT EXISTS 'common';
CREATE ROLE IF NOT EXISTS 'user_not_registered';


-- =========================================================
-- 3. ASIGNACIÓN DE PRIVILEGIOS A LOS ROLES
-- =========================================================

-- Superadmin
GRANT ALL PRIVILEGES ON *.* TO 'superadmin' WITH GRANT OPTION;

-- Admin
GRANT ALL PRIVILEGES ON db_test_7b.* TO 'admin';

-- Support
GRANT SELECT, UPDATE, INSERT ON db_test_7b.tb_users TO 'support';
GRANT SELECT, UPDATE, INSERT ON db_test_7b.tb_products TO 'support';

-- Seller
GRANT SELECT, INSERT, UPDATE ON db_test_7b.tb_products TO 'seller';

-- User Not Registered (CORREGIDO: Solo EXECUTE para la rutina)
GRANT INSERT ON db_test_7b.tb_users TO 'user_not_registered';
GRANT INSERT ON db_test_7b.tb_people TO 'user_not_registered';
GRANT EXECUTE ON PROCEDURE db_test_7b.sp_register_new_user TO 'user_not_registered';


-- =========================================================
-- 4. PRIVILEGIOS DIRECTOS Y ASIGNACIÓN DE ROLES A USUARIOS
-- =========================================================

-- Permisos directos de superusuario a tu cuenta
GRANT ALL PRIVILEGES ON *.* TO 'mario.banda'@'%' WITH GRANT OPTION;
GRANT SELECT, UPDATE, INSERT, DELETE ON db_test_7b.* TO 'alfonso.garcia'@'%';

-- Asignar roles a las cuentas del equipo
GRANT 'admin' TO 'marco.ramirez'@'%';
GRANT 'seller' TO 'alfonso.garcia'@'%';
GRANT 'support' TO 'aaron.ali'@'%';
GRANT 'superadmin' TO 'mario.banda'@'%';
GRANT 'seller' TO 'jona.papu'@'%';

-- Asignar roles a las credenciales de conexión para las apps
GRANT 'user_not_registered' TO 'app_web'@'%';
GRANT 'user_not_registered' TO 'app_mobile'@'%';


-- =========================================================
-- 5. ACTIVACIÓN DE ROLES POR DEFECTO Y APLICACIÓN DE CAMBIOS
-- =========================================================

-- Activa automáticamente todos los roles asignados al iniciar sesión
SET DEFAULT ROLE ALL TO 
    'marco.ramirez'@'%',
    'mario.banda'@'%',
    'alfonso.garcia'@'%',
    'aaron.ali'@'%',
    'jona.papu'@'%',
    'app_web'@'%',
    'app_mobile'@'%';

FLUSH PRIVILEGES;