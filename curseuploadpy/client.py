import requests
import json

class CurseUploadClient:
    """
    CurseUploadClient - This class exposes the raw CurseForge Upload API.

    Specs: https://support.curseforge.com/en/support/solutions/articles/9000197321-curseforge-upload-api
    """
    def __init__(self,
                 api_key,
                 endpoint='https://minecraft.curseforge.com'):
        """
        Create a new handler. Pass in a valid CurseForge API key.
        :param self:
        :param api_key: The API key created under account's API Tokens
        :param endpoint: Game-specific endpoint. Default is Minecraft.
        :return: The client
        """
        self._endpoint = endpoint
        self._key = api_key

    def _call_get(self, url, **kwargs):
        headers = {'X-Api-Token': self._key}
        response = requests.get(self._endpoint + url, headers=headers, **kwargs)
        return response.json()

    def _call_post(self, url, **kwargs):
        headers = {'X-Api-Token': self._key}
        response = requests.post(self._endpoint + url, headers=headers, **kwargs)
        return response.json()

    def game_versions(self):
        url = '/api/game/versions'
        response = self._call_get(url)
        return response

    def game_dependencies(self):
        url = '/api/game/dependencies'
        response = self._call_get(url)
        return response

    def upload_file(self,
                    project_id: int,
                    file_path: str,
                    changelog: str,
                    changelog_type: str,
                    releaseType: str,
                    parent_file_id: int = None,
                    game_versions: list[int] = None,
                    displayName: str = None,
                    deps: list[tuple[str, str]] = None):
        """
        Upload a file to the specified project. Use this to upload new files or append child files to existing files

        :param project_id: The project ID to upload the file to
        :param file_path: The path to the file to upload
        :param changelog: Changelog string
        :param changelog_type: Format of changelog string. Either "text", "html" or "markdown"
        :param releaseType: Release type of the file. Either "alpha", "beta" or "release"
        :param parent_file_id: (Optional) The parent file ID to append this file to
        :param game_versions: Array of game versions this file is compatible with. Required if parent_file_id is not provided
        :param displayName: (Optional) A friendly display name for this file
        :param deps: (Optional) A list of 2-string tuples containing dependency slug and dependency type. The dependency type
                     is one of: "embeddedLibrary", "incompatible", "optionalDependency", "requiredDependency", or "tool"
        :return:
        """
        url = f'/api/projects/{project_id}/upload-file'
        metadata = {
            'changelog': changelog,
            'changelogType': changelog_type,
            'releaseType': releaseType
        }

        if parent_file_id and game_versions:
            raise ValueError('You must provide either parent_file_id or game_versions, not both')
        elif parent_file_id:
            metadata['parentFile'] = parent_file_id
        elif game_versions:
            metadata['gameVersions'] = game_versions
        else:
            raise ValueError('You must provide either parent_file_id or game_versions')

        if displayName:
            metadata['displayName'] = displayName

        if deps and len(deps) > 0:
            metadata['relations'] = {'projects': []}
            for slug, dep_type in deps:
                metadata['relations']['projects'].append({
                    'slug': slug,
                    'type': dep_type
                })

        files = {
            'file': open(file_path, 'rb'),
            'metadata': (None, json.dumps(metadata), 'application/json')
        }
        response = self._call_post(url, files=files)
        return response