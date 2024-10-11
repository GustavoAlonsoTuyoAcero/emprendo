# emprendo


GET GENERAL:

curl -X GET "http://localhost:80/productos"


GET POR ID EMPRENDIMIENTO:

curl -X GET "http://localhost:80/emprendimientos/kV81SsDpGyopnhrgWDC1/productos"

GET POR NOMBRE: 
curl -X GET "http://localhost:80/productos?nombre=NombreDelProducto"


CREATE:

curl -X POST "http://localhost:80/emprendimientos/kV81SsDpGyopnhrgWDC1/agregar_producto" -H "Content-Type: application/json" -d '{
  "nombre": "ProductoEjemplo",
  "descripcion": "Descripción del producto de ejemplo",
  "flgDisponible": true,
  "categoria": "CategoríaEjemplo",
  "precio": 19.99,
  "images": ["https://ejemplo.com/imagen1.jpg"],
  "cantidadFavoritos": 5
}'

DELETE:

curl -X DELETE "http://localhost:80/emprendimientos/kV81SsDpGyopnhrgWDC1/borrar_producto" -H "Content-Type: application/json" -d '{
  "nombre": "ProductoEjemplo"
}'

PUT:

curl -X PUT "http://localhost:80/emprendimientos/kV81SsDpGyopnhrgWDC1/actualizar_producto" -H "Content-Type: application/json" -d '{
  "nombre": "ProductoEjemplo",
  "descripcion": "Descripción actualizada del producto de ejemplo",
  "precio": 24.99,
  "flgDisponible": false
}'
