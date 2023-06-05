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
```bash
$ poetry install
$ poetry run python ./main.py
```

## Todo:
- [ ] Benchmark with other famous commit message generator
- [ ] Smarter prompt for commit message
- [ ] Binary for Windows, Linux, and Mac
- [ ] Tests and CI
- [ ] Publish to PyPI, Homebrew, AUR, and scoop

## License:
GPLv3