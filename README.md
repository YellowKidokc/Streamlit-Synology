# Streamlit Hub for Synology

A Synology NAS package that lets you run and manage multiple Streamlit applications from a single web interface. Install it once, then add as many Streamlit apps as you want!

## Features

- **Synology Package (SPK)** - Install directly from Package Center
- **Multi-App Hub** - Run 5, 10, or more Streamlit apps from one interface
- **Easy App Management** - Just drop Python files into a folder
- **Hot-Reload** - Changes appear automatically (Streamlit default behavior)
- **Docker-Based** - Runs in a container via Synology's Container Manager

## Installation Options

### Option 1: Synology Package (Recommended)

1. **Download or Build the SPK**
   - Download the latest `.spk` file from [Releases](../../releases), OR
   - Build it yourself:
     ```bash
     git clone https://github.com/YellowKidokc/Streamlit-Synology.git
     cd Streamlit-Synology
     ./build-spk.sh
     ```
     The SPK file will be in the `dist/` folder.

2. **Install via Package Center**
   - Open DSM and go to **Package Center**
   - Click **Manual Install** (top-right)
   - Browse and select the `.spk` file
   - Follow the installation wizard

3. **Access Streamlit Hub**
   - Open `http://<your-nas-ip>:8501` in your browser
   - Your apps folder is at `/volume1/docker/streamlit-hub/apps/`

### Option 2: Docker Compose (Manual)

If you prefer to run it manually without the SPK:

1. **Clone the repository** to your NAS:
   ```bash
   git clone https://github.com/YellowKidokc/Streamlit-Synology.git
   cd Streamlit-Synology
   ```

2. **Start the container**:
   ```bash
   docker compose up -d
   ```

3. **Access the UI** at `http://<NAS_IP>:8501`

## Adding Your Streamlit Apps

Once installed, adding apps is easy:

### Method 1: Single-File Apps
Drop a Python file into the apps folder:
```
/volume1/docker/streamlit-hub/apps/my_dashboard.py
```

Your app needs either a `main()` or `app()` function:
```python
import streamlit as st

def main():
    st.title("My Dashboard")
    st.write("Hello from my custom app!")

# Optional: allow running standalone
if __name__ == "__main__":
    main()
```

### Method 2: Multi-File Apps
Create a subfolder with an entry point:
```
/volume1/docker/streamlit-hub/apps/
  sales_app/
    app.py          # or main.py or streamlit_app.py
    utils.py
    data/
      sales.csv
```

The hub will discover any folder containing:
- `streamlit_app.py`
- `app.py`
- `main.py`

### Supported App Structures

| Structure | Example |
|-----------|---------|
| Single file | `apps/dashboard.py` with `main()` function |
| Folder with app.py | `apps/sales/app.py` |
| Folder with main.py | `apps/analytics/main.py` |
| Folder with streamlit_app.py | `apps/reports/streamlit_app.py` |

## Managing Apps

### Adding Apps
Just copy files to the apps folder. They'll appear in the dropdown automatically.

### Updating Apps
Edit your files. Streamlit hot-reloads changes automatically.

### Removing Apps
Delete the file or folder. Refresh the page to update the list.

### Custom Dependencies
For apps that need extra Python packages:

1. SSH into your NAS
2. Access the container:
   ```bash
   docker exec -it streamlit-hub /bin/bash
   ```
3. Install packages:
   ```bash
   pip install pandas numpy plotly
   ```

For permanent changes, edit `requirements.txt` and rebuild:
```bash
docker compose up -d --build
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ROOT` | `/apps` | Directory to scan for apps |
| `DEFAULT_APP` | (none) | Pre-select an app by name |

### Changing the Port

Edit `compose.yaml` (or the Synology container settings):
```yaml
ports:
  - "8080:8501"  # Access on port 8080 instead
```

## Building the SPK Package

To build your own Synology package:

```bash
# Clone the repo
git clone https://github.com/YellowKidokc/Streamlit-Synology.git
cd Streamlit-Synology

# Build the SPK (optional: specify version)
./build-spk.sh 1.0.0

# Find your package
ls dist/
# streamlit-hub-1.0.0-0001.spk
```

### Customizing the Package

Before building:

1. **Icons**: Replace `spk/PACKAGE_ICON.PNG` (72x72) and `spk/PACKAGE_ICON_256.PNG` (256x256)
2. **Metadata**: Edit `spk/INFO` to change description, maintainer, etc.
3. **Scripts**: Modify files in `spk/scripts/` for custom install behavior

## File Structure

```
Streamlit-Synology/
├── build-spk.sh           # Build script for SPK package
├── compose.yaml           # Docker Compose configuration
├── Dockerfile             # Container image definition
├── requirements.txt       # Python dependencies
├── streamlit_app.py       # Main hub/launcher application
├── apps/                  # Your Streamlit apps go here
│   └── hello_world.py     # Sample app
├── spk/                   # Synology package files
│   ├── INFO               # Package metadata
│   ├── PACKAGE_ICON.PNG   # 72x72 icon
│   ├── PACKAGE_ICON_256.PNG # 256x256 icon
│   ├── conf/              # Package configuration
│   └── scripts/           # Install/uninstall scripts
└── dist/                  # Built SPK files (after running build)
```

## Requirements

- Synology DSM 7.0 or later
- Container Manager (Docker) package installed
- About 500MB disk space

## Troubleshooting

### No apps showing up
- Ensure your `.py` files have a `main()` or `app()` function
- Check that files aren't hidden (no `.` prefix)

### App not loading
- Check the container logs: `docker logs streamlit-hub`
- Verify your app runs locally first: `streamlit run your_app.py`

### Port conflict
- Change the port in `compose.yaml` or Synology Container Manager settings

### Permission issues
- The container runs as root by default
- Adjust file permissions on your apps folder if needed

## Uninstalling

### SPK Package
- Go to Package Center > Installed
- Find "Streamlit Hub" and click Uninstall
- Your apps are preserved in `/volume1/docker/streamlit-hub/apps/`

### Docker Compose
```bash
docker compose down
docker rmi streamlit-hub:latest  # optional: remove image
```

## License

MIT License - feel free to modify and distribute.
