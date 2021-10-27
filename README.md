# Remote Administration Tool (RAT)

Rat written in python, for educational purposes only.

Functions:

1. Explore the remote file system
2. Get files from the victim
3. Set or place files on the victim
4. Take screenshots (macOS and Linux may need sudo)
5. Run cmd or terminal commands remotely

## Installation of files

If you want to take screenshots of the victim you may need to install
ImageGrab from the PIL library on that host.

```bash
pip3 install Pillow
or
pip3 freeze > requirements.txt
```

## Usage

```bash
python3 hacker.py
or
python3 victim.py
```
