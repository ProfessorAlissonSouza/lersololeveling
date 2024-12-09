import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_images_from_page(url, output_folder):
    try:
        # Criar pasta de saída, se não existir
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Cabeçalhos para evitar bloqueios
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Obter o conteúdo da página
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica se a solicitação foi bem-sucedida
        soup = BeautifulSoup(response.text, 'html.parser')

        # Localizar divs com a classe "page-break"
        divs = soup.find_all('div', class_='page-break')

        # Processar cada div
        for div in divs:
            # Verificar se a div contém uma tag <img>
            img_tag = div.find('img')
            if img_tag:
                # Primeiro tenta capturar o atributo data-src
                img_url = img_tag.get('data-src') or img_tag.get('src')
            else:
                img_url = None

            if img_url:
                # Resolver URLs relativas
                img_url = urljoin(url, img_url)

                # Ignorar imagens embutidas (base64)
                if img_url.startswith('data:image'):
                    print(f"Ignorado (imagem embutida): {img_url}")
                    continue

                img_name = os.path.basename(img_url.split('?')[0])  # Nome da imagem sem parâmetros
                img_path = os.path.join(output_folder, img_name)

                # Baixar a imagem
                try:
                    img_data = requests.get(img_url, headers=headers).content
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_data)
                    print(f"Imagem salva: {img_path}")
                except Exception as e:
                    print(f"Erro ao baixar {img_url}: {e}")
            else:
                print(f"Ignorado (URL da imagem não encontrada na div): {div}")

    except Exception as e:
        print(f"Erro ao processar: {e}")


# Iterar pelos capítulos
base_url = "https://mugiwarasoficial.com/manga/solo-leveling/capitulo-"
for chapter in range(1, 180):  # Capítulos de 1 a 179
    chapter_url = f"{base_url}{chapter:02}/?style=list"  # Formatar o número do capítulo com 2 dígitos
    output_folder = f"./capitulo-{chapter:03}"  # Formatar a pasta com 3 dígitos para organização
    print(f"Baixando capítulo {chapter} de: {chapter_url}")
    download_images_from_page(chapter_url, output_folder)
