# homebysix-recipes

My recipes for AutoPkg. If you use them, click the ![Star](README-images/star.png) button above to show your support!

Many of these recipes were created with the aid of [Recipe Robot](https://github.com/homebysix/recipe-robot), an app you should definitely check out.


## Installation

To add my repo to your Mac (with AutoPkg and Git already installed), run this command:

```
autopkg repo-add homebysix-recipes
```


## Dependencies

Some of my recipes have parent recipes that live in another repo. Refer to a given recipe's parent recipe identifier to determine which repo you'll need to add. For example, my Sketch.pkg recipe uses `com.github.foigus.download.Sketch` as its parent, so you would need to run `autopkg repo-add foigus-recipes` before you could run Sketch.pkg successfully.


## Known issues

If you're having a problem with one of my recipes, [check the issues](https://github.com/autopkg/homebysix-recipes/issues) to see whether a known problem exists. If not, please [submit an issue](https://github.com/autopkg/homebysix-recipes/issues/new) so I can investigate.


## Shared Processors

I wrote a couple custom processors for my own recipes. Feel free to refer to them if you find them useful, or modify and redistribute as you like.

- __[BinaryFileVersioner](BinaryFileVersioner/README.md)__  
    This processor returns the version number of a binary file that has an embedded info plist, using the /usr/bin/otool command.

- __[FindAndReplace](FindAndReplace/README.md)__  
This processor performs a find/replace on a specified environment variable. The result is saved as a new variable, `%output_string%`.

- __[VersionSplitter](VersionSplitter/README.md)__  
    This processor splits version numbers. This is especially useful if the version contains two parts (e.g. version and build) but you only need/want one of them. For example, "0.3.4 (build 352ac3)" could become simply "0.3.4".


## Submissions

Forks/pulls/issues are welcome. I'm always tweaking.
