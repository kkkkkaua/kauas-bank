from contas import Conta


class ContaPoupanca(Conta):
    contas = Conta.contas

    def __init__(self, nome, numero, limite=1000):
        super().__init__(nome, numero)
        self._tipo = 'poupanca'
        self._contador_saques = 0
        self._contador_transferencia = 0

    @property
    def contador_saques(self):
        return self._contador_saques

    @property
    def contador_transferencia(self):
        return self._contador_transferencia

    def sacar_da_conta(self, valor):
        if self.bloqueia_movimentacoes():
            super().sacar_da_conta(valor)
            self._contador_saques += 1
        else:
            raise ValueError('Não se pode sacar mais que duas vezes no mês.')

    def transferir_para_outra_conta(self, conta, valor):
        if self.bloqueia_movimentacoes():
            super().transferir_para_outra_conta(conta, valor)
            self._contador_transferencia += 1
        else:
            raise ValueError('Não se pode transferir mais que duas vezes no mês.')

    def bloqueia_movimentacoes(self):
        if self.contador_saques >= 2 or self._contador_transferencia >= 2:
            return False
        else:
            return True
