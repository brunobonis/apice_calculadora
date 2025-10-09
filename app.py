from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static')

# Dados baseados nos seus sistemas (VALORES À VISTA CORRETOS)
SISTEMAS_SOLARES = {
    '300': {
        'potencia': 2.48,
        'geracao_mensal': 300,
        'preco_a_vista': 7100,
        'preco_parcelado': '21x de R$ 415,81',
        'modulos': 4,
        'inversor': 'Micro inversor',
        'descricao': 'Sistema Fotovoltaico'
    },
    '450': {
        'potencia': 3.72,
        'geracao_mensal': 450,
        'preco_a_vista': 9900,
        'preco_parcelado': '21x de R$ 579,79',
        'modulos': 6,
        'inversor': '3kW',
        'descricao': 'Sistema Fotovoltaico'
    },
    '600': {
        'potencia': 4.96,
        'geracao_mensal': 600,
        'preco_a_vista': 11300,
        'preco_parcelado': '21x de R$ 661,78',
        'modulos': 8,
        'inversor': '3kW',
        'descricao': 'Sistema Fotovoltaico'
    },
    '750': {
        'potencia': 6.20,
        'geracao_mensal': 750,
        'preco_a_vista': 14600,
        'preco_parcelado': '21x de R$ 855,05',
        'modulos': 10,
        'inversor': '4kW',
        'descricao': 'Sistema Fotovoltaico'
    },
    '900': {
        'potencia': 7.44,
        'geracao_mensal': 900,
        'preco_a_vista': 16100,
        'preco_parcelado': '21x de R$ 942,89',
        'modulos': 12,
        'inversor': '5kW',
        'descricao': 'Sistema Fotovoltaico'
    },
    '1200': {
        'potencia': 9.92,
        'geracao_mensal': 1200,
        'preco_a_vista': 22500,
        'preco_parcelado': '21x de R$ 1.317,71',
        'modulos': 16,
        'inversor': '7.5K',
        'descricao': 'Sistema Fotovoltaico'
    },
    '1500': {
        'potencia': 13.64,
        'geracao_mensal': 1500,
        'preco_a_vista': 29000,
        'preco_parcelado': '21x de R$ 1.698,15',
        'modulos': 22,
        'inversor': '10K',
        'descricao': 'Sistema Fotovoltaico'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        dados = request.get_json()
        conta_mensal = float(dados['conta_mensal'])
        
        # Cálculo do sistema ideal conforme solicitado
        # Subtrai 100 da conta e divide por 1.2
        valor_apos_subtracao = conta_mensal - 100
        if valor_apos_subtracao < 0:
            valor_apos_subtracao = 0
            
        consumo_kwh = valor_apos_subtracao / 1.2
        
        # Encontrar sistema ideal (próximo kWh maior)
        sistema_ideal = encontrar_sistema_ideal(consumo_kwh)
        
        # Verificar se precisa de projeto personalizado
        precisa_projeto_personalizado = consumo_kwh > 1500
        
        # Cálculos de economia
        MINIMO_CONTA = 100.00
        economia_mensal = max(conta_mensal - MINIMO_CONTA, 0)
        economia_anual = economia_mensal * 12
        
        # Payback baseado no valor à vista
        payback_anos = sistema_ideal['preco_a_vista'] / economia_anual if economia_anual > 0 else 999
        
        # Projeção 25 anos com aumento de 5% ao ano na conta
        projecao = []
        economia_total_25_anos = 0
        
        for ano in range(1, 26):
            # Aumento de 5% ao ano na conta (e consequentemente na economia)
            aumento_anual = 1.05 ** (ano - 1)
            economia_anual_com_aumento = economia_anual * aumento_anual
            economia_acumulada_ate_ano = sum([economia_anual * (1.05 ** (i - 1)) for i in range(1, ano + 1)])
            economia_total_25_anos = economia_acumulada_ate_ano
            
            projecao.append({
                'ano': ano,
                'economia_anual': economia_anual_com_aumento,
                'economia_acumulada': economia_acumulada_ate_ano
            })
        
        return jsonify({
            'success': True,
            'minimo_concessionaria': MINIMO_CONTA,
            'sistema_ideal': sistema_ideal,
            'precisa_projeto_personalizado': precisa_projeto_personalizado,
            'consumo_calculado': consumo_kwh,
            'resultados': {
                'conta_atual': conta_mensal,
                'conta_pos_instalacao': MINIMO_CONTA,
                'economia_mensal': economia_mensal,
                'economia_anual': economia_anual,
                'investimento_a_vista': sistema_ideal['preco_a_vista'],
                'payback_anos': payback_anos,
                'economia_total_25_anos': economia_total_25_anos,
                'projecao': projecao
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def encontrar_sistema_ideal(consumo_kwh):
    """Encontra o sistema solar ideal baseado no consumo calculado em kWh"""
    
    # Se consumo for maior que 1500, retorna o maior sistema disponível
    if consumo_kwh > 1500:
        return SISTEMAS_SOLARES['1500']
    
    # Lista de sistemas ordenados por geração
    sistemas_ordenados = ['300', '450', '600', '750', '900', '1200', '1500']
    
    # Encontra o próximo sistema maior que o consumo
    for sistema_key in sistemas_ordenados:
        sistema = SISTEMAS_SOLARES[sistema_key]
        if consumo_kwh <= sistema['geracao_mensal']:
            return sistema
    
    # Se não encontrou, retorna o maior sistema
    return SISTEMAS_SOLARES['1500']

if __name__ == '__main__':
    print("🌞 Calculadora Solar Ápice Solar - Black Friday")
    print("💰 Sistemas com preços reais:")
    for nome, sistema in SISTEMAS_SOLARES.items():
        print(f"   {sistema['geracao_mensal']} kWh - R$ {sistema['preco_a_vista']:,} à vista - {sistema['potencia']} kWp")
    
    print(f"\n🚀 Servidor iniciando... Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)