#-*- coding: utf-8 -*-
from pyboleto.data import BoletoData, custom_property
import os.path

### CAUTION - NÃO TESTADO ###
class BoletoCaixa( BoletoData ):
    '''
        Gera Dados necessários para criação de boleto para o banco Caixa
        Economica Federal
    '''

    def __init__(self, *args, **kwargs):
        super(BoletoCaixa , self).__init__(*args, **kwargs)

        self.codigo_banco = "104"
        self.moeda = "9"
        self.local_pagamento = "Preferencialmente nas Casas Lotéricas e Agências da Caixa"
        self.logo_image_path = os.path.dirname(__file__) + \
            "/../media/logo_bancocaixa.jpg"

        ''' 
            Carteira SR: 80, 81 ou 82  -  
            Carteira CR: 90 (Confirmar com gerente qual usar)
        '''
        self.inicio_nosso_numero = '80'

    # Nosso numero (sem dv) sao 17 digitos
    def _nosso_numero_get(self):
        return self._nosso_numero
    '''
        Nosso Número sem DV, máximo 8 chars
    '''
    def _nosso_numero_set(self, val):
        try:
            self._nosso_numero = self.inicio_nosso_numero + \
                str(self.formata_numero(val, 15))
        except AttributeError:
            pass

    nosso_numero = property(_nosso_numero_get, _nosso_numero_set)

    @property
    def dv_nosso_numero(self):
        resto2 = self.modulo11(self.nosso_numero.split('-')[0],9,1)
        digito = 11 - resto2
        if digito == 10 or digito == 11:
            dv = 0
        else:
            dv = digito
        return dv

    '''
        agencia do cedente sem DV
    '''
    agencia_cedente = custom_property('agencia_cedente', 4)

    conta_cedente = custom_property('conta_cedente', 11)

    # Numero para o codigo de barras com 44 digitos
    @property
    def barcode(self):
        num = "%3s%1s%1s%4s%10s%25s" % (
            self.codigo_banco,
            self.moeda,
            'X',
            self.fator_vencimento,
            self.formata_valor(self.valor_documento,10),
            self.campo_livre
        )
        dv = self.calculate_dv_barcode(num.replace('X', '', 1))
        num = num.replace('X', str(dv), 1)
        return num

    @property
    def campo_livre(self):
        num = '%7s%3s%1s%3s%1s%9s' % (
            self.conta_cedente.replace('-', '')[-7:],
            self.nosso_numero[3:6],
            self.nosso_numero[0],
            self.nosso_numero[6:9],
            self.nosso_numero[1],
            self.nosso_numero[8:18]
        )
        num += str(self.modulo11(num))
        return num

    @property
    def linha_digitavel(self):
        '''
            Monta a linha que o cliente pode utilizar para digitar se o código 
            de barras não puder ser lido

            CAMPO 1:
            ========
            1 a 3    Número do banco (1 a 3 do barcode)
            4        Código da Moeda - 9 para Real  (4 do barcode)
            5 a 9    5 primeiras posições do campo livre (20 a 24 do barcode)
            10       Dígito verificador deste campo

            CAMPO 2:
            ========
            11 a 20  Posições 6 a 15 do campo livre (25 a 34 do barcode)
            21       Dígito verificador deste campo

            CAMPO 3:
            ========
            32 a 43  Posições 16 a 25 do campo livre (35 a 44 do barcode)
            44       Dígito verificador deste campo

            CAMPO 4:
            ========
            45       Dígito Verificador geral do código de barras (5 do barcode)

            CAMPO 5:
            ========
            46 a 50  Fator de vencimento (6 a 9 do barcode)
            51 a 60  Valor Nominal do título (10 a 19 do barcode)
        '''
        linha = self.barcode
        if not linha:
            BoletoException("Boleto doesn't have a barcode")

        ## campo1
        campo1 = linha[0:3] + linha[3] + linha[19:24]
        campo1 += str(self.modulo10(campo1))
        campo1 = '%s.%s' % (campo1[:5], campo1[5:])

        ## campo2
        campo2 = linha[24:34]
        campo2 += str(self.modulo10(campo2))
        campo2 = '%s.%s' % (campo2[:5], campo2[5:])

        ## campo3
        campo3 = linha[34:44]
        campo3 += str(self.modulo10(campo3))
        campo3 = '%s.%s' % (campo3[:5], campo3[5:])

        ## campo4
        campo4 = linha[4]

        ## campo5
        campo5 = linha[5:9] + linha[9:19]

        return "%s %s %s %s %s" % (campo1, campo2, campo3, campo4, campo5)

    def format_nosso_numero(self):
        return self._nosso_numero + '-' + str(self.dv_nosso_numero)

    @property
    def agencia_conta_cedente(self):
        val = self.conta_cedente.split('-')
        val[0] = val[0][-6:]
        return "%s/%s" % (self.agencia_cedente, '-'.join(val))
