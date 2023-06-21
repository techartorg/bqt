only admins and maintainers can release new versions

## Releasing a new version

Find the current version, and use [semver](https://semver.org/) to decide the new version:
> Given a version number MAJOR.MINOR.PATCH, increment the:  
> - MAJOR version when you make incompatible API changes  
> - MINOR version when you add functionality in a backward compatible manner  
> - PATCH version when you make backward compatible bug fixes  
>   
> Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

2. update the addon version in [bqt/__init__.py](https://github.com/techartorg/bqt/blob/master/bqt/__init__.py), and the package version in [setup.py](https://github.com/techartorg/bqt/blob/master/setup.py) 
2. Click `draft a new release` in the top right in [releases](https://github.com/techartorg/bqt/releases) 
3. Click choose a tag, and type the new version in there to create a new tag for it.
   Click `generate release notes`, and add a description and/or title for the release if needed. Feel free to leave them blank.
4. click the green 🟩 `publish release` button, to create the release.
   This triggers a github action that publishes automatically to pypi: https://pypi.org/project/bqt/

If all went well you now should see a new release 
- on github: https://github.com/techartorg/bqt/releases
- the pypi release action should have started, check on it's status in [actions](https://github.com/techartorg/bqt/actions)
- if the action failed, it's likely because you didn't update the version correctly in the `setup.py`.