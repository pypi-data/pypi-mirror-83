# latex-todo-gen

TODOs and FIXMEs from your LaTeX project.

## Usage

```
usage: latex-todo-gen [-h] [--directories DIRECTORIES] [--files FILES]
                      [--keywords KEYWORDS] [--outfile OUTFILE]
                      [--description DESCRIPTION] [--footer FOOTER]

Extract TODOs from TeX files.

optional arguments:
  -h, --help            show this help message and exit
  --directories DIRECTORIES, -d DIRECTORIES
                        comma separated list of directories
  --files FILES, -f FILES
                        comma separated list of files
  --keywords KEYWORDS, -k KEYWORDS
                        comma separated list of keywords
  --outfile OUTFILE, -o OUTFILE
                        output file
  --description DESCRIPTION
                        set output file description
  --footer FOOTER       set output file footer

For more information, see https://gitlab.com/matyashorky/latex-todo-gen.
```

## Examples
```bash
# Use default settings
./latex_todo_gen.py

# Set keywords
./latex_todo_gen.py -k "REVIEW,FIXME,TODO,NOTE"

# Set description and output file
./latex_todo_gen.py --description "This file is generated on every commit." -o "WIP.md"

# Set sources
./latex_todo_gen.py -d "src,settings" -f "main.tex"
```

To use arguments in pre-commit, use `args` parameter:

```yaml
- repo: https://gitlab.com/matyashorky/latex-todo-gen
  rev: 'v0.4'
  hooks:
  - id: latex-todo-gen
  	args: [-k "REVIEW,FIXME,TODO,NOTE", -d "src,settings"]
```

## Contributing

**PRs are welcome.**

I'm currently looking for:

- [`pre-commit`](https://pre-commit.com): I haven't been able to make it work, it seemed not to be able to locate the python script.
