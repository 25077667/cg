The cg (commit generator) tool which is generated by OpenAI's API.
==================================================

## Demo:
![](./assert/demo.jpg)

## Requirements:
- Python 3.10+
- poetry
- OpenAI API key

### The OpenAI API key:
You can get the OpenAI API key from [here](https://beta.openai.com/).

Our python code in src/config_parser.py:
```python=
GPT_TOKENS = tuple(os.environ.get('GPT_TOKENS', '').replace(
    ';', ',').replace(':', ',').split(','))
```
So, you can set the environment variable `GPT_TOKENS` to your OpenAI API keys.
Or you could just insert your API key to the `GPT_TOKENS` config file (~/.cg/config.json).

## Usage:
### Download the binary from the latest release:

Linux:
```bash
./cg.elf
```
> Before we publish this tool to the package manager, you could use this command to link the binary to `/usr/local/bin/cg`:
> ```bash
> sudo ln -s ./cg.elf /usr/local/bin/cg
> ```

Mac:
```bash
./cg.macho
```

Windows:
```powershell
.\cg.exe
```

### Using the raw python code:
```bash
$ poetry install
$ poetry run python ./main.py
```

## Todo:
- [ ] Benchmark with other famous commit message generator
- [x] Smarter prompt for commit message
  - [x] Use score to measure the quality of the commit message
- [x] Binary for Windows, Linux, and Mac
- [x] Tests and CI
- [ ] Publish to PyPI, Homebrew, AUR, and scoop

## License:
GPLv3
