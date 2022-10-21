## Eclipse

(Copied from sheagcraig-recipes repo in May 2021 to allow for
deprecation/archive of that recipe repository. For details see:
https://github.com/autopkg/sheagcraig-recipes/issues/71)

## OptionSelector

This recipe uses a processor named OptionSelector to choose which of many
Eclipse packages to get the newest version of. By default, the recipe gets the
"Eclipse IDE for Java Developers" package. To select a different one, override
the `SELECTION` input variable with one of the choices below.

Valid choices are:

- Eclipse IDE for Java EE Developers
- Eclipse IDE for Java Developers
- Eclipse IDE for C/C++ Developers
- Eclipse IDE for Eclipse Committers
- Eclipse for PHP Developers
- Eclipse IDE for Java and DSL Developers
- Eclipse for RCP and RAP Developers
- Eclipse IDE for Automotive Software Developers
- Eclipse Modeling Tools
- Eclipse IDE for Java and Report Developers
- Eclipse for Parallel Application Developers
- Eclipse for Testers
- Eclipse for Scout Developers

## Name

Also, you may wish to override `NAME` to differentiate the package from others.
For example, if you're maintaining both "Eclipse IDE for Java Developers" and
"Eclipse for C/C++ Developers", you may want to set `NAME` to "Eclipse-Java"
and "Eclipse-C" respectively. The `NAME` is used for the output package's
filename, so this can aid in keeping things organized.

## Architecture

An `ARCHITECTURE` input variable has also been provided to specify which
architecture-specific download you wish to obtain. Valid choices are:

- `x86_64` for Intel
- `aarch64` for Apple Silicon
