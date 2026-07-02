# SMART-ROOM
## Descrição
SMART-ROOM é um projeto de Internet das Coisas que simula um ambiente inteligente. O sistema utiliza visão computacional para detectar e reconhecer pessoas no ambiente, permitindo a automação de dispositivos que simulam luz, ar-condicionado e sistema de segurança. 

## Funcionalidades
- Detecção de presença de pessoas no ambiente
- Integração com **Adafruit IO** para envio e leitura de dados
- Controle automático de LEDs simulando luz e ar-condicionado conforme presença no ambiente
- Sistema de alarme (buzzer) baseado no reconhecimento facial (verifica se o rosto está no dataset)


## Tecnologias

### Linguagens
- Python
- C++

### Visão computacional
- OpenCV
- RF-DETR (Roboflow)
- face-recognition

### IoT / Simulação
- Adafruit IO
- MQTT
- Wokwi (simulação de hardware)
- PlatformIO (VS Code)

### Hardware simulado
- LEDs como indicadores de estado (luz e ar-condicionado)
- Buzzer como sistema de alarme

## Arquitetura do sistema
O SMART-ROOM é dividido em três partes principais:
### Visão computacional (Python)
Responsável pela captura de imagens, detecção e reconhecimento facial dos indivíduos utilizando **OpenCV**, o modelo de detecção de objetos **RF-DETR** e a biblioteca **face-recognition**. Após o processamento, o sistema envia o estado do ambiente para o **Adafruit IO** via **MQTT**.

### Integração IoT (Adafruit IO)
Plataforma que recebe os dados enviados pelo Python e os disponibiliza em tempo real para o sistema embarcado.

### Sistema embarcado
Simulado via **Wokwi** e desenvolvido com **PlatformIO**, o **ESP32** recebe os dados do **Adafruit IO** e controla LEDs indicadores de estado da luz e do ar-condicionado e um buzzer de alarme.

## Como rodar
### Passo 1: clonar o repositório
```bash
git clone https://github.com/mrlopessil/smart-room.git
cd smart-room
```
### Passo 2: crie um ambiente virtual
```bash
python -m venv venv
```

### Passo 3: ativar o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate.bat
```
**Linux/Mac**:
```bash
source venv/bin/activate
```

### Passo 4: instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 5: configurar arquivos
Abra o arquivo `config.py` na raiz do projeto e configure suas credenciais do Adafruit IO.
```python
# ADAFRUIT CONFIG
AIO_USERNAME = "SEU_USERNAME"
AIO_KEY = "SUA_KEY"
```
Abra também o arquivo `config.h` localizado em `esp32-smart-room/include/` e configure com os mesmos valores.
```cpp
#define AIO_USERNAME    "SEU_USERNAME"
#define AIO_KEY         "SUA_ADAFRUIT_KEY"
```

### Passo 6: adicione fotos ao dataset
Para que o sistema consiga reconhecer rostos conhecidos, é necessário adicionar imagens na base de dados.

Crie uma pasta em `data/faces/` com o seu nome e adicione algumas fotos suas dentro dela.

### Passo 7: compilar com PlatformIO
No VS Code e com a extensão do PlatformIO instalada aperte F1 e selecione PlatformIO: Show PlatformIO, será aberta uma sidebar, selecione para escolher uma pasta e selecione a pasta esp32-smart-room dentro do projeto.

Aperte F1 e selecione PlatformIO: Build.

### Passo 8: simular sistema embarcado com Wokwi
Quando a compilação terminar aperte F1 novamente e selecione Wokwi: Start Simulator.

O simulador será iniciado. Quando o terminal exibir as mensagens:
```text
Connecting WiFi... WiFi Connected!
Connected MQTT
```

O ESP32 estará conectado ao Adafruit IO e pronto para receber os dados enviados pela aplicação Python.

### Passo 9: rode o sistema
Em um terminal com o ambiente virtual ativado, navegue até a raiz do projeto e execute:
```bash
python main.py
```

## Troubleshoot
### ESP32 não conecta ao MQTT:
- Certifique-se que AIO_USERNAME e AIO_KEY foram configuradas corretamente em `config.py` e `config.h`.

### Aplicação Python fecha automaticamente
Se a aplicação for encerrada antes de exibir a imagem da câmera, verifique se o índice da câmera configurado no arquivo `config.py` está correto.

Caso o computador não possua uma câmera ou você prefira utilizar o celular, é possível usá-lo como uma câmera IP. Para isso, instale um aplicativo de câmera IP no dispositivo móvel e configure a URL de transmissão no arquivo `config.py`.

Passos para usar o celular como câmera:
1. Instale o aplicativo **IP Webcam** no celular.
2. Inicie a transmissão de vídeo.
3. Copie a URL informada pelo aplicativo.
4. Configure essa URL no arquivo `config.py` (provavelmente tendo que adicionar /video no final).

## Melhorias
O sistema pode ser adaptado para um ambiente físico real, substituindo os componentes de simulação por dispositivos reais:
- LEDs (iluminação e ar-condicionado) -> controles de iluminação e climatização controlados via relé ou dispositivos inteligentes.
- Buzzer -> sistema de alarme físico.