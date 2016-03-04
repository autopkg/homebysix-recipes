# homebysix-recipes

My recipes for AutoPkg. If you use them, click the ![Star](README-images/star.png) button above to show your support!

Many of these recipes were created with the aid of [Recipe Robot](https://github.com/homebysix/recipe-robot), an app you should definitely check out.


## Installation

To add my repo to your Mac (with AutoPkg and Git already installed), run this command:

```
autopkg repo-add homebysix-recipes
```


## Dependencies

Some of my recipes have parent recipes that live in another repo. To add them all in one shot, here is the command you'll need:

```
autopkg repo-add recipes eholtam-recipes gerardkok-recipes hansen-m-recipes jaharmi-recipes jessepeterson-recipes jleggat-recipes jps3-recipes keeleysam-recipes rustymyers-recipes
```


## Known issues

If you're having a problem with one of my recipes, [check the issues](https://github.com/autopkg/homebysix-recipes/issues) to see whether a known problem exists. If not, please [submit an issue](https://github.com/autopkg/homebysix-recipes/issues/new) so I can investigate.


## Processors

I wrote a couple custom processors for my own recipes. Feel free to refer to them if you find them useful, or modify and redistribute as you like.

- __GoToMeetingURLProvider__ - Uses the GoToMeeting updater JSON to determine the URL to the latest release and the build number for that release.

- __VersionSplitter__ - Takes a string, splits it on a specified character, and returns the specified index. Particularly useful for breaking down multi-part version numbers. For example, "0.3.4 (build 352ac3)" might become simply "0.3.4".


## Submissions

Forks/pulls/issues are welcome. I'm always tweaking.
