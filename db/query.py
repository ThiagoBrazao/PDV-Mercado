import psycopg2

class PostgresDB:

    def __init__(self, banco=None):  # Cria banco de dados!
        self.conn = None
        self.cursor = None
        
        if banco:
            self.open(banco)
            
            
    def open(self, banco):
        try:
            self.conn = psycopg2.connect(
                dbname=banco,
                user='user_do_db',
                password='senha_do_db',
                host='localhost',
                port='5432'
            )
            self.cursor = self.conn.cursor()
            #print("Conexão criada com sucesso!")
        except psycopg2.Error as e:
            print(f"Não foi possível estabelecer conexão: {e}")

    def criar_tabelas(self):
        cur = self.cursor
        cur.execute('''
        CREATE TABLE cliente_funcio (
            id SERIAL PRIMARY KEY,
            Nome VARCHAR(70) NOT NULL,
            telefone VARCHAR(20) NOT NULL,
            endereco VARCHAR(100)
        );
    ''')
        self.conn.commit()



    def inserir_apagar_atualizar(self, query, values):
        cur = self.cursor
        cur.execute(query, values)
        self.conn.commit()


    def pega_dados(self, query, params=None):
        cur = self.cursor
        cur.execute(query, params)
        return cur.fetchall()





# Exemplo de uso
db = PostgresDB("name_do_db")
#db.criar_tabelas()

#db.inserir_apagar_atualizar("INSERT INTO cliente_funcio (Nome, telefone, endereco) VALUES ('Manuela', '98982312', 'Casa do Jacki')")
#db.inserir_apagar_atualizar("UPDATE cliente_funcio SET nome='Thiago Brazao' WHERE nome='THIAGOBRABO' ")
#db.inserir_apagar_atualizar("DELETE FROM cliente_funcio WHERE nome='Thiago Brazao'")
#print(db.pega_dados("SELECT * FROM cliente_funcio")) #Pega todos os campos 