# Práctica 03: Diseño, Población, Auditoría y Documentación de Base de Datos E-Commerce (`db_test_7b`)

## 🌐 Enlaces de Documentación Interactiva (GitHub Pages)

| Recurso | Descripción | Enlace Directo |
| :--- | :--- | :--- |
| **🏠 Portada Principal** | Portal general de navegación del proyecto | [Ver Portada (`index.html`)](https://POZOLEBLANC0.github.io/Practicas_BDN_240597-2/Practica_03/backups/index.html) |
| **📖 Diccionario de Datos** | Fichas técnicas desplegables de las 25 tablas, conteos reales, vistas y triggers | [Ver Diccionario (`diccionario_datos.html`)](https://POZOLEBLANC0.github.io/Practicas_BDN_240597-2/Practica_03/backups/diccionario_datos.html) |
| **🕸️ Diagrama Entidad-Relación** | Modelo ER interactivo (25 tablas / 34 FKs) exportable a SVG y PNG | [Ver Diagrama ER (`diagrama_er.html`)](https://POZOLEBLANC0.github.io/Practicas_BDN_240597-2/Practica_03/backups/diagrama_er.html) |

---

## 1. Descripción General del Proyecto

El objetivo de esta práctica fue diseñar, implementar, poblar, auditar y documentar la base de datos relacional **`db_test_7b`** en **MySQL 8.0+** (motor `InnoDB`, cotejamiento `utf8mb4`), orientada a una plataforma de comercio electrónico (*e-commerce*).

La arquitectura abarca de extremo a extremo la gestión de usuarios y perfiles, seguridad por roles, catálogo jerárquico de categorías, inventario de productos, proveedores, métodos de pago, órdenes de compra, envíos, devoluciones, cancelaciones y un sistema integral de trazabilidad automática.

---

## 2. Arquitectura y Objetos Construidos

La base de datos sigue una convención estricta de prefijos (`tb_` para entidades principales, `tbc_` para catálogos, `tbd_` para tablas puente/detalle, `vw_` para vistas, `trg_` para triggers, `fn_` para funciones, `sp_` para procedimientos almacenados y `evt_` para eventos) e integra los siguientes componentes:

| Tipo de Objeto | Cantidad | Detalle Técnico |
| :--- | :---: | :--- |
| **Tablas Base** | **25** | Divididas en 5 módulos funcionales (Usuarios, Catálogo, Órdenes/Pagos, Logística y Auditoría). |
| **Llaves Foráneas (FK)** | **34** | Garantizan integridad referencial en relaciones `1:1`, `1:N`, `N:M` y autorrelaciones recursivas. |
| **Vistas (`vw_`)** | **25** | Incluyen consultas recursivas con CTE (`vw_total_products_by_category`) y vistas de auditoría (`vw_trazabilidad_*`). |
| **Triggers (`trg_`)** | **72** | Disparadores `AFTER INSERT`, `AFTER UPDATE` y `AFTER DELETE` sobre las 24 tablas operativas hacia `tb_logs`. |
| **Funciones (`fn_`)** | **6** | Rutinas almacenadas para cálculos de negocio, validaciones y formateo de datos. |
| **Procedimientos (`sp_`)** | **5** | Procesos transaccionales para operaciones automatizadas y carga controlada. |
| **Eventos (`evt_`)** | **2** | Tareas programadas en el planificador de MySQL para mantenimiento y control periódico. |

---

## 3. Actividades Realizadas y Reglas de Negocio

### A. Población Masiva y Cardinalidad Real
* **Usuarios y Personas (~7,510 registros):** Implementación de relación `1:1` entre `tb_users` y `tb_people`, aplicando una distribución de estados `BIT(1)` del **80% activos (`1`) y 20% inactivos (`0`)**.
* **Catálogo Jerárquico (100 categorías):** Construcción de un árbol multinivel en `tbc_categories` mediante la llave foránea recursiva `sup_id_category`, explotado mediante expresiones de tabla comunes (`WITH RECURSIVE`) en la vista `vw_total_products_by_category`.
* **Productos y Relación $N:M$ Real (7,007 productos):** Resolución de cardinalidad muchos a muchos en `tbd_products_categorias`, asignando múltiples categorías por producto (categoría base, subcategorías y campañas temporales como *Hot Sale*, *Buen Fin* y *Black Friday*) y asegurando un mínimo de productos por categoría, además de la vinculación con proveedores en `tbd_products_users_providers`.

### B. Seguridad, Roles y Trazabilidad (`tb_logs`)
* Creación de roles y cuentas de acceso remoto (`superadmin`, `seller1`, `seller2`, entre otros) con privilegios segmentados por función.
* Registro automático en `tb_logs` de cada inserción, actualización y eliminación ejecutada en el sistema, capturando tabla afectada, tipo de operación (`Create`, `Read`, `Update`, `Delete`), usuario remoto (`db_user`), fecha exacta y descripción del movimiento.

### C. Auditoría y Verificación SQL
Se ejecutaron baterías de consultas de validación sobre cinco ejes:
1. **Cantidades:** Conteo volumétrico de registros por tabla y verificación de inventario de objetos en `information_schema`.
2. **Estados (`BIT(1)`):** Comprobación de proporciones entre registros activos e inactivos en usuarios, productos y relaciones.
3. **Restricciones:** Validación de llaves primarias (`PK`), foráneas (`FK`), únicas (`UNIQUE`) y reglas de dominio (precios positivos, stock no negativo y SKUs sin duplicados).
4. **Integridad Referencial:** Comprobación de **0 registros huérfanos** a través de las 34 llaves foráneas del esquema.
5. **Trazabilidad:** Agrupación de movimientos en `tb_logs` por usuario remoto y consulta de las vistas `vw_trazabilidad_*`.

### D. Documentación Técnica Automatizada
A partir del respaldo completo `db_test_7b1211.sql`, se generó la documentación técnica (con estética *Spider-Man: Miles Morales*) que incluye:
* **Portada web (`index.html`):** Resumen ejecutivo y acceso directo a los entregables visuales.
* **Diccionario de Datos (`diccionario_datos.html` / `.md`):** Inventario de objetos, resumen volumétrico con conteos reales extraídos del respaldo y 25 fichas técnicas desplegables.
* **Diagrama Entidad-Relación (`diagrama_er.html` / `.md` / `schema.dbml`):** Representación en notación *Crow's Foot* (Pata de Gallo) con el conteo de registros por entidad y exportación directa a `SVG` y `PNG`.

---

## 4. Estructura de Archivos de la Práctica

```text
Practica_03/
├── README.md                              # Documentación general de la práctica
└── backups/
    ├── index.html                         # Portada principal para GitHub Pages
    ├── diccionario_datos.html             # Diccionario de datos interactivo (acordeón)
    ├── diagrama_er.html                   # Diagrama ER interactivo exportable a SVG/PNG
    ├── DICCIONARIO_DATOS_db_test_7b.md    # Diccionario de datos en formato Markdown
    ├── DIAGRAMA_ER_db_test_7b.md          # Código fuente Mermaid del Diagrama ER
    ├── schema.dbml                        # Esquema relacional compatible con dbdiagram.io
    ├── db_test_7b1211.sql                 # Respaldo completo final (estructura, datos, triggers, vistas y rutinas)
    └── .generate_database_docs.py         # Script de extracción y generación documental