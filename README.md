# File Watcher Mover
This project monitors one or more directories and automatically moves files newly created or renamed to other directories based on their extensions or a regular expression pattern. Ideal for organizing downloads, images, videos and other file types automatically.

<p align="center">
  <img src="./assets/app-flow-example.svg" alt="app-flow-example"/>
</p>

## Features

- Monitors multiple directories simultaneously.
- Moves files to target folders based on their extension and regex.
- Supports custom extensions and regex via configuration file.
- Compatible with Windows, Linux, and macOS.

## How It Works

The system uses the [watchdog](https://pypi.org/project/watchdog/) library to observe file creation and movement events. When it detects a new file or a name change of an existing file (e.g. a file is created as '.tmp' and renamed to '.mp4'), it checks the configuration and moves the file to the corresponding directory. This application also has unique run functionality, when using the `--once` argument, it runs only once and then exits.

## Configuration
> [!IMPORTANT]\
> Always keep the `config.json` file in the same directory as `main.py` or the generated `.exe`.  
> Make sure the `config.json` is filled with valid directory paths for both the `"targets"` and `"extension"` fields.
> The 'extensionConfig' key can be kept as an empty object `{}` if there is no custom configuration for extensions.
> The 'regexConfig' key can be kept as an empty object `{}` if there is no custom configuration for regex.
> If a key is specified inside the extensionConfig/regexConfig object, it must be filled with a non-empty string.
> Example:
> ```json
> {
>   "extensionConfig": {
>     "targets": ["C:\\Users\\your_user\\google_drive"],
>     "extensionToPath": {
>       ".pdf": "C:\\Users\\your_user\\Documents\\pdf"
>     }
>   },
>   "regexConfig": {
>     "targets": ["C:\\Users\\your_user\\azure"],
>     "patternToPath": {
>       "^[a-f0-9]{32}( \\(\\d+\\))?$": "C:\\Users\\your_user\\Documents\\college\\docs"
>     }
>   }
> }
> ```

There are no limitations — configure any file extension/regex and as many target directories as you want.

Edit the `config.json` file to define the monitored directories and the destinations for each extension:
- **targets**: List of directories to be monitored.
- **extensionToPath**: Mapping of extensions to destination directories.
- **patternToPath**: Mapping of regex to destination directories.

<details>
  <summary><h2>How to Run</h2></summary>

| Options | Description |
| ------- | ----------- |
| `--once` | Run only once. |

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

This is the approach I recommend the most, I created this app precisely with the intention of using it as a Windows service.

<details>
  <summary><h3>Build (optional)</h3></summary>
If you downloaded File-Watcher-Move-Win64.zip of the releases, you don't need to run the built.

#### Prerequisites
- Pyinstaller

#### Packaging
1. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Build together with the configuration schema file:
    ```sh
    pyinstaller --onefile --add-data "src\\config_schema.json;src" -n "file-watcher-mover.exe" main.py
    ```
</details>

### Prerequisites
- NSSM CLI
- The executable of this application, available in the [releases page](https://github.com/mtpontes/file-watcher-mover/releases)


### Turning into a Windows service
> **WARNING**\
> **For this step it is necessary to execute the terminal as administrator.**

> **Before starting this process, download the `file-watcher-mover-win64.zip` file from the releases, unzip the contents and place both the `.exe` and `config.json` files together in a final directory where you want to keep the program. Only then proceed with the installation of the service.**

```sh
nssm install <service_name> "C:\example\absolute\path\file-watcher-mover.exe"
```

#### Start service
You can either use an NSSM command, or do this manually via the native Windows CLI or via the Services interface.

Examples:
```sh
# Native
net start <service_name>
```

```sh
nssm start <service_name>
```

The `.exe` is linked to the service; to manage it, you need to stop and remove the service.

#### Stop service
To stop the service from running, use one of the commands below. This will stop the program, but it does not remove it from the system — it can be started again at any time.

Examples:
```sh
# Native
net stop <service_name>
```
```sh
nssm stop <service_name>
```

#### Remove service
To completely remove the Windows service, use the command below. After executing this command, the service will no longer exist on the system and will no longer be able to be started until it is reinstalled.

```sh
nssm remove <service_name>
```


### Resource allocation
The process consumes only 12.2MB of RAM, CPU consumption is also irrelevant, while no event is triggered, the CPU remains at 0% usage, when an event is triggered it does not even reach 1% (Ryzen 7 5800X) usage, in addition to the processing occurring fast enough that you don't even notice it happened.
![Windows Task Manager process print](./assets/process.png)

> **NOTE**  
> For more information about NSSM commands, please refer to the official documentation.
</details>

