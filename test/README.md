# homebysix-recipes tests

These modules use `nose` to test various recipes in the repo.

## Requirements

You'll need Python 3. (Note: AutoPkg's included Python 3 does not include `nose`, so it's recommended to use a separate Python 3. Homebrew is one way to get that.)

    brew install python3

You'll need the `nose` testing tool.

    pip3 install nose --user

You'll also need a few repos that contain required parent recipes:

    autopkg repo-add \
        recipes \
        eholtam-recipes \
        foigus-recipes \
        gerardkok-recipes \
        hansen-m-recipes \
        jaharmi-recipes \
        jessepeterson-recipes \
        jleggat-recipes \
        jps3-recipes \
        keeleysam-recipes \
        rustymyers-recipes

Make sure your working directory is the __homebysix-recipes__ folder (the clone you made with `git clone`, not the clone in your ~/Library/AutoPkg/RecipeRepos folder).

    cd ~/Developer/homebysix-recipes

## Steps

Once you've met the above requirements, run the tests with this command:

    python3 -m nose --verbose --nocapture test

Full testing takes about 30-45 minutes to run, depending on your internet connection speed.
