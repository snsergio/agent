Este guia aplica-se a dispositivos com arquitetura x86-64 bits e Sistema Operacional Ubuntu 22.04 LTS
###################################################
##### Instalação do Ubuntu 22.04 LTS - Server #####
###################################################
# Para Instalar UBUNTU SERVER 22.04 LTS siga as etapas abaixo
######################################################
# Requerimentos                                      #
# Endereço IP (IPv4) do servidor com as informações: #
#   - Subnet no formato xxx.xxx.xxx.xxx/yy           #
#   - Endereço IP do servidor                        #
#   - Endeteço IP do Gateway                         #
#   - Endereços de DNS, normalmente 8.8.8.8, 8.8.4.4 #
# Senha para o Usuário eyeflow                       #
######################################################
# Download da versão Ubuntu Server 22.04.2 LTS:
https://releases.ubuntu.com/22.04.2/ubuntu-22.04.2-live-server-amd64.iso?_ga=2.264990991.1897287738.1684850903-132447652.1684850903
# Tela GNU GRUB - Version 2.06 Selecione:
*Try or Install Ubuntu Server
# Tela Willkommen! Bienvenue! Welcome! Selecoine a opção default:
English
# Tela Installer update available Selecione a opção default:
Continue without updating
# Tela Keyboard configuration Selecione o teclado adequado entre as duas opções:
# Opção 1:
Layout: [English (US)] 
Variant: [English (US)]
# OU Opção 2:
Layout: [Portuguese (Brazil)] 
Variant: [Portuguese (Brazil)]
# em seguida selecione [Done]
# Tela Choose type of install Selecione a opção default:
(X) Ubuntu Server
[Done]
# Tela Network connections Selecione a conexão ativa e faça as configurações
- Edit IPv4
  - IPv4 Method: Manual
  - Subnet: Entre com a rede no formato xxx.xxx.xxx.xxx/yy
  - Address: Entre com o endereço IP do servidor
  - Gateway: Entre com o endeteço IP do Gateway 
  - Name Servers: Entre com os endereços de DNS, normalmente 8.8.8.8, 8.8.4.4
  - Search domains: deixe em branco
  [Save]
  [Done]
# Tela Configure Proxy - Deixe em branco e clique
[Done]
# Tela Configure Ubuntu archive mirror Deixe a informação default e clique
[Done]
# Caso apareça a tela Installer Update Available Clique:
[Continue without updating]
# Tela Guided Storage configuration Selecione:
(X) Use an entire disk
# Mantenha todas as configurações default
Certifique que o default [X] Set up this disk as an LVM group (está selecionado)
Mantenha o default (não selecionado)
[ ] Encrypt the LVM group with LUKS
clique [Done]
# Tela Storage configuration: Mantenha o default e clique:
[Done]
# Na mensagem Confirm destructive action Clique:
[Continue]
# Tela Profile setup
  - Your name: eyeflow
  - Your server's name: <Entre com o nome do servidor>
  - Pick a username: eyeflow
  - Choose a password <Entre com a senha do usuário eyeflow>
  - Confirm your password: <repita a senha do usuário eyeflow>
[Done]
# Tela Upgrade to Ubuntu Pro Mantenha o default:
(X) Skip for now
[Continue]
# Tela SSH Setup Selecione:
[X] Install OpenSSH server
Mantenha o default em Import SSH identty:
Import SSH identity: [No]
[Done]
# Tela Featured Server Snaps Mantenha o default, não selecione nenhuma opção
[Done]
# Aguarde a conclusão da instalação - aparecerá a opção Reboot Now
[Reboot Now]
Se aparecer a mensagem Remove CD-ROM e clique ENTER: pressione <ENTER>
aguarde o reboot
# Caso a tela fique na última mensagem [ OK ] Reached target Cloud-init target
# tecle <enter> para aparecer a menssagem de login

########################################################################
##### Instalação do Eyeflow EDGE em servidor remoto                #####
#####     Versão Eyeflow Python em dispositivo físico ou em Docker #####
#####     Versão Eyeflow C++ em Docker - em construção             #####
########################################################################
# Para Instalar EYEFLOW EDGE siga as etapas abaixo
######################################################
# Requerimentos                                      #
#     Endereço IP (IPv4) do servidor EDGE            #
#     Senha do Usuário eyeflow                       #
######################################################
# Conectar ao servidor com usuário eyeflow
ssh eyeflow@<IP do servidor>

# Download do script de instalação no diretório default do usuário eyeflow
wget https://raw.githubusercontent.com/snsergio/agent/main/install-edge.sh
# Certifique-se que é executável:
chmod a+x install-edge.sh
# Certifique-se que o arquivos está presente e é executável:
ls -l
# Execute o script como SUDO:
sudo ./install-edge.sh
# Será solicitada a senha SUDO do usuário eyeflow
# Na tela:
# Use arrow keys to select installation type and hit <ENTER> or <CTRL-C> to exit:
#     >Install EDGE Python on Ubuntu Station
#      Install EDGE Python on Docker container
#      Install EDGE C++ on Docker container
#
# Selecione a versão do Eyeflow EDGE que deseja Instalar
#     Utilize as setas para cima ou para baixo para selecionar e pressione <ENTER>
# Observe as mensagens, caso precise interagir durante a instalação, utilize sempre as opções default
# Não modifique nenhuma opção - normalmente utilize <TAB> para chegar ao <OK> e selecione o OK com <ENTER> ou <SPACE BAR>
# Aguarde a mensagem:
#    #################################################################################
#    # Rebooting station - login as eyeflow user after reboot to resume installation #
#    #################################################################################
# Quando o sistema retornar do BOOT, faça novamente o login com o usuário eyeflow para continuar a instalação
# Siga as orientações na tela do equipamento, ao fazer o login, será solicitada a senha do usuário eyeflow novamente
#    #########################################################################
#    #    Resuming EDGE on <environment> installation - Enter SUDO password  #
#    #########################################################################
# Entre com a senha SUDO do usuário eyeflow
[sudo] password for eyeflow:
# Observe as mensagens, caso precise interagir durante a instalação, utilize sempre as opções default
# Não modifique nenhuma opção - normalmente utilize <TAB> para chegar ao <OK> e selecione o OK com <ENTER> ou <SPACE BAR>
# Aguarde completar a instalação, ao final verá a mensagem:
# ###############################################
# #####   end of EDGE installation script   #####
# #####     <language> on <environment>     #####
#
# Instruções para instalar o agente de monitoração, caso queira instalar no EDGE:
# ######################################################################################
# #  To install Metric collector run the following command:                            #
# #      wget https://raw.githubusercontent.com/snsergio/agent/main/install-monitor.sh #
# #      chmod a+x install-monitor.sh                                                  #
# #      sudo ./install-monitor.sh                                                     #
# ######################################################################################
#
#################################################################
#          Rebooting station to complete installation           #
#################################################################
#
#################################################################
# LOG file at: /opt/eyeflow/install/edge-install<date time>.log #
#################################################################
# Após o reboot a estação EDGE estará pronta para uso
#
# Ao instalar as versões para DOCKER estarão disponíveis instruções para executar o Eyeflow EDGE
############################################################################################
# Instructions to run Eyeflow Edge at: /opt/eyeflow/install/how-execute-eyeflow-docker.txt #
############################################################################################
As instruções também estarão na tela
# 
# Tempo estimado de execução da versão Edge em servidor físico (o mais lento):
#                     hh:mm:ss
#    INICIO:          00:00:00
#    REBOOT:          00:05:08
#    RETORNO DO BOOT: 00:10:43
#    TERMINO:         00:32:36
#-----------------------------
###############################################################
##### Instalação do Agente de monitoração em estação EDGE #####
###############################################################
# Para Instalar o AGENTE DE MONITORAÇÃO siga as etapas abaixo
#######################################################################################
# Requerimentos                                                                       #
#     Informações de configuração de monitoramento                                    #
#         Consulte detalhes no github:                                                #
#         https://github.com/Eyeflow-AI/station-monitoring/tree/main/metric-collector #
#     Senha do Usuário eyeflow                                                        #
#######################################################################################
# Conectar ao servidor com usuário eyeflow
ssh eyeflow@<IP do servidor>
# Download do script de instalação no diretório default do usuário eyeflow
wget https://raw.githubusercontent.com/snsergio/agent/main/install-monitor.sh
# Certifique-se que é executável:
chmod +x install-monitor.sh
# Certifique-se que o arquivos está presente e é executável:
ls -l
# Execute o script como SUDO:
sudo ./install-monitor.sh
# Será solicitada a senha do usuário eyeflow
# Observe as mensagens, caso precise interagir durante a instalação, utilize sempre as opções default
# Não modifique nenhuma opção - normalmente utilize <TAB> para chegar no <OK> e selecione o OK com <ENTER>
# Aguarde a mensagem abaixo e edite o arquivo de configuração para refletir os requerimentos do EDGE:
##### Editing monitoring agent configuration file
#################################################################################
# Edit Monitoring Agent configuration file to reflect Edge Station requirements #
#   Press <ENTER> to edit or <CTRL-C> to cancel Monitoring Agent instalation    #
#################################################################################
# Para salvar as modificações do arquivo, no editor NANO pressione <CTRL-x> para salvar e em seguida <y> para sair
# Verifique se o status do serviço de monitoração está ativo e sem erros
# Aguarde a mensagem
###########################################################
#####   end of Metric Collector installation script   #####
#<DATA> <HORA>
####################################################################
# LOG file at: /opt/eyeflow/install/monitor-install<date time>.log #
####################################################################
