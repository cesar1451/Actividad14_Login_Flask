import mysql.connector

bd = mysql.connector.connect(
    user='Cesar', password='Cesar14ilse21', 
    database='cinemapp')

cursor = bd.cursor()

def get_usuarios():
    consulta = "SELECT * FROM  usuario" #Hacer consulta
    
    cursor.execute(consulta) #Ejecutar la consulta
    usuarios = [] #Crear lista
    for row in cursor.fetchall(): #Obtener los datos de la consulta
        usuario = { #Generar un usuario como tupla
            'id': row[0],
            'correo': row[1],
            'contraseña': row[2]
        }
        
        usuarios.append(usuario) #Guardar usuarios como tupla
    return usuarios
    
def existe_usuario(correo):
    query = "SELECT COUNT(*) FROM usuario WHERE correo = %s" #COUNT(*) -> devuelve las coincidencias que se encontraron en la consulta
    cursor.execute(query, (correo,)) #Ejecutar el query. (correo,) -> envía una tupla y si se omite la coma marca error.
    
    if cursor.fetchone()[0] == 1: #Devuelve una tupla[0] las coincidencias
        return True
    else:
        return False    

import hashlib #importar libreria para hashear la contraseña
def crear_usuario(correo, contra):
    if existe_usuario(correo):
        return False
    else:
        h = hashlib.new('sha256', bytes(contra, 'utf-8')) #Algoritmo de hasheo y le envía los bytes
        h = h.hexdigest() #Recibe 64 caracteres del hasheo
        insertar = "INSERT INTO usuario(correo, contraseña) VALUES (%s, %s)"
        
        cursor.execute(insertar, (correo, h))
        bd.commit()
        
        return True
        
def iniciar_sesion(correo, contra):
    h = hashlib.new('sha256', bytes(contra, 'utf-8')) #Algoritmo de hasheo y le envía los bytes
    h = h.hexdigest() #Recibe 64 caracteres del hasheo
    #Hacer una consulta a la base de datos para que retorne el id 
    query = "SELECT id FROM usuario WHERE correo = %s AND contraseña = %s"
    
    cursor.execute(query, (correo, h)) #Ejecutar consulta
    id = cursor.fetchone() #Obtener tupla 
    if id:
        return id[0], True
    else:
        return None, False
    
    