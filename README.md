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
> [!IMPORTANT]\
> Always keep the `config.json` file in the same directory as `main.py` or the generated `.exe`.  
> Make sure the `config.json` is filled with valid directory paths for both the `"targets"` and `"extension"` fields.  
> Example:
> ```json
> {
>   "targets": [
>     "C:\\Users\\your_user\\Downloads"
>   ],
>   "extension": {
>     ".pdf": "C:\\Users\\your_user\\Documents\\pdf"
>   }
> }
> ```

There are no limitations — configure any file extension and as many target directories as you want.

Edit the `config.json` file to define the monitored directories and the destinations for each extension:



- **targets**: List of directories to be monitored.
- **extensions**: Mapping of extensions to destination directories.

<details>
  <summary><h2>How to Run</h2></summary>

<details>
  <summary><h4>Executable</h4></summary>

  Go to the [releases page](https://github.com/mtpontes/file-watcher-mover/releases), download the `file-watcher-mover.zip`, extract the zip file to the final directory where you want to keep the application, and run the executable.

</details>

<details>
  <summary><h4>Script</h4></summary>

#### Installation
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

4. **Run:**
```sh
python main.py
```
The program will stay running, monitoring the defined directories. To stop it, press `Ctrl+C`.
</details>

</details>

<details>
  <summary><h2>Windows Service</h2></summary>

<!-- ### Build
#### Prerequisites
- Pyinstaller

```bash
pyinstaller --onefile main.py
``` -->

<!-- **Build together with the configuration file:**
```bash
pyinstaller --onefile --add-data "config.json;." main.py
``` -->

#### Prerequisites
- NSSM CLI

#### Turning into a service
```bash
nssm install <service_name> "C:\example\absolute\path\main.exe"
```

#### Start
```bash
nssm start <service_name>
```

The `.exe` is linked to the service; to manage it, you need to stop and remove the service.

> **NOTE:**  
> For more information about NSSM commands, troubleshooting with PyInstaller, and other advanced usage, please refer to the official documentation of each tool.
</details>

