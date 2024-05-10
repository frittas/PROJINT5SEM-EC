import pymongo
from pymongo import cursor


class ImageRepository:
    def __init__(self, connection_string: str, db_name: str, collection_name: str):#esta parte estabelece a conexao com o mongo usando a string de conexao
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def salvar_imagem(self, frame_imagem, nome_pessoa:str) -> str: # falo que database sera uma string e que ira salvar no mongodb
            # with open(frame_imagem, 'rb') as imagem_arquivo:#le e tranforma a imagem em bytes/numeros binarios
            #     imagem_conteudo = imagem_arquivo.read() #imagem_conteudo recebe os bytes lidos  em imagem_arquivo
                resultado = self.collection.insert_one({'nome': nome_pessoa, 'imagem': frame_imagem})#salva os bytes em imagens no meu mongoDB
                return resultado.inserted_id #retornando o id do documento inserido       
            
    def buscar_imagem(self, nome_pessoa: str) -> bytes: 
        documento = self.collection.find_one({'nome': nome_pessoa})
        if documento:
            return documento['imagem'] #retornara os bytes da imagem 
        else:
            return print("IMAGEM NAO ENCONTRADA!!!")
        
    def bucar_todas_imagens(self) -> cursor.Cursor:
        cursor = self.collection.find({})
        return cursor

        