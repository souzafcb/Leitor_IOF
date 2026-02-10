# 📊 Analisador de Publicações do Diário Oficial de Minas Gerais

## 🎯 Descrição

Aplicação Python reutilizável que **extrai e tabula automaticamente** todas as publicações relacionadas a qualquer órgão do Diário Oficial de Minas Gerais. Basta informar o nome do órgão!

---

## ✨ Funcionalidades

✅ **Busca Inteligente**: Identifica publicações por nome completo, siglas e variantes  
✅ **Classificação Automática**: Reconhece 20+ tipos de publicações (Decretos, Portarias, Editais, etc.)  
✅ **Extração de Dados**: Número, data, resumo, conteúdo completo e referências  
✅ **Planilha Excel Estruturada**: Múltiplas abas com resumos estatísticos e dados organizados  
✅ **100% Reutilizável**: Funciona para qualquer órgão, basta especificar o nome  

---

## 📥 Requisitos

```bash
pip install pandas openpyxl
```

---

## 🚀 Como Usar

### Modo 1: Linha de Comando (Recomendado)

```bash
python analisador_diario_oficial.py <arquivo_json> <nome_orgao> [variantes...]
```

#### **Exemplos Práticos:**

```bash
# Exemplo 1: Fundação Hemominas
python analisador_diario_oficial.py diario_executivo.json "Fundação Hemominas" "HEMOMINAS"

# Exemplo 2: Secretaria de Saúde
python analisador_diario_oficial.py diario_executivo.json "Secretaria de Estado de Saúde" "SES-MG" "SES"

# Exemplo 3: Polícia Militar
python analisador_diario_oficial.py diario_executivo.json "Polícia Militar de Minas Gerais" "PMMG" "PM-MG"

# Exemplo 4: COPASA
python analisador_diario_oficial.py diario_executivo.json "COPASA" "Companhia de Saneamento de Minas Gerais"

# Exemplo 5: CEMIG
python analisador_diario_oficial.py diario_executivo.json "CEMIG" "Companhia Energética de Minas Gerais"
```

---

### Modo 2: Uso Programático (Python Script)

```python
from analisador_diario_oficial import AnalisadorDiarioOficial

# Inicializar analisador
analisador = AnalisadorDiarioOficial('diario_executivo.json')

# Processar órgão específico
df, arquivo = analisador.processar(
    nome_orgao="Fundação Hemominas",
    variantes=["HEMOMINAS", "Fundação Centro de Hematologia"],
    arquivo_saida="hemominas_publicacoes.xlsx"  # opcional
)

# Visualizar resultados
print(df[['Tipo de Publicação', 'Data de Publicação', 'Assunto/Resumo']])
```

---

## 📁 Estrutura da Planilha Gerada

A planilha Excel contém múltiplas abas:

### **Aba "Resumo"**
| Tipo de Publicação | Quantidade |
|--------------------|-----------|
| Portaria           | 15        |
| Decreto            | 8         |
| Edital             | 5         |
| **TOTAL**          | **28**    |

### **Aba "Todas"**
Todas as publicações consolidadas com:
- Tipo de Publicação
- Número/Identificação
- Assunto/Resumo
- Conteúdo Completo
- Data de Publicação
- Edição
- Página
- Ano
- Caderno
- Referência Completa

### **Abas Individuais**
Uma aba para cada tipo (Portarias, Decretos, Editais, etc.)

---

## 🔍 Tipos de Publicação Reconhecidos

O sistema identifica automaticamente:

- ✅ Decretos
- ✅ Portarias
- ✅ Resoluções
- ✅ Editais
- ✅ Avisos
- ✅ Despachos
- ✅ Extratos (Contratos, Convênios)
- ✅ Comunicados
- ✅ Termos de Colaboração/Fomento
- ✅ Convênios
- ✅ Contratos
- ✅ Licitações (Pregões, Concorrências)
- ✅ Nomeações
- ✅ Exonerações
- ✅ Designações
- ✅ Dispensas
- ✅ Retificações
- ✅ Ratificações
- ✅ Homologações
- ✅ Atas de Registro de Preços
- ✅ Outros

---

## 💡 Dicas de Uso

### **1. Use Variantes para Melhorar a Busca**
```bash
# ✅ BOM - Com variantes
python analisador_diario_oficial.py diario.json "FHEMIG" "Fundação Hospitalar" "Fundação Hospitalar do Estado"

# ❌ LIMITADO - Apenas nome oficial
python analisador_diario_oficial.py diario.json "FHEMIG"
```

### **2. Nomes Compostos Entre Aspas**
```bash
# ✅ CORRETO
python analisador_diario_oficial.py diario.json "Polícia Civil do Estado"

# ❌ ERRADO
python analisador_diario_oficial.py diario.json Polícia Civil do Estado
```

### **3. Verificar o Arquivo JSON**
```bash
# Verificar se o arquivo existe
ls -lh diario_executivo.json

# Ver estrutura básica
head -c 1000 diario_executivo.json
```

---

## 📊 Exemplo de Saída

```
================================================================================
BUSCANDO PUBLICAÇÕES DE: Fundação Hemominas
================================================================================

Termos de busca: FUNDACAO HEMOMINAS, HEMOMINAS, FUNDACAO CENTRO DE HEMATOLOGIA
Processando página 100/1104...
Processando página 200/1104...
...

✓ 4 publicações encontradas!

Gerando planilha: publicacoes_Fundação_Hemominas_20260210.xlsx
✓ Planilha gerada com sucesso!

================================================================================
PROCESSAMENTO CONCLUÍDO COM SUCESSO!
================================================================================
Total de publicações: 4
Arquivo gerado: publicacoes_Fundação_Hemominas_20260210.xlsx
================================================================================
```

---

## 🛠️ Personalização

### **Adicionar Novos Tipos de Publicação**

Edite a variável `tipos_publicacao` na classe:

```python
self.tipos_publicacao = {
    'Seu Novo Tipo': r'\b(PADRÃO\s+REGEX)\s+N[ºª°]?\s*\d+',
    # ... outros tipos
}
```

### **Ajustar Tamanho do Resumo**

Modifique o parâmetro `max_chars` no método `_extrair_resumo`:

```python
'Assunto/Resumo': self._extrair_resumo(conteudo, 300),  # 300 caracteres
```

---

## 📋 Lista de Órgãos Comuns

Use estes nomes para buscar publicações:

| Órgão | Nome Completo | Variantes Sugeridas |
|-------|---------------|---------------------|
| **Saúde** | Secretaria de Estado de Saúde | SES, SES-MG |
| **Educação** | Secretaria de Estado de Educação | SEE, SEE-MG |
| **Fazenda** | Secretaria de Estado de Fazenda | SEF, SEF-MG |
| **PMMG** | Polícia Militar de Minas Gerais | PMMG, PM-MG |
| **CEMIG** | Companhia Energética de Minas Gerais | CEMIG |
| **COPASA** | Companhia de Saneamento de Minas Gerais | COPASA-MG |
| **HEMOMINAS** | Fundação Hemominas | Fundação Centro de Hematologia |
| **FHEMIG** | Fundação Hospitalar do Estado | FHEMIG |
| **IPSEMG** | Instituto de Previdência dos Servidores | IPSEMG |
| **UEMG** | Universidade do Estado de Minas Gerais | UEMG |

---

## 🐛 Solução de Problemas

### **Problema: "Nenhuma publicação encontrada"**
**Solução:**
- Verifique a grafia do nome do órgão
- Adicione mais variantes/siglas
- Teste com parte do nome: `"Hemominas"` ao invés de `"Fundação Centro de Hematologia e Hemoterapia de Minas Gerais"`

### **Problema: "ModuleNotFoundError: No module named 'pandas'"**
**Solução:**
```bash
pip install pandas openpyxl
```

### **Problema: Arquivo JSON não encontrado**
**Solução:**
```bash
# Verifique o caminho completo
python analisador_diario_oficial.py /caminho/completo/para/diario.json "Órgão"
```

---

## 📝 Formato do Arquivo JSON

O arquivo deve ter esta estrutura:

```json
[
  {
    "DataPublicacao": "2026-02-10T00:00:00",
    "Descricao": "Diário do Executivo",
    "Titulo": "caderno1",
    "Pagina": 1,
    "Ano": "134",
    "Edicao": "26",
    "Conteudo": "Texto completo da publicação..."
  }
]
```

---

## 🎓 Casos de Uso

### **1. Monitoramento de Licitações**
```bash
python analisador_diario_oficial.py diario.json "Secretaria de Obras" "SEOBRAS"
# Filtre a aba "Licitação" na planilha gerada
```

### **2. Rastreamento de Nomeações**
```bash
python analisador_diario_oficial.py diario.json "Secretaria de Planejamento"
# Verifique a aba "Nomeação"
```

### **3. Auditoria de Contratos**
```bash
python analisador_diario_oficial.py diario.json "COPASA"
# Analise as abas "Extrato" e "Contrato"
```

### **4. Pesquisa Jurídica**
```bash
python analisador_diario_oficial.py diario.json "Advocacia-Geral do Estado" "AGE"
# Consulte decretos e resoluções
```

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este guia primeiro
2. Teste com exemplos fornecidos
3. Valide o formato do arquivo JSON

---

## 📄 Licença

Código livre para uso, modificação e distribuição.

---

## 🎉 Resultado da Análise - Fundação Hemominas

**Data de Processamento**: 10/02/2026  
**Total de Publicações Encontradas**: 4  
**Arquivo Gerado**: `publicacoes_Fundação_Hemominas_20260210.xlsx`

### Distribuição por Tipo
- Consulte a aba "Resumo" da planilha para estatísticas detalhadas

---

**Desenvolvido para análise automatizada de diários oficiais** 🚀
