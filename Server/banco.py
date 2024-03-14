import pymongo
from PIL import Image
import io

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
meu_banco = cliente['banco_de_dados']
colecao_imagens = meu_banco['imagens']

with open('kawa.jpg', 'rb') as arquivo_imagem:
    conteudo_imagem = arquivo_imagem.read()

resultado_insercao = colecao_imagens.insert_one({'imagem': conteudo_imagem})

print("ID da imagem inserida:", resultado_insercao.inserted_id)

documento = colecao_imagens.find_one()  
imagem_bytes = documento['imagem']

imagem = Image.open(io.BytesIO(imagem_bytes))

imagem.show()

cliente.close()


