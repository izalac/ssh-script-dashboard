# Command setup for SSH Script Dashboard

Edit the config/commands.json file to add your commands. Commands are listed in JSON format (be mindful of the proper JSON formatting), and listed as simple key-value pairs.

The key part should be URL-safe, as it is used for both button labels on the webpage to name, and link that calls it in the backend.

The value part is the script that you wish to run. Regular commands can also be executed instead (and are provided in the examples).

Script and command paths depend on the user executing them, depending on the [EXECUTE_MODEL](environment.md) variable whether the local user who runs flask, or the configured SSH remote user and their default login environment.

[Back to Readme](../README.md)