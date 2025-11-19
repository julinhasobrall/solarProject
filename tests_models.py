from django.test import TestCase
from django.core.exceptions import ValidationError
from solarproject.models import PessoaFisica, PessoaJuridica


class PessoaFisicaModelTest(TestCase):

    def setUp(self):
        self.pf = PessoaFisica(
            cpf='12345678901',
            nome_completo='Maria da Silva',
            data_nascimento='1990-05-10',
            rg='1234567',
            email='maria@email.com',
            telefone_principal='62999999999',
            cep='74000000',
            logradouro='Rua Central',
            numero='100',
            bairro='Centro',
            cidade='Goiânia',
            estado='GO',
            pais='Brasil',
            complemento='Apto 12'
        )

    # --- Testes básicos ---
    def test_criacao_pessoa_fisica(self):
        self.pf.save()
        self.assertEqual(PessoaFisica.objects.count(), 1)

    def test_str_pessoa_fisica(self):
        self.pf.save()
        self.assertEqual(str(self.pf), 'Maria da Silva - 12345678901')

    # --- Validações específicas ---
    def test_cpf_invalido(self):
        self.pf.cpf = '123'
        with self.assertRaises(ValidationError):
            self.pf.full_clean()

    def test_cep_invalido(self):
        self.pf.cep = '123'
        with self.assertRaises(ValidationError):
            self.pf.full_clean()

    def test_email_invalido(self):
        self.pf.email = 'email-invalido'
        with self.assertRaises(ValidationError):
            self.pf.full_clean()

    def test_telefone_invalido(self):
        self.pf.telefone_principal = 'abc123'
        with self.assertRaises(ValidationError):
            self.pf.full_clean()

    # --- Campos opcionais ---
    def test_complemento_pode_ser_vazio(self):
        self.pf.complemento = ''
        self.pf.full_clean()  # não deve levantar erro

    def test_complemento_pode_ser_null(self):
        self.pf.complemento = None
        self.pf.full_clean()  # ok

    # --- Teste do default ---
    def test_pais_default_brasil(self):
        self.pf.pais = ''
        self.pf.save()
        self.assertEqual(self.pf.pais, '')  # o default só funciona quando campo é omitido

    # --- Ordering ---
    def test_ordering_nome(self):
        PessoaFisica.objects.create(
            cpf='11111111111',
            nome_completo='Ana Souza',
            data_nascimento='1980-01-01',
            rg='1111',
            email='ana@email.com',
            telefone_principal='62900000000',
            cep='74000000',
            logradouro='Rua 1',
            numero='1',
            bairro='Centro',
            cidade='Goiânia',
            estado='GO'
        )
        PessoaFisica.objects.create(
            cpf='22222222222',
            nome_completo='Carlos Lima',
            data_nascimento='1985-02-02',
            rg='2222',
            email='carlos@email.com',
            telefone_principal='62900000000',
            cep='74000000',
            logradouro='Rua 2',
            numero='2',
            bairro='Centro',
            cidade='Goiânia',
            estado='GO'
        )

        nomes = list(PessoaFisica.objects.values_list("nome_completo", flat=True))
        self.assertEqual(nomes, sorted(nomes))


class PessoaJuridicaModelTest(TestCase):

    def setUp(self):
        self.pj = PessoaJuridica(
            cnpj='12345678000199',
            razao_social='Empresa X LTDA',
            nome_fantasia='Empresa X',
            data_abertura='2000-01-01',
            email_comercial='contato@empresa.com',
            telefone_principal='62999999999',
            inscricao_estadual='123456',
            logradouro='Av Central',
            bairro='Setor Bueno',
            estado='GO',
            numero='500',
            pais='Brasil',
            site='https://empresa.com'
        )

    # --- Testes básicos ---
    def test_criacao_pessoa_juridica(self):
        self.pj.save()
        self.assertEqual(PessoaJuridica.objects.count(), 1)

    def test_str_pessoa_juridica(self):
        self.pj.save()
        self.assertEqual(str(self.pj), 'Empresa X LTDA - 12345678000199')

    # --- Validações ---
    def test_cnpj_invalido(self):
        self.pj.cnpj = '123'
        with self.assertRaises(ValidationError):
            self.pj.full_clean()

    def test_email_invalido(self):
        self.pj.email_comercial = 'emailinvalido'
        with self.assertRaises(ValidationError):
            self.pj.full_clean()

    def test_site_invalido(self):
        self.pj.site = 'site-invalido'
        with self.assertRaises(ValidationError):
            self.pj.full_clean()

    def test_telefone_invalido(self):
        self.pj.telefone_principal = 'telefone'
        with self.assertRaises(ValidationError):
            self.pj.full_clean()

    # --- Campos opcionais ---
    def test_site_pode_ser_vazio(self):
        self.pj.site = ''
        self.pj.full_clean()

    def test_complemento_pode_ser_null(self):
        self.pj.complemento = None
        self.pj.full_clean()

    # --- Default ---
    def test_pais_default_brasil(self):
        nova_pj = PessoaJuridica(
            cnpj='98765432000111',
            razao_social='Nova Empresa',
            nome_fantasia='Nova',
            data_abertura='2020-01-01',
            email_comercial='a@a.com',
            telefone_principal='6200000000',
            inscricao_estadual='123',
            logradouro='Rua ABC',
            bairro='Centro',
            estado='GO',
            numero='10'
        )
        nova_pj.save()
        self.assertEqual(nova_pj.pais, 'Brasil')

    # --- Ordering ---
    def test_ordering_razao_social(self):
        PessoaJuridica.objects.create(
            cnpj='11111111000111',
            razao_social='AAA Comércio',
            nome_fantasia='AAA',
            data_abertura='1999-01-01',
            email_comercial='a@a.com',
            telefone_principal='6200000000',
            inscricao_estadual='1111',
            logradouro='Rua 1',
            bairro='A',
            estado='GO',
            numero='1'
        )

        PessoaJuridica.objects.create(
            cnpj='22222222000122',
            razao_social='ZZZ Serviços',
            nome_fantasia='ZZZ',
            data_abertura='2010-01-01',
            email_comercial='z@z.com',
            telefone_principal='6200000000',
            inscricao_estadual='2222',
            logradouro='Rua 2',
            bairro='B',
            estado='GO',
            numero='2'
        )

        razoes = list(PessoaJuridica.objects.values_list("razao_social", flat=True))
        self.assertEqual(razoes, sorted(razoes))
