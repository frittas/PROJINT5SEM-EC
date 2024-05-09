import pymongo
connection_string = "mongodb://localhost:27017/" #configuracao do mongo
db_name = "banco_de_dados"
collection_name = "imagens"
caminho_pasta = 'C:/Users/Pichau/Desktop/imagens'

class SalvaImagem:
    def _init_(self, connection_string: str, db_name: str, collection_name: str):#esta parte estabelece a conexao com o mongo usando a string de conexao
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def salvar_imagem(self, frame_imagem: str, nome_pessoa:str) -> str: # falo que database sera uma string e que ira salvar no mongodb
        
            with open(frame_imagem, 'rb') as imagem_arquivo:#le e tranforma a imagem em bytes/numeros binarios
                imagem_conteudo = imagem_arquivo.read() #imagem_conteudo recebe os bytes lidos  em imagem_arquivo
                resultado = self.collection.insert_one({'nome': nome_pessoa, 'imagem': imagem_conteudo})#salva os bytes em imagens no meu mongoDB
                return resultado.inserted_id #retornando o id do documento inserido       
        
class BuscarImagem:
    def _init_(self, connection_string: str, db_name: str, collection_name: str):#estabele a conexao com o mongoDB
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def buscar_imagem(self, nome_pessoa: str) -> bytes: 
        documento = self.collection.find_one({'nome': nome_pessoa})
        if documento:
            return documento['imagem'] #retornara os bytes da imagem 
        else:
            return print("IMAGEM NAO ENCONTRADA!!!")
              
         
         