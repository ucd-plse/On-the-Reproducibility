# Breakage Root Causes and Fixes
In RQ4, we provided root causes analysis for breakages. Also, we provided 10 patches to fix breakages. All patches are applied in an automated manner. Here we provide script for each patches.

## Patches applied to fix breakages

**Table 3: Root Causes and Patches for Breakages**
| Category # | Root Cause                   | Patch                                    | Count |
|------------|------------------------------|------------------------------------------|-------|
|          1 | Maven TLS Failure            | Update TLSv1.0 to TLSv1.2                |   730 |
|          2 | Unavailable PPAs             | Remove PPAs no longer available          |   679 |
|          3 | Unavailable Ubuntu Release   | Change URLs for repository               |   392 |
|          4 | Insecure Link                | Change URLs using HTTP to HTTPS          |   339 |
|          5 | Unavailable JDK Version      | Retrieve unavailable JDK version         |   316 |
|          6 | Unavailable Gradle Plugin    | Correct URL for specific Gradle Plugin   |   158 |
|          7 | Unavailable NodeJS Installer | Correct URL to retrieve NodeJS installer |    91 |
|          8 | Incompatible NPM Package     | Pin NPM package version                  |    91 |
|          9 | Unavailable XML              | Change URL to retrieve DTD files         |    83 |
|         10 | Deprecated CheckStyle Link   | Replace deprecated checkstyle URL        |    69 |

**[Maven TLS Failure](patches/maven-tls-failure)**: Adds flag for Maven to force TLS 1.2 in build scripts for Java jobs using JDK 7 in `pom.xml`, `.m2/settings.xml`, Maven invoker plugin `invoker.properties`, Maven archetype plugin `goal.txt`, and Travis build scripts (`run_passed.sh`, `run_failed.sh`).

**[Unavailable PPAs](patches/unavailable-ppas)**: Removes PPAs from the list of repositories that are retrieved when running `apt-get update`.

**[Unavailable Ubuntu Release](patches/unavailable-ubuntu-release)**: Updates the apt source list to use the new Ubuntu URL.

**[Insecure Link](patches/insecure-link)**: Fixes broken artifacts by replacing the insecure maven links in `/home/travis/.m2/settings.xml` with the correct repo link to avoid error code 501. There is a also special version for artifacts that use Ivy.

**[Unavailable JDK Version](patches/unavailable-jdk-version)**: Replaces the artifact's JDK with the correct Java version specified by the original build log to fix compilation Failure.


**[Unavailable Gradle Plugin](patches/unavailable-gradle-plugin)**: Repairs artifacts broken with `Gradle access denied error` by replacing gradle repo http link with https.

**[Unavailable NodeJS Installer](patches/unavailable-nodejs-installer)**: Removes custom nodejs download url by removing XML tag in `BaragonService/pom.xml`.

**[Deprecated CheckStyle Link](patches/deprecated-checkstyle-link)**: Repairs `SuppressionsLoaderTest` and `SuppressionFilterTest` failure by replacing deprecated links.
