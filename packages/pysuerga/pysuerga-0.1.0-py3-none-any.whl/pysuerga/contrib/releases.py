import datetime
import urllib.request
import json


def main(context):
    """
    Fetch the information about the available releases.

    To set up the extension, use:

    ```yaml
    releases:
      kind: github
      repo_url: datapythonista/pysuerga
    ```

    This will make available in the context the next information:

    ```
    {% for version in releases.versions %}
        {{ version.name }}
        {{ version.tag }}
        {{ version.published }}
        {{ version.url }}
    {% endfor %}
    ```
    """
    context['releases']['versions'] = []
    config = context['releases']
    if config.get('kind') == 'github':
        url = f'https://api.github.com/repos/{config["repo_url"]}/releases'
        resp = json.loads(urllib.request.urlopen(url).read())
        for version in resp:
            if version['prerelease']:
                continue
            context['releases']['versions'].append({
                'name': version['tag_name'].lstrip('v'),
                'tag': version['tag_name'],
                'published': datetime.datetime.strptime(version['published_at'],
                                                        '%Y-%m-%dT%H:%M:%SZ'),
                'url': version['assets'][0]['browser_download_url'] if version['assets'] else ''})

    else:
        raise ValueError(
            'The value of releases.config in congif.yml is missing or unknown. '
            'Found: "{config.get("kind")}". Supported: "github"'
        )
    return context
