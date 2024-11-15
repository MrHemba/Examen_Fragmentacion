import xmlrpc.client

# Conexión al servidor RPC
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Solicitar datos de un empleado
employeeID = int(input("Ingrese el EmployeeID que desea buscar: "))
resultado = proxy.getEmployeeData(employeeID)

# Mostrar el resultado
print("Resultado:")
print(resultado)
