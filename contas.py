import requests


class Conta:
    def __init__(self, nome, numero, limite=1000):
        self._nome = self.formata_nome(nome.lower())
        self._numero = str(numero)
        self._saldo = 0
        self._bandeira = self.valida_numero(self.numero)
        self._limite = limite
        self._agencia = 20
        self._moeda = 'real'

    def __str__(self):
        if self._moeda == 'real':
            return f'Titular: {self.nome}, Numero: {self.numero}, Bandeira: {self.bandeira}, ' \
                   f'Saldo: R${self.saldo}, Limite: R${self.limite}, Agência: {self.agencia}'
        else:
            return f'Titular: {self.nome}, Numero: {self.numero}, Bandeira: {self.bandeira}, ' \
                   f'Saldo: ${self.saldo}, Limite: ${self.limite}, Agência: {self.agencia}'

    def __eq__(self, other):
        if self.numero == other.numero:
            return True
        else:
            return False

    @property
    def nome(self):
        return self._nome

    @property
    def limite(self):
        return self._limite

    @property
    def agencia(self):
        return self._agencia

    @property
    def numero(self):
        return self.formata_numero(self._numero)

    @property
    def bandeira(self):
        return self._bandeira

    @property
    def saldo(self):
        return self._saldo

    @property
    def moeda(self):
        return self._moeda

    @staticmethod
    def formata_nome(nome):
        separa_nome = nome.lstrip().split(' ')
        nome_maiusculo = [nome.title() for nome in separa_nome]
        nome_inteiro = f''
        for nome in nome_maiusculo:
            nome_inteiro += nome + ' '
        return nome_inteiro.rstrip()

    @staticmethod
    def formata_numero(numero):
        primeira_parte = numero[0:4]
        segunda_parte = numero[4:8]
        terceira_parte = numero[8:12]
        quarta_parte = numero[12:]
        return f'{primeira_parte} {segunda_parte} {terceira_parte} {quarta_parte}'

    @staticmethod
    def valida_numero(numero):
        numeros_validos = [14, 15, 16]
        numero = numero.replace(' ', '')
        if numero[0] == '3' and len(numero) in numeros_validos:
            return 'American Express'
        elif numero[0] == '4' and len(numero) in numeros_validos:
            return 'Visa'
        elif numero[0] == '5' and len(numero) in numeros_validos:
            return 'Mastercard'
        else:
            raise ValueError('Número inválido.')

    def mostra_o_saldo(self):
        if self.moeda == 'real':
            print(f'O saldo do titular {self.nome} é de R${self.saldo}')
        else:
            print(f'O saldo do titular {self.nome} é de ${self.saldo}')

    def depositar_na_conta(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'Depositado com sucesso na conta do titular: {self.nome}')
        else:
            raise ValueError('Não se pode depositar este valor.')

    def sacar_da_conta(self, valor):
        if 0 < valor <= self.saldo + self.limite:
            self._saldo -= valor
            print(f'Valor retirado com sucesso!')
            self.mostra_o_saldo()
            return True
        else:
            raise ValueError('O valor solicitado está indisponível.')

    def transferir_para_outra_conta(self, conta, valor):
        if self.sacar_da_conta(valor):
            if conta.moeda == self.moeda:
                conta.depositar_na_conta(valor)
            elif conta.moeda == 'dolar' and self.moeda == 'real':
                r = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL')
                valor_dolar = float(r.json()['USDBRL']['bid'])
                conta.depositar_na_conta(round(valor/valor_dolar))
            elif conta.moeda == 'real' and self.moeda == 'dolar':
                r = requests.get('https://economia.awesomeapi.com.br/last/BRL-USD')
                valor_real_em_dolar = float(r.json()['BRLUSD']['bid'])
                conta.depositar_na_conta(round(valor/valor_real_em_dolar))
        else:
            raise ValueError('Não foi possivel realizar a transação.')

    def transformar_saldo_de_real_para_dolar(self):
        r = requests.get('https://economia.awesomeapi.com.br/last/BRL-USD')
        valor_real_em_dolar = float(r.json()['BRLUSD']['bid'])
        if self.moeda == 'real':
            self._saldo = round(self.saldo * valor_real_em_dolar)
            self._limite = round(self._limite * valor_real_em_dolar)
            self._moeda = 'dolar'
            print(f'Saldo da conta convertido para doláres!')
            self.mostra_o_saldo()
        else:
            raise ValueError('O saldo já está em dólares.')

    def transformar_saldo_de_dolar_para_real(self):
        r = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL')
        valor_dolar = float(r.json()['USDBRL']['bid'])
        if self.moeda == 'dolar':
            self._saldo = round(self.saldo * valor_dolar)
            self._limite = round(self._limite * valor_dolar)
            self._moeda = 'real'
            print(f'Saldo da conta convertido para reais!')
            self.mostra_o_saldo()
        else:
            raise ValueError('O saldo já está em reais.')
