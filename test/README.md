# homebysix-recipes tests

These modules use `nose` to test various recipes in the repo.

## Requirements

You must have the `nose` tool installed.

    pip install nose --user

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

Make sure your working directory is the __homebysix-recipes__ folder (the clone you made, not the clone in your ~/Library/AutoPkg/RecipeRepos folder).

    cd ~/Developer/homebysix-recipes

## Steps

Once you've met the above requirements, run the tests with this command:

    nosetests --verbose --nocapture test

Full testing takes about 30-45 minutes to run, depending on your internet connection speed.
