import requests
import json

# Lista para armazenar os dados dos assegurados
assegurados = []

# Função para consultar o CEP na API do ViaCEP
def consultar_cep(cep):
    try:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        response.raise_for_status()  

        endereco = response.json()
        if 'cep' in endereco:
            return endereco
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação ao ViaCEP: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar resposta JSON: {e}")
        return None

# Função para enviar o guincho com base no endereço e modalidade do guincho certo
def enviar_guincho(endereco, modalidade, nome):
    if endereco:
        print("Endereço encontrado para", nome + ":")
        print(f"CEP: {endereco['cep']}")
        print(f"Rua: {endereco['logradouro']}")
        print(f"Bairro: {endereco['bairro']}")
        print(f"Cidade: {endereco['localidade']}")
        print(f"Estado: {endereco['uf']}")
        print(f"Guincho enviado na modalidade: {modalidade}")
    else:
        print("CEP não encontrado para", nome + ". Não é possível enviar o guincho.")

# Função para criar/cadastrar um novo assegurado e adicionar à lista
def criar_assegurado(apolice, cpf, peso_veiculo, cep, nome):
    # Verificar se o CPF é único
    for assegurado_existente in assegurados:
        if assegurado_existente['CPF'] == cpf:
            print("CPF já cadastrado. Não é permitido cadastrar o mesmo CPF mais de uma vez.")
            return

    # Outras verificações de dados, se necessário
    if not apolice or not cpf or not peso_veiculo or not cep or not nome:
        print("Dados incompletos. Todos os campos devem ser preenchidos.")
        return

    novo_assegurado = {'Apólice': apolice, 'CPF': cpf, 'Nome': nome, 'Alteracao': None, 'PesoVeiculo': peso_veiculo, 'CEP': cep}
    assegurados.append(novo_assegurado)
    print(f"Assegurado {nome} cadastrado com sucesso.")

# Função para consultar os dados de um assegurado na lista
def consultar_assegurado(apolice):
    encontrado = False
    for assegurado in assegurados:
        if assegurado['Apólice'] == apolice:
            print(f"Dados do assegurado {assegurado['Nome']}:")
            print(f"Número da apólice: {apolice}")
            print(f"CPF: {assegurado['CPF']}")
            print(f"Alteração: {assegurado['Alteracao']}")
            print(f"Peso do veículo: {assegurado['PesoVeiculo']}")
            print(f"CEP: {assegurado['CEP']}")
            encontrado = True
            break
    if not encontrado:
        print("Assegurado não encontrado.")

# Função para alterar dados do assegurado
def alterar_dados(apolice, alteracao, peso_veiculo, cep):
    for assegurado in assegurados:
        if assegurado['Apólice'] == apolice:
            assegurado['Alteracao'] = alteracao
            assegurado['PesoVeiculo'] = peso_veiculo
            assegurado['CEP'] = cep
            print("Dados do assegurado atualizados com sucesso.")
            return
    print("Assegurado não encontrado.")

# Função para excluir dados do assegurado na lista
def excluir_dados(apolice):
    for assegurado in assegurados:
        if assegurado['Apólice'] == apolice:
            assegurados.remove(assegurado)
            print("Assegurado excluído com sucesso.")
            return
    print("Assegurado não encontrado.")

# Solicitando o guincho certo, o sistema busca a localização precisa do cep, então é importante colocar o cep correto,
# além disso o sistema vai escolher o guincho ideal de acordo com o peso do veículo.
def solicitar_guincho():
    try:
        apolice = input("Digite o número da apólice: ")
        cpf = input("Digite o seu CPF: ")

        # Verificar se a apólice está cadastrada
        assegurado_encontrado = None
        for assegurado in assegurados:
            if assegurado['Apólice'] == apolice and assegurado['CPF'] == cpf:
                assegurado_encontrado = assegurado
                break

        if assegurado_encontrado:
            print(f"Olá, {assegurado_encontrado['Nome']}!")
            print("Dados do assegurado:")
            print(f"Número da apólice: {apolice}")
            print(f"CPF: {cpf}")
            print(f"Peso do veículo: {assegurado_encontrado['PesoVeiculo']}")
            cep = input(f"Confirme o CEP ou digite um novo CEP: ({assegurado_encontrado['CEP']}): ")
        else:
            print("Apólice não encontrada ou CPF inválido. Preencha os dados necessários para solicitar o guincho.")
            nome = input("Digite o seu nome: ")
            cep = input("Digite o CEP de onde você precisa do guincho: ")

        alteracao = input("O veículo sofreu alguma alteração? Digite 's' para sim ou 'n' para não: ")

        if alteracao.lower() == "n":
            print("Ok,")
        elif alteracao.lower() == "s":
            tipo_alteracao = input("Qual alteração foi feita? ")
            print("Entendi a alteração feita foi:", tipo_alteracao)
        else:
            print("Desculpe, não entendi a resposta. Por favor, responda com 's' ou 'n'.")

        peso_veiculo = float(input("Digite o peso do veículo: "))
        if peso_veiculo <= 2.5:
            modalidade = "Plataforma"
        elif peso_veiculo <= 4.0:
            modalidade = "Guincho Cegonha"
        elif peso_veiculo <= 6.0:
            modalidade = "Guincho Rotativo"
        elif peso_veiculo <= 8.0:
            modalidade = "Guincho Prancha Rebaixada"

        endereco = consultar_cep(cep)
        enviar_guincho(endereco, modalidade, assegurado_encontrado['Nome'] if assegurado_encontrado else nome)
    except ValueError as e:
        print(f"Erro ao ler entrada do usuário: {e}")

# Menu principal
try:
    while True:
        print("\nBem vindo(a) a Porto Seguro! Escolha a opção desejada:")
        print("1 - Solicitar guincho")
        print("2 - Fazer cadastro")
        print("3 - Consultar cadastro")
        print("4 - Alterar dados")
        print("5 - Excluir cadastro")
        print("6 - Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            solicitar_guincho()
            resposta = input("Deseja realizar uma nova operação? Digite 's' para sim ou 'n' para não: ")
            if resposta.lower() == 'n':
                break
        elif opcao == '2':
            apolice = input("Digite o número da apólice: ")
            cpf = input("Digite o seu CPF: ")
            peso_veiculo = input("Digite o peso do seu veículo: ")
            cep = input("Digite o seu CEP: ")
            nome = input("Digite o seu nome: ")
            criar_assegurado(apolice, cpf, peso_veiculo, cep, nome)
        elif opcao == '3':
            apolice = input("Digite o número da apólice do assegurado a ser consultado: ")
            consultar_assegurado(apolice)
        elif opcao == '4':
            apolice = input("Digite o número da apólice do assegurado a ser alterado: ")
            alteracao = input("Digite a alteração feita no veículo: ")
            peso_veiculo = float(input("Digite o peso do veículo: "))
            cep = input("Digite o CEP de onde você precisa do guincho: ")
            alterar_dados(apolice, alteracao, peso_veiculo, cep)
        elif opcao == '5':
            apolice = input("Digite o número da apólice do assegurado a ser excluído: ")
            excluir_dados(apolice)
        elif opcao == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")

except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

finally:
    print("Atendimento encerrado. A Porto Seguro agradece a preferência!")