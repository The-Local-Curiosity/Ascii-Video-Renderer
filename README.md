# Ascii-Video-Renderer
A tool that converts the video into colored ASCII art frames to display into terminal

## Usage 
> python bad_apple.py videos/ritviz.mp4
>
<img width="2454" height="1402" alt="image" src="https://github.com/user-attachments/assets/24de7390-2227-44a2-a4d3-e9ff50aed4a9" />

<img width="2525" height="1405" alt="image" src="https://github.com/user-attachments/assets/28a4b428-6500-4114-ac59-4deee927a3c8" />

## Requirements 
1️⃣ Python Environment (using uv)
I prefers uv for dependency management because it’s fast and reliable.
Create a virtual environment
uv venv

Activate it (Windows)
source .venv/Scripts/activate

Install dependencies
uv pip install -r requirements.txt


2️⃣ FFmpeg (Required for Audio)

ffplay is used to play audio alongside the ASCII video.
FFmpeg does not come with Python and must be installed separately.

Recommended (Windows — using Scoop)

Open PowerShell and run:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
scoop install ffmpeg
