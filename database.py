import mysql.connector
from mysql.connector import Error


def connect():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='app_db',
                                       user='db_user',
                                       password='db_user_pass')
        return conn
    except Error as e:
        print(e)


def create_db(name):
    conn = connect()

    if conn.is_connected():
        print('Connected to MySQL database')
        mycursor = conn.cursor()
        mycursor.execute(f"CREATE TABLE {name} (personID INT PRIMARY KEY AUTO_INCREMENT, "
                         "user_id INT UNSIGNED, fullname VARCHAR(50),"
                         "phone VARCHAR(12), email VARCHAR(100), instagram VARCHAR(100))")
    conn.close()


def add_user(table, USER_ID, FULLNAME, PHONE, EMAIL, INSTAGRAM):
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT * FROM {table} WHERE user_id=%s", (USER_ID,))
    data = "error"  # initially just assign the value
    for i in mycursor:
        data = i  # if cursor has no data then loop will not run and value of data will be 'error'
    if data == "error":
        mycursor.execute(f"INSERT INTO {table} (user_id, fullname, phone, email, instagram) VALUES (%s,%s,%s,%s,%s)",
                         (USER_ID, FULLNAME, PHONE, EMAIL, INSTAGRAM))
        status = False
    else:
        status = True
    conn.commit()
    conn.close()
    return status


def retrieve_users(table):
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT * FROM {table}")
    for x in mycursor:
        print(x)
    conn.close()


def retrieve_users_offset(table, offset):
    conn = connect()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT fullname, phone, email, instagram FROM {table} LIMIT 5 OFFSET {offset}")
    info = mycursor.fetchall()
    # print(info)
    # for index, data in enumerate(info):
    #     print(data)
    conn.close()
    return info


if __name__ == '__main__':
    # info = retrieve_users_offset('santas', 0)
    # for index, data in enumerate(info):
    #     if data[2] == 'https://www.instagram.com/vgarrusv/':
    #         print('ok the first')
    #     elif data[2] == "https://www.instagram.com/vgarrusv/":
    #         print('ok the second')

    # add_user('toastmasters', 203720323, 'Марат', '+79153335231', 'marat@mail.com',
    #          'https://www.instagram.com/marat_sultanof/')
    # add_user('toastmasters', 203723323, 'Алексей', '+79343335231', 'alex@mail.com',
    #          'https://www.instagram.com/alexbelov/')
    # add_user('toastmasters', 103720323, 'Андрей', '+79333335231', 'adnrei@mail.com',
    #          'https://www.instagram.com/barabanov_andrei/')
    # add_user('santas', 10372034, 'Иван Сидоров', 'sidorov@mail.com', 'sidorovinsta')
    # add_user('santas', 30372034, 'Иван Петров', 'petrov@mail.com', 'petrovinsta')
    # add_user('santas', 40372034, 'Иван Крылов', 'krilov@mail.com', 'krilovinsta')
    # add_user('santas', 50372034, 'Иван Cусанин', 'susanin@mail.com', 'susanininsta')
    # add_user('santas', 60372034, 'Иван Бунин', 'bunin@mail.com', 'bunininsta')
    # add_user('santas', 70372034, 'Иван Жиглов', 'zhiglov@mail.com', 'zhiglovinsta')
    # if status:
    create_db("toastmasters")
    create_db("snow_maidens")
    create_db("santas")
    create_db("prom_presenters")
    #     print('user already exists')")
    # create_db("santas")
    # create_db("prom_presenters")
