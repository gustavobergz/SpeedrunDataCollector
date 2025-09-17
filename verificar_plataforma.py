import requests
import logging

# Configuração de logging para uma saída mais limpa e informativa
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class SpeedrunGameExplorer:
    """
    Explora um jogo na API do speedrun.com para listar de forma clara
    todas as categorias, suas variáveis e os valores possíveis (como plataformas).
    """
    API_BASE = "https://www.speedrun.com/api/v1"

    def __init__(self, game_id: str ):
        if not game_id:
            raise ValueError("O ID do jogo não pode ser vazio.")
        self.game_id = game_id
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Python/3.9 SpeedrunGameExplorer/1.0",
            "Accept": "application/json"
        })

    def fetch_game_data(self):
        """
        Busca todos os dados do jogo, incluindo categorias e suas variáveis,
        em uma única chamada de API para máxima eficiência.
        """
        logging.info(f"Buscando dados completos para o jogo ID: {self.game_id}...")
        
        # O parâmetro 'embed' é a chave para a eficiência.
        # Ele instrui a API a incluir os dados relacionados no mesmo pedido.
        endpoint = f"games/{self.game_id}?embed=categories.variables"
        url = f"{self.API_BASE}/{endpoint}"
        
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            logging.info("Dados recebidos com sucesso!")
            return response.json().get('data')
        except requests.exceptions.RequestException as e:
            logging.error(f"Falha ao buscar dados do jogo: {e}")
            return None

    def display_results(self, game_data):
        """Formata e exibe os dados de forma organizada no console."""
        if not game_data:
            logging.error("Nenhum dado para exibir.")
            return

        print("\n" + "=" * 70)
        print(f"🕹️  Análise do Jogo: {game_data.get('names', {}).get('international', 'Nome não encontrado')}")
        print(f"🆔 Game ID: {self.game_id}")
        print("=" * 70)

        categories = game_data.get('categories', {}).get('data', [])
        if not categories:
            print("\n❌ Nenhuma categoria encontrada para este jogo.")
            return

        for category in categories:
            print(f"\n📁 Categoria: {category['name']}")
            print(f"   └── 🆔 ID da Categoria: {category['id']}")
            
            variables = category.get('variables', {}).get('data', [])
            if not variables:
                print("       └── ℹ️ Nenhuma variável (filtro) associada.")
                continue

            for var in variables:
                # Verifica se a variável atua como um filtro de subcategoria
                is_subcategory = " (Subcategoria)" if var.get('is-subcategory') else ""
                
                print(f"\n   ⭐ Variável: {var['name']}{is_subcategory}")
                print(f"      ├── 🆔 ID da Variável: {var['id']}")
                
                values = var.get('values', {}).get('values', {})
                if not values:
                    print("      └── ⚠️ Nenhum valor definido para esta variável.")
                    continue
                
                print("      └── 📋 Valores Possíveis:")
                for value_id, value_details in values.items():
                    label = value_details.get('label', 'N/A')
                    print(f"         ├── {label}")
                    print(f"         │   └── 🆔 ID do Valor: {value_id}")
        
        print("\n" + "=" * 70)
        print("✅ Análise concluída!")
        print("=" * 70)


def main():
    """Função principal para executar o explorador."""
    # ID do jogo Subway Surfers
    game_id = "y65797de"
    
    explorer = SpeedrunGameExplorer(game_id)
    game_data = explorer.fetch_game_data()
    
    if game_data:
        explorer.display_results(game_data)

if __name__ == "__main__":
    main()
