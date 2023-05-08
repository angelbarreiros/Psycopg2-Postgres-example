import psycopg2, psycopg2.extras, psycopg2.extensions, sys, psycopg2.errorcodes
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
       conn= psycopg2.connect("")
       conn.autocommit = False
       return conn
    except psycopg2.Error as e:
        print(f"Imposible conectar: {e} . Abortando programa")
        sys.exit(1)

def disconnect_db(conn):
    conn.commit()
    conn.close()


def create_table(conn):
    """
    Crea as táboas
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(open("CreateTables.sql", "r").read())
            conn.commit()
            print("Táboas creadas")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.DUPLICATE_TABLE:
                print("Non se poden crear as táboas, xa existen")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()

def drop_db(conn):
    sql= "DROP TABLE TallerAsistente;DROP TABLE Asistente;DROP TABLE Taller; DROP TABLE Poniente"
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            conn.commit()
            print("Base de datos eliminada")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("Non se poden eliminar as táboas, non existen")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()

def insert_Poniente(conn):
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
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


def insert_Asistente(conn):
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
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()
        except AttributeError as e:
            print(f"{bcolors.WARNING}Numero de targeta no puede ser nulo{bcolors.ENDC}")
            conn.rollback()

def insert_Taller(conn):
    sponiente=input("Dni poniente: ")
    ponitente=None if sponiente=="" else sponiente
    query="""
    Select id from poniente where poniente.dni = %(a)s
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(query,{'a':ponitente})
            row = cursor.fetchone()
            if(row == None):
                print(f"{bcolors.WARNING}No existe ese poniente{bcolors.ENDC}")
                conn.rollback()
            else:
                
                poniente=row[0]
                snombre=input("Nombre: ")
                nombre=None if snombre=="" else snombre
                sespecialidad=input("Especialidad (0-> SequreApi, 1->OSINT, 2-> Reversing): ")
                especialidad=None if sespecialidad=="" else sespecialidad
                sinitFecha = input("Ingrese una fecha de inicio en formato yyyy-mm-dd: ")
                sfinFecha = input("Ingrese una fecha de fin en formato yyyy-mm-dd: ")
                sPrecio=input("Precio: ")
                precio = None if sPrecio=="" else float(sPrecio)
                select="""
                        Select initfecha,finfecha from taller where taller.idponiente = %(a)s
                        """
                try:
                    initFecha = datetime.strptime(sinitFecha, "%Y-%m-%d").date()
                    finFecha = datetime.strptime(sfinFecha, "%Y-%m-%d").date()
                    cursor.execute(select,{'a': poniente})
                    row = cursor.fetchall()
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
                        print(f"Erro: {e.pgcode} - {e.pgerror}")
                    conn.rollback()


        except psycopg2.Error as e:
            conn.rollback()
            raise e
            
            

def insert_TallerAsistente(conn):
    sasistente=input("Dni del asistente: ")
    asistente=None if sasistente=="" else sasistente
    staller=input('Numero del taller: ')
    taller= None if staller =="" else staller
    select="""
    Select id from asistente where asistente.dni = %(a)s
    """
    query="""
        insert into TallerAsistente(idTaller,idAsistente) values (%(a)s,%(b)s)
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(select,{'a':asistente})
            row = cursor.fetchone()
            if(row == None):
                print(f"{bcolors.WARNING}No existe ese asistente{bcolors.ENDC}")
                conn.rollback()
                
            else:
                asis=row[0]
                try:
                    cursor.execute(query,{'a':taller ,'b':asis })
                    print(f"{bcolors.OKGREEN}Asistente alistado con éxito{bcolors.ENDC}")   
                    conn.commit()
                except psycopg2.Error as e:
                    if(e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION):
                        if("idTaller" in e.pgerror):
                            print(f"{bcolors.WARNING}idTaller no puede ser nulo{bcolors.ENDC}")
                        elif("idAsistente" in e.pgerror):
                            print(f"{bcolors.WARNING}idAsistente no puede ser nulo{bcolors.ENDC}")
                    elif(e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION):
                        if("tallerasitente_fk_taller" in e.pgerror):
                            print(f"{bcolors.WARNING}No existe ese numero de taller{bcolors.ENDC}")
                    else:
                        print(f"Erro: {e.pgcode} - {e.pgerror}")
                conn.rollback()
        except psycopg2.Error as e:
            conn.rollback()
            raise e
def delete_asistenteDeUnTaller(conn):
    sasistente=input("Dni del asistente: ")
    asistente=None if sasistente=="" else sasistente
    staller=input('Numero del taller: ')
    taller= None if staller =="" else staller
    select="""
    Select id from asistente where asistente.dni = %(a)s
    """
    query="""
        Delete from TallerAsistente where TallerAsistente.idTaller = %(a)s and TallerAsistente.idasistente = %(b)s
    """
    with conn.cursor() as cursor:
            cursor.execute(select,{'a':asistente})
            row = cursor.fetchone()
            if(row == None):
                print(f"{bcolors.WARNING}No existe ese asistente{bcolors.ENDC}")
                conn.rollback()
                
            else:
                idasistente=row[0]
                try:
                    cursor.execute(query,{'a':taller, 'b': idasistente})
                    if(cursor.rowcount == 0):
                        print(f"{bcolors.WARNING}No existe ese taller{bcolors.ENDC}")
                    else:
                        print(f"{bcolors.OKGREEN}Asistente eliminado del taller{bcolors.ENDC}")
                    conn.commit()
                    
                except psycopg2.Error as e:
                    conn.rollback()
                    print(f"Erro: {e.pgcode} - {e.pgerror}")
                    
                except Exception as e:
                    raise e;

    
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
        
        
def cambiar_precio_taller(conn):
    staller = input("ID del taller: ")
    taller= None if staller =="" else staller
    sdescuento= input("descuento que quieres aplicar: ")
    descuento= None if sdescuento =="" else float(sdescuento)
    query_price = """
    SELECT precio FROM Taller
    WHERE id = %(a)s
    """
    query = """
        UPDATE Taller
        SET precio = %(a)s
        WHERE id = %(b)s
    """
    with conn.cursor() as cursor:
        
        try:
            cursor.execute(query_price, {'a': taller})
            row = cursor.fetchone()
            if(row == None):
                print(f"{bcolors.WARNING}No existe ese taller{bcolors.ENDC}")
                conn.rollback()
            else:
                precio_actual=row[0]
                nuevo_precio = precio_actual * (1-descuento)
                cursor.execute(query, {'a': nuevo_precio, 'b':taller })
                print(f"{bcolors.OKGREEN}Descuento aplicado.{bcolors.ENDC}")
                conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            raise e
        except TypeError as e:
            print(f"{bcolors.WARNING}El valor del descuento no puede ser nulo{bcolors.ENDC}")
            conn.rollback()           

def eliminar_taller_y_descuento(conn):
    staller = input("ID del taller: ")
    id_taller= None if staller =="" else staller
    with conn.cursor() as cursor:
        try:
        # Obtener información del taller a eliminar
            cursor.execute("SELECT * FROM Taller WHERE id = %s", (id_taller,))
            row = cursor.fetchone()
            if row == None:
                print(f"{bcolors.WARNING}No existe ese taller{bcolors.ENDC}")
                conn.rollback()
            else:
                cursor.execute("UPDATE Poniente SET reputacion = reputacion - 10 WHERE id=%s", (row[1],))
                cursor.execute("SELECT idAsistente FROM TallerAsistente WHERE idTaller = %s", (id_taller,))
                asistentes = [a[0] for a in cursor.fetchall()]
                
                nueva_fecha_init = row[4] + timedelta(days=7)
                nueva_fecha_fin = row[5] + timedelta(days=7)
                cursor.execute("INSERT INTO Taller (idPoniente, nombre, especialidad, initFecha, finFecha, precio) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                            (row[1], row[2], row[3], nueva_fecha_init, nueva_fecha_fin, row[6] // 2))
                nuevo_id_taller = cursor.fetchone()[0]

                for asistente in asistentes:
                    cursor.execute("INSERT INTO TallerAsistente (idTaller, idAsistente) VALUES (%s, %s)", (nuevo_id_taller, asistente))

                cursor.execute("DELETE FROM Taller WHERE id = %s", (id_taller,))

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
