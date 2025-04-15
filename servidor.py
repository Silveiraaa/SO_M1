import threading
import sqlite3
from multiprocessing import Pipe, Process
from cliente import iniciar_cliente

mutex = threading.Lock()

def criar_banco():
    conn = sqlite3.connect("banco.sqlite")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def logar(msg):
    with open("log.txt", "a") as f:
        f.write(msg + "\n")

def processar_requisicao(requisicao):
    with mutex:
        conn = sqlite3.connect("banco.sqlite")
        cur = conn.cursor()

        try:
            if requisicao.startswith("INSERT"):
                partes = requisicao.split()
                id_ = int(partes[1].split('=')[1])
                nome = partes[2].split('=')[1].strip("'")
                cur.execute("INSERT INTO registros (id, nome) VALUES (?, ?)", (id_, nome))
                conn.commit()
                logar(f"INSERT feito: id={id_}, nome={nome}")

            elif requisicao.startswith("DELETE"):
                id_ = int(requisicao.split('=')[1])
                cur.execute("DELETE FROM registros WHERE id=?", (id_,))
                conn.commit()
                logar(f"DELETE feito: id={id_}")

            elif requisicao.startswith("SELECT"):
                id_ = int(requisicao.split('=')[1])
                cur.execute("SELECT nome FROM registros WHERE id=?", (id_,))
                resultado = cur.fetchone()
                logar(f"SELECT resultado: {resultado}")

            elif requisicao.startswith("UPDATE"):
                partes = requisicao.split()
                id_ = int(partes[1].split('=')[1])
                novo_nome = partes[2].split('=')[1].strip("'")
                cur.execute("UPDATE registros SET nome=? WHERE id=?", (novo_nome, id_))
                conn.commit()
                logar(f"UPDATE feito: id={id_}, nome={novo_nome}")

        except Exception as e:
            logar(f"Erro: {e}")
        finally:
            conn.close()

def servidor_loop(pipe_conn):
    criar_banco()
    print("Servidor aguardando requisições...")
    while True:
        if pipe_conn.poll():
            requisicao = pipe_conn.recv()
            threading.Thread(target=processar_requisicao, args=(requisicao,)).start()

if __name__ == "__main__":
    conn_cliente, conn_servidor = Pipe()

    cliente_proc = Process(target=iniciar_cliente, args=(conn_cliente,))
    cliente_proc.start()

    servidor_loop(conn_servidor)
