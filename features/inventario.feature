Feature: Gestión de inventario
  Scenario: Crear un producto exitosamente
    Given la API está activa
    When envío un POST a /api/productos con datos válidos
    Then la respuesta debe tener código 201

  Scenario: Listar productos
    Given existen productos registrados
    When envío un GET a /api/productos
    Then la respuesta debe tener código 200

  Scenario: Actualizar stock
    Given existe un producto
    When envío un PUT a /api/productos/{id}/stock con nuevo stock
    Then la respuesta debe ser exitosa

  Scenario: Eliminar producto existente
    Given existe un producto
    When envío un DELETE a /api/productos/{id}
    Then la respuesta debe ser exitosa

  Scenario: Error al eliminar producto inexistente
    When envío un DELETE a /api/productos/999
    Then la respuesta debe ser 404
