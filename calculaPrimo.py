# Função para verificar se um número é primo
def eh_primo(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True

# Função para a calculadora de número primo
def calculadora_primo():
    try:
        numero = int(input("Digite um número para verificar se é primo: "))
        if eh_primo(numero):
            print(f"O número {numero} é primo.")
        else:
            print(f"O número {numero} não é primo.")
    except ValueError:
        print("Por favor, digite um número inteiro válido.")

# Executando a calculadora
calculadora_primo()
