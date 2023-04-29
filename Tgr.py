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
        except Exception as e :
            raise e

def drop_db(conn):
    sql= "DROP TABLE TallerAsitente;DROP TABLE Asistente;DROP TABLE Taller; DROP TABLE Poniente"
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
        except Exception as e:
            raise e

def menu(conn):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """
    MENU_TEXT = """
      -- MENÚ --
1 - Crear táboa artigo  
2 - Eliminar Tabla 
3 - Insertar en la tabla   
4 - Eliminar una fila
5 - Ver un artigo
6 - Ver por precio
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



def main():
    print('Conectando a PostgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)

if __name__ == '__main__':
    main()
