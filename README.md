# LionDocs Sublime Text Plugin

[![Latest Stable Version](https://img.shields.io/badge/version-1.0.0--beta-informational)](https://github.com/liondocs/liondocs-sublime/releases)

This is an LionDocs plugin for Sublime Text.

[Demo](https://www.youtube.com/watch?v=RRPShnY_10E)

## Installation

For now the plugin is not part of the [Package Control](https://packagecontrol.io/) plugin repository so it must be installed manually.

Go to `Preferences` -> `Package Settings` and in the folder that opens, clone this repository

````
git clone https://github.com/liondocs/liondocs-sublime.git
````

## Configuration

Go to `Preferences` -> `Browse Packages` -> `LionDocs` -> `Settings`

Your user configuration file should look like this:

```jsonc
{
  // Absolute paths to the repositories
  "paths":{
    "content": "",
    "translated-content": ""
  },
  // It must be the same as the one in translated-content
  "lang_code":"",
  // Show alerts in successfully silent operations
  "alerts":true
}
```

> **Note:** Silent operations are those that although they are executed correctly, they do not instantly show some sign that they were executed. As for example the transfer of a file.

## Usage

Plugin functions are executed from the Sublime Text context menu.

### Functions

* **Transfer**: Copies the current opened file file in content to translated-content in its respective path.
	* **Same file**: Copies exactly the same file.
	* **With SourceCommit**: Copies the file and adds the respective SHA in metadata format.
* **Get SHA**: Gets the SHA commit of the current opened file but in content.
	* **To cursor position**: Inserts the SHA commit in metadata format at the current cursor position.
	* **To clipboard**: Copies the SHA commit to the clipboard.

## Advice

For now it is being assumed that your directory tree is something similar to the following:

```
mdn/
├─ content/
├─ translated-content/
```

So with different structures it can cause problems. The root does not necessarily have to be `mdn`, but the sub-directories must have the same name and be in the same folder.

Just tested in Windows.
