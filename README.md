# File Watcher Mover

This project monitors one or more directories and automatically moves newly created or renamed files to other directories based on their extensions. Ideal for organizing downloads, images, videos, and other types of files automatically.

## Features

- Monitors multiple directories simultaneously.
- Moves files to target folders based on their extension.
- Supports custom extensions via configuration file.
- Compatible with Windows, Linux, and macOS.

## How It Works

The system uses the [watchdog](https://pypi.org/project/watchdog/) library to observe file creation and movement events. When it detects a new file or a change in extension (e.g., a file is created as '.tmp' and renamed to '.mp4'), it checks the configuration and moves the file to the corresponding directory.

## Configuration

There are no limitations — configure any file extension and as many target directories as you want.

Edit the `config.json` file to define the monitored directories and the destinations for each extension:

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

- **targets**: List of directories to be monitored.
- **extensions**: Mapping of extensions to destination directories.

<details>
  <summary><h2>How to Run</h2></summary>

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/mtpontes/file-watcher-mover.git
   cd file-mover
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # On Windows
   source venv/bin/activate  # On Linux/macOS
   ```

3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

### Usage

Run the main script:

```sh
python main.py
```

The program will stay running, monitoring the defined directories. To stop it, press `Ctrl+C`.
</details>

## License

This project is licensed under the MIT License.

---

Feel free to contribute or suggest improvements!
