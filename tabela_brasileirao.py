from flask import Flask, request, render_template_string
import pandas as pd
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Função para sanitizar o nome do time para gerar o caminho da imagem
def sanitize_team_name(team_name):
    return team_name.lower().replace(" ", "_").replace("-", "_")

# Lista de times com estatísticas iniciais
times = [
    {'Time': 'Atlético-GO', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Atlético-MG', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Athletico-PR', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Bahia', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Botafogo', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Corinthians', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Criciúma', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Cruzeiro', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Cuiabá', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Flamengo', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Fluminense', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Fortaleza', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Grêmio', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Internacional', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Juventude', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Palmeiras', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Red Bull Bragantino', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'São Paulo', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Vasco', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},
    {'Time': 'Vitória', 'Jogos': 0, 'Vitórias': 0, 'Empates': 0, 'Derrotas': 0, 'Gols Marcados': 0, 'Gols Sofridos': 0},  
]

# Inicializa a tabela de dados com o Pandas
tabela = pd.DataFrame(times)
tabela['Pontos'] = tabela['Vitórias'] * 3 + tabela['Empates']
tabela['GP'] = tabela['Gols Marcados']
tabela['GC'] = tabela['Gols Sofridos']
tabela['SG'] = tabela['GP'] - tabela['GC']
tabela['%'] = (tabela['Pontos'] / (tabela['Jogos'] * 3)) * 100  # Aproveitamento
tabela = tabela.sort_values(by='Pontos', ascending=False).reset_index(drop=True)

# Dados de próximos jogos (simulados)
proximos_jogos = [
    {'time1': 'Flamengo', 'time2': 'Palmeiras', 'data': '24/11', 'local': 'Maracanã'},
    {'time1': 'Vasco', 'time2': 'São Paulo', 'data': '26/11', 'local': 'São Januário'},
    {'time1': 'Corinthians', 'time2': 'Internacional', 'data': '20/11', 'local': 'Neo Química Arena'},
    {'time1': 'Grêmio', 'time2': 'Fluminense', 'data': '21/11', 'local': 'Arena do Grêmio'},
    {'time1': 'Atlético-MG', 'time2': 'Cruzeiro', 'data': '22/11', 'local': 'Mineirão'},
    {'time1': 'Athletico-PR', 'time2': 'Cuiabá', 'data': '23/11', 'local': 'Arena da Baixada'},
]

# Configuração do Flask
app = Flask(__name__)

# Adicionando a coluna de classe de cor com base na posição
def get_classe_posicao(posicao):
    if posicao <= 5:
        return 'azul'
    elif posicao <= 7:
        return 'azul-ciano'
    elif posicao <= 13:
        return 'verde-escuro'
    elif posicao <= 16:
        return 'cinza-claro'
    else:
        return 'vermelho'

# Calcula as classes de posição para a tabela
tabela['Classe_Posição'] = tabela.index + 1
tabela['Classe_Posição'] = tabela['Classe_Posição'].apply(get_classe_posicao)

# Exemplo de tabela com a nova coluna
print(tabela[['Time', 'Classe_Posição']])

# Template HTML para a tabela
TEMPLATE = """
<!doctype html>
<html lang="pt-br">
  <head>
    <meta charset="UTF-8">
    <title>Tabela do Brasileirão</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="icon" href="{{ url_for('static', filename='img/logo.png') }}" type="image/png">
  </head>
  <body>
    <header>
    <h1>BRASILEIRÃO SÉRIE A</h1>
    </header>
    <div class="container">
      <div class="tabela-container">
      <h2>Tabela</h2>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
          <thead>
            <tr>
              <th>Posição</th>
              <th>Time</th>
              <th>Pontos</th>
              <th>Jogos</th>
              <th>Vitórias</th>
              <th>Empates</th>
              <th>Derrotas</th>
              <th>GP</th>
              <th>GC</th>
              <th>SG</th>
              <th>%</th>
            </tr>
          </thead>
          <tbody>
            {% for i, row in tabela.iterrows() %}
            <tr>
              <td class="{{ row['Classe_Posição'] }}">{{ i + 1 }}</td>
              <td class="time-info">
                <img src="{{ url_for('static', filename='img/' + sanitize_team_name(row['Time']) + '.png') }}" alt="Escudo do {{ row['Time'] }}" class="escudo-small">
                {{ row['Time'] }}
              </td>
              <td>{{ row['Pontos'] }}</td>
              <td>{{ row['Jogos'] }}</td>
              <td>{{ row['Vitórias'] }}</td>
              <td>{{ row['Empates'] }}</td>
              <td>{{ row['Derrotas'] }}</td>
              <td>{{ row['GP'] }}</td>
              <td>{{ row['GC'] }}</td>
              <td>{{ row['SG'] }}</td>
              <td>{{ row['%'] | round(2) }}%</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>

      <div class="proximos-jogos-container">
        <h2>Simulador</h2>
        <ul>
          {% for jogo in proximos_jogos %}
          <li class="jogo-item">
            <div class="jogo-info">
              <!-- Data e Local acima dos times -->
              <div class="jogo-data">
                <strong>{{ jogo.data }}</strong> <br>
              {{ jogo.local }}
              </div>

              <!-- Div dos times e palpites -->
              <div class="jogo-times">
                <div class="time">
                  <img src="{{ url_for('static', filename='img/' + sanitize_team_name(jogo.time1) + '.png') }}" alt="Escudo {{ jogo.time1 }}" class="escudo-proxjogo">
                  <span>{{ jogo.time1 }}</span>
                </div>
                
                <!-- Campo de palpites para o primeiro time -->
                <div class="palpite">
                  <input type="number" id="placar_{{ loop.index }}_time1" name="placar_{{ loop.index }}_time1" Gols" min="0">
                </div>
                
                <div class="versus">X</div>
                
                <!-- Campo de palpites para o segundo time -->
                <div class="palpite">
                  <input type="number" id="placar_{{ loop.index }}_time2" name="placar_{{ loop.index }}_time2" Gols" min="0">
                </div>
                
                <div class="time">
                  <img src="{{ url_for('static', filename='img/' + sanitize_team_name(jogo.time2) + '.png') }}" alt="Escudo {{ jogo.time2 }}" class="escudo-proxjogo">
                  <span>{{ jogo.time2 }}</span>
                </div>
              </div>
            </div>
          </li>
          {% endfor %}
        </ul>
      </div>

      <div class="forms-container">
        <div class="form-section">
          <h2>Escolha o Resultado</h2>
          <form method="post">
            Time: 
            <select name="time" required>
              <option value="" disabled selected>Escolha um time</option>
              {% for time in times %} 
                <option value="{{ time }}">{{ time }}</option>
              {% endfor %}
            </select><br>
            Jogos: <input type="number" name="jogos" required min="0"><br>
            Vitórias: <input type="number" name="vitorias" required min="0"><br>
            Empates: <input type="number" name="empates" required min="0"><br>
            Derrotas: <input type="number" name="derrotas" required min="0"><br>
            Gols Marcados: <input type="number" name="gols_marcados" required min="0"><br>
            Gols Sofridos: <input type="number" name="gols_sofridos" required min="0"><br>
            <input type="submit" value="Atualizar Tabela">
          </form>
        </div>

        <div class="form-section">
          <h2>Reiniciar Tabela</h2>
          <form method="post">
            <input type="hidden" name="reiniciar" value="true">
            <input type="submit" value="Reiniciar Tabela">
          </form>
        </div>
      </div>
    </div>
  </body>
</html>
"""

# Rota principal que exibe e processa as ações
@app.route('/', methods=['GET', 'POST'])
def tabela_brasileirao():
    global tabela

    # Lista de times para o dropdown
    times_lista = tabela['Time'].tolist()

    if request.method == 'POST' and 'reiniciar' in request.form:
        # Reiniciar os dados
        tabela = pd.DataFrame(times)
        tabela['Pontos'] = tabela['Vitórias'] * 3 + tabela['Empates']
        tabela['GP'] = tabela['Gols Marcados']
        tabela['GC'] = tabela['Gols Sofridos']
        tabela['SG'] = tabela['GP'] - tabela['GC']
        tabela['%'] = (tabela['Pontos'] / (tabela['Jogos'] * 3)) * 100
        tabela = tabela.sort_values(by='Pontos', ascending=False).reset_index(drop=True)

    return render_template_string(TEMPLATE, tabela=tabela, times=times_lista, proximos_jogos=proximos_jogos, sanitize_team_name=sanitize_team_name)


if __name__ == '__main__':
    app.run(debug=True)