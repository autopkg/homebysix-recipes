## Eclipse

(Copied from sheagcraig-recipes repo in May 2021 to allow for
deprecation/archive of that recipe repository. For details see:
https://github.com/autopkg/sheagcraig-recipes/issues/71)

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
