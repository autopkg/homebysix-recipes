# GitLabArtifact recipe templates

These [AutoPkg](http://autopkg.github.io/autopkg/) recipes enable Mac admins to easily obtain artifacts built by GitLab CI/CD jobs and copy them elsewhere or import them into Munki. This removes one unnecessary manual step between approval of internal tool code changes and the distribution of the resulting installers to managed Macs.

These recipes are specifically targeted at organizations who use MunkiPkg to build installers for their managed Macs, and who store the source files for those installers in a GitLab repository. However, the same framework could be used to import other types of files from GitLab artifacts.

The recipes aren't meant to be run directly, and won't function without creating an override first. See the directions below.

## Configuring MunkiPkg builds in GitLab CI/CD

(You can skip this section if you produce your GitLab artifacts using something other than MunkiPkg.)

You will need a [macOS GitLab runner](https://docs.gitlab.com/runner/install/osx.html) installed and registered in order to do this. Additionally, MunkiPkg will need to be installed on the runner and symlinked from the PATH.

Configure the .gitlab-ci.yml file with the job for building MunkiPkg projects. If your repo contains a single MunkiPkg project, your job might look like this:

```yaml
munkipkg_building:
  stage: build
  tags:
    - macOS
  script: /usr/local/bin/munkipkg .
  artifacts:
    paths:
    - build/*.pkg
  only:
    - master
```

If your repo contains multiple MunkiPkg project folders, your job might reference a separate build script and different artifact paths, like this:

```yaml
munkipkg_building:
  stage: build
  tags:
    - macOS
    script: munkipkg_building.sh
  artifacts:
    paths:
    - */build/*.pkg
  only:
    - master
```

The contents of the munkipkg_building.sh script would look something like this:

```sh
#!/bin/bash
for proj in */build-info.*; do
    /usr/local/bin/munkipkg "$(dirname "$proj")" || exit 1
done
```

With this configuration, every commit or merge to the master branch will result in a fresh pkg file being created and stored in the GitLab repo artifacts.

## Creating overrides and using the recipes

Before you can use any of the recipes, please create a [personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) in GitLab and store it somewhere safe. You will need this token when creating the overrides.

Note: If storing the token in your AutoPkg override is not advisable for security purposes, it's also possible to inject the variable during your AutoPkg recipe run using `-k`. For example: `autopkg run -v MyGitLabOverride.pkg -k PRIVATE_TOKEN=abcdef123456`

### GitLabArtifact.download

This recipe produces a zip file that contains all artifacts produced by the specified CI/CD job in your GitLab repo.

Note: If your artifacts contain packages, it's more likely that you'll want to use the GitLabArtifact.pkg recipe as the basis for your override instead.

1. Create a recipe override, specifying the download recipe as the parent and the name of the resulting override you'll be using. For example:

        autopkg make-override GitLabArtifact.download -n YourCoolProject.download

2. Edit the resulting override file, being sure to replace the following Input variables:

    - `GITLAB_HOSTNAME` - Your company's GitLab host.
    - `JOB_NAME` - The name of the job that produces artifacts, as described in the .gitlab-ci.yml file in your repository.
    - `NAME` - The name of the product you're downloading artifacts for, e.g. YourCoolProject.
    - `PRIVATE_TOKEN` - Your GitLab [personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html).
    - `URLENCODED_PROJECT` - The URL-encoded project path of your GitLab repository, e.g. `yourname%2fcoolproject`

3. Test out the recipe.

        autopkg run -v YourCoolProject.download

4. If it works, a zip file should be downloaded which contains the built artifacts.

### GitLabArtifact.pkg

This recipe extracts a package file from the zip file downloaded by GitLabArtifact.download.

1. Create a recipe override, specifying the pkg recipe as the parent and the name of the resulting override you'll be using. For example:

        autopkg make-override GitLabArtifact.pkg -n YourCoolProject.pkg

2. Edit the resulting override file, being sure to replace above Input variables from GitLabArtifact.download, plus this additional variable:

    - `ARTIFACT_PATH` - The glob path that will match the package you wish to extract. For a repository consisting of a single MunkiPkg project, this might be `build/*.pkg`.

3. Test out the recipe.

        autopkg run -v YourCoolProject.pkg

4. If it works, a pkg file should be produced in your recipe cache directory.

### GitLabArtifact.munki

This recipe imports the specified package from your GitLab repo artifacts into your Munki repo.

1. Create a recipe override, specifying the munki recipe as the parent and the name of the resulting override you'll be using. For example:

        autopkg make-override GitLabArtifact.munki -n YourCoolProject.munki

2. Edit the resulting override file, being sure to replace above Input variables from GitLabArtifact.download, plus these additional variables:

- `ARTIFACT_PATH` - The glob path that will match the package you wish to extract. For a repository consisting of a single MunkiPkg project, this might be `build/*.pkg`.
- `DESCRIPTION` - Description that will be seen by your users in Managed Software Center.
- `DISPLAY_NAME` - Product display name that will be seen by your users in Managed Software Center.
- `MUNKI_REPO_SUBDIR` - Subdirectory of your Munki repo you wish to import the pkginfo/pkg to.

3. Customize the `pkginfo` input key if necessary, adding things like `blocking_applications`, `category`, `developer`, and `unattended_install`.

4. Test out the recipe.

        autopkg run -v YourCoolProject.munki MakeCatalogs.munki

5. If it works, the pkg file should be imported into your Munki repo.

### GitLabArtifact.install

This recipe installs the specified package from your GitLab repo artifacts on your AutoPkg Mac. Not recommended for production systems.

1. Create a recipe override, specifying the install recipe as the parent and the name of the resulting override you'll be using. For example:

        autopkg make-override GitLabArtifact.install -n YourCoolProject.install

2. Edit the resulting override file, being sure to replace above Input variables from GitLabArtifact.download and GitLabArtifact.pkg referenced above.

3. Test out the recipe.

        autopkg run -v YourCoolProject.install

4. If it works, the pkg file contained within your GitLab repo artifacts should be installed on your AutoPkg Mac.
