#!/usr/bin/env python3
"""
Analisador de Publicações do Diário Oficial de Minas Gerais
Extrai e tabula publicações de qualquer órgão especificado pelo usuário
"""

import json
import re
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys


class AnalisadorDiarioOficial:
    """
    Classe para análise e extração de publicações do Diário Oficial
    """
    
    def __init__(self, arquivo_json):
        """
        Inicializa o analisador com o arquivo JSON do diário
        
        Args:
            arquivo_json: Caminho para o arquivo JSON
        """
        self.arquivo_json = arquivo_json
        self.dados = self._carregar_dados()
        
        # Padrões de tipos de publicação
        self.tipos_publicacao = {
            'Decreto': r'\b(DECRETO)\s+N[ºª°]?\s*\d+',
            'Portaria': r'\b(PORTARIA)\s+N[ºª°]?\s*\d+',
            'Resolução': r'\b(RESOLU[ÇC][ÃA]O)\s+N[ºª°]?\s*\d+',
            'Edital': r'\b(EDITAL)\s+N[ºª°]?\s*\d+',
            'Aviso': r'\b(AVISO)\s+N[ºª°]?\s*\d+',
            'Despacho': r'\b(DESPACHO)\s*(DO)?\s*(GOVERNADOR|SECRETÁRIO|PRESIDENTE)?',
            'Extrato': r'\b(EXTRATO)\s+(DE\s+)?(CONTRATO|TERMO|CONV[ÊE]NIO)',
            'Comunicado': r'\b(COMUNICADO)',
            'Termo de Colaboração': r'\b(TERMO\s+DE\s+COLABORA[ÇC][ÃA]O)',
            'Termo de Fomento': r'\b(TERMO\s+DE\s+FOMENTO)',
            'Convênio': r'\b(CONV[ÊE]NIO)\s+N[ºª°]?\s*\d+',
            'Contrato': r'\b(CONTRATO)\s+N[ºª°]?\s*\d+',
            'Licitação': r'\b(LICITA[ÇC][ÃA]O|PREG[ÃA]O|CONCORR[ÊE]NCIA|TOMADA\s+DE\s+PRE[ÇC]OS)',
            'Nomeação': r'\b(NOMEA[ÇC][ÃA]O|NOMEAR)',
            'Exoneração': r'\b(EXONERA[ÇC][ÃA]O|EXONERAR)',
            'Designação': r'\b(DESIGNA[ÇC][ÃA]O|DESIGNAR)',
            'Dispensa': r'\b(DISPENSA)\s+(DE\s+)?(LICITAÇÃO|PONTO)',
            'Retificação': r'\b(RETIFICA[ÇC][ÃA]O)',
            'Ratificação': r'\b(RATIFICA[ÇC][ÃA]O)',
            'Homologação': r'\b(HOMOLOGA[ÇC][ÃA]O)',
            'Ata': r'\b(ATA)\s+(DE\s+)?(REGISTRO\s+DE\s+PRE[ÇC]OS)?'
        }
    
    def _carregar_dados(self):
        """Carrega os dados do arquivo JSON"""
        print(f"Carregando dados de {self.arquivo_json}...")
        with open(self.arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        print(f"✓ {len(dados)} páginas carregadas")
        return dados
    
    def _normalizar_texto(self, texto):
        """Normaliza texto para comparação (remove acentos, converte para maiúsculas)"""
        if not texto:
            return ""
        # Mapeamento de caracteres acentuados
        mapa = str.maketrans(
            'áàâãäéèêëíìîïóòôõöúùûüçñÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ',
            'aaaaaeeeeiiiiooooouuuucnAAAAAEEEEIIIIOOOOOUUUUCN'
        )
        return texto.translate(mapa).upper()
    
    def _identificar_tipo_publicacao(self, conteudo):
        """
        Identifica o tipo de publicação com base no conteúdo
        
        Returns:
            tuple: (tipo, numero_identificacao)
        """
        conteudo_upper = conteudo.upper()
        
        for tipo, padrao in self.tipos_publicacao.items():
            match = re.search(padrao, conteudo_upper, re.IGNORECASE)
            if match:
                # Tentar extrair número/identificação
                numero_match = re.search(r'N[ºª°]?\s*(\d+[/-]?\d*)', match.group(0))
                numero = numero_match.group(1) if numero_match else ""
                return tipo, numero
        
        return "Outros", ""
    
    def _extrair_resumo(self, conteudo, max_chars=200):
        """Extrai um resumo do conteúdo"""
        # Remove quebras de linha excessivas e espaços
        texto_limpo = re.sub(r'\s+', ' ', conteudo).strip()
        
        if len(texto_limpo) <= max_chars:
            return texto_limpo
        
        # Tenta pegar até o final da primeira sentença
        match = re.search(r'^(.{50,200}?)[.!?]\s', texto_limpo)
        if match:
            return match.group(1) + "..."
        
        # Se não encontrar, corta no caractere
        return texto_limpo[:max_chars] + "..."
    
    def buscar_orgao(self, nome_orgao, variantes=None):
        """
        Busca todas as publicações relacionadas a um órgão
        
        Args:
            nome_orgao: Nome do órgão a buscar
            variantes: Lista opcional de variantes/siglas do nome do órgão
            
        Returns:
            DataFrame com as publicações encontradas
        """
        print(f"\n{'='*80}")
        print(f"BUSCANDO PUBLICAÇÕES DE: {nome_orgao}")
        print(f"{'='*80}\n")
        
        # Criar lista de termos de busca
        termos_busca = [self._normalizar_texto(nome_orgao)]
        if variantes:
            termos_busca.extend([self._normalizar_texto(v) for v in variantes])
        
        print(f"Termos de busca: {', '.join(termos_busca)}")
        
        publicacoes = []
        
        for idx, pagina in enumerate(self.dados, 1):
            if idx % 100 == 0:
                print(f"Processando página {idx}/{len(self.dados)}...")
            
            conteudo = pagina.get('Conteudo', '')
            conteudo_normalizado = self._normalizar_texto(conteudo)
            
            # Verificar se algum termo está presente
            encontrado = any(termo in conteudo_normalizado for termo in termos_busca)
            
            if encontrado:
                # Identificar tipo de publicação
                tipo, numero = self._identificar_tipo_publicacao(conteudo)
                
                # Criar referência completa
                data_pub = pagina.get('DataPublicacao', '').split('T')[0]
                referencia = (f"Diário Oficial MG - Edição {pagina.get('Edicao', 'N/A')}, "
                            f"Página {pagina.get('Pagina', 'N/A')}, "
                            f"Data {data_pub}")
                
                publicacoes.append({
                    'Tipo de Publicação': tipo,
                    'Número/Identificação': numero,
                    'Assunto/Resumo': self._extrair_resumo(conteudo, 150),
                    'Conteúdo Completo': conteudo,
                    'Data de Publicação': data_pub,
                    'Edição': pagina.get('Edicao', ''),
                    'Página': pagina.get('Pagina', ''),
                    'Ano': pagina.get('Ano', ''),
                    'Caderno': pagina.get('Titulo', ''),
                    'Referência Completa': referencia
                })
        
        print(f"\n✓ {len(publicacoes)} publicações encontradas!")
        
        if len(publicacoes) == 0:
            print("\n⚠ Nenhuma publicação encontrada. Verifique o nome do órgão.")
            return pd.DataFrame()
        
        return pd.DataFrame(publicacoes)
    
    def gerar_planilha(self, df, nome_orgao, arquivo_saida=None):
        """
        Gera planilha Excel com os resultados
        
        Args:
            df: DataFrame com os dados
            nome_orgao: Nome do órgão para nomenclatura
            arquivo_saida: Nome do arquivo de saída (opcional)
        """
        if df.empty:
            print("⚠ Nenhum dado para exportar.")
            return None
        
        # Gerar nome do arquivo se não fornecido
        if not arquivo_saida:
            nome_limpo = re.sub(r'[^\w\s-]', '', nome_orgao).strip().replace(' ', '_')
            data_hoje = datetime.now().strftime('%Y%m%d')
            arquivo_saida = f"publicacoes_{nome_limpo}_{data_hoje}.xlsx"
        
        # Garantir extensão .xlsx
        if not arquivo_saida.endswith('.xlsx'):
            arquivo_saida += '.xlsx'
        
        print(f"\nGerando planilha: {arquivo_saida}")
        
        # Criar writer Excel
        with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
            # Aba 1: Resumo Estatístico
            resumo = df['Tipo de Publicação'].value_counts().reset_index()
            resumo.columns = ['Tipo de Publicação', 'Quantidade']
            resumo.loc[len(resumo)] = ['TOTAL', resumo['Quantidade'].sum()]
            
            resumo.to_excel(writer, sheet_name='Resumo', index=False)
            
            # Aba 2: Todas as publicações
            df_sorted = df.sort_values(['Tipo de Publicação', 'Data de Publicação'])
            df_sorted.to_excel(writer, sheet_name='Todas', index=False)
            
            # Abas individuais por tipo de publicação
            for tipo in df['Tipo de Publicação'].unique():
                # Limitar nome da aba a 31 caracteres (limite do Excel)
                nome_aba = tipo[:31]
                df_tipo = df[df['Tipo de Publicação'] == tipo].copy()
                df_tipo = df_tipo.sort_values('Data de Publicação')
                df_tipo.to_excel(writer, sheet_name=nome_aba, index=False)
            
            # Ajustar largura das colunas
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"✓ Planilha gerada com sucesso!")
        print(f"✓ Localização: {Path(arquivo_saida).absolute()}")
        
        return arquivo_saida
    
    def processar(self, nome_orgao, variantes=None, arquivo_saida=None):
        """
        Método principal: busca e gera planilha em uma única chamada
        
        Args:
            nome_orgao: Nome do órgão
            variantes: Lista de variantes/siglas (opcional)
            arquivo_saida: Nome do arquivo de saída (opcional)
            
        Returns:
            tuple: (DataFrame, caminho_arquivo)
        """
        df = self.buscar_orgao(nome_orgao, variantes)
        
        if not df.empty:
            arquivo = self.gerar_planilha(df, nome_orgao, arquivo_saida)
            return df, arquivo
        
        return df, None


def main():
    """Função principal para uso via linha de comando"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║          ANALISADOR DE PUBLICAÇÕES DO DIÁRIO OFICIAL DE MINAS GERAIS        ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar argumentos
    if len(sys.argv) < 3:
        print("""
USO:
    python analisador_diario_oficial.py <arquivo_json> <nome_orgao> [variantes...]

EXEMPLOS:
    python analisador_diario_oficial.py diario.json "Fundação Hemominas"
    python analisador_diario_oficial.py diario.json "Fundação Hemominas" "HEMOMINAS" "Fundação Centro de Hematologia"
    python analisador_diario_oficial.py diario.json "Secretaria de Estado de Saúde" "SES-MG" "SES"

DESCRIÇÃO:
    - arquivo_json: Arquivo JSON do Diário Oficial
    - nome_orgao: Nome principal do órgão a buscar
    - variantes: Nomes alternativos, siglas ou variações (opcional)
        """)
        sys.exit(1)
    
    arquivo_json = sys.argv[1]
    nome_orgao = sys.argv[2]
    variantes = sys.argv[3:] if len(sys.argv) > 3 else None
    
    # Verificar se arquivo existe
    if not Path(arquivo_json).exists():
        print(f"❌ ERRO: Arquivo não encontrado: {arquivo_json}")
        sys.exit(1)
    
    # Processar
    try:
        analisador = AnalisadorDiarioOficial(arquivo_json)
        df, arquivo_saida = analisador.processar(nome_orgao, variantes)
        
        if arquivo_saida:
            print(f"\n{'='*80}")
            print(f"PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            print(f"{'='*80}")
            print(f"Total de publicações: {len(df)}")
            print(f"Arquivo gerado: {arquivo_saida}")
            print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"\n❌ ERRO durante o processamento: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
