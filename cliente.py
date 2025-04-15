import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from multiprocessing.connection import Connection
import threading
import time
import os

LOG_FILE = "log.txt"

def iniciar_cliente(pipe_conn: Connection):
    def enviar_requisicao():
        req = entrada.get()
        if req:
            pipe_conn.send(req)
            entrada.delete(0, tk.END)

    def atualizar_log():
        ultima_posicao = 0
        while True:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    f.seek(ultima_posicao)
                    novas_linhas = f.readlines()
                    if novas_linhas:
                        for linha in novas_linhas:
                            log_texto.insert(tk.END, linha)
                            log_texto.see(tk.END)  # Scroll automático
                        ultima_posicao = f.tell()
            time.sleep(1)  # Atualiza a cada 1s

    # --- Interface gráfica ---
    janela = tk.Tk()
    janela.title("Cliente - Banco de Dados")

    entrada = tk.Entry(janela, width=50)
    entrada.pack(padx=10, pady=(10, 5))

    botao = tk.Button(janela, text="Enviar Requisição", command=enviar_requisicao)
    botao.pack(pady=(0, 10))

    log_texto = ScrolledText(janela, width=60, height=15, state=tk.NORMAL)
    log_texto.pack(padx=10, pady=(0, 10))

    # --- Thread para atualizar o log ---
    thread_log = threading.Thread(target=atualizar_log, daemon=True)
    thread_log.start()

    janela.mainloop()
