import psycopg2, psycopg2.extras, psycopg2.extensions, json, sys, psycopg2.errorcodes, hashlib
from cryptography.fernet import Fernet
from datetime import datetime

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
        con.set_session(autocommit=False, deferrable=False,
                        isolation_level=psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
        return con
    except psycopg2.Error as e:
        raise e


def disconnect_db(conn):
    conn.commit()
    conn.close()


def create_table(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute(open("CreateTables.sql", "r").read())
            conn.commit()
        except Exception as e :
            raise e

def drop_db(conn):
    sql= "DROP TABLE TallerAsitente;DROP TABLE Asistente;DROP TABLE Taller; DROP TABLE Poniente"
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            raise e

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
    sql="""INSERT INTO Poniente(nombre, apellido1, apellido2, telefono, correo, dni, empresa)
    values (%(a)s,%(b)s,%(c)s,%(d)s,%(e)s,%(f)s,%(g)s)"""
    with conn.cursor() as cursor:
        try:
              cursor.execute(sql,{"a":nombre,"b":apellido1,"c":apellido2,"d":telf,"e":correo,"f":dni,"g":empresa})  
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
    clave = Fernet.generate_key()
    fernet = Fernet(clave)

    sql="""INSERT INTO Asistente(nombre, apellido1, apellido2, telefono,correo, metodoDePago, dni)
    values (%(a)s,%(b)s,%(c)s,%(d)s,%(e)s,%(f)s,%(g)s)"""
    with conn.cursor() as cursor:
        try:
              cursor.execute(sql,{"a":nombre,"b":apellido1,"c":apellido2,"d":telf,"e": fernet.encrypt(metododepago.encode()),"f":correo,"g":dni})  
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
                print("No existe ese poniente")
                conn.rollback()
            else:
                
                poniente=row[0]
                snombre=input("Nombre: ")
                nombre=None if snombre=="" else snombre
                sespecialidad=input("Especialidad (0-> SequreApi, 1->OSINT, 2-> Reversing): ")
                especialidad=None if sespecialidad=="" else sespecialidad
                sinitFecha = input("Ingrese una fecha de inicio en formato yyyy-mm-dd: ")
                initFecha = datetime.strptime(sinitFecha, "%Y-%m-%d").date()
                sfinFecha = input("Ingrese una fecha de fin en formato yyyy-mm-dd: ")
                finFecha = datetime.strptime(sfinFecha, "%Y-%m-%d").date()
                sPrecio=input("Precio: ")
                precio = None if sPrecio=="" else float(sPrecio)
                sql="""INSERT INTO Taller(idPoniente, nombre, especialidad, initFecha,finFecha, precio)
                values (%(a)s,%(b)s,%(c)s,%(d)s,%(e)s,%(f)s)"""
                try:
                    cursor.execute(sql,{"a":poniente,"b":nombre,"c":especialidad,"d":initFecha,"e":finFecha ,"f":precio})
                    conn.commit()
                    print(f"{bcolors.OKGREEN}Taller añadido con éxito{bcolors.ENDC}")   
                except Exception as e:
                    raise e


        except Exception as e:
            raise e

    

    

def menu(conn):
    MENU_TEXT = """
      -- MENÚ --
1 - Crear la bd
2 - Elminar la bd
3 - Insertar un poniente
4 - Insertar un asistente
5 - Isertar un taller
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



def main():
    print('Conectando a PostgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)

if __name__ == '__main__':
    main()
