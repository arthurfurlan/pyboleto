# -*- coding: utf-8
from pyboleto.data import BoletoData, custom_property
import os.path

### CAUTION - NÃO TESTADO ###
class BoletoBB( BoletoData ):
    '''
        Gera Dados necessários para criação de boleto para o Banco do Brasil
    '''

    def __init__(self, format_convenio, format_nnumero, *args, **kwargs):
        '''
            Construtor para boleto do Banco deo Brasil

            Args:
                format_convenio Formato do convenio 6, 7 ou 8
                format_nnumero Formato nosso numero 1 ou 2
        '''
        super(BoletoBB , self).__init__(*args, **kwargs)

        self.codigo_banco = "001"
        self.carteira = 18
        self.logo_image_path = os.path.dirname(__file__) + \
            "/../media/logo_bb.jpg"

        # Size of convenio 6, 7 or 8
        self.format_convenio = format_convenio
        
        #  Nosso Numero format. 1 or 2
        #  1: Nosso Numero with 5 positions
        #  2: Nosso Numero with 17 positions
        self.format_nnumero = format_nnumero

    def format_nosso_numero(self):
        return "%s-%s" % (
            self.nosso_numero, 
            self.dv_nosso_numero
        )

    # Nosso numero (sem dv) sao 11 digitos
    def _get_nosso_numero(self):
        return self.convenio + self._nosso_numero   

    def _set_nosso_numero(self,val):
        val = str(val)
        if self.format_convenio is 6:
            if self.format_nnumero is 1:
                nn = val.zfill(5)
            elif self.format_nnumero is 2:
                nn = val.zfill(17)
        elif self.format_convenio is 7:
            nn = val.zfill(10)
        elif self.format_convenio is 8:
            nn = val.zfill(9)
        self._nosso_numero = nn

    nosso_numero = property(_get_nosso_numero, _set_nosso_numero)

    def _get_convenio(self):
        return self._convenio

    def _set_convenio(self, val):
        self._convenio = str(val).ljust(self.format_convenio, '0')
    convenio = property(_get_convenio, _set_convenio)
    
    @property
    def agencia_conta_cedente(self):
        return "%s-%s / %s-%s" % (
            self.agencia_cedente,
            self.modulo11(self.agencia_cedente),
            self.conta_cedente,
            self.modulo11(self.conta_cedente)
        )

    @property
    def dv_nosso_numero(self):
        return self.modulo11(self.nosso_numero)

    agencia_cedente = custom_property('agencia_cedente', 4)

    conta_cedente = custom_property('conta_cedente', 8)

    # Numero para o codigo de barras com 44 digitos
    @property
    def barcode(self):
        if self.format_convenio in (7, 8):
            num = "%3s%1s%1s%4s%10s%6s%s%s" % (
                self.codigo_banco,
                self.moeda,
                'X',
                self.fator_vencimento,
                self.formata_valor(self.valor_documento,10),
                '000000',
                self.nosso_numero, 
                self.carteira
            )
        elif self.format_convenio is 6:
            if self.format_nnumero is 1:
                num = "%3s%1s%1s%4s%10s%s%s%s%s" % (
                    self.codigo_banco,
                    self.moeda,
                    'X',
                    self.fator_vencimento,
                    self.formata_valor(self.valor_documento,10),
                    self.nosso_numero, 
                    self.agencia_cedente,
                    self.conta_cedente,
                    self.carteira
                )
            if self.format_nnumero is 2:
                num = "%3s%1s%1s%4s%10s%s%2s" % (
                    self.codigo_banco,
                    self.moeda,
                    'X',
                    self.fator_vencimento,
                    self.formata_valor(self.valor_documento,10),
                    self.nosso_numero, 
                    '21' # numero do serviço
                )
            
        
        dv = self.modulo11(num.replace('X', '', 1))

        num = num.replace('X', str(dv), 1)
        return num

