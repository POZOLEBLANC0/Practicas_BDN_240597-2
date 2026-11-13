# Diccionario de Datos — db_test_7b

**Motor:** MySQL 8.0+ / InnoDB · **Juego de caracteres:** utf8mb4 · **Fuente:** `db_test_7b1211.sql`

## Índice general

1. [Resumen ejecutivo e inventario](#resumen-ejecutivo-e-inventario)
2. [Clasificación por módulos](#clasificación-por-módulos-funcionales)
3. [Fichas de tablas](#fichas-técnicas-de-tablas)
4. [Vistas y automatización](#catálogo-de-automatización-y-vistas)

## Resumen ejecutivo e inventario

El esquema modela comercio electrónico: identidad, catálogo, órdenes, pagos, logística y trazabilidad. El siguiente inventario se obtuvo del DDL; los textos funcionales no definidos mediante comentarios en el SQL se identifican como interpretación basada en nombres y restricciones.

| Objeto | Cantidad |
|---|---:|
| Tablas | 25 |
| Llaves foráneas | 34 |
| Vistas | 25 |
| Triggers | 72 |
| Funciones | 6 |
| Procedimientos | 5 |
| Eventos | 2 |

**Integridad de extracción:** 25 tablas físicas y 34 cláusulas `FOREIGN KEY` extraídas.

## Resumen Volumétrico y Estado de Población de Datos

Conteos calculados a partir de las tuplas de cada sentencia `INSERT INTO` del respaldo. Las tablas sin sentencias de inserción se reportan con cero filas.

| # | Nombre de la Tabla | Módulo | Registros Poblados | Porcentaje del Total | Observaciones / Regla de Negocio Aplicada |
|---:|---|---|---:|---:|---|
| 1 | `tb_users` | 1. Usuarios y Seguridad | 7,510 | 8.43% | Cuentas cargadas como entidades de identidad; el estado activo/inactivo se conserva por fila. |
| 2 | `tb_people` | 1. Usuarios y Seguridad | 7,502 | 8.42% | Datos personales asociados a cuentas; la carga mantiene la relación definida por sus claves. |
| 3 | `tb_user_addresses` | 1. Usuarios y Seguridad | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 4 | `tbd_address_components` | 1. Usuarios y Seguridad | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 5 | `tbd_user_payment_methods` | 1. Usuarios y Seguridad | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 6 | `tbd_users_wishlist_products` | 1. Usuarios y Seguridad | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 7 | `tb_products` | 2. Catálogo y Productos | 7,007 | 7.87% | Catálogo de productos poblado con sus atributos comerciales. |
| 8 | `tbc_categories` | 2. Catálogo y Productos | 100 | 0.11% | Catálogo de 100 categorías, con jerarquía/autorreferencia definida por el DDL. |
| 9 | `tbd_products_categorias` | 2. Catálogo y Productos | 15,348 | 17.23% | Relaciones producto-categoría cargadas para clasificar el catálogo. |
| 10 | `tbd_products_users_providers` | 2. Catálogo y Productos | 7,007 | 7.87% | Ofertas producto-proveedor cargadas para asociar inventario y proveedor. |
| 11 | `tbc_payment_methods_types` | 2. Catálogo y Productos | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 12 | `tb_buyer_orders` | 3. Órdenes y Pagos | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 13 | `tb_carts` | 3. Órdenes y Pagos | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 14 | `tb_payment_methods` | 3. Órdenes y Pagos | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 15 | `tb_payment_transaction` | 3. Órdenes y Pagos | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 16 | `tb_payments` | 3. Órdenes y Pagos | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 17 | `tbd_carts_items` | 3. Órdenes y Pagos | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 18 | `tbd_order_items` | 3. Órdenes y Pagos | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 19 | `tb_shipments` | 4. Envíos, Devoluciones y Cancelaciones | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 20 | `tb_returns` | 4. Envíos, Devoluciones y Cancelaciones | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 21 | `tb_refunds` | 4. Envíos, Devoluciones y Cancelaciones | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 22 | `tb_order_cancellations` | 4. Envíos, Devoluciones y Cancelaciones | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 23 | `tbd_return_items` | 4. Envíos, Devoluciones y Cancelaciones | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 24 | `tbd_cancellation_items` | 4. Envíos, Devoluciones y Cancelaciones | 0 | 0.00% | Tabla estructural lista para operación; el respaldo no contiene sentencias INSERT para esta tabla. |
| 25 | `tb_logs` | 5. Auditoría y Bitácora | 44,610 | 50.08% | Bitácora con 44,610 eventos; conserva operaciones de auditoría registradas en el respaldo. |
|  | **Total General de Registros** | **25 tablas** | **89,084** | **100.00%** | Conteo exacto de tuplas INSERT. |

## Clasificación por módulos funcionales

### Usuarios y Seguridad

`tb_users`, `tb_people`, `tb_user_addresses`, `tbd_address_components`, `tbd_user_payment_methods`, `tbd_users_wishlist_products`

### Catálogo y Productos

`tb_products`, `tbc_categories`, `tbd_products_categorias`, `tbd_products_users_providers`, `tbc_payment_methods_types`

### Órdenes y Pagos

`tb_buyer_orders`, `tb_carts`, `tb_payment_methods`, `tb_payment_transaction`, `tb_payments`, `tbd_carts_items`, `tbd_order_items`

### Envíos, Devoluciones y Cancelaciones

`tb_shipments`, `tb_returns`, `tb_refunds`, `tb_order_cancellations`, `tbd_return_items`, `tbd_cancellation_items`

### Auditoría y Bitácora

`tb_logs`

## Fichas técnicas de tablas

### `tb_buyer_orders`

- **Nombre:** `tb_buyer_orders`
- **Módulo:** Órdenes y Pagos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Órdenes de compra, importes y estado de cumplimiento.
- **Triggers asociados:** `trg_tb_buyer_orders_after_insert`, `trg_tb_buyer_orders_after_update`, `trg_tb_buyer_orders_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `seller_ID` | `int` | FK, NN | — | tb_buyer_orders_ibfk_1: tb_users.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador del vendedor. |
| 3 | `subtotal` | `decimal(12,2)` | NN | '0.00' | — | Campo subtotal; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `shipping_cost` | `decimal(12,2)` | NN | '0.00' | — | Campo shipping_cost; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `fulfillment_status` | `enum('Pending','Accepted','Preparing','Sent','Delivered','Canceled','Returned')` | NN | 'Pending' | — | Campo fulfillment_status; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 6 | `status` | `bit(1)` | NN | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 7 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 8 | `last_update` | `datetime` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `seller_ID` (`seller_ID`)`
- `CONSTRAINT `tb_buyer_orders_ibfk_1` FOREIGN KEY (`seller_ID`) REFERENCES `tb_users` (`ID`)`
- `CONSTRAINT `tb_buyer_orders_chk_1` CHECK ((`subtotal` >= 0))`
- `CONSTRAINT `tb_buyer_orders_chk_2` CHECK ((`shipping_cost` >= 0))`

### `tb_carts`

- **Nombre:** `tb_carts`
- **Módulo:** Órdenes y Pagos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Carritos de compra asociados a usuarios.
- **Triggers asociados:** `trg_tb_carts_after_insert`, `trg_tb_carts_after_update`, `trg_tb_carts_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `user_ID` | `int` | FK, UQ, NN | — | tb_carts_ibfk_1: tb_users.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de usuario asociado. |
| 3 | `status` | `bit(1)` | — | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 4 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 5 | `last_update` | `datetime` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_cart_user` (`user_ID`)`
- `CONSTRAINT `tb_carts_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

### `tb_logs`

- **Nombre:** `tb_logs`
- **Módulo:** Auditoría y Bitácora
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 44,610 registros
- **Descripción funcional:** Bitácora de operaciones, usuario, fecha y descripción para auditoría.
- **Triggers asociados:** ninguno.
- **Vistas asociadas:** `vw_trazabilidad_address_components`, `vw_trazabilidad_buyer_orders`, `vw_trazabilidad_cancellation_items`, `vw_trazabilidad_carts`, `vw_trazabilidad_carts_items`, `vw_trazabilidad_categories`, `vw_trazabilidad_order_cancellations`, `vw_trazabilidad_order_items`, `vw_trazabilidad_payment_methods`, `vw_trazabilidad_payment_methods_types`, `vw_trazabilidad_payment_transaction`, `vw_trazabilidad_payments`, `vw_trazabilidad_people`, `vw_trazabilidad_productos`, `vw_trazabilidad_products_categorias`, `vw_trazabilidad_products_users_providers`, `vw_trazabilidad_refunds`, `vw_trazabilidad_return_items`, `vw_trazabilidad_returns`, `vw_trazabilidad_shipments`, `vw_trazabilidad_user_addresses`, `vw_trazabilidad_user_payment_methods`, `vw_trazabilidad_users_wishlist_products`, `vw_trazabilidad_usuarios`.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int` | PK, NN, AI | — | — | Identificador primario de la fila. |
| 2 | `table_name` | `varchar(80)` | NN | — | — | Nombre de la tabla afectada. |
| 3 | `table_operation` | `enum('Create','Read','Update','Delete')` | — | NULL | — | Tipo de operación auditada. |
| 4 | `db_user` | `varchar(80)` | NN | — | — | Usuario de base de datos que ejecutó la operación. |
| 5 | `operation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de la operación auditada. |
| 6 | `table_description` | `text` | NN | — | — | Campo table_description; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `operation_status` | `bit(1)` | — | b'1' | — | Campo operation_status; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`

### `tb_order_cancellations`

- **Nombre:** `tb_order_cancellations`
- **Módulo:** Envíos, Devoluciones y Cancelaciones
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Cancelaciones solicitadas para órdenes.
- **Triggers asociados:** `trg_tb_order_cancellations_after_insert`, `trg_tb_order_cancellations_after_update`, `trg_tb_order_cancellations_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `order_ID` | `int unsigned` | FK, NN, UN | — | fk_order_cancellations_order: tb_buyer_orders.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Campo order_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `reason` | `text` | — | — | — | Campo reason; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `status` | `bit(1)` | — | NULL | — | Indicador de estado/activo según la lógica de la entidad. |
| 5 | `creation_date` | `datetime` | — | NULL | — | Fecha y hora de creación del registro. |
| 6 | `created_at` | `timestamp` | — | CURRENT_TIMESTAMP | — | Campo created_at; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `created_by` | `varchar(100)` | — | NULL | — | Campo created_by; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `last_update` | `timestamp` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `fk_order_cancellations_order` (`order_ID`)`
- `CONSTRAINT `fk_order_cancellations_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_buyer_orders` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`

### `tb_payment_methods`

- **Nombre:** `tb_payment_methods`
- **Módulo:** Órdenes y Pagos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Métodos de pago registrados por usuarios.
- **Triggers asociados:** `trg_tb_payment_methods_after_insert`, `trg_tb_payment_methods_after_update`, `trg_tb_payment_methods_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `user_ID` | `int` | FK, NN | — | fk_payment_methods_user: tb_users.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Identificador de usuario asociado. |
| 3 | `name` | `varchar(50)` | — | NULL | — | Nombre visible de la entidad. |
| 4 | `description` | `varchar(255)` | — | NULL | — | Descripción textual de la entidad. |
| 5 | `status` | `bit(1)` | — | NULL | — | Indicador de estado/activo según la lógica de la entidad. |
| 6 | `creation_date` | `datetime` | — | NULL | — | Fecha y hora de creación del registro. |
| 7 | `created_at` | `timestamp` | — | CURRENT_TIMESTAMP | — | Campo created_at; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `created_by` | `varchar(100)` | — | NULL | — | Campo created_by; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 9 | `last_update` | `timestamp` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `fk_payment_methods_user` (`user_ID`)`
- `CONSTRAINT `fk_payment_methods_user` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`

### `tb_payment_transaction`

- **Nombre:** `tb_payment_transaction`
- **Módulo:** Órdenes y Pagos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Transacciones enviadas al procesador de pagos.
- **Triggers asociados:** `trg_tb_payment_transaction_after_insert`, `trg_tb_payment_transaction_after_update`, `trg_tb_payment_transaction_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `payment_ID` | `int unsigned` | FK, NN, UN | — | fk_payment_transaction_payment: tb_payments.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Campo payment_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `transaction_ref` | `varchar(255)` | — | NULL | — | Campo transaction_ref; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `amount` | `decimal(12,2)` | — | NULL | — | Campo amount; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `status` | `bit(1)` | — | NULL | — | Indicador de estado/activo según la lógica de la entidad. |
| 6 | `creation_date` | `datetime` | — | NULL | — | Fecha y hora de creación del registro. |
| 7 | `created_at` | `timestamp` | — | CURRENT_TIMESTAMP | — | Campo created_at; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `created_by` | `varchar(100)` | — | NULL | — | Campo created_by; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 9 | `last_update` | `timestamp` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `fk_payment_transaction_payment` (`payment_ID`)`
- `CONSTRAINT `fk_payment_transaction_payment` FOREIGN KEY (`payment_ID`) REFERENCES `tb_payments` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`

### `tb_payments`

- **Nombre:** `tb_payments`
- **Módulo:** Órdenes y Pagos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Pagos aplicados a órdenes con un método asociado.
- **Triggers asociados:** `trg_tb_payments_after_insert`, `trg_tb_payments_after_update`, `trg_tb_payments_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `order_ID` | `int unsigned` | FK, NN, UN | — | fk_payments_order: tb_buyer_orders.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Campo order_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `user_payment_method_ID` | `bigint unsigned` | FK, UN | NULL | fk_payments_user_payment_method: tbd_user_payment_methods.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Campo user_payment_method_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `amount` | `decimal(12,2)` | — | NULL | — | Campo amount; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `status` | `bit(1)` | — | NULL | — | Indicador de estado/activo según la lógica de la entidad. |
| 6 | `creation_date` | `datetime` | — | NULL | — | Fecha y hora de creación del registro. |
| 7 | `created_at` | `timestamp` | — | CURRENT_TIMESTAMP | — | Campo created_at; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `created_by` | `varchar(100)` | — | NULL | — | Campo created_by; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 9 | `last_update` | `timestamp` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `fk_payments_order` (`order_ID`)`
- `KEY `fk_payments_user_payment_method` (`user_payment_method_ID`)`
- `CONSTRAINT `fk_payments_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_buyer_orders` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`
- `CONSTRAINT `fk_payments_user_payment_method` FOREIGN KEY (`user_payment_method_ID`) REFERENCES `tbd_user_payment_methods` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`

### `tb_people`

- **Nombre:** `tb_people`
- **Módulo:** Usuarios y Seguridad
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 7,502 registros
- **Descripción funcional:** Datos personales asociados a una cuenta.
- **Triggers asociados:** `trg_tb_people_after_insert`, `trg_tb_people_after_update`, `trg_tb_people_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `person_ID` | `bigint unsigned` | PK, NN, UN, AI | — | — | Campo person_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 2 | `user_ID` | `int` | FK, UQ | NULL | fk_people_users: tb_users.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de usuario asociado. |
| 3 | `courtesy_title` | `varchar(20)` | — | NULL | — | Campo courtesy_title; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `given_names` | `varchar(150)` | NN | — | — | Campo given_names; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `family_names` | `varchar(150)` | NN | — | — | Campo family_names; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 6 | `birth_date` | `date` | — | NULL | — | Campo birth_date; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `gender` | `enum('Hombre','Mujer','Prefiero no decirlo')` | NN | 'Prefiero no decirlo' | — | Campo gender; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `country_code` | `char(2)` | — | NULL | — | Campo country_code; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 9 | `phone` | `varchar(25)` | — | NULL | — | Campo phone; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 10 | `status` | `bit(1)` | — | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 11 | `creation_date` | `datetime` | — | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 12 | `last_update` | `datetime` | — | CURRENT_TIMESTAMP | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`person_ID`)`
- `UNIQUE KEY `user_ID` (`user_ID`)`
- `CONSTRAINT `fk_people_users` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

### `tb_products`

- **Nombre:** `tb_products`
- **Módulo:** Catálogo y Productos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 7,007 registros
- **Descripción funcional:** Catálogo de productos, precios, existencias y estado.
- **Triggers asociados:** `trg_tb_products_after_insert`, `trg_tb_products_after_update`, `trg_tb_products_after_delete`.
- **Vistas asociadas:** `vw_total_products_by_category`.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `SKU` | `varchar(50)` | UQ, NN | — | — | Campo SKU; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `name` | `varchar(250)` | NN | — | — | Nombre visible de la entidad. |
| 4 | `description` | `text` | — | — | — | Descripción textual de la entidad. |
| 5 | `current_price` | `decimal(10,2)` | NN | '0.00' | — | Precio vigente. |
| 6 | `current_stock` | `int unsigned` | NN, UN | '0' | — | Existencia disponible. |
| 7 | `status` | `bit(1)` | — | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 8 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 9 | `last_update` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `SKU` (`SKU`)`

### `tb_refunds`

- **Nombre:** `tb_refunds`
- **Módulo:** Envíos, Devoluciones y Cancelaciones
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Reembolsos vinculados con órdenes.
- **Triggers asociados:** `trg_tb_refunds_after_insert`, `trg_tb_refunds_after_update`, `trg_tb_refunds_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `order_ID` | `int unsigned` | FK, NN, UN | — | fk_refunds_order: tb_buyer_orders.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Campo order_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `reason` | `text` | — | — | — | Campo reason; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `amount` | `decimal(12,2)` | — | NULL | — | Campo amount; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `status` | `bit(1)` | — | NULL | — | Indicador de estado/activo según la lógica de la entidad. |
| 6 | `creation_date` | `datetime` | — | NULL | — | Fecha y hora de creación del registro. |
| 7 | `created_at` | `timestamp` | — | CURRENT_TIMESTAMP | — | Campo created_at; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `created_by` | `varchar(100)` | — | NULL | — | Campo created_by; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 9 | `last_update` | `timestamp` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `fk_refunds_order` (`order_ID`)`
- `CONSTRAINT `fk_refunds_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_buyer_orders` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`

### `tb_returns`

- **Nombre:** `tb_returns`
- **Módulo:** Envíos, Devoluciones y Cancelaciones
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Solicitudes de devolución asociadas a órdenes.
- **Triggers asociados:** `trg_tb_returns_after_insert`, `trg_tb_returns_after_update`, `trg_tb_returns_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `order_ID` | `int unsigned` | FK, NN, UN | — | fk_returns_order: tb_buyer_orders.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Campo order_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `reason` | `text` | — | — | — | Campo reason; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `status` | `bit(1)` | — | NULL | — | Indicador de estado/activo según la lógica de la entidad. |
| 5 | `creation_date` | `datetime` | — | NULL | — | Fecha y hora de creación del registro. |
| 6 | `created_at` | `timestamp` | — | CURRENT_TIMESTAMP | — | Campo created_at; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `created_by` | `varchar(100)` | — | NULL | — | Campo created_by; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `last_update` | `timestamp` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `fk_returns_order` (`order_ID`)`
- `CONSTRAINT `fk_returns_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_buyer_orders` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`

### `tb_shipments`

- **Nombre:** `tb_shipments`
- **Módulo:** Envíos, Devoluciones y Cancelaciones
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Envíos de órdenes y dirección de entrega.
- **Triggers asociados:** `trg_tb_shipments_after_insert`, `trg_tb_shipments_after_update`, `trg_tb_shipments_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `order_ID` | `int unsigned` | FK, NN, UN | — | fk_shipments_order: tb_buyer_orders.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Campo order_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `address_ID` | `bigint unsigned` | FK, UN | NULL | fk_shipments_address: tb_user_addresses.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Campo address_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `carrier` | `varchar(50)` | — | NULL | — | Campo carrier; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `tracking_number` | `varchar(100)` | — | NULL | — | Campo tracking_number; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 6 | `status` | `bit(1)` | — | NULL | — | Indicador de estado/activo según la lógica de la entidad. |
| 7 | `creation_date` | `datetime` | — | NULL | — | Fecha y hora de creación del registro. |
| 8 | `created_at` | `timestamp` | — | CURRENT_TIMESTAMP | — | Campo created_at; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 9 | `created_by` | `varchar(100)` | — | NULL | — | Campo created_by; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 10 | `last_update` | `timestamp` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `fk_shipments_order` (`order_ID`)`
- `KEY `fk_shipments_address` (`address_ID`)`
- `CONSTRAINT `fk_shipments_address` FOREIGN KEY (`address_ID`) REFERENCES `tb_user_addresses` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`
- `CONSTRAINT `fk_shipments_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_buyer_orders` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`

### `tb_user_addresses`

- **Nombre:** `tb_user_addresses`
- **Módulo:** Usuarios y Seguridad
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Direcciones de entrega vinculadas a usuarios.
- **Triggers asociados:** `trg_tb_user_addresses_after_insert`, `trg_tb_user_addresses_after_update`, `trg_tb_user_addresses_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `bigint unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `user_ID` | `int` | FK, NN | — | fk_addresses_users: tb_users.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de usuario asociado. |
| 3 | `address_label` | `varchar(100)` | NN | — | — | Campo address_label; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `recipient_name` | `varchar(150)` | — | NULL | — | Campo recipient_name; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `recipient_phone` | `varchar(25)` | — | NULL | — | Campo recipient_phone; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 6 | `delivery_instructions` | `varchar(500)` | — | NULL | — | Campo delivery_instructions; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `latitude` | `decimal(10,7)` | — | NULL | — | Campo latitude; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `longitude` | `decimal(10,7)` | — | NULL | — | Campo longitude; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 9 | `is_default` | `tinyint(1)` | NN | '0' | — | Campo is_default; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 10 | `status` | `bit(1)` | NN | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 11 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 12 | `last_update` | `datetime` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `idx_user_addresses` (`user_ID`)`
- `CONSTRAINT `fk_addresses_users` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`
- `CONSTRAINT `chk_coordinates` CHECK ((((`latitude` is null) and (`longitude` is null)) or ((`latitude` is not null) and (`longitude` is not null))))`
- `CONSTRAINT `chk_latitude` CHECK ((`latitude` between -(90) and 90))`
- `CONSTRAINT `chk_longitude` CHECK ((`longitude` between -(180) and 180))`

### `tb_users`

- **Nombre:** `tb_users`
- **Módulo:** Usuarios y Seguridad
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 7,510 registros
- **Descripción funcional:** Cuentas, credenciales y estado de usuario.
- **Triggers asociados:** `trg_tb_users_after_insert`, `trg_tb_users_after_update`, `trg_tb_users_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int` | PK, NN, AI | — | — | Identificador primario de la fila. |
| 2 | `email` | `varchar(100)` | UQ, NN | — | — | Correo de acceso/contacto. |
| 3 | `nick` | `varchar(50)` | UQ, NN | — | — | Nombre de usuario público o de acceso. |
| 4 | `password` | `varchar(255)` | NN | — | — | Credencial almacenada. |
| 5 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 6 | `last_update` | `datetime` | — | NULL | — | Fecha y hora de la última modificación. |
| 7 | `last_login` | `datetime` | — | NULL | — | Campo last_login; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `status` | `bit(1)` | — | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `email` (`email`)`
- `UNIQUE KEY `nick` (`nick`)`

### `tbc_categories`

- **Nombre:** `tbc_categories`
- **Módulo:** Catálogo y Productos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 100 registros
- **Descripción funcional:** Catálogo jerárquico de categorías con autorreferencia.
- **Triggers asociados:** `trg_tbc_categories_after_insert`, `trg_tbc_categories_after_update`, `trg_tbc_categories_after_delete`.
- **Vistas asociadas:** `vw_total_products_by_category`.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `name` | `varchar(120)` | UQ, NN | — | — | Nombre visible de la entidad. |
| 3 | `description` | `text` | — | — | — | Descripción textual de la entidad. |
| 4 | `sup_id_category` | `int unsigned` | FK, UN | NULL | fk_superior_category: tbc_categories.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Campo sup_id_category; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `status` | `bit(1)` | NN | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 6 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 7 | `last_update` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `name` (`name`)`
- `KEY `fk_superior_category` (`sup_id_category`)`
- `CONSTRAINT `fk_superior_category` FOREIGN KEY (`sup_id_category`) REFERENCES `tbc_categories` (`ID`)`

### `tbc_payment_methods_types`

- **Nombre:** `tbc_payment_methods_types`
- **Módulo:** Catálogo y Productos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Catálogo de tipos de método de pago.
- **Triggers asociados:** `trg_tbc_payment_methods_types_after_insert`, `trg_tbc_payment_methods_types_after_update`, `trg_tbc_payment_methods_types_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `code` | `varchar(30)` | NN | — | — | Campo code; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `description` | `text` | NN | — | — | Descripción textual de la entidad. |
| 4 | `status` | `bit(1)` | NN | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 5 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 6 | `last_update` | `datetime` | — | CURRENT_TIMESTAMP | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`

### `tbd_address_components`

- **Nombre:** `tbd_address_components`
- **Módulo:** Usuarios y Seguridad
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Componentes jerárquicos de direcciones y relación padre-hijo.
- **Triggers asociados:** `trg_tbd_address_components_after_insert`, `trg_tbd_address_components_after_update`, `trg_tbd_address_components_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `bigint unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `address_ID` | `bigint unsigned` | FK, UQ, NN, UN | — | fk_component_address: tb_user_addresses.ID (ON DELETE RESTRICT); fk_component_parent: tbd_address_components.address_ID (ON DELETE RESTRICT) | Campo address_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `value` | `varchar(255)` | NN | — | — | Campo value; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `component_type` | `varchar(50)` | NN | — | — | Campo component_type; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `status` | `bit(1)` | NN | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 6 | `address_sup_ID` | `bigint unsigned` | FK, UN | NULL | fk_component_parent: tbd_address_components.ID (ON DELETE RESTRICT) | Campo address_sup_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 8 | `last_update` | `datetime` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_address_component` (`address_ID`,`ID`)`
- `KEY `idx_address_parent` (`address_ID`,`address_sup_ID`)`
- `CONSTRAINT `fk_component_address` FOREIGN KEY (`address_ID`) REFERENCES `tb_user_addresses` (`ID`) ON DELETE RESTRICT`
- `CONSTRAINT `fk_component_parent` FOREIGN KEY (`address_ID`, `address_sup_ID`) REFERENCES `tbd_address_components` (`address_ID`, `ID`) ON DELETE RESTRICT`

### `tbd_cancellation_items`

- **Nombre:** `tbd_cancellation_items`
- **Módulo:** Envíos, Devoluciones y Cancelaciones
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Productos incluidos en cancelaciones.
- **Triggers asociados:** `trg_tbd_cancellation_items_after_insert`, `trg_tbd_cancellation_items_after_update`, `trg_tbd_cancellation_items_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `cancellation_ID` | `int unsigned` | PK, FK, NN, UN | — | fk_cancellation_items_cancellation: tb_order_cancellations.ID (ON DELETE CASCADE; ON UPDATE CASCADE) | Campo cancellation_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 2 | `product_ID` | `int unsigned` | PK, FK, NN, UN | — | fk_cancellation_items_product: tb_products.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Identificador de producto asociado. |
| 3 | `quantity` | `int unsigned` | UN | NULL | — | Campo quantity; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `creation_date` | `datetime` | — | NULL | — | Fecha y hora de creación del registro. |
| 5 | `created_at` | `timestamp` | — | CURRENT_TIMESTAMP | — | Campo created_at; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 6 | `created_by` | `varchar(100)` | — | NULL | — | Campo created_by; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `last_update` | `timestamp` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`cancellation_ID`,`product_ID`)`
- `KEY `fk_cancellation_items_product` (`product_ID`)`
- `CONSTRAINT `fk_cancellation_items_cancellation` FOREIGN KEY (`cancellation_ID`) REFERENCES `tb_order_cancellations` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE`
- `CONSTRAINT `fk_cancellation_items_product` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`

### `tbd_carts_items`

- **Nombre:** `tbd_carts_items`
- **Módulo:** Órdenes y Pagos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Renglones de producto/proveedor dentro de carritos.
- **Triggers asociados:** `trg_tbd_carts_items_after_insert`, `trg_tbd_carts_items_after_update`, `trg_tbd_carts_items_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `cart_ID` | `int unsigned` | PK, FK, NN, UN | — | tbd_carts_items_ibfk_1: tb_carts.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Campo cart_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 2 | `provider_ID` | `int` | PK, FK, NN | — | tbd_carts_items_ibfk_2: tbd_products_users_providers.user_ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Campo provider_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `product_ID` | `int unsigned` | PK, FK, NN, UN | — | tbd_carts_items_ibfk_3: tbd_products_users_providers.product_ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de producto asociado. |
| 4 | `quantity` | `int unsigned` | NN, UN | '1' | — | Campo quantity; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`cart_ID`,`provider_ID`,`product_ID`)`
- `KEY `provider_ID` (`provider_ID`)`
- `KEY `product_ID` (`product_ID`)`
- `CONSTRAINT `tbd_carts_items_ibfk_1` FOREIGN KEY (`cart_ID`) REFERENCES `tb_carts` (`ID`)`
- `CONSTRAINT `tbd_carts_items_ibfk_2` FOREIGN KEY (`provider_ID`) REFERENCES `tbd_products_users_providers` (`user_ID`)`
- `CONSTRAINT `tbd_carts_items_ibfk_3` FOREIGN KEY (`product_ID`) REFERENCES `tbd_products_users_providers` (`product_ID`)`
- `CONSTRAINT `chk_cart_quantity` CHECK ((`quantity` > 0))`

### `tbd_order_items`

- **Nombre:** `tbd_order_items`
- **Módulo:** Órdenes y Pagos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Renglones de producto/proveedor dentro de órdenes.
- **Triggers asociados:** `trg_tbd_order_items_after_insert`, `trg_tbd_order_items_after_update`, `trg_tbd_order_items_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `int unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `seller_order_ID` | `int unsigned` | FK, NN, UN | — | tbd_order_items_ibfk_1: tb_buyer_orders.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Campo seller_order_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 3 | `product_ID` | `int unsigned` | FK, NN, UN | — | tbd_order_items_ibfk_2: tbd_products_users_providers.product_ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de producto asociado. |
| 4 | `provider_ID` | `int` | FK, NN | — | tbd_order_items_ibfk_3: tbd_products_users_providers.user_ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Campo provider_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `product_name` | `varchar(255)` | NN | — | — | Campo product_name; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 6 | `quantity` | `int unsigned` | NN, UN | — | — | Campo quantity; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `unit_price` | `decimal(12,2)` | NN | — | — | Campo unit_price; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `subtotal` | `decimal(12,2)` | — | — | — | Campo subtotal; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 9 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `KEY `seller_order_ID` (`seller_order_ID`)`
- `KEY `product_ID` (`product_ID`)`
- `KEY `provider_ID` (`provider_ID`)`
- `CONSTRAINT `tbd_order_items_ibfk_1` FOREIGN KEY (`seller_order_ID`) REFERENCES `tb_buyer_orders` (`ID`)`
- `CONSTRAINT `tbd_order_items_ibfk_2` FOREIGN KEY (`product_ID`) REFERENCES `tbd_products_users_providers` (`product_ID`)`
- `CONSTRAINT `tbd_order_items_ibfk_3` FOREIGN KEY (`provider_ID`) REFERENCES `tbd_products_users_providers` (`user_ID`)`
- `CONSTRAINT `tbd_order_items_chk_1` CHECK ((`quantity` > 0))`
- `CONSTRAINT `tbd_order_items_chk_2` CHECK ((`unit_price` >= 0))`

### `tbd_products_categorias`

- **Nombre:** `tbd_products_categorias`
- **Módulo:** Catálogo y Productos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 15,348 registros
- **Descripción funcional:** Asociación de productos con categorías.
- **Triggers asociados:** `trg_tbd_products_categorias_after_insert`, `trg_tbd_products_categorias_after_update`, `trg_tbd_products_categorias_after_delete`.
- **Vistas asociadas:** `vw_total_products_by_category`.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `product_ID` | `int unsigned` | PK, FK, NN, UN | — | fk_product1: tb_products.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de producto asociado. |
| 2 | `category_ID` | `int unsigned` | PK, FK, NN, UN | — | fk_category1: tbc_categories.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de categoría asociada. |
| 3 | `status` | `bit(1)` | NN | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 4 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 5 | `last_update` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`product_ID`,`category_ID`)`
- `KEY `fk_category1_idx` (`category_ID`)`
- `KEY `fk_product1_idx` (`product_ID`)`
- `CONSTRAINT `fk_category1` FOREIGN KEY (`category_ID`) REFERENCES `tbc_categories` (`ID`)`
- `CONSTRAINT `fk_product1` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`)`

### `tbd_products_users_providers`

- **Nombre:** `tbd_products_users_providers`
- **Módulo:** Catálogo y Productos
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 7,007 registros
- **Descripción funcional:** Ofertas de productos por proveedores/vendedores.
- **Triggers asociados:** `trg_tbd_products_users_providers_after_insert`, `trg_tbd_products_users_providers_after_update`, `trg_tbd_products_users_providers_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `user_ID` | `int` | PK, FK, NN | — | fk_user1: tb_users.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de usuario asociado. |
| 2 | `product_ID` | `int unsigned` | PK, FK, NN, UN | — | fk_products2: tb_products.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de producto asociado. |
| 3 | `type_ownership` | `enum('Owner','Reseller','Distributor')` | — | NULL | — | Campo type_ownership; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `status` | `bit(1)` | NN | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 5 | `avalaible_date` | `datetime` | NN | — | — | Campo avalaible_date; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 6 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 7 | `last_update` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`user_ID`,`product_ID`)`
- `KEY `fk_products2` (`product_ID`)`
- `CONSTRAINT `fk_products2` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`)`
- `CONSTRAINT `fk_user1` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

### `tbd_return_items`

- **Nombre:** `tbd_return_items`
- **Módulo:** Envíos, Devoluciones y Cancelaciones
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Productos incluidos en solicitudes de devolución.
- **Triggers asociados:** `trg_tbd_return_items_after_insert`, `trg_tbd_return_items_after_update`, `trg_tbd_return_items_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `return_ID` | `int unsigned` | PK, FK, NN, UN | — | fk_return_items_return: tb_returns.ID (ON DELETE CASCADE; ON UPDATE CASCADE) | Campo return_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 2 | `product_ID` | `int unsigned` | PK, FK, NN, UN | — | fk_return_items_product: tb_products.ID (ON DELETE RESTRICT; ON UPDATE CASCADE) | Identificador de producto asociado. |
| 3 | `quantity` | `int unsigned` | UN | NULL | — | Campo quantity; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `creation_date` | `datetime` | — | NULL | — | Fecha y hora de creación del registro. |
| 5 | `created_at` | `timestamp` | — | CURRENT_TIMESTAMP | — | Campo created_at; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 6 | `created_by` | `varchar(100)` | — | NULL | — | Campo created_by; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `last_update` | `timestamp` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`return_ID`,`product_ID`)`
- `KEY `fk_return_items_product` (`product_ID`)`
- `CONSTRAINT `fk_return_items_product` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE`
- `CONSTRAINT `fk_return_items_return` FOREIGN KEY (`return_ID`) REFERENCES `tb_returns` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE`

### `tbd_user_payment_methods`

- **Nombre:** `tbd_user_payment_methods`
- **Módulo:** Usuarios y Seguridad
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Métodos de pago asociados a usuarios.
- **Triggers asociados:** `trg_tbd_user_payment_methods_after_insert`, `trg_tbd_user_payment_methods_after_update`, `trg_tbd_user_payment_methods_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `ID` | `bigint unsigned` | PK, NN, UN, AI | — | — | Identificador primario de la fila. |
| 2 | `user_ID` | `int` | FK, NN | — | fk_user_payment_user: tb_users.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de usuario asociado. |
| 3 | `payment_method_type_ID` | `int unsigned` | FK, NN, UN | — | fk_user_payment_type: tbc_payment_methods_types.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Campo payment_method_type_ID; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 4 | `provider` | `varchar(60)` | UQ, NN | — | — | Campo provider; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 5 | `provider_method_ref` | `varchar(255)` | UQ, NN | — | — | Campo provider_method_ref; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 6 | `label` | `varchar(100)` | — | NULL | — | Campo label; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 7 | `last_four` | `char(4)` | — | NULL | — | Campo last_four; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 8 | `is_default` | `tinyint(1)` | NN | '0' | — | Campo is_default; interpretación funcional inferida por el nombre. Regla efectiva según restricciones y procesos de la aplicación. |
| 9 | `status` | `bit(1)` | NN | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 10 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 11 | `last_update` | `datetime` | — | NULL | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_provider_method` (`provider`,`provider_method_ref`)`
- `KEY `fk_user_idx` (`user_ID`)`
- `KEY `fk_payment_type_idx` (`payment_method_type_ID`)`
- `CONSTRAINT `fk_user_payment_type` FOREIGN KEY (`payment_method_type_ID`) REFERENCES `tbc_payment_methods_types` (`ID`)`
- `CONSTRAINT `fk_user_payment_user` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

### `tbd_users_wishlist_products`

- **Nombre:** `tbd_users_wishlist_products`
- **Módulo:** Usuarios y Seguridad
- **Motor:** InnoDB
- **Cotejamiento:** utf8mb4 (`utf8mb4_0900_ai_ci`, según DDL).
- **Registros Actuales:** 0 registros (Tabla estructural lista para operación)
- **Descripción funcional:** Productos guardados por usuarios en listas de deseos.
- **Triggers asociados:** `trg_tbd_users_wishlist_products_after_insert`, `trg_tbd_users_wishlist_products_after_update`, `trg_tbd_users_wishlist_products_after_delete`.
- **Vistas asociadas:** ninguna.

| # | Nombre de Columna | Tipo de Dato y Longitud | Restricciones (PK, FK, UQ, NN, UN, AI) | Valor por Defecto | Referencia FK (Tabla.Columna y reglas ON DELETE / ON UPDATE) | Descripción Funcional |
|---:|---|---|---|---|---|---|
| 1 | `user_ID` | `int` | PK, FK, NN | — | fk_user2: tb_users.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de usuario asociado. |
| 2 | `product_ID` | `int unsigned` | PK, FK, NN, UN | — | fk_products3: tb_products.ID (regla no declarada (MySQL: RESTRICT/NO ACTION)) | Identificador de producto asociado. |
| 3 | `status` | `bit(1)` | NN | b'1' | — | Indicador de estado/activo según la lógica de la entidad. |
| 4 | `creation_date` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de creación del registro. |
| 5 | `last_update` | `datetime` | NN | CURRENT_TIMESTAMP | — | Fecha y hora de la última modificación. |

**Índices y restricciones declaradas:**
- `PRIMARY KEY (`user_ID`,`product_ID`)`
- `KEY `fk_products3` (`product_ID`)`
- `CONSTRAINT `fk_products3` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`)`
- `CONSTRAINT `fk_user2` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

## Catálogo de automatización y vistas

### Vistas

| Vista | Tablas base detectadas | Propósito (según SQL) |
|---|---|---|
| `vw_total_products_by_category` | `tbc_categories`, `tbd_products_categorias`, `tb_products` | Árbol recursivo y agregados de productos por categoría. |
| `vw_trazabilidad_address_components` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_buyer_orders` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_cancellation_items` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_carts` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_carts_items` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_categories` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_order_cancellations` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_order_items` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_payment_methods` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_payment_methods_types` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_payment_transaction` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_payments` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_people` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_productos` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_products_categorias` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_products_users_providers` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_refunds` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_return_items` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_returns` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_shipments` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_user_addresses` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_user_payment_methods` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_users_wishlist_products` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |
| `vw_trazabilidad_usuarios` | `tb_logs` | Consulta de trazabilidad de operaciones desde `tb_logs`. |

### Procedimientos almacenados

| Procedimiento | Propósito / tablas según código |
|---|---|
| `sp_register_new_user` | Ver cuerpo |
| `sp_registrar_producto_categoria` | Ver cuerpo |
| `sp_restore_product` | Ver cuerpo |
| `sp_simular_usuarios_masivo` | Ver cuerpo |
| `sp_soft_delete_product` | Ver cuerpo |

### Funciones

| Función | Características declaradas |
|---|---|
| `fn_calcular_edad` | NO SQL     DETERMINISTIC |
| `fn_elemento_aleatorio` | NO SQL |
| `fn_entero_aleatorio` | NO SQL |
| `fn_estatus_probabilistico` | NO SQL |
| `fn_generar_fecha_nacimiento` | NO SQL |
| `fn_verificar_stock` | READS SQL DATA |

### Eventos programados

| Evento | Agenda y operación |
|---|---|
| `evt_depurar_logs_antiguos` | ON SCHEDULE EVERY 1 DAY STARTS '2026-11-11 23:07:50' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN |
| `evt_desactivar_productos_sin_stock` | ON SCHEDULE EVERY 1 HOUR STARTS '2026-11-11 23:06:50' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN |

### Triggers de auditoría

El esquema contiene **72 triggers**. Son AFTER INSERT, AFTER UPDATE o AFTER DELETE y escriben eventos en `tb_logs` con tabla, operación, usuario y fecha. Se distribuyen en las tablas operativas que tienen las tres operaciones; el inventario completo:

| Trigger | Evento/tabla | Destino |
|---|---|---|
| `trg_tb_buyer_orders_after_insert` | AFTER INSERT ON `tb_buyer_orders` | `tb_logs` |
| `trg_tb_buyer_orders_after_update` | AFTER UPDATE ON `tb_buyer_orders` | `tb_logs` |
| `trg_tb_buyer_orders_after_delete` | AFTER DELETE ON `tb_buyer_orders` | `tb_logs` |
| `trg_tb_carts_after_insert` | AFTER INSERT ON `tb_carts` | `tb_logs` |
| `trg_tb_carts_after_update` | AFTER UPDATE ON `tb_carts` | `tb_logs` |
| `trg_tb_carts_after_delete` | AFTER DELETE ON `tb_carts` | `tb_logs` |
| `trg_tb_order_cancellations_after_insert` | AFTER INSERT ON `tb_order_cancellations` | `tb_logs` |
| `trg_tb_order_cancellations_after_update` | AFTER UPDATE ON `tb_order_cancellations` | `tb_logs` |
| `trg_tb_order_cancellations_after_delete` | AFTER DELETE ON `tb_order_cancellations` | `tb_logs` |
| `trg_tb_payment_methods_after_insert` | AFTER INSERT ON `tb_payment_methods` | `tb_logs` |
| `trg_tb_payment_methods_after_update` | AFTER UPDATE ON `tb_payment_methods` | `tb_logs` |
| `trg_tb_payment_methods_after_delete` | AFTER DELETE ON `tb_payment_methods` | `tb_logs` |
| `trg_tb_payment_transaction_after_insert` | AFTER INSERT ON `tb_payment_transaction` | `tb_logs` |
| `trg_tb_payment_transaction_after_update` | AFTER UPDATE ON `tb_payment_transaction` | `tb_logs` |
| `trg_tb_payment_transaction_after_delete` | AFTER DELETE ON `tb_payment_transaction` | `tb_logs` |
| `trg_tb_payments_after_insert` | AFTER INSERT ON `tb_payments` | `tb_logs` |
| `trg_tb_payments_after_update` | AFTER UPDATE ON `tb_payments` | `tb_logs` |
| `trg_tb_payments_after_delete` | AFTER DELETE ON `tb_payments` | `tb_logs` |
| `trg_tb_people_after_insert` | AFTER INSERT ON `tb_people` | `tb_logs` |
| `trg_tb_people_after_update` | AFTER UPDATE ON `tb_people` | `tb_logs` |
| `trg_tb_people_after_delete` | AFTER DELETE ON `tb_people` | `tb_logs` |
| `trg_tb_products_after_insert` | AFTER INSERT ON `tb_products` | `tb_logs` |
| `trg_tb_products_after_update` | AFTER UPDATE ON `tb_products` | `tb_logs` |
| `trg_tb_products_after_delete` | AFTER DELETE ON `tb_products` | `tb_logs` |
| `trg_tb_refunds_after_insert` | AFTER INSERT ON `tb_refunds` | `tb_logs` |
| `trg_tb_refunds_after_update` | AFTER UPDATE ON `tb_refunds` | `tb_logs` |
| `trg_tb_refunds_after_delete` | AFTER DELETE ON `tb_refunds` | `tb_logs` |
| `trg_tb_returns_after_insert` | AFTER INSERT ON `tb_returns` | `tb_logs` |
| `trg_tb_returns_after_update` | AFTER UPDATE ON `tb_returns` | `tb_logs` |
| `trg_tb_returns_after_delete` | AFTER DELETE ON `tb_returns` | `tb_logs` |
| `trg_tb_shipments_after_insert` | AFTER INSERT ON `tb_shipments` | `tb_logs` |
| `trg_tb_shipments_after_update` | AFTER UPDATE ON `tb_shipments` | `tb_logs` |
| `trg_tb_shipments_after_delete` | AFTER DELETE ON `tb_shipments` | `tb_logs` |
| `trg_tb_user_addresses_after_insert` | AFTER INSERT ON `tb_user_addresses` | `tb_logs` |
| `trg_tb_user_addresses_after_update` | AFTER UPDATE ON `tb_user_addresses` | `tb_logs` |
| `trg_tb_user_addresses_after_delete` | AFTER DELETE ON `tb_user_addresses` | `tb_logs` |
| `trg_tb_users_after_insert` | AFTER INSERT ON `tb_users` | `tb_logs` |
| `trg_tb_users_after_update` | AFTER UPDATE ON `tb_users` | `tb_logs` |
| `trg_tb_users_after_delete` | AFTER DELETE ON `tb_users` | `tb_logs` |
| `trg_tbc_categories_after_insert` | AFTER INSERT ON `tbc_categories` | `tb_logs` |
| `trg_tbc_categories_after_update` | AFTER UPDATE ON `tbc_categories` | `tb_logs` |
| `trg_tbc_categories_after_delete` | AFTER DELETE ON `tbc_categories` | `tb_logs` |
| `trg_tbc_payment_methods_types_after_insert` | AFTER INSERT ON `tbc_payment_methods_types` | `tb_logs` |
| `trg_tbc_payment_methods_types_after_update` | AFTER UPDATE ON `tbc_payment_methods_types` | `tb_logs` |
| `trg_tbc_payment_methods_types_after_delete` | AFTER DELETE ON `tbc_payment_methods_types` | `tb_logs` |
| `trg_tbd_address_components_after_insert` | AFTER INSERT ON `tbd_address_components` | `tb_logs` |
| `trg_tbd_address_components_after_update` | AFTER UPDATE ON `tbd_address_components` | `tb_logs` |
| `trg_tbd_address_components_after_delete` | AFTER DELETE ON `tbd_address_components` | `tb_logs` |
| `trg_tbd_cancellation_items_after_insert` | AFTER INSERT ON `tbd_cancellation_items` | `tb_logs` |
| `trg_tbd_cancellation_items_after_update` | AFTER UPDATE ON `tbd_cancellation_items` | `tb_logs` |
| `trg_tbd_cancellation_items_after_delete` | AFTER DELETE ON `tbd_cancellation_items` | `tb_logs` |
| `trg_tbd_carts_items_after_insert` | AFTER INSERT ON `tbd_carts_items` | `tb_logs` |
| `trg_tbd_carts_items_after_update` | AFTER UPDATE ON `tbd_carts_items` | `tb_logs` |
| `trg_tbd_carts_items_after_delete` | AFTER DELETE ON `tbd_carts_items` | `tb_logs` |
| `trg_tbd_order_items_after_insert` | AFTER INSERT ON `tbd_order_items` | `tb_logs` |
| `trg_tbd_order_items_after_update` | AFTER UPDATE ON `tbd_order_items` | `tb_logs` |
| `trg_tbd_order_items_after_delete` | AFTER DELETE ON `tbd_order_items` | `tb_logs` |
| `trg_tbd_products_categorias_after_insert` | AFTER INSERT ON `tbd_products_categorias` | `tb_logs` |
| `trg_tbd_products_categorias_after_update` | AFTER UPDATE ON `tbd_products_categorias` | `tb_logs` |
| `trg_tbd_products_categorias_after_delete` | AFTER DELETE ON `tbd_products_categorias` | `tb_logs` |
| `trg_tbd_products_users_providers_after_insert` | AFTER INSERT ON `tbd_products_users_providers` | `tb_logs` |
| `trg_tbd_products_users_providers_after_update` | AFTER UPDATE ON `tbd_products_users_providers` | `tb_logs` |
| `trg_tbd_products_users_providers_after_delete` | AFTER DELETE ON `tbd_products_users_providers` | `tb_logs` |
| `trg_tbd_return_items_after_insert` | AFTER INSERT ON `tbd_return_items` | `tb_logs` |
| `trg_tbd_return_items_after_update` | AFTER UPDATE ON `tbd_return_items` | `tb_logs` |
| `trg_tbd_return_items_after_delete` | AFTER DELETE ON `tbd_return_items` | `tb_logs` |
| `trg_tbd_user_payment_methods_after_insert` | AFTER INSERT ON `tbd_user_payment_methods` | `tb_logs` |
| `trg_tbd_user_payment_methods_after_update` | AFTER UPDATE ON `tbd_user_payment_methods` | `tb_logs` |
| `trg_tbd_user_payment_methods_after_delete` | AFTER DELETE ON `tbd_user_payment_methods` | `tb_logs` |
| `trg_tbd_users_wishlist_products_after_insert` | AFTER INSERT ON `tbd_users_wishlist_products` | `tb_logs` |
| `trg_tbd_users_wishlist_products_after_update` | AFTER UPDATE ON `tbd_users_wishlist_products` | `tb_logs` |
| `trg_tbd_users_wishlist_products_after_delete` | AFTER DELETE ON `tbd_users_wishlist_products` | `tb_logs` |

---

## Notas de interpretación

- Los tipos, nullabilidad, claves, valores predeterminados, motor y cotejamiento provienen del DDL. La descripción funcional por columna es interpretativa cuando el respaldo no contiene comentarios `COMMENT`.
- Las reglas FK `ON DELETE` y `ON UPDATE` solo se consignan si aparecen explícitamente; en ausencia de cláusula se indica la regla predeterminada de restricción de MySQL.
- El archivo SQL registra definiciones y también datos. El diccionario se construye desde `CREATE TABLE`, `CREATE VIEW` y bloques de rutinas, sin tratar filas de datos como DDL.
