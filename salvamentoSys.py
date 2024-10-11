#   VINICIUS RODRIGUES DA COSTA
#   RAFAEL LUIZ CUYPERS

import pickle  # biblioteca para serialização/deserialização de objetos Python
import os  # biblioteca para operações do sistema operacional

class salvamento:  # classe salvamento
    def __init__(self, file_extension, save_folder):  # construtor da classe
        self.file_extension = file_extension  # extensão do arquivo a ser salvo
        self.save_folder = save_folder  # pasta onde os arquivos serão salvos

    def save_data(self, data, name):  # método para salvar dados em arquivo
        data_file = open(self.save_folder+"/"+name+self.file_extension, "wb")  # abre o arquivo para escrita em modo binário
        pickle.dump(data, data_file)  # serializa e salva os dados no arquivo
        data_file.close()  # fecha o arquivo após a operação de escrita

    def load_data(self, name):  # método para carregar dados de um arquivo
        data_file = open(self.save_folder+"/"+name+self.file_extension, "rb")  # abre o arquivo para leitura em modo binário
        data = pickle.load(data_file)  # desserializa os dados do arquivo
        data_file.close()  # fecha o arquivo após a operação de leitura
        return data  # retorna os dados carregados do arquivo

    def check_file(self, name):  # método para verificar se um arquivo existe
        return os.path.exists(self.save_folder+"/"+name+self.file_extension)  # verifica se o arquivo existe no sistema de arquivos

    def load_game_data(self, files_to_load, default_data):  # método para carregar dados do jogo
        variables = []  # lista para armazenar os dados carregados
        for index, file in enumerate(files_to_load):  # itera sobre os arquivos a serem carregados
            if self.check_file(file):  # verifica se o arquivo existe
                variables.append(self.load_data(file))  # se existir, carrega os dados do arquivo
            else:
                variables.append(default_data[index])  # se não existir, usa os dados padrão

        if len(variables) > 1:  # se houver mais de uma variável carregada
            return tuple(variables)  # retorna uma tupla com as variáveis
        else:
            return variables[0]  # se houver apenas uma variável carregada, retorna ela diretamente

    def save_game_data(self, data_to_save, file_names):  # método para salvar dados do jogo
        for index, file in enumerate(data_to_save):  # itera sobre os dados a serem salvos
            self.save_data(file, file_names[index])  # salva cada conjunto de dados em um arquivo correspondente
