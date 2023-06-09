Este guia aplica-se a dispositivos com arquitetura x86-64 bits e Sistema Operacional Ubuntu 22.04 LTS

##### Instalação do Eyeflow EDGE em servidor remoto #####
#####  Versão Eyeflow Python em dispositivo físico e em Docker #####

# Para Instalar EYEFLOW EDGE siga as etapas abaixo
######################################################
# Requerimentos                                      #
# Endereço IP (IPv4) do servidor EDGE                #
# Senha do Usuário eyeflow                           #
######################################################
# Conectar ao servidor com usuário eyeflow
ssh eyeflow@<IP do servidor>

# Download do script de instalação no diretório default do usuário eyeflow
wget https://raw.githubusercontent.com/snsergio/agent/main/install-edge.sh
# Certifique-se que o arquivos está presente:
ls -l
# O arquivo install-edge.sh deve aparecer listado
# Certifique-se que é executável:
chmod a+x install-edge.sh
# Execute o script como SUDO:
sudo ./install-edge.sh
# Será solicitada a senha do usuário eyeflow
# Observe as mensagens, caso precise interagir durante a instalação, utilize sempre as opções default
# Não modifique nenhuma opção - normalmente utilize <TAB> para chegar no <OK> e selecione o OK com <ENTER>
# Aguarde a mensagem:
    #################################################################################
    # Rebooting station - login as eyeflow user after reboot to resume installation #
    #################################################################################
# Quando o sistema retornar do BOOT, faça novamente o login com o usuário eyeflow para continuar a instalação
# Siga as orientações na tela do equipamento, ao fazer o login, será solicitada a senha do usuário eyeflow novamente
    #########################################################################
    # returning from boot-resuming Edge <language> on <environment> Install #
    #########################################################################
# Entre com a senha SUDO do usuário eyeflow
[sudo] password for eyeflow:
# Aguarde completar a instalação, ao final verá a mensagem:
#################################################################
#          Rebooting station to complete installation           #
#################################################################

#################################################################
# LOG file at: /opt/eyeflow/install/edge-install<date time>.log #
#################################################################
# Após o reboot a estação EDGE estará pronta para uso

# Tempo estimado de execução:
#                     hh:mm:ss
#    INICIO:          00:00:00
#    REBOOT:          00:05:08
#    RETORNO DO BOOT: 00:10:43
#    TERMINO:         00:32:36
#-----------------------------

##### Instalação do Agente de monitoração em estação EDGE #####
###################################################################################
# Requerimentos                                                                   #
# Informações de configuração de monitoramento                                    #
#     Consulte detalhes no github:                                                #
#     https://github.com/Eyeflow-AI/station-monitoring/tree/main/metric-collector #
# Senha do Usuário eyeflow                                                        #
###################################################################################
# Conectar ao servidor com usuário eyeflow
ssh eyeflow@<IP do servidor>
# Download do script de instalação no diretório default do usuário eyeflow
wget https://raw.githubusercontent.com/snsergio/agent/main/install-monitor.sh
# Certifique-se que o arquivos está presente:
ls -l
# O arquivo install-monitor.sh deve aparecer listado
# Certifique-se que é executável:
chmod +x install-monitor.sh
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
##### end of script
<DATA> <HORA>
####################################################################
# LOG file at: /opt/eyeflow/install/monitor-install<date time>.log #
####################################################################
