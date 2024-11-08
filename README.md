# Chivalry 2 Weapons
This project provides a set of json files which contain all weapon data for chivalry 2 weapons, as well as some 
typescript classes to help work with the data, calculating things like damage bonus and stamina damage.

## Using this in your own project
Add the npm package to your project: https://www.npmjs.com/package/chivalry2-weapons

Review the classes in src. Not much is documented, but it should be fairly straight forward. 
The weapon class maps 1:1 with the json files.

## Updating weapon attack data

1. Obtain AbilitiesOverride.json from the game files somehow. I've used FModel with great success.
2. Place it in the `raw_data` directory
3. Run `ingest-new-data.bat` from the project root directory
4. Submit a pull request

Changelog.txt will contain a readable set of stat changes.

Range values are not managed by the script and must be determined manually, currently.
