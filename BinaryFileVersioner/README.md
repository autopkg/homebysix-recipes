# BinaryFileVersioner

This processor returns the version number of a binary file that has an embedded info plist, using the /usr/bin/otool command.

## Input Variables

- `input_file_path`: File path to a binary file (not app bundle).
- `plist_version_key`: Which plist key to use. Defaults to CFBundleShortVersionString.

## Output Variables

- `version`: Version of the file.

## Example

```xml
<dict>
    <key>Processor</key>
    <string>com.github.homebysix.BinaryFileVersioner/BinaryFileVersioner</string>
    <key>Arguments</key>
    <dict>
        <key>input_file_path</key>
        <string>%RECIPE_CACHE_DIR%/%NAME%/usr/local/bin/updatetool</string>
        <key>plist_version_key</key>
        <string>CFBundleVersion</string>
    </dict>
</dict>
```
