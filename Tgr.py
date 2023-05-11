import psycopg2, psycopg2.extras, psycopg2.extensions, json, sys, psycopg2.errorcodes
from cryptography.fernet import Fernet
from datetime import datetime,timedelta
clave = b'3VPhKiFrEIF3sfGJ9Lp3ncaEbpa3-AEhc3vCDBF3bpU='
fernet = Fernet(clave)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def connect_db():
    try:
        with open('./connection.json') as archive:
            data = json.load(archive)

        con = psycopg2.connect(
            host=data["host"],
            user=data["user"],
            password=data["password"],
            dbname=data["dbname"]
        )
        return con
    except psycopg2.Error as e:
        print(f"Non podo conectar: {e}. Abortando programa")
        sys.exit(1)


def disconnect_db(conn):
    conn.commit()
    conn.close()


def create_table(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute(open("CreateTables.sql", "r").read())
            conn.commit()
            print(f"{bcolors.OKGREEN}Creada con exito{bcolors.ENDC}")   
        except psycopg2.errors.DuplicateTable as e:
            print(f"{bcolors.WARNING}Error: La tabla ya existe.{bcolors.ENDC}")
            conn.rollback()
       


def drop_db(conn):
    sql = "DROP TABLE IF EXISTS TallerAsistente; DROP TABLE IF EXISTS Asistente; DROP TABLE IF EXISTS Taller; DROP TABLE IF EXISTS Poniente"
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            conn.commit()
            print(f"{bcolors.OKGREEN}Eliminada con éxito{bcolors.ENDC}")   
        except psycopg2.Error as e:
            print(f"{bcolors.WARNING}Error al eliminar las tablas: {e}{bcolors.ENDC}")
            conn.rollback()
            


def insert_Poniente(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    snombre=input("Nombre: ")
    nombre=None if snombre=="" else snombre
    sapellido1=input("Apellido1: ")
    apellido1=None if sapellido1=="" else sapellido1
    sapellido2=input("Apellido2: ")
    apellido2=None if sapellido2=="" else sapellido2
    stelf=input("Telf: ")
    telf=None if stelf=="" else stelf
    scorreo=input("Correo: ")
    correo=None if scorreo=="" else scorreo
    sdni=input("Dni: ")
    dni=None if sdni=="" else sdni
    sempresa=input("Empresa: ")
    empresa=None if sempresa=="" else sempresa
    sql="""INSERT INTO Poniente(nombre, apellido1, apellido2, telefono, correo, dni, empresa,reputacion)
    values (%(a)s,%(b)s,%(c)s,%(d)s,%(e)s,%(f)s,%(g)s,%(h)s)"""
    with conn.cursor() as cursor:
        try:
              cursor.execute(sql,{"a":nombre,"b":apellido1,"c":apellido2,"d":telf,"e":correo,"f":dni,"g":empresa,'h':100})  
              conn.commit()  
              print(f"{bcolors.OKGREEN}Poniente añadido con éxito{bcolors.ENDC}")   
        except psycopg2.Error as e:
            if(e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION):
                if("poniente_telefono_check" in e.pgerror):
                    print(f"{bcolors.WARNING}O teléfono ten que ser de 9 dixitos{bcolors.ENDC}")
                elif("poniente_correo_check" in e.pgerror):
                    print(f"{bcolors.WARNING}Debes añadir un correo válido{bcolors.ENDC}")
            elif(e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION):
                if("nombre" in e.pgerror):
                    print(f"{bcolors.WARNING}Nombre no puede ser nulo{bcolors.ENDC}")
                elif("correo" in e.pgerror):
                    print(f"{bcolors.WARNING}correo no puede ser nulo{bcolors.ENDC}")
                elif("dni" in e.pgerror):
                    print(f"{bcolors.WARNING}dni no pude ser nulo{bcolors.ENDC}")
            elif(e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION):
                if("correo" in e.pgerror):
                    print(f"{bcolors.WARNING}correo no puede estar duplicado{bcolors.ENDC}")
                elif("dni" in e.pgerror):
                    print(f"{bcolors.WARNING}dni no puede estar duplicado{bcolors.ENDC}")
            else:
                print(e)
            conn.rollback()


def insert_Asistente(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    snombre=input("Nombre: ")
    nombre=None if snombre=="" else snombre
    sapellido1=input("Apellido1: ")
    apellido1=None if sapellido1=="" else sapellido1
    sapellido2=input("Apellido2: ")
    apellido2=None if sapellido2=="" else sapellido2
    stelf=input("Telf: ")
    telf=None if stelf=="" else stelf
    scorreo=input("Correo: ")
    correo=None if scorreo=="" else scorreo
    smetododepago=input("Targeta: ")
    metododepago=None if smetododepago=="" else smetododepago
    sdni=input("Dni: ")
    dni=None if sdni=="" else sdni

    sql="""INSERT INTO Asistente(nombre, apellido1, apellido2, telefono,correo, metodoDePago, dni)
    values (%(a)s,%(b)s,%(c)s,%(d)s,%(e)s,%(f)s,%(g)s)"""
    with conn.cursor() as cursor:
        try:
              cursor.execute(sql,{"a":nombre,"b":apellido1,"c":apellido2,"d":telf,"e":correo ,"f":fernet.encrypt(metododepago.encode()),"g":dni})  
              conn.commit()  
              print(f"{bcolors.OKGREEN}Asistente añadido con éxito{bcolors.ENDC}")   
        except psycopg2.Error as e:
            if(e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION):
                if("asistente_telefono_check" in e.pgerror):
                    print(f"{bcolors.WARNING}O teléfono ten que ser de 9 dixitos{bcolors.ENDC}")
                elif("asistente_correo_check" in e.pgerror):
                    print(f"{bcolors.WARNING}Debes añadir un correo válido{bcolors.ENDC}")
            elif(e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION):
                if("nombre" in e.pgerror):
                    print(f"{bcolors.WARNING}Nombre no puede ser nulo{bcolors.ENDC}")
                elif("correo" in e.pgerror):
                    print(f"{bcolors.WARNING}correo no puede ser nulo{bcolors.ENDC}")
                elif("dni" in e.pgerror):
                    print(f"{bcolors.WARNING}dni no pude ser nulo{bcolors.ENDC}")
                elif("metodoDePago" in e.pgerror):
                    print(f"{bcolors.WARNING}metodoDePago no pude ser nulo{bcolors.ENDC}")
            elif(e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION):
                if("correo" in e.pgerror):
                    print(f"{bcolors.WARNING}correo no puede estar duplicado{bcolors.ENDC}")
                elif("dni" in e.pgerror):
                    print(f"{bcolors.WARNING}dni no puede estar duplicado{bcolors.ENDC}")
            else:
                print(e)
            conn.rollback()
        except AttributeError as e:
            print(f"{bcolors.WARNING}Numero de targeta no puede ser nulo{bcolors.ENDC}")
            conn.rollback()
def select_poniente_by_dni(conn, dni,control_tx=True):
    query = "SELECT id FROM poniente WHERE poniente.dni = %(dni)s"
    with conn.cursor() as cursor:
        cursor.execute(query, {'dni': dni})
        row = cursor.fetchone()
        if control_tx:
            conn.commit()
        return row[0] if row else None
        
def select_initfecha_by_poniente(conn, poniente_id,control_tx=True):
    select = "SELECT initfecha, finfecha FROM taller WHERE taller.idponiente = %(poniente_id)s"
    with conn.cursor() as cursor:
        cursor.execute(select, {'poniente_id': poniente_id})
        if control_tx:
            conn.commit()
        return cursor.fetchall()

def insert_Taller(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    sponiente=input("Dni poniente: ")
    ponitente=None if sponiente=="" else sponiente
    with conn.cursor() as cursor:
        try:  
            poniente = select_poniente_by_dni(conn,sponiente,control_tx=False)
            if(poniente == None):
                print(f"{bcolors.WARNING}No existe ese poniente{bcolors.ENDC}")
                conn.rollback()
            else:
                snombre=input("Nombre: ")
                nombre=None if snombre=="" else snombre
                sespecialidad=input("Especialidad (0-> SequreApi, 1->OSINT, 2-> Reversing): ")
                especialidad=None if sespecialidad=="" else sespecialidad
                sinitFecha = input("Ingrese una fecha de inicio en formato yyyy-mm-dd: ")
                sfinFecha = input("Ingrese una fecha de fin en formato yyyy-mm-dd: ")
                sPrecio=input("Precio: ")
                precio = None if sPrecio=="" else float(sPrecio)            
                try:
                    initFecha = datetime.strptime(sinitFecha, "%Y-%m-%d").date()
                    finFecha = datetime.strptime(sfinFecha, "%Y-%m-%d").date()
                    row=select_initfecha_by_poniente(conn,poniente)
                    if(len(row)!= 0):
                        for r in row:
                            if(r[0]<=initFecha<=r[1]):
                                print(f"{bcolors.WARNING}No puedes empezar un taller cuando ya has iniciado otro{bcolors.ENDC}")
                                conn.rollback()
                    
                except Exception as e:
                    initFecha=None
                    finFecha=None
                
                sql="""INSERT INTO Taller(idPoniente, nombre, especialidad, initFecha,finFecha, precio)
                values (%(a)s,%(b)s,%(c)s,%(d)s,%(e)s,%(f)s)"""
                try:
                    cursor.execute(sql,{"a":poniente,"b":nombre,"c":especialidad,"d":initFecha,"e":finFecha ,"f":precio})
                    conn.commit()
                    print(f"{bcolors.OKGREEN}Taller añadido con éxito{bcolors.ENDC}")   
                except psycopg2.Error as e:
                    if(e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION):
                        if("taller_finfecha_check" in e.pgerror):
                            print(f"{bcolors.WARNING}La fecha final no puede ser antes que la fecha inical{bcolors.ENDC}")
                    elif(e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION):
                        if("nombre" in e.pgerror):
                            print(f"{bcolors.WARNING}Nombre no puede ser nulo{bcolors.ENDC}")
                        elif("initfecha" in e.pgerror):
                            print(f"{bcolors.WARNING}initFecha no puede ser nulo{bcolors.ENDC}")
                        elif("finfecha" in e.pgerror):
                            print(f"{bcolors.WARNING}finFecha no pude ser nulo{bcolors.ENDC}")
                    elif(e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION):
                        if("initfecha" in e.pgerror):
                            print(f"{bcolors.WARNING}2 eventos no pueden empezar el mismo dia{bcolors.ENDC}")
                        elif("finfecha" in e.pgerror):
                            print(f"{bcolors.WARNING}2 eventos no pueden acabar el mismo dia{bcolors.ENDC}")
                    else:
                        raise e
                    conn.rollback()


        except psycopg2.Error as e:
            conn.rollback()
            raise e
            
            

def select_id_asistente(conn, asistente,control_tx=True):
    select = "SELECT id FROM asistente WHERE asistente.dni = %(a)s"
    with conn.cursor() as cursor:
        cursor.execute(select, {'a': asistente})
        row = cursor.fetchone()
        if row is None:
            if control_tx:
                conn.rollback()
            print(f"{bcolors.WARNING}No existe ese asistente{bcolors.ENDC}")
            return None
        else:
            if control_tx:
                conn.commit()
            return row[0]

def insert_TallerAsistente(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    sasistente = input("Dni del asistente: ")
    asistente = None if sasistente == "" else sasistente
    staller = input('Numero del taller: ')
    taller = None if staller == "" else staller
    
    query = "INSERT INTO TallerAsistente (idTaller, idAsistente) VALUES (%(a)s, %(b)s)"
    
    with conn.cursor() as cursor:
        try:
            asis = select_id_asistente(conn, asistente,control_tx=False)
            if asis is None:
                conn.rollback()
            else:
                try:
                    cursor.execute(query, {'a': taller, 'b': asis})
                    print(f"{bcolors.OKGREEN}Asistente alistado con éxito{bcolors.ENDC}")
                    conn.commit()
                except psycopg2.Error as e:
                    if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                        if "idTaller" in e.pgerror:
                            print(f"{bcolors.WARNING}idTaller no puede ser nulo{bcolors.ENDC}")
                        elif "idAsistente" in e.pgerror:
                            print(f"{bcolors.WARNING}idAsistente no puede ser nulo{bcolors.ENDC}")
                    elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                        if "tallerasitente_fk_taller" in e.pgerror:
                            print(f"{bcolors.WARNING}No existe ese numero de taller{bcolors.ENDC}")
                    else:
                        raise e
                conn.rollback()
        except psycopg2.Error as e:
            conn.rollback()
            raise e
def delete_asistenteDeUnTaller(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    sasistente = input("Dni del asistente: ")
    asistente = None if sasistente == "" else sasistente
    staller = input('Numero del taller: ')
    taller = None if staller == "" else staller
    
    query = "DELETE FROM TallerAsistente WHERE TallerAsistente.idTaller = %(a)s AND TallerAsistente.idasistente = %(b)s"
    
    with conn.cursor() as cursor:
        try:
            idasistente = select_id_asistente(conn, asistente)
            if idasistente is None:
                conn.rollback()
            else:
                try:
                    cursor.execute(query, {'a': taller, 'b': idasistente})
                    if cursor.rowcount == 0:
                        print(f"{bcolors.WARNING}No existe ese taller{bcolors.ENDC}")
                    else:
                        print(f"{bcolors.OKGREEN}Asistente eliminado del taller{bcolors.ENDC}")
                    conn.commit()
                    
                except psycopg2.Error as e:
                    conn.rollback()
                    raise e
                    
                except Exception as e:
                    raise e
        except psycopg2.Error as e:
            conn.rollback()
            raise e


    
def print_table(rows,column_names):
    
    column_lengths = [len(col_name) for col_name in column_names]
    for row in rows:
        for i, col_value in enumerate(row):
            col_length = column_lengths[i]
            if len(str(col_value)) > col_length:
                column_lengths[i] = len(str(col_value))
    
    #cabecera
    for i, col_name in enumerate(column_names):
        print(col_name.ljust(column_lengths[i]), end=' ')
    print('')
    for i in range(sum(column_lengths) + len(column_lengths)):
        print('-', end='')
    print('')
    
    #filas
    for row in rows:
        for i, col_value in enumerate(row):
            col_length = column_lengths[i]
            print(str(col_value).ljust(col_length), end=' ')
        print('')

           
def select_todos_asistentes_de_un_taller(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    staller=input('Numero del taller: ')
    taller= None if staller =="" else staller
    query = """
    SELECT a.id, a.nombre, a.apellido1, a.apellido2, a.correo, a.telefono, a.dni, ta.idTaller
    FROM Asistente a
    INNER JOIN TallerAsistente ta ON a.id = ta.idAsistente
    WHERE ta.idTaller = %(a)s
"""
    with conn.cursor() as cursor:
        try:
            cursor.execute(query,{'a': taller})
            rows= cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            if (cursor.rowcount!=0):
               print_table(rows,column_names)
            else:
                print(f"{bcolors.WARNING}No se encontro ningun asistente para este taller{bcolors.ENDC}")
            
        except psycopg2.Error as e:
            raise e

def select_ponente_de_un_taller(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    staller = input("ID del taller: ")
    taller= None if staller =="" else staller
    query = """
        SELECT p.*
        FROM Poniente p
        INNER JOIN Taller t ON p.id = t.idPoniente
        WHERE t.id = %(taller_id)s
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(query, {'taller_id': taller})
            ponente = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            if (cursor.rowcount!=0):
               print_table(ponente,column_names)
            else:
                print(f"{bcolors.WARNING}No se encontro ningun ponente para este taller{bcolors.ENDC}")
        except  psycopg2.Error as e:
            conn.rollback()
            raise e
def select_todos_tallers(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    query = """
    SELECT *
    FROM Taller
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        if(cursor.rowcount != 0):
            column_names = [desc[0] for desc in cursor.description]
            print_table(rows,column_names)
        else:
            print(f"{bcolors.WARNING}No se encontro ningun taller{bcolors.ENDC}")
        
def select_precio_taller(conn, taller,control_tx=True):
    query_price = "SELECT precio FROM Taller WHERE id = %(a)s"
    with conn.cursor() as cursor:
        cursor.execute(query_price, {'a': taller})
        row = cursor.fetchone()
        if row is None:
            if control_tx:
                conn.rollback()
            print(f"{bcolors.WARNING}No existe ese taller{bcolors.ENDC}")
            return None
        else:
            if control_tx:
                conn.commit()
            return row[0]   
           
def cambiar_precio_taller(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    staller = input("ID del taller: ")
    taller= None if staller =="" else staller
    sdescuento= input("descuento que quieres aplicar: ")
    descuento= None if sdescuento =="" else float(sdescuento)
    query = """
        UPDATE Taller
        SET precio = %(a)s
        WHERE id = %(b)s
    """
    with conn.cursor() as cursor:
        
        try:
            precio = select_precio_taller(conn,taller,control_tx=False)
            if(precio == None):
                conn.rollback()
            else:
                precio
                nuevo_precio = precio * (1-descuento)
                cursor.execute(query, {'a': nuevo_precio, 'b':taller })
                print(f"{bcolors.OKGREEN}Descuento aplicado.{bcolors.ENDC}")
                conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            raise e
        

def obtener_informacion_taller(conn, id_taller,control_tx=True):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Taller WHERE id = %s", (id_taller,))
        row=cursor.fetchone()
        if row is None:
            if control_tx:
                conn.rollback()

            return None
        else:
            if control_tx:
                conn.commit()
            return row   
           
def actualizar_reputacion_poniente(conn, id_poniente,control_tx=True):
    with conn.cursor() as cursor:
        try:
            cursor.execute("UPDATE Poniente SET reputacion = reputacion - 10 WHERE id = %s", (id_poniente,))
            if control_tx:
                conn.commit()
            return True
        except psycopg2.Error as e:
            if(e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION):
                if("reputacion_non_negative" in e.pgerror):
                    if control_tx:
                        conn.rollback()
                    return False     
            conn.rollback()
            raise e;
                
            
def obtener_asistentes_taller(conn, id_taller, control_tx=True):
    with conn.cursor() as cursor:
        cursor.execute("SELECT idAsistente FROM TallerAsistente WHERE idTaller = %s", (id_taller,))
        asistentes = [a[0] for a in cursor.fetchall()]

        if asistentes is None:
            if control_tx:
                conn.rollback()
            return None

        if control_tx:
            conn.commit()

        return asistentes


    
def insertar_nuevo_taller(conn, id_poniente, nombre, especialidad, init_fecha, fin_fecha, precio,control_tx=True):
    query = "INSERT INTO Taller (idPoniente, nombre, especialidad, initFecha, finFecha, precio) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (id_poniente, nombre, especialidad, init_fecha, fin_fecha, precio))
            created_id = cursor.fetchone()[0]
            if control_tx:
                conn.commit()
        return created_id
    except psycopg2.Error as e:
        if control_tx:
            conn.rollback()
        return None
def eliminar_taller(conn, id_taller,control_tx=True):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Taller WHERE id = %s", (id_taller,))
            if control_tx:
                conn.commit()
        return True
    except psycopg2.Error as e:
        if control_tx:
            conn.rollback()
        return False
    

    
def eliminar_taller_y_descuento(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    
    staller = input("ID del taller: ")
    id_taller= None if staller =="" else staller
    with conn.cursor() as cursor:
        try:
            row = obtener_informacion_taller(conn,id_taller,control_tx=False)
            if row == None:
                print(f"{bcolors.WARNING}No existe ese taller{bcolors.ENDC}")
                conn.rollback()                
            else:
                id_poniente = row[0]
                update=actualizar_reputacion_poniente(conn,id_poniente,control_tx=False)
                if update == False:
                   print(f"{bcolors.WARNING}Error: La reputación del poniente no puede bajar más.{bcolors.ENDC}")
                   conn.rollback()
                else:
                    
                    asistentes = obtener_asistentes_taller(conn,id_taller,control_tx=False)
                    
                    nueva_fecha_init = row[4] + timedelta(days=7)
                    nueva_fecha_fin = row[5] + timedelta(days=7)
                    id_nuevo_taller=insertar_nuevo_taller(conn,row[1], row[2], row[3], nueva_fecha_init, nueva_fecha_fin, row[6]/2,control_tx=False)
                    if id_nuevo_taller == None:
                        print(f"{bcolors.WARNING}Error al insertar un nuevo taller: {e}{bcolors.ENDC}")
                    else: 
                        for asistente in asistentes:
                            cursor.execute("INSERT INTO TallerAsistente (idTaller, idAsistente) VALUES (%s, %s)", (id_nuevo_taller, asistente))

                        eliminar=eliminar_taller(conn,id_taller,control_tx=False)
                        if eliminar==False:
                            print(f"{bcolors.WARNING}Error al eliminar el taller: {e}{bcolors.ENDC}")
                        else:
                            conn.commit()
                            print(f"{bcolors.OKGREEN}Transaccion realizada.{bcolors.ENDC}")


            
        except psycopg2.Error as e:
            raise e
            

def menu(conn):
    MENU_TEXT = """
      -- MENÚ --
1 - Crear la bd
2 - Elminar la bd
3 - Insertar un poniente
4 - Insertar un asistente
5 - Insertar un taller
6 - Alistarse a un taller
7 - Eliminar un asistente de un taller
8 - Ver los asistentes de un taller
9 - Ver el poniente de un taller
10 - Ver todos los talleres
11 - Aplicar descuento a un taller
12 - Eliminar un taller y dar compensacion con descuento en el siguiente en 7 dias

q - Saír   
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        if tecla == '1':
            create_table(conn)  
        if tecla == '2':
            drop_db(conn)
        if tecla == '3':
            insert_Poniente(conn)
        if tecla == '4':
            insert_Asistente(conn)
        if tecla == '5':
            insert_Taller(conn)
        if tecla == '6':
            insert_TallerAsistente(conn)
        if tecla =='7':
            delete_asistenteDeUnTaller(conn)
        if tecla =='8':
            select_todos_asistentes_de_un_taller(conn)
        if tecla== '9':
            select_ponente_de_un_taller(conn)
        if tecla=='10':
            select_todos_tallers(conn)
        if tecla=='11':
            cambiar_precio_taller(conn)
        if tecla=='12':
            eliminar_taller_y_descuento(conn)
            



def main():
    print('Conectando a PostgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)

if __name__ == '__main__':
    main()
