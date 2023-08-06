# Pysuerga - Python simple static site generator for open source projects

Pysuerga is a very simple static site generator. It was initially created
for [pandas](https://pandas.pydata.org), but is used in other projects.

To use Pysuerga you need to create the website structure for your project,
with markdown templates, and Pysuerga will generate the same structure after
rendering the files.

It is able to manage variables in a structured way, can use Jinja2 in the templates
and includes plugins for some common pages: team page with GitHub info, blog
aggregator, release information, etc.

## Installation

You can install Pysuerga with `pip`:
```sh
$ pip install pysuerga
```

Or with `conda`:
```sh
$ conda install -c conda-forge pysuerga
```

## Usage

A simple example of using Pysuerga. Create a directory `myproject` with the
next content:
```
+ myproject
  - config.yml
  - index.md
  - about.md
  + static
    logo.svg
```

Run `python -m pysuerga <project-directory>` to build the website. The output
will be:
```
+ build
  - index.html
  - about.html
  + static
    logo.svg
```

As you can see, the content of the directory is replicated, but markdown (`.md`)
files are rendered and coverted to `.html` files.

The file `config.yml` contains the settings of the project, as well as any variables
that are needed.

For example, consider this `index.md` file:

```markdown
# Home page

Hey, welcome to the home page of the {{ project_name }} project.

Visit [our about us page](about.html) for more information about us.
```

And this `config.yml` file:

```yaml
pysuerga:
  ...  # Pysuerga main settings (see Settings section)
project_name: "My project"
```

Pysuerga will perform these actions:
- Render markdown and html files with [Jinja2](https://jinja.palletsprojects.com/) and the content of `config.html`
- Render mardown files as html with [Markdown](https://github.com/Python-Markdown/markdown)
- Copy all files to the output directory

## Settings

You can add any arbitrary content you want to `config.yml`, and it will be available to use in your files.

For example, we can add the next content:

```yaml
pysuerga:
  ...  # Pysuerga main settings

topic: "open source analytics languages"

languages:
- Python
- R
- Julia
- Scala
```

And then, in any of our files, we can access them using Jinja2:

```markdown
This is a list of {{ topic }}:

{% for language in languages %}
- {{ language }}
{% endfor %}
```

Pysuerga has a set of predefined settings. These should be under the section `pysuerga` of `config.yml`, and are used for
different aspects.
