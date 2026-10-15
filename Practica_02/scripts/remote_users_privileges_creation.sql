-- Eliminar usuarios si ya existen antes de crearlos
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

/* Asignar los privilegios de super usuario (Nota: Corregido PRIVILEGIES -> PRIVILEGES) */
GRANT ALL PRIVILEGES ON *.* TO 'mario.banda'@'%';

/* Asignar Privilegios de seleccion, insercion, Actualizacion y eliminacion a vane 
   (Nota: Corregido el nombre de usuario 'alfonso.garcia' a 'alfonso.garcia') */
GRANT SELECT, UPDATE, INSERT, DELETE ON db_test_7b.* TO 'alfonso.garcia'@'%';

/* Creacion de roles para el sistema ecomerce */
CREATE ROLE IF NOT EXISTS 'superadmin';
CREATE ROLE IF NOT EXISTS 'admin';
CREATE ROLE IF NOT EXISTS 'seller';
CREATE ROLE IF NOT EXISTS 'buyer';
CREATE ROLE IF NOT EXISTS 'support';
CREATE ROLE IF NOT EXISTS 'common';
CREATE ROLE IF NOT EXISTS 'user_not_registered';

/* Asignar Privilegios a los roles creados */

/*Superadmin*/
Grant ALL PRIVILEGES ON *.* TO 'superadmin';

-- ADMIN
GRANT ALL PRIVILEGES ON db_test_7b.* TO 'admin';

-- support
GRANT SELECT, UPDATE, INSERT ON db_test_7b.tb_users TO 'support';
GRANT SELECT, UPDATE, INSERT ON db_test_7b.tb_products TO 'support';

/*Seller*/
Grant select,insert, update on db_test_7b.tb_products to 'seller';

/* Asignar rol a los usuarios creados */
GRANT 'admin' TO 'marco.ramirez'@'%';
GRANT 'seller' TO 'alfonso.garcia'@'%';
GRANT 'support' TO 'aaron.ali'@'%';
GRANT 'superadmin' TO 'mario.banda'@'%';
GRANT 'seller' TO 'jona.papu'@'%';

-- Nota: Para que los roles se apliquen automáticamente al iniciar sesión, puedes activar el siguiente comando:
-- SET DEFAULT ROLE 'admin' TO 'marco.ramirez'@'%';
SET DEFAULT ROLE 'support' TO 'aaron.ali'@'%';
-- SET DEFAULT ROLE 'seller' TO 'aaron.ali'@'%';