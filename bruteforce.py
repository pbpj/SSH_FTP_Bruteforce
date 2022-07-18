import services


host = "127.0.0.1"
port_ftp = 21 #Porta default FTP
port_ssh = 22 #Porta default SSH

user = open("user.txt").read().split("\n") # Dicionario default users
passw = open("pass.txt").read().split("\n") # Dicionario default passwords

# Ciclo para apresentação de menu na consola
while True:
    services.hud_menu(host,port_ftp,port_ssh) 
    try:
       escolha = services.prompt_menu()  #função de qol
    except:
        services.limpar_terminal()  #função de qol
        services.menu_else() #função de qol
    else:
        services.limpar_terminal()
        if escolha == 0:
            host = services.change_hostname() #chama a função para mudança da variável host
        elif escolha == 1:
            if services.ping(host) == 1: #função que pinga o ip definido em host para garantir a conectividade antes do NMAP
                services.portscan(host, port_ftp, port_ssh) #chama a função de nmap para mapear as portas atribuidas em port_ftp e port_ssh
        elif escolha == 2:
            services.ftp(host, port_ftp, user, passw) #inicia a função de ftp bruteforce
        elif escolha == 3:
            services.ssh(host, port_ssh, user, passw) #inicia a função de ssh bruteforce
        elif escolha == 8:
            port_ftp = services.change_ftp_port() #função para mudança porta serviço FTP
        elif escolha == 9:
            port_ssh = services.change_ssh_port() #função para mudança porta serviço FTP
        else:
            services.menu_else() #função de qol
