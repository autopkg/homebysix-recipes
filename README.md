homebysix-recipes
=========================

My recipes for AutoPkg.

Big thanks to [@rtrouton](https://github.com/rtrouton) for writing the [AutoPkgr](https://github.com/lindegroup/autopkgr) recipes.


## Installation

To use, run this command:
```
autopkg repo-add https://github.com/autopkg/homebysix-recipes.git
```

If you previously subscribed to my old repo, you'll need to remove that one and add this new one:
```
autopkg repo-delete https://github.com/homebysix/homebysix-autopkg-recipes.git
autopkg repo-add https://github.com/autopkg/homebysix-recipes.git
```


## Dependencies

My `GitHub.pkg` recipe requires [@keeleysam](https://github.com/keeleysam)'s `GitHub.download` recipe, so be sure to add his repo:
```
autopkg repo-add https://github.com/autopkg/keeleysam-recipes.git
```
My `BonjourBrowser.pkg` recipe requires [@jleggat](https://github.com/jleggat)'s `BonjourBrowser.download`:
```
autopkg repo-add https://github.com/autopkg/jleggat-recipes.git
```
And my `Divvy.pkg` recipe requires [@jaharmi](https://github.com/jaharmi)'s `Divvy.download`:
```
autopkg repo-add https://github.com/autopkg/jaharmi-recipes.git
```


## Submissions

Forks/pulls/issues are welcome. I'm always tweaking.