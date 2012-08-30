# -*- coding: utf-8 -*-
import unittest
import datetime

from pyboleto.bank.caixa import BoletoCaixa

class TestBancoCaixa(unittest.TestCase):
    def setUp(self):
        d = BoletoCaixa()
        d.carteira = 'SR'
        d.inicio_nosso_numero = '24'
        d.agencia_cedente = '1565'
        d.conta_cedente = '414-3'
        d.data_vencimento = datetime.date(2011, 2, 5)
        d.data_documento = datetime.date(2011, 1, 18)
        d.data_processamento = datetime.date(201, 1, 18)
        d.valor_documento = 355.00
        d.nosso_numero = '19525086'
        d.numero_documento = '19525086'
        self.dados = d

    def test_linha_digitavel(self):
        self.assertEqual(self.dados.linha_digitavel, 
            '10490.00415 43000.200048 01952.508669 6 48690000035500'
        )
    
    def test_tamanho_codigo_de_barras(self):
        self.assertEqual(len(self.dados.barcode), 44)

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados.barcode,
            '10496486900000355000004143000200040195250866'
        )


class TestBancoCaixaSIGCB(unittest.TestCase):

    def setUp(self):
        d = BoletoCaixa()
        d.carteira = 'SR'
        d.inicio_nosso_numero = '24'
        d.agencia_cedente = '1565'
        d.conta_cedente = '414-3'
        d.data_vencimento = datetime.date(2011, 2, 5)
        d.data_documento = datetime.date(2011, 1, 18)
        d.data_processamento = datetime.date(201, 1, 18)
        d.valor_documento = 355.00
        d.nosso_numero = '19525086'
        d.numero_documento = '19525086'
        self.dados = d

        self.barcode = self.dados.barcode
        self.linhadig = self.dados.linha_digitavel.replace('.', '').replace(' ', '')
        self.campolivre = self.dados.campo_livre
        self.nossonumero = self.dados.nosso_numero


    ## CODIGO DE BARRAS

    def test_barcode_codigobanco(self):
        self.assertEquals(len(self.barcode[0:3]), 3)
        self.assertEquals(self.barcode[0:3], self.dados.codigo_banco)
        self.assertEquals(self.barcode[0:3], '104') ## CAIXA ECONOMICA

    def test_barcode_codigomoeda(self):
        self.assertEquals(len(self.barcode[3]), 1)
        self.assertEquals(self.barcode[3], self.dados.moeda)
        self.assertEquals(self.barcode[3], '9')     ## BRL (R$)

    def test_barcode_digitoverificadorgeral(self):
        self.assertEquals(len(self.barcode[4]), 1)
        bc = self.barcode[:4] + self.barcode[5:]
        self.assertEquals(self.barcode[4], str(self.dados.calculate_dv_barcode(bc)))
        self.assertEquals(self.barcode[4], '6')

    def test_barcode_fatorvencimento(self):
        self.assertEquals(len(self.barcode[5:9]), 4)
        self.assertEquals(self.barcode[5:9], str(self.dados.fator_vencimento))
        self.assertEquals(self.barcode[5:9], '4869')

    def test_barcode_valordocumento(self):
        self.assertEquals(len(self.barcode[9:19]), 10)
        valor_documento = '%010d' % (float(self.dados.valor_documento) * 100)
        self.assertEquals(self.barcode[9:19], valor_documento)
        self.assertEquals(self.barcode[9:19], '0000035500') ## R$355.00

    def test_barcode_campolivre(self):
        self.assertEquals(len(self.barcode[19:44]), 25)
        self.assertEquals(self.barcode[19:44], self.campolivre)
        self.assertEquals(self.barcode[19:44], '0004143000200040195250866')

    def test_barcode_campolivre_codigocedente(self):
        self.assertEquals(len(self.campolivre[0:6]), 6)
        self.assertEquals(self.barcode[19:25], self.campolivre[0:6])
        self.assertEquals(self.barcode[19:25], self.dados.conta_cedente.split('-')[0].lstrip('0').zfill(6))
        self.assertEquals(self.barcode[19:25], '000414')

    def test_barcode_campolivre_digitoverificadorcodigocedente(self):
        self.assertEquals(len(self.campolivre[6]), 1)
        self.assertEquals(self.barcode[25], self.campolivre[6])
        self.assertEquals(self.barcode[25], self.dados.conta_cedente.split('-')[1])
        self.assertEquals(self.barcode[25], '3')

    def test_barcode_campolivre_sequencia1(self):
        self.assertEquals(len(self.campolivre[7:10]), 3)
        self.assertEquals(self.barcode[26:29], self.campolivre[7:10])
        self.assertEquals(self.barcode[26:29], self.nossonumero[2:5])
        self.assertEquals(self.barcode[26:29], '000')

    def test_barcode_campolivre_constante1(self):
        self.assertEquals(len(self.campolivre[10]), 1)
        self.assertEquals(self.barcode[29], self.campolivre[10])
        self.assertEquals(self.barcode[29], self.nossonumero[0])
        self.assertEquals(self.barcode[29], '2')    ## SR (SEM REGISTRO)

    def test_barcode_campolivre_sequencia2(self):
        self.assertEquals(len(self.campolivre[11:14]), 3)
        self.assertEquals(self.barcode[30:33], self.campolivre[11:14])
        self.assertEquals(self.barcode[30:33], self.nossonumero[5:8])
        self.assertEquals(self.barcode[30:33], '000')

    def test_barcode_campolivre_constante2(self):
        self.assertEquals(len(self.campolivre[14]), 1)
        self.assertEquals(self.barcode[33], self.campolivre[14])
        self.assertEquals(self.barcode[33], self.nossonumero[1])
        self.assertEquals(self.barcode[33], '4')    ## EMISSAO CEDENTE

    def test_barcode_campolivre_sequencia3(self):
        self.assertEquals(len(self.campolivre[15:24]), 9)
        self.assertEquals(self.barcode[34:43], self.campolivre[15:24])
        self.assertEquals(self.barcode[34:43], self.nossonumero[8:17])
        self.assertEquals(self.barcode[34:43], self.dados.numero_documento.zfill(9))
        self.assertEquals(self.barcode[34:43], '019525086')

    def test_barcode_campolivre_digitoverificadorcampolivre(self):
        self.assertEquals(len(self.campolivre[24]), 1)
        self.assertEquals(self.barcode[43], str(self.dados.modulo11(self.barcode[19:43])))
        self.assertEquals(self.barcode[43], self.campolivre[24])
        self.assertEquals(self.barcode[43], '6')

    def test_barcode_nossonumero(self):
        self.assertEquals(len(self.nossonumero), 17)

    def test_barcode_nossonumero_constante1(self):
        self.assertEquals(len(self.nossonumero[0]), 1)
        self.assertEquals(self.nossonumero[0], '2')    ## SR (SEM REGISTRO)

    def test_barcode_nossonumero_constante2(self):
        self.assertEquals(len(self.nossonumero[1]), 1)
        self.assertEquals(self.nossonumero[1], '4')    ## EMISSAO CEDENTE

    def test_barcode_nossonumero_sequencia(self):
        self.assertEquals(len(self.nossonumero[2:]), 15)
        self.assertEquals(self.nossonumero[2:], '%015d' % int(self.dados.numero_documento))


    ## LINHA DIGITAVEL

    def test_linhadig_campo1(self):
        campo1 = self.barcode[0:4] + self.barcode[19:24]
        self.assertEquals(len(campo1), 9)
        self.assertEquals(self.linhadig[0:9], campo1)

    def test_linhadig_dvcampo1(self):
        campo1 = self.barcode[0:4] + self.barcode[19:24]
        dvcampo1 = self.dados.modulo10(campo1)
        self.assertEquals(self.linhadig[9], str(dvcampo1))

    def test_linhadig_campo2(self):
        campo2 = self.barcode[24:34]
        self.assertEquals(len(campo2), 10)
        self.assertEquals(self.linhadig[10:20], campo2)

    def test_linhadig_dvcampo2(self):
        campo2 = self.barcode[24:34]
        dvcampo2 = self.dados.modulo10(campo2)
        self.assertEquals(self.linhadig[20], str(dvcampo2))

    def test_linhadig_campo3(self):
        campo3 = self.barcode[34:44]
        self.assertEquals(len(campo3), 10)
        self.assertEquals(self.linhadig[21:31], campo3)

    def test_linhadig_dvcampo3(self):
        campo3 = self.barcode[34:44]
        dvcampo3 = self.dados.modulo10(campo3)
        self.assertEquals(self.linhadig[31], str(dvcampo3))

    def test_linhadig_campo4(self): ## digito verificador geral
        self.assertEquals(self.linhadig[32], self.barcode[4])

    def test_linhadig_campo5_parte1(self):
        campo5 = self.barcode[5:9]
        self.assertEquals(len(campo5), 4)
        self.assertEquals(self.linhadig[33:37], campo5)

    def test_linhadig_campo5_parte1(self):
        campo5 = self.barcode[9:19]
        self.assertEquals(len(campo5), 10)
        self.assertEquals(self.linhadig[37:47], campo5)


if __name__ == '__main__':
    unittest.main()
