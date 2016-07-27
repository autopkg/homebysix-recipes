# FindAndReplace

This processor performs a find/replace on a specified environment variable. The result is saved as a new variable, `%output_string%`.

## Example

Here's an example of using FindAndReplace to replace `http:///` in a developer's Sparkle feed with `https://` prior to calling URLDownloader:

```
<dict>
    <key>Arguments</key>
    <dict>
        <key>find</key>
        <string>http:///scrivener.s3.amazonaws.com</string>
        <key>input_string</key>
        <string>%url%</string>
        <key>replace</key>
        <string>https://scrivener.s3.amazonaws.com</string>
    </dict>
    <key>Processor</key>
    <string>com.github.homebysix.FindAndReplace/FindAndReplace</string>
</dict>
```
