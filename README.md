# homebysix-recipes

My recipes for AutoPkg. If you use them, click the Star button above to show your support!

Big thanks to [@rtrouton](https://github.com/rtrouton) for writing the [AutoPkgr](https://github.com/lindegroup/autopkgr) recipes.


## Installation

To use, run this command:

```
autopkg repo-add homebysix-recipes
```

If you previously subscribed to my old repo, you'll need to remove that one and add this new one:

```
autopkg repo-delete https://github.com/homebysix/homebysix-autopkg-recipes.git
autopkg repo-add homebysix-recipes
```


## Dependencies

Some of my recipes have parent recipes that live in another repo. To add them all in one shot, here is the command you'll need:

```
autopkg repo-add recipes eholtam-recipes gerardkok-recipes hansen-m-recipes jaharmi-recipes jleggat-recipes jps3-recipes keeleysam-recipes rustymyers-recipes
```


## Known issues

- __IrradiatedSoftware/Tuck.download.recipe__
    A previous version of this app was signed, but the current version (as of 2015-09-30) is not. This recipe will fail until the developer re-signs the app.

- __LiteratureAndLatte/Scapple.download.recipe__
    The Sparkle feed for this app lists incorrect `http:/` download URLs instead of `http://`. The developer is aware and will correct this in a future release.

- __MacPaw/Gemini.download.recipe__
    The Sparkle feed for this app is malformed, and will probably be corrected by the developer in the future. You can also use an [AppStoreApp recipe](https://github.com/autopkg/nmcspadden-recipes#appstoreapp-recipe) for this app, since it's available in the App Store.

- __Anvil/Anvil.download.recipe__
    The app used to be a standard app-within-a-zip, but as of version 1.1.6, it's now an app-within-a-folder-within-a-zip. I suspect this was a mistake and will be corrected by the developer in the next release. Until then, Anvil recipes will fail.

## Submissions

Forks/pulls/issues are welcome. I'm always tweaking.
