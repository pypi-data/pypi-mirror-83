import urllib.request
import json


def main(context):
    """
    Fetch the information from the members defined in `config.yml`.

    The members should be defined in the next way:

    ```yaml
    team:
    - name: "Maintainers"
      kind: github
      members:
      - github_user_of_active_maintainer_1
      - github_user_of_active_maintainer_2

    - name: "Emeritus maintainers"
      members:
      - github_user_of_emeritus_maintainer_1
      - github_user_of_emeritus_maintainer_2
      - github_user_of_emeritus_maintainer_3
    ```

    When `kind` is "github", this extension fetches the information of the user
    from the GitHub API.

    There can be as many sections as needed, and any names can be used, but the
    next are recommended, if the corresponding sections are of interest:

    - Maintainers
    - Triaggers
    - Code of conduct committee
    - Emeritus maintainers
    """
    for group in context['team']:
        if group['kind'] == 'github':
            members = []
            for member in group['members']:
                url = f'https://api.github.com/users/{member}'
                members.append(json.loads(urllib.request.urlopen(url).read()))
            group['members'] = members
    return context
