# Ponto Lab Soft

Ponto para controle de acesso de alunos no laboratorio de pesquisa utilizando reconhecimento facial.

![Ponto Lab Soft](/test/print.png)

## Autores:

- Julio Nunes Avelar

## Requisitos

### Software:

- Python 3.6 ou superior
- OpenCV 4.5.3 ou superior
- Dlib 19.24.0 ou superior
- Numpy 1.23.4 ou superior
- Pillow 9.2.0 ou superior
- PyZbar 0.1.9 ou superior
- Requests 2.28.1 ou superior

### Hardware:

- Webcam
- Raspberry Pi 3 ou superior ou qualquer outro computador que possa utilizar uma webcam

## Instalação

### Linux e MacOS

Para instalar as dependências do projeto, crie um ambiente virtual utilizando python-virtualenv e instale as dependências do projeto:

```bash
python3 -m venv env
```

Para ativar o ambiente virtual utilize:

```bash
source env/bin/activate
```

Para instalar as dependências do projeto utilize:

```bash
pip install -r requirements.txt
```

caso esteja utilizando um Raspberry Pi utlize:

```bash
pip install -r requirements-rpi.txt
```

### Windows

Para instalar as dependências do projeto, crie um ambiente virtual utilizando python-virtualenv e instale as dependências do projeto:

```bash
python -m venv env
```

Para ativar o ambiente virtual utilize:

```bash
env\Scripts\activate
```

Para instalar as dependências do projeto utilize:

```bash
pip install -r requirements.txt
```

## Execução

Para executar o projeto, ative o ambiente virtual e execute o arquivo main.py:

Na primeira execução antes de executar o arquivo main.py, será necessario criar o banco de dados, para isso, abra um shell python e utiliza:

```python
from core.database_manager import create_database
create_database()
```

O procedimento acima será necessario apenas antes de realizar a primeira execução do sistema.

Linux e MacOS:
```bash
source env/bin/activate
python main.py
```
Windows:
```bash
env\Scripts\activate
python main.py
```

## Configuração

Para configurar o projeto, edite o arquivo *consts.py* na pasta *core*, para utilizar as configurações padrões será necessario exportar um token de autenticação da API.

## Arquiteura

### Diretórios

- *core*: Contém os arquivos com funções e classes do projeto
- *dataset*: Contém os arquivos de treinamento do modelo
- *classificadores*: Contém os arquivos de modelos treinados
- *utils*: Contém os arquivos de utilidades do projeto
- *snapshots*: Contém os arquivos de capturas de tela do projeto
- *tests*: Contém os arquivos de testes do projeto

### Arquivos

- *main.py*: Arquivo principal do projeto
- *consts.py*: Arquivo de constantes do projeto
- *requirements.txt*: Arquivo de dependências do projeto
- *requirements-rpi.txt*: Arquivo de dependências do projeto para Raspberry Pi
- *README.md*: Arquivo de documentação do projeto
- *LICENSE*: Arquivo de licença do projeto
- *treino.py*: Arquivo de treinamento do modelo
- *database.db*: Arquivo de banco de dados do projeto

## Licença

Este projeto está licenciado sob a licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.

## Agradecimentos

- [OpenCV](https://opencv.org/)
- [Dlib](http://dlib.net/)
- [PyZbar](https://github.com/NaturalHistoryMuseum/pyzbar/)
- [Laboratório de Tecnologias de Software e Computação Aplicada à Educação - LabSoft](http://labsoft.muz.ifsuldeminas.edu.br/)

## Duvidas e Sugestões

Caso tenha alguma dúvida ou sugestão, fique a vontade para reportar no campo de [**issues**](https://github.com/JN513/access-control-with-facial-recognition/issues).
