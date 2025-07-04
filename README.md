# Enhanced Torrench

![Screenshot](https://github.com/almezali/enhanced-torrench/blob/main/01-Screenshot.png)
![Screenshot](https://github.com/almezali/enhanced-torrench/blob/main/02-Screenshot.png)
![Screenshot](https://github.com/almezali/enhanced-torrench/blob/main/03-Screenshot.png)

A powerful multi-site torrent search tool that allows you to search across multiple popular torrent sites simultaneously from the command line. Enhanced Torrench automatically tests site availability and provides comprehensive search results with detailed information.

## ✨ Features

- **Multi-site Search**: Search across 5 popular torrent sites simultaneously
- **Smart Site Testing**: Automatically tests site availability and uses only working mirrors
- **Comprehensive Results**: Displays detailed information including seeds, leeches, size, category, and uploader
- **Interactive Interface**: Browse results with an interactive index system
- **Color-coded Output**: VIP and Trusted uploaders are highlighted for easy identification
- **Pagination Support**: Search multiple pages for comprehensive results
- **Flexible Filtering**: Limit results and customize search parameters
- **Cross-platform**: Works on Linux, macOS, and Windows

### Supported Torrent Sites

- **The Pirate Bay** (Multiple mirrors)
- **Kickass Torrents** (Multiple mirrors)
- **Torrentz2** (Multiple mirrors)
- **LimeTorrents** (Multiple mirrors)
- **RARBG** (Multiple mirrors)

## 🔧 Requirements

### System Requirements

- **Python**: 3.6 or higher
- **Internet Connection**: Required for searching torrent sites
- **Terminal/Command Prompt**: For command-line interface

### Python Dependencies

```
requests>=2.25.0
beautifulsoup4>=4.9.0
lxml>=4.6.0
tabulate>=0.8.0
termcolor>=1.1.0
```

## 📦 Installation

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Install required packages
pip3 install requests beautifulsoup4 lxml tabulate termcolor

# Download the script
wget https://raw.githubusercontent.com/almezali/enhanced-torrench/main/torrench.py

# Make it executable
chmod +x torrench.py
```

### Linux (CentOS/RHEL/Fedora)

```bash
# Install Python and pip
sudo yum install python3 python3-pip  # CentOS/RHEL
# OR
sudo dnf install python3 python3-pip  # Fedora

# Install required packages
pip3 install requests beautifulsoup4 lxml tabulate termcolor

# Download the script
wget https://raw.githubusercontent.com/almezali/enhanced-torrench/main/torrench.py

# Make it executable
chmod +x torrench.py
```

### Linux (Arch Linux)

```bash
# Install Python and pip
sudo pacman -S python python-pip

# Install required packages
pip install requests beautifulsoup4 lxml tabulate termcolor

# Download the script
wget https://raw.githubusercontent.com/almezali/enhanced-torrench/main/torrench.py

# Make it executable
chmod +x torrench.py
```

### macOS

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Install required packages
pip3 install requests beautifulsoup4 lxml tabulate termcolor

# Download the script
curl -O https://raw.githubusercontent.com/almezali/enhanced-torrench/main/torrench.py

# Make it executable
chmod +x torrench.py
```

### Windows

#### Method 1: Using Python from Microsoft Store

1. Install Python from Microsoft Store (Python 3.11 recommended)
2. Open Command Prompt or PowerShell
3. Install required packages:
```cmd
pip install requests beautifulsoup4 lxml tabulate termcolor
```
4. Download the script to your desired location
5. Run from Command Prompt/PowerShell

#### Method 2: Using Python from python.org

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, make sure to check "Add Python to PATH"
3. Open Command Prompt
4. Install required packages:
```cmd
pip install requests beautifulsoup4 lxml tabulate termcolor
```
5. Download the script to your desired location

## 🚀 Usage

### Basic Usage

```bash
# Search for torrents
python3 torrench.py "Ubuntu 22.04"

# On Windows
python torrench.py "Ubuntu 22.04"
```

### Advanced Usage

```bash
# Search multiple pages (up to 10 pages per site)
python3 torrench.py "Linux distro" -p 3

# Limit number of results
python3 torrench.py "Python tutorial" -l 20

# Combine options
python3 torrench.py "Movie 2023" -p 2 -l 50
```

### Command Line Options

```
positional arguments:
  QUERY                 Search query (in English)

optional arguments:
  -h, --help            show this help message and exit
  -p N, --pages N       Number of pages to search per site (default: 1, max: 10)
  -s SITES, --sites SITES
                        Comma-separated list of sites to search (default: all)
  -l N, --limit N       Maximum number of results to display (default: unlimited)
  -v, --version         show program's version number and exit
```

### Interactive Features

After search results are displayed, you can:

- Enter a torrent index number to view detailed information
- Enter `0` or `exit` to quit the interactive mode
- Use `Ctrl+C` to exit at any time

## 📊 Output Format

The tool displays results in a formatted table with the following columns:

- **SITE**: The torrent site where the result was found
- **CATEGORY**: Category of the torrent (if available)
- **NAME**: Torrent name (color-coded for VIP/Trusted uploaders)
- **INDEX**: Reference number for interactive selection
- **UPLOADER**: Username of the uploader
- **SIZE**: File size
- **SEEDS**: Number of seeders
- **LEECHES**: Number of leechers
- **DATE**: Upload date

### Color Coding

- **Green**: VIP uploaders
- **Magenta**: Trusted uploaders
- **White**: Regular uploaders

## 🔍 Examples

### Example 1: Basic Search
```bash
python3 torrench.py "Ubuntu 22.04"
```

### Example 2: Movie Search with Multiple Pages
```bash
python3 torrench.py "Inception 2010" -p 3 -l 25
```

### Example 3: Software Search
```bash
python3 torrench.py "Adobe Photoshop" -p 2
```

## 🛠️ Troubleshooting

### Common Issues

1. **No working torrent sites found**
   - Check your internet connection
   - Try using a VPN as some sites may be blocked in your region
   - Wait and try again later as sites may be temporarily down

2. **Import errors**
   - Ensure all required packages are installed: `pip install -r requirements.txt`
   - Check Python version: `python --version` (should be 3.6+)

3. **Permission denied (Linux/macOS)**
   - Make the script executable: `chmod +x torrench.py`
   - Run with `python3` instead of `./torrench.py`

4. **Encoding issues (Windows)**
   - Use Command Prompt or PowerShell instead of older terminal emulators
   - Ensure your terminal supports UTF-8 encoding

### Platform-Specific Notes

#### Linux
- Some distributions may require `python3-dev` package for lxml compilation
- Use `python3` command instead of `python` on most distributions

#### macOS
- May require Xcode command line tools for some packages: `xcode-select --install`
- Use `python3` command, as `python` might point to Python 2.7

#### Windows
- Use Command Prompt or PowerShell for best compatibility
- Ensure Python is added to PATH during installation
- Some antivirus software may flag the script - add it to exceptions if needed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This tool is for educational purposes only. Users are responsible for complying with their local laws and the terms of service of the torrent sites. The authors do not encourage or support piracy or copyright infringement.

## 🔗 Links

- [Report Issues](https://github.com/almezali/enhanced-torrench/issues)

---
