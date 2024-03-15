import pymongo
from PIL import Image
import io
import os

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
meu_banco = cliente['banco_de_dados']
colecao_imagens = meu_banco['imagens']
caminho_da_pasta = 'C:/Users/Pichau/Desktop/banco/fotos'

if os.path.exists(caminho_da_pasta) and os.path.isdir(caminho_da_pasta): #vendo se o caminho da pasta e valido  /   a funcao "os.path.isdir" e usada para ve um caminho especifico no sistema e um diretorio
    arquivos_na_pasta = os.listdir(caminho_da_pasta)#listando todos os arquivos da pasta
    
    for arquivo in arquivos_na_pasta:#percorrer os arquivos da pasta
        caminho_completo = os.path.join(caminho_da_pasta, arquivo)# o "os.path.join" serve para garantir que o caminho resultante seja correto, independentemente do sistema operacional 
        
        
        if os.path.isfile(caminho_completo):# verificar se o caminho especificado corresponde a um arquivo existente

            with open(caminho_completo, 'rb') as arquivo_imagem:#ira le o conteudo do arquivo
                conteudo_imagem = arquivo_imagem.read()
     
                resultado_insercao = colecao_imagens.insert_one({'imagem': conteudo_imagem})#insere no banco de dados os bytes da imagem

                print("ID da imagem inserida:", resultado_insercao.inserted_id)
