import psycopg2, psycopg2.extras, psycopg2.extensions, json, sys, psycopg2.errorcodes


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
def insert_Taller(conn):
    pass
def insert_Asistente(conn):
    pass
def insert_Poniente(conn):
    pass

def menu(conn):
    MENU_TEXT = """
      -- MENÚ --
1 - Crear la bd
2 - Elminar la bd
3 - Insertar un taller
4 - Insertar un asistente
5 - Isertar un poniente
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
            insert_Taller(conn)
        if tecla == '4':
            insert_Asistente(conn)
        if tecla == '5':
            insert_Poniente(conn)



def main():
    print('Conectando a PostgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)

if __name__ == '__main__':
    main()
