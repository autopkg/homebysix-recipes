# Corel recipes

These AutoPkg recipes aim to automate the process of packaging Corel software products for IT administrators, based on the workflow described [here](https://community.jamf.com/t5/jamf-pro/deploying-corel-painter-2018-to-a-lab/m-p/205674). **These recipes are a rough draft only and largely unfinished.**

## Usage

Let's say we want to build a package for deploying Corel Painter 2022.

1. Create an override:

        autopkg make-override CorelPainter2022.pkg

1. In your override, adjust the `CHOICE_CHANGES_XML` variable as needed to include/exclude components.

1. Put your Painter serial number in the `SERIAL_NUMBER` variable.

1. Test it out:

        autopkg run -vv CorelPainter2022.pkg

## Current features

- Corel Painter download recipes successfully leverage Corel's API for downloading full installers, allowing administrators to skip the "stub" installer workflow provided by the first-party installation experience.
- Corel Painter pkg recipes use the `create_dta` program to create a serialization file that can be deployed at install time, allowing users to skip inputting serial numbers manually.
- Recipes have been abstracted into the CorelProduct functional group, allowing multiple products to serve as child recipes for a single central recipe workflow. (Similar to the [OmniGroup recipes here](https://github.com/autopkg/recipes/tree/master/OmniGroup).)
- A choice changes XML is included in pkg input variables and [incorporated](https://sneakypockets.wordpress.com/2020/03/17/creating-a-wrapper-package-for-a-choices-xml-file/) into the built package, allowing administrators to customize which package components are included in the installation.

## Future improvements

- Need to test with additional Corel products and create recipes leveraging CorelProduct for each.
- Need to create Munki and/or Jamf recipes that use the pkg recipes as a parent.
- Need to discover a way to generate the /Library/Preferences folder needed to skip user registration at first app launch.
- Occasionally after installation the app would fail to launch. Unsure why.
- A smoother way to build the choice changes XML would be desirable to avoid the plist-within-a-plist messiness. I've submitted a feature request [here](https://github.com/autopkg/grahampugh-recipes/issues/81) that may allow use of [ChoicesXMLGenerator](https://github.com/autopkg/grahampugh-recipes/blob/main/CommonProcessors/ChoicesXMLGenerator.py).

While this is a fine workaround, ultimately Mac admins should coordinate to provide feedback to Corel on their lack of support for unattended installs.
