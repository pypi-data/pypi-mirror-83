#!/usr/bin/env python
"""
Simple static site generator for open source projects

Pysuerga takes a directory as parameter, and copies all the files into the
target directory after converting markdown files into html and rendering both
markdown and html files with a context. The context is obtained by parsing
the file ``config.yml`` in the root of the source directory.
"""
import importlib
import os
import pathlib
import shutil
import sys
import textwrap
import typing

import markdown
import jinja2
import yaml


def get_callable(obj_as_str: str) -> typing.Callable:
    """
    Get a Python object from its string representation.

    For example, for ``sys.stdout.write`` would import the module ``sys``
    and return the ``write`` function.

    This is used to get the callable of the extensions.
    """
    components = obj_as_str.split(".")
    attrs: typing.List[str] = []
    obj = None
    while components:
        try:
            obj = importlib.import_module(".".join(components))
        except ModuleNotFoundError as exc:
            if str(exc) == "No module named '{'.'.join(components)}'":
                attrs.insert(0, components.pop())
            else:  # The module was found, but not one of its dependencies
                raise
        else:
            break

    if not obj:
        raise ImportError(f'Could not import "{obj_as_str}"')

    for attr in (attrs or ['main']):
        obj = getattr(obj, attr)

    return obj  # type: ignore


def get_context(config_fname: pathlib.Path, **kwargs):
    """
    Load the config yaml as the base context, and enrich it with the
    information added by the extensions defined in the file.
    """
    with open(config_fname) as f:
        context = yaml.safe_load(f)
    context.update(kwargs)

    for extension in context['pysuerga'].get('extensions', []):
        context = get_callable(extension)(context)
        assert context is not None, f'{extension} is missing the return statement'

    return context


def get_source_files(source_path: pathlib.Path) -> typing.Generator[pathlib.Path, None, None]:
    """
    Generate the list of files present in the source directory.
    """
    for root, dirs, fnames in os.walk(source_path):
        base = pathlib.Path(root).relative_to(source_path)
        for fname in fnames:
            yield base / fname


def extend_base_template(content: str, base_template: str) -> str:
    """
    Wrap document to extend the base template, before it is rendered with
    Jinja2.
    """
    return textwrap.dedent(f'''{{% extends "{base_template or 'layout.html'}" %}}
                               {{% block body %}}
                               {content}
                               {{% endblock %}}''')


def main(source_path: pathlib.Path, target_path: pathlib.Path, base_url: str, remove_target: bool):
    """
    Copy every file in the source directory to the target directory.

    For ``.md`` and ``.html`` files, render them with the context
    before copyings them. ``.md`` files are transformed to HTML.
    """
    config_fname = source_path / 'config.yml'

    if remove_target:
        shutil.rmtree(target_path, ignore_errors=True)
    os.makedirs(target_path, exist_ok=True)

    print('Generating context...', file=sys.stderr)
    context = get_context(config_fname, base_url=base_url)
    print('Context generated', file=sys.stderr)

    templates_path = context['pysuerga'].get('templates_path')
    if not templates_path:
        templates_path = pathlib.Path(__file__).parent.resolve() / 'templates'
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))

    for fname in get_source_files(source_path):
        print(f'Processing {fname}', file=sys.stderr)
        os.makedirs(target_path / fname.parent, exist_ok=True)

        if fname.suffix in ('.html', '.md'):
            with open(source_path / fname) as f:
                content = f.read()
            if fname.suffix == '.md':
                body = markdown.markdown(content,
                                         extensions=context['pysuerga'].get('markdown_extensions'))
                content = extend_base_template(body, context['pysuerga'].get('base_template'))
            content = jinja_env.from_string(content).render(**context)
            with open(target_path / fname.with_suffix('.html'), 'w') as f:
                f.write(content)
        else:
            shutil.copy(source_path / fname, target_path / fname.parent)
