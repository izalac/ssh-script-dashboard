# Command setup for SSH Script Dashboard

Edit the config/commands.json file to add your commands. Commands are listed in JSON format (be mindful of the proper JSON formatting), and listed as simple key-value pairs.

The key part should be URL-safe, as it is used for both button labels on the webpage to name, and link that calls it in the backend.

The value part is the script that you wish to run. Regular commands can also be executed instead (and are provided in the examples).

Script and command paths depend on the user executing them, depending on the [EXECUTE_MODEL](environment.md) variable whether the local user who runs flask, or the configured SSH remote user and their default login environment.

## Display behavior

Most command line tools and scripts output in plaintext. Internally, this app converts all script standard output to HTML by replacing newline characters with a \<br /> tag. If you wish to disable this behavior, comment out the corresponding lines in envexecute.py by adding a # symbol in front, like this:

    # output = output.replace('\n', '<br />')

Any HTML tags in your output will be rendered, using the same environment as index.html. This means Tailwind CSS classes and HTMX are also available, so you can use this to enhance your script output or extend the SSH Script Dashboard itself.

You can further customize the appearance and behavior in index.html.

[Back to Readme](../README.md)