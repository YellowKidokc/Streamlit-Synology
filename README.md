# Streamlit Synology Hub

This repository packages a small Streamlit launcher that you can run on a Synology NAS. It lets you drop multiple Streamlit apps into a shared folder and switch between them from a single web UI.

## Features
- Runs in Docker (works with Synology's Container Manager/Docker package).
- Mount a host folder; each `.py` file or sub-folder with an `app.py`, `main.py`, or `streamlit_app.py` becomes a selectable app.
- Hot-reloads when files change (Streamlit default behavior).
- Ships with a sample `hello_world` app.

## Quick start (Synology Docker/Container Manager)
1. **Prepare a folder** on your NAS (e.g., `streamlit-apps`). Put your Streamlit app files inside it; include at least one `.py` file with a `main()` (or `app()`) function.
2. **Copy this repository** somewhere on your NAS and open a terminal/SSH session.
3. **Create the container**:
   ```bash
   cd /path/to/Streamlit-Synology
   docker compose up -d
   ```
   The container mounts `./apps` (in this repo) to `/apps` inside the container. Replace it with your NAS folder by editing `compose.yaml` if desired.
4. **Open the UI** at `http://<NAS_IP>:8501`. Use the dropdown to pick any discovered app.

### Adding or updating apps
- Drop a new file like `apps/my_dashboard.py` (with a `main()` or `app()` function), or create a folder like `apps/sales_app/app.py`.
- Streamlit reloads code automatically. You can also restart the container with `docker compose restart`.

### Environment variables
- `APP_ROOT` (default `/apps`): where the launcher looks for apps.
- `DEFAULT_APP` (optional): preselects an app by its folder/filename stem.

### Custom Python dependencies
For per-app dependencies, add a `requirements.txt` next to the app file or folder and install it inside the container (e.g., `docker exec -it <container> /bin/bash` then `pip install -r /apps/your_app/requirements.txt`). To change global dependencies, edit `requirements.txt` in this repo and rebuild (`docker compose up -d --build`).

### Stopping and removing
```bash
docker compose down
```

## File layout
- `compose.yaml`: One-service stack exposing port 8501.
- `Dockerfile`: Builds a minimal image with Streamlit and the launcher.
- `streamlit_app.py`: Launcher that discovers and runs child apps.
- `apps/`: Place your Streamlit apps here; includes `hello_world.py` as an example.

## Troubleshooting
- If no apps appear, ensure the `APP_ROOT` folder exists and contains at least one `.py` file with `main()` or `app()`.
- If a specific app fails to render, open the app file and confirm it defines `main()` (preferred) or `app()`; errors from that app will show in the UI.

## Notes
- The container runs as root by default. Adjust `user:` in `compose.yaml` if you need different permissions on your Synology volume.
- Streamlit's default hot-reload watches files inside the mounted folder; large folders may consume more CPU.
