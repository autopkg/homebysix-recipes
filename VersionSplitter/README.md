# VersionSplitter

This processor splits version numbers. This is especially useful if the version contains two parts (e.g. version and build) but you only need/want one of them.

## Example 1

By default, it splits using a space, and returns the first item.

```
<dict>
    <key>Processor</key>
    <string>com.github.homebysix.VersionSplitter/VersionSplitter</string>
</dict>
```

- Example 1 `version` input: `3.0.8 :074a131:`
- Example 1 `version` output: `3.0.8`

## Example 2

You can also split on other characters, like hyphens.

```
<dict>
    <key>Processor</key>
    <string>com.github.homebysix.VersionSplitter/VersionSplitter</string>
    <key>Arguments</key>
    <dict>
        <key>split_on</key>
        <string>-</string>
    </dict>
</dict>
```

- Example 2 `version` input: `1.3.1-stable`
- Example 2 `version` output: `1.3.1`

## Example 3

You can also return a part of the version other than the first part. For example, here we can retrieve index 2 (the third part, after splitting).

```
<dict>
    <key>Processor</key>
    <string>com.github.homebysix.VersionSplitter/VersionSplitter</string>
    <key>Arguments</key>
    <dict>
        <key>index</key>
        <integer>2</integer>
        <key>split_on</key>
        <string>_</string>
    </dict>
</dict>
```

- Example 3 `version` input: `macosx_64bit_3.0`
- Example 3 `version` output: `3.0`
