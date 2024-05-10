from queue import Queue 
import threading, socket, sys

if len(sys.argv) < 2:
    print("Modo de uso: subdomain.py dominio.com -w /caminho/wordlist")
    sys.exit(1)

dominio = sys.argv[1]
wordlist_path = None

if "-w" in sys.argv:
    try:
        wordlist_index = sys.argv.index("-w") + 1
        wordlist_path = sys.argv[wordlist_index]
    except IndexError:
        print("Erro: O caminho para a wordlist não foi fornecido após -w.")
        sys.exit(1)

    try:
        with open(wordlist_path):
            pass
    except FileNotFoundError:
        print(f"Erro: A wordlist no caminho '{wordlist_path}' não foi encontrada.")
        sys.exit(1)

    sys.argv = [arg for arg in sys.argv if arg != "-w"]
    sys.argv.remove(wordlist_path)

    dominio = sys.argv[1]

    print(f"Wordlist personalizada carregada: {wordlist_path}")
    print()

else:
    print("Exemplo de uso com wordlist personalizada:")
    print("python subdomain.py dominio.com -w /caminho/wordlist")
    sys.exit(1)

lock = threading.Lock()

def forca_bruta():
    while True:
        DNS = q.get()
        if DNS is None:
            break
        DNS += "." + dominio
        try:
            IP = socket.gethostbyname(DNS)
            with lock:
                print(DNS + ":\t" + IP)
        except socket.error:
            pass
        finally:
            q.task_done()

q = Queue()

threads = []
for i in range(20):
    t = threading.Thread(target=forca_bruta)
    t.start()
    threads.append(t)

with open(wordlist_path) as lista:
    for nome in lista:
        q.put(nome.strip())

q.join()

for _ in range(20):
    q.put(None)
for t in threads:
    t.join()

print("Mapeamento completo!")
