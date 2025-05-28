# File Watcher Mover

Este projeto monitora um ou mais diretórios e move automaticamente arquivos recém-criados ou renomeados para outros diretórios, de acordo com sua extensão. Ideal para organizar downloads, imagens, vídeos e outros tipos de arquivos de forma automática.

## Funcionalidades

- Monitora múltiplos diretórios simultaneamente.
- Move arquivos para pastas de destino configuradas conforme a extensão.
- Suporte a extensões personalizadas via arquivo de configuração.
- Compatível com Windows, Linux e macOS.

## Como funciona

O sistema utiliza a biblioteca [watchdog](https://pypi.org/project/watchdog/) para observar eventos de criação e movimentação de arquivos. Ao detectar um novo arquivo ou uma mudança de extensão (Ex: o arquivo é criado como '.tmp' e é renomeado para '.mp4'), ele verifica a configuração e move o arquivo para o diretório correspondente.

## Configuração

Não há limitações, configure a extensão de arquivo que você quiser e quantos diretórios alvo quiser.

Edite o arquivo `config.json` para definir os diretórios monitorados e os destinos para cada extensão:

```json
{
  "targets": [
    "./dir-teste",
    "./outros-arquivos"
  ],
  "extensions": {
    ".txt":   "./textos",
    ".jpg":   "./imagens/jpg",
    ".mp4":   "./videos/mp4"
  }
}
```

- **targets**: Lista de diretórios a serem monitorados.
- **extensions**: Mapeamento de extensões para diretórios de destino.

<details>
  <summary><h2>Como rodar</h2></summary>

### Instalação

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-usuario/file-mover.git
   cd file-mover
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # No Windows
   source venv/bin/activate  # No Linux/macOS
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

### Uso

Execute o script principal:

```sh
python main.py
```

O programa ficará em execução, monitorando os diretórios definidos. Para interromper, pressione `Ctrl+C`.
</details>

## Licença

Este projeto está licenciado sob a licença MIT.

---

Sinta-se à vontade para contribuir ou sugerir melhorias!