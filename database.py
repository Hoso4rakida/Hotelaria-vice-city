import psycopg2
conexao = psycopg2.connect(
    host="localhost",
    database="hotelaria",
    user= "postgres",
    password= "Arakida",
    port= "5432"
)
cursor = conexao.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Hospedes(
    Nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(15) NOT NULL
    );""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Quartos(
    tipo VARCHAR(50) NOT NULL,
    numero INT PRIMARY KEY,
    capacidade INT NOT NULL CHECK (capacidade >=1),
    preco_diaria DECIMAL(10,2) NOT NULL CHECK (preco_diaria > 0)
    );""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Reservas(
    id_reserva SERIAL PRIMARY KEY,
    cpf_hospede char(11) NOT NULL REFERENCES Hospedes(cpf),
    numero_quarto INT NOT NULL REFERENCES Quartos(numero)
    );""")

conexao.commit()
