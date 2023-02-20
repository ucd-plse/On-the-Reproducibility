# On the Reproducibility of Software Defect Datasets

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7577662.svg)](https://doi.org/10.5281/zenodo.7577662)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7645975.svg)](https://doi.org/10.5281/zenodo.7645975)

This study focuses on the reproducibility of software defect datasets. Specifically, we present a study on the reproducibility of five Java software defect datasets, examine the reproducibility of one of them in a 13-month period, propose fixes for software breakages and explore two ways to reduce breakage for long-term reproducibility. 

This package consists of two parts: raw data description and study reproduction. To explore the raw data used in this study, please refer to the [Raw Data Description](#1-raw-data-description). To reproduce the study using the raw data provided or from scratch, please refer to [Study Reproduction](#2-study-reproduction).

## 1. Raw Data Description

In this section, we describe all raw data used in our reproducibility study.
- [1.1] Reproducibility data for all artifacts in Defects4j, GrowingBugs, Bugs.jar, BugSwarm and Bears (Section 2/RQ2 in the paper).
    - Original/Historical logs or reproducibility metadata provided by the datasets.
    - Reproduced logs obtained from running buggy and fixed versions of each artifact.
- [1.2] All data for the case study on BugSwarm (Section 3 in the paper).
    - [1.2.1] Reproduced logs for the artifacts in each of the 36 test suites from the 13-month range of study (RQ3).
    - [1.2.2] Patches applied to each artifact (RQ4).
    - [1.2.3] 20 test suites from the 8-month evaluation of cached and isolated artifacts (RQ5).

### 1.1 Raw data for reproducibility of Java defect datasets (RQ2)
In this section, we provide the original logs/metadata provided by the maintainers of each dataset and the reproduced logs generated in the study.

| Dataset | # Projects | # Artifacts | Artifact Source | Build System | Bug Location | Release | Original Logs or Metadata | Reproduced Logs |
|---|---|---|---|---|---|---|---|---|
| Defects4J | 17 | 864 | Issue Tracker | Ant / Maven | Source Code | [397075d](https://github.com/rjust/defects4j/tree/397075d427d44d153fa5436f4b82d58f0afea712) | [orig-trigger-tests](section-2/first-run/defects4j/original) | [buggy & fixed](section-2/first-run/defects4j/reproduced) |
| GrowingBugs | 150 | 570 | Issue Tracker | Ant | Source Code | [6071840](https://github.com/liuhuigmail/GrowingBugRepository/tree/6071840060d1d143f8a34ffcd97cced21ad4f06c) | [orig-trigger-tests](section-2/first-run/growingbugs/original) | [buggy & fixed](section-2/first-run/growingbugs/reproduced) |
| Bugs.jar | 8 | 1158 | Issue Tracker | Maven | Source Code | [8410717](https://github.com/bugs-dot-jar/bugs-dot-jar/tree/84107172868b44295d2d7a664ce0f139a48990a3) | [original buggy logs](section-2/first-run/bugs-dot-jar/original) | [buggy](section-2/first-run/bugs-dot-jar/reproduced/buggy) \| [fixed](section-2/first-run/bugs-dot-jar/reproduced/fixed) |
| BugSwarm | 120 | 1795 | Travis-CI | Ant / Gradle/ Maven | Source Code / Configurations | [181f304](https://github.com/BugSwarm/bugswarm/tree/181f30456121c6864575ede6c62c42429957be0c) | original [buggy](section-2/first-run/bugswarm/original/buggy) \| [fixed](section-2/first-run/bugswarm/original/fixed) | [buggy](section-2/first-run/bugswarm/reproduced/buggy) \| [fixed](section-2/first-run/bugswarm/reproduced/fixed) |
| Bears | 72 | 251 | Travis-CI | Maven | Source Code | [912bb98](https://github.com/bears-bugs/bears-benchmark/tree/912bb98c2269b6db7e21e27520d7a1a0e5c5f568) | [metadata](section-2/first-run/bears/original) | [buggy](section-2/first-run/bears/reproduced/buggy) \| [fixed](section-2/first-run/bears/reproduced/fixed) |

* The reproducibility of each dataset was tested 3 times. The links in the above table correspond to the [first run](section-2/first-run). The logs for the [second](section-2/second-run) and [third](section-2/third-run) runs are also available.

#### Defects4J

- **Defects4J** maintainers provide original trigger tests for each artifact, which can be found [here](section-2/first-run/defects4j/original).
- The reproduced logs for **Defects4J** can be found [here](section-2/first-run/defects4j/reproduced).
- Examples:
    - `Chart-1` is a reproducible artifact, see its [reproduced log](section-2/first-run/defects4j/reproduced/Chart-1.log).
    - `Cli-6` is a broken artifact, see its [reproduced log](section-2/first-run/defects4j/reproduced/Cli-6.log).
- The reproduced logs were generated using the [script](https://github.com/rjust/defects4j/blob/master/framework/test/test_verify_bugs.sh) provided by **Defects4J** maintainers. Please refer to [Study Reproduction](#2-study-reproducition) for instructions on how to generate the reproduced logs from scratch using a Docker container.

> Please note that the maintainers of Defects4J state that 29 artifacts are currently broken (deprecated). However, our test run shows that only 27 are broken. The differences are `Closure-63` and `Closure-93`, which are tagged as broken by maintainers but actually reproducible in our run.

#### GrowingBugs

- **GrowingBugs** maintainers provide original trigger tests for each artifact, which can be found [here](section-2/first-run/growingbugs/original).
- The reproduced logs for **GrowingBugs** can be found [here](section-2/first-run/growingbugs/reproduced).
- Examples:
    - `AaltoXml-1` is a reproducible artifact, see its [reproduced log](section-2/first-run/growingbugs/reproduced/AaltoXml-1.log).
    - `JacksonCore-31` is a broken artifact, see its [reproduced log](section-2/first-run/growingbugs/reproduced/JacksonCore-31.log).
- The reproduced logs were generated using the [script](https://github.com/liuhuigmail/GrowingBugRepository/blob/main/framework/test/test_verify_bugs.sh) provided by **GrowingBugs** maintainers. Please refer to [Study Reproduction](#2-study-reproduction) for instructions on how to generate the reproduced logs from scratch using a Docker container.

> Please note that GrowingBugs is a bug dataset that is continuously growing. For this study, we use [version 4.0](https://github.com/liuhuigmail/GrowingBugRepository/releases/tag/v4.0) committed on Jan 3, 2022. This is the latest release of the dataset to the data of this study.

#### Bugs.jar

- **Bugs.jar** maintainers only provide original logs for the buggy version, which can be found [here](section-2/first-run/bugs-dot-jar/original).
- The reproduced logs for **Bugs.jar** can be found [here](section-2/first-run/bugs-dot-jar/reproduced).
- Example:
    - `ACCUMULO-151_b007b22e` is a broken artifact.
        - Original logs: [buggy version](section-2/first-run/bugs-dot-jar/original/bugs-dot-jar_ACCUMULO-151_b007b22e.log).
        - Reproduced logs: [buggy version](section-2/first-run/bugs-dot-jar/reproduced/buggy/bugs-dot-jar_ACCUMULO-151_b007b22e.log) | [fixed version](section-2/first-run/bugs-dot-jar/reproduced/fixed/bugs-dot-jar_ACCUMULO-151_b007b22e.log).
        - Explanation: the reproduced buggy version has new test failures compared with the original version and the reproduced fixed version does not pass all tests.
    - `MATH-1257_03178c8b` is a reproducible artifact.
        - Original logs: [buggy version](section-2/first-run/bugs-dot-jar/original/bugs-dot-jar_MATH-1257_03178c8b.log).
        - Reproduced logs: [buggy version](section-2/first-run/bugs-dot-jar/reproduced/buggy/bugs-dot-jar_MATH-1257_03178c8b.log) | [fixed version](section-2/first-run/bugs-dot-jar/reproduced/fixed/bugs-dot-jar_MATH-1257_03178c8b.log).
        - Explanation: the buggy version matches the original log and the fixed version passes all tests.
- Note that maintainers of **Bugs.jar** do not provide scripts to test the reproducibility of the dataset. Please refer to [Study Reproduction](#2-study-reproduction) for instructions on how to generate the reproduced logs from scratch using a Docker container. The details on how the **Bugs.jar** artifacts are reproduced can be found [here](https://github.com/ucd-plse/reproducibility-scanner/tree/master/reproducer).

#### BugSwarm

- **BugSwarm** maintainers provide original logs for both buggy and fixed versions, which can be found [here](section-2/first-run/bugswarm/original).
- The reproduced logs for **BugSwarm** can be found [here](section-2/first-run/bugswarm/reproduced).
- Example:
    - `square-okhttp-45400990` is a broken artifact.
        - Original logs: [buggy version](section-2/first-run/bugswarm/original/buggy/square-okhttp-45400990.log) | [fixed version](section-2/first-run/bugswarm/original/fixed/square-okhttp-45400990.log).
        - Reproduced logs: [buggy version](section-2/first-run/bugswarm/reproduced/buggy/square-okhttp-45400990.log) | [fixed version](section-2/first-run/bugswarm/reproduced/fixed/square-okhttp-45400990.log).
        - Explanation: the artifact is broken due to failure retrieving dependencies. 
    - `languagetool-org-languagetool-393031702` is a reproducible artifact.
        - Original logs: [buggy version](section-2/first-run/bugswarm/original/buggy/languagetool-org-languagetool-393031702.log) | [fixed version](section-2/first-run/bugswarm/original/fixed/languagetool-org-languagetool-393031702.log).
        - Reproduced logs: [buggy version](section-2/first-run/bugswarm/reproduced/buggy/languagetool-org-languagetool-393031702.log) | [fixed version](section-2/first-run/bugswarm/reproduced/fixed/languagetool-org-languagetool-393031702.log).
        - Explanation: the artifact is reproducible as the buggy version matches the original log and the fixed version passes all tests.
- Note that **BugSwarm** maintainers do not provide scripts to test the reproducibility of the dataset, but each **BugSwarm** artifact includes scripts to run buggy and and fixed versions within a provided Docker container. The reproduced logs were generated using these scripts and Docker containers. Please refer to [Study Reproduction](#2-study-reproduction) for instructions on how to generate the reproduced logs from scratch using a Docker container.

#### Bears

- **Bears** maintainers does not provide original logs. Instead, a json-formatted file with metadata about the initial run (at the time of dataset creation) is given, which can be found [here](section-2/first-run/bears/original).
- The reproduced logs for **Bears** can be found [here](section-2/first-run/bears/reproduced).
- Example:
    - `Bears-83` is a broken artifact
        - Original logs: [metadata](section-2/first-run/bears/original/Bears-83.json)
        - Reproduced logs: [buggy version](section-2/first-run/bears/reproduced/buggy/Bears-83.log) | [fixed version.](section-2/first-run/bears/reproduced/fixed/Bears-83.log)
        - Explanation: the artifact is broken due to an unexpected test failure in `spoon.reflect.declaration.CtTypeInformationTest` that affects both buggy and fixed versions. Thus, the buggy version does not match the original log and the fixed version does not pass all tests.
    - `Bears-1` is a reproducible artifact
        - Original logs: [metadata](section-2/first-run/bears/original/Bears-1.json)
        - Reproduced logs: [buggy version](section-2/first-run/bears/reproduced/buggy/Bears-1.log) | [fixed version](section-2/first-run/bears/reproduced/fixed/Bears-1.log).
        - Explanation: the artifact is reproducible as the buggy version matches the original log and the fixed version passes all tests.
- Note that **Bears** maintainers do not provide scripts to test the reproducibility of the dataset, but maintainers provide a [script](https://github.com/bears-bugs/bears-benchmark/blob/master/scripts/run_tests_all.py) to run all artifacts. The reproduced logs were generated using this script. Please refer to [Study Reproduction](#2-study-reproduction) for instructions on how to generate the reproduced logs from scratch using a Docker container.


### 1.2 All data for the case study on BugSwarm

In this section, we provide the raw data for the reproducibility study on BugSwarm, including (1) reproduced logs for all artifacts in each test suite from the 13-month study, (2) patches applied for each artifact, and (3) reproduced logs for all artifacts in each test suite from the 8-month evaluation period on the reproducibility of BugSwarm.

#### 1.2.1 Reproduced logs for artifacts in all test suites from 13-month study (RQ3)

RQ3 investigates breakage frequency of 1795 non-flaky BugSwarm artifacts across 36 test suites (or runs) in a 13-month period.

- We use the [BugSwarm's API](http://www.bugswarm.org/docs/toolset/bugswarm-rest-api/) to identify non-flaky artifacts. The IDs for non-flaky artifacts can be found [here](section-3/1795-Non-Flaky-Tags.csv).
- A CSV file for each of the 36 test suites can be found [here](section-3/test-suites-in-13-months-study-range). Each CSV file lists the reproducibility outcome of each artifact.
- The reproduced logs for both buggy and fixed versions of each artifact for each test suite are available [here](https://github.com/ucd-plse/bugswarm-reproducibility/tree/master/36-suites-for-study).

#### 1.2.2 Patched applied for each artifact (RQ4)

RQ4 investigates root causes of breakages and applies 10 different patches to fix broken artifacts.

- A CSV file summarizing which patches were applied to each artifact can be found [here](section-3/RQ4/Patches-Applied.csv). Note that multiple patches are applied to several artifacts.
- Scripts to apply each patch can be found [here](section-3/RQ4).

#### 1.2.3 Reproduced logs for artifacts in all test suits from 8-month evaluation on cached and isolated artifacts (RQ5)

RQ5 studies the impact of dependency caching and artifact isolation on preventing breakage. Cached and isolated artifacts were evaluated on 13 test suites over a 8-month period. 

- A CSV file for each of the 20 test suites can be found [here](section-3/test-suites-for-eval-after-study-range). Each CSV file lists the reproducibility outcome for each artifact.
- The reproduced logs for both buggy and fixed versions of each artifact for each test suite are available [here](https://github.com/ucd-plse/bugswarm-reproducibility/tree/master/20-suites-for-eval).

## 2. Study Reproduction

This section provides instructions on how to reproduce our study using the raw data provided and from scratch.

- [2.1] Set up reproduction environment.
- [2.2] Reproduce the reproducibility study on five software defect datasets (Section 2 in the paper).
    - [2.2.1] Run log analyzer to get reproducibility data from provided reproduced logs.
    - [2.2.2] [Optional] Run reproducer to generate reproduced logs from scratch.
- [2.3] Reproduce the case study on BugSwarm (Section 3 in the paper).

### 2.1 Set up reproduction environment

#### Prerequisites

- Ubuntu version `20.04` is required. The reproduction package has not been tested on other systems.
- Docker version `20.10.17` is required. The reproduction package has not been tested with other Docker versions ([how to install Docker](https://docs.docker.com/engine/install/ubuntu/#install-docker-engine)). If you encounter a permission error when running `docker` commands, please check this [workaround](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

#### Setup
We have three options to setup the reproduction environment.

- **[Option 1]** Pull and run our Docker container with environment, then set up the reproduction package. 

    1. Pull and run the Docker container with environment. Note that Docker will automatically pull the image if not found locally.
        ``` sh
        docker run -v /var/run/docker.sock:/var/run/docker.sock \
            -v /var/lib/docker:/var/lib/docker -it ucdavisplse/reproducibility:env
        ```

        > The Zenodo archive of the Docker image `ucdavisplse/reproducibility:env` is available [here](https://zenodo.org/record/7641690).

    2. In the container, clone the repository for reproduction package. It may take up to 10 mins based on the network status.
        ``` sh
        git clone https://github.com/ucd-plse/On-the-Reproducibility.git /On-the-Reproducibility && \
        git clone --recurse-submodules -j5 https://github.com/ucd-plse/reproducibility-scanner.git \
            /On-the-Reproducibility/section-2/reproducibility-scanner
        ```
        > It is expected to have an error massage `fatal: No url found for submodule path 'benchmarks/growingbugs/framework/projects/pdfbox' in .gitmodules. Failed to recurse into submodule path 'benchmarks/growingbugs'` when executing the above command. The root cause comes from the misconfiguration of GrowingBugs. However, this error message does not affect the reproduction process.

    3. Copy the reproduced logs from first run of experiment to the framework directory.
        ``` sh
        cp -r /On-the-Reproducibility/section-2/first-run/* \
            /On-the-Reproducibility/section-2/reproducibility-scanner/outputs/
        ```

    4. Change directory to `/On-the-Reproducibility/section-2/reproducibility-scanner`.
        ``` sh
        cd /On-the-Reproducibility/section-2/reproducibility-scanner
        ```

    5. Run initialization script, it may take up to 1 hour.
        ``` sh
        python init.py
        ```
    
    > It is possible that the initialization script fails due to network issues. If this happens, please try running the initialization script for Defects4J and GrowingBugs manually. The commands are listed below.
    >
    > To manually initialize Defects4J, run the following commands in the container.
    > ``` sh
    > cd /On-the-Reproducibility/section-2/reproducibility-scanner/benchmarks/defects4j/
    > cpanm --installdeps .
    > ./init.sh
    > ```
    > The commands above are to [manually set up Defects4J](https://github.com/rjust/defects4j#steps-to-set-up-defects4j). You can see the output for each command and make sure it is completed.
    > After successfully running the initialization script (`init.sh`) for Defects4J, please continue with the following command.
    > ``` sh
    > cd /On-the-Reproducibility/section-2/reproducibility-scanner/
    > python init.py
    > ```
    > 
    > To manually initialize GrowingBugs, run the following commands in the container.
    > ``` sh
    > cd /On-the-Reproducibility/section-2/reproducibility-scanner/benchmarks/growingbugs/
    > cpanm --installdeps .
    > ./init.sh
    > ./repos.sh
    > ```
    > The commands above are to [manually set up GrowingBugs](https://github.com/liuhuigmail/GrowingBugRepository#steps-to-set-up-growingbugs). You can see the output for each command and make sure it is completed. After successfully running the initialization scripts (`init.sh` and `repos.sh`) for GrowingBugs, please continue with the following command.
    > ``` sh
    > cd /On-the-Reproducibility/section-2/reproducibility-scanner/
    > python init.py
    > ```
    > Please feel free to reach out to us if you have any questions.
    > 



- **[Option 2]** Build a Docker container on your own machine with the Dockerfile we provide.

    1. Build Docker image. Note that this step may a few hours since you are building the image from scratch; the size of the Docker image will be around 45 GB. 
   
        ``` sh
        docker build . -t reproducibility-study
        ```
    
    2. Run Docker container.

        ``` sh
        docker run -v /var/run/docker.sock:/var/run/docker.sock \
            -v /var/lib/docker:/var/lib/docker -it reproducibility-study
        ```

- **[Option 3]** Set up environment on your host. 

    Please refer to the documentation of [reproducibility-scanner](https://github.com/ucd-plse/reproducibility-scanner).

- **[Option 4]** Download the Docker image from Zenodo archive.

    1. Download the Docker image from [Zenodo archive](https://zenodo.org/record/7645975) (33 GB).
    
    2. Load the Docker image.
        ``` sh
        docker load --input reproducibility-full.tar.gz
        ```

    3. Run Docker container and navigate to working directory.
        ``` sh
        docker run -v /var/run/docker.sock:/var/run/docker.sock \
            -v /var/lib/docker:/var/lib/docker -it reproducibility-full:latest
        ```

If you selected **option 1**, **option 2**, or **option 4** please continue to follow the instructions and run any given commands *inside* the Docker container. If you selected **option 3**, please run the commands on your host machine instead.

### 2.2 Reproduce the reproducibility study on five software defect datasets (Section 2)

We provide the instructions to generate the reproducibility data (1) using the reproduced logs we provide in [Raw Data Description](#1-raw-data-description) or (2) from scratch, which includes generating the reproduced logs.

- Pre-step 1: Change directory to `reproducibility-scanner`
    ``` sh
    cd /On-the-Reproducibility/section-2/reproducibility-scanner
    ```

- Pre-step 2: Activate Perl DBI. This is for reproducing Defects4J and GrowingBugs.
    ``` sh
    cpan DBI
    ```

- Pre-step 3: Check default Java version if you chose to run the reproduction package in your host machine.
    ``` sh
    java -version
    ```
    The output should be version `1.8.0` for OpenJDK or Oracle JDK. If not, please refer to [How to set default Java version?](https://askubuntu.com/questions/121654/how-to-set-default-java-version)


#### 2.2.1 Run log analyzer to generate reproducibility data from provided reproduced logs
    
Log analyzer scans and compares the reproduced logs we provide ([here](section-2/first-run)) and their corresponding original logs to calculate reproducibility rates. This section provides the commands to run log analyzer on *one* artifact and in *all* artifacts from each given dataset using our reproduced logs. We provide sample output for each command. 

> Note that we have three measures for reproducibility: `Existence`, `NumMatch` and `NameMatch`. 
> - `Existence`: the artifact is reproducible if there exists at lease one test failure in buggy version. 
> - `NumMatch`: the artifact is reproducible if the number of test failures match the number the original log. 
> - `NameMatch`: the artifact is reproducible only if the names of test failures match the original log.   
>  
> All the measures are based on the assumption that the fixed version of artifact should have no test failures. More details can be found at Section 2 of the paper.

##### Defects4J

- To run log analyzer on *one* artifact from the Defects4j dataset, use the flag `-b` to indicate the name of the dataset and flag `-i` to provide the name of the artifact, as given by the dataset. The flag `-a` is used to run analyzer on the existing reproduced logs. For example, the following command will run log analyzer on the artifact `Chart-1` from Defects4j. [Estimated runtime: ~1 sec].

    ``` sh
    python scan4r.py -b defects4j -i Chart-1 -a
    ```

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-07 14:38:38 INFO     Reproducing Defects4J Chart-1
    2022-08-07 14:38:38 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    ```
    </details>


- To run log analyzer on *all* artifacts from the Defects4j dataset, simply use the flag `-a` after specifying the name of the dataset as follows. [Estimated runtime: ~1 sec].

    ``` sh
    python scan4r.py -b defects4j -a
    ```

    

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-07 14:39:30 INFO     Reproducing all bugs in defects4j
    2022-08-07 14:39:30 INFO     Reproducing 864 Defects4J bugs
    2022-08-07 14:39:30 INFO     Reproducing Defects4J Chart-1
    2022-08-07 14:39:30 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    2022-08-07 14:39:30 INFO     Reproducing Defects4J Chart-2
    2022-08-07 14:39:30 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    ...
    2022-08-07 14:39:31 INFO     Reproducing Defects4J Time-27
    2022-08-07 14:39:31 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    2022-08-07 14:39:31 INFO     Overall reproducibility for 864 Defects4J artifacts
    2022-08-07 14:39:31 INFO     {'Existence': 837, 'NumMatch': 837, 'NameMatch': 837}
    ```
    </details>



##### GrowingBugs

- To run log analyzer on *one* artifact from the GrowingBugs dataset, use the flag `-b` to indicate the name of the dataset and flag `-i` to provide the name of the artifact, as given by the dataset. The flag `-a` is used to run analyzer on the existing reproduced logs. For example, the following command will run log analyzer on the artifact `Mshared_archiver-1` from GrowingBugs. [Estimated runtime: ~1 sec].

    ``` sh
    python scan4r.py -b growingbugs -i Mshared_archiver-1 -a
    ```

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-13 12:53:15 INFO     Reproducing GrowingBugs Mshared_archiver-1
    2022-08-13 12:53:15 INFO     Reproducibility (Existence, NumMatch, NameMatch): False False False
    ```
    </details>


- To run log analyzer on *all* artifacts from the GrowingBugs dataset, simply use the flag `-a` after specifying the name of the dataset as follows. [Estimated runtime: ~1 sec].

    ``` sh
    python scan4r.py -b growingbugs -a
    ```

    

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-13 12:54:09 INFO     Reproducing all bugs in growingbugs
    2022-08-13 12:54:09 INFO     Reproducing 570 GrowingBugs bugs
    2022-08-13 12:54:09 INFO     Reproducing GrowingBugs Mshared_archiver-1
    2022-08-13 12:54:09 INFO     Reproducibility (Existence, NumMatch, NameMatch): False False False
    2022-08-13 12:54:09 INFO     Reproducing GrowingBugs Switchyard_admin-1
    2022-08-13 12:54:09 INFO     Reproducibility (Existence, NumMatch, NameMatch): False False False
    ...
    2022-08-13 12:54:09 INFO     Reproducing GrowingBugs Email-5
    2022-08-13 12:54:09 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    2022-08-13 12:54:09 INFO     Reproducing GrowingBugs Wicket_cdi-1
    2022-08-13 12:54:09 INFO     Reproducibility (Existence, NumMatch, NameMatch): False False False
    2022-08-13 12:54:09 INFO     Overall reproducibility for 570 GrowingBugs artifacts
    2022-08-13 12:54:09 INFO     {'Existence': 175, 'NumMatch': 170, 'NameMatch': 170}
    ```
    </details>



##### Bugs.jar

- To run log analyzer on *one* artifact from the Bugs.jar dataset, use the flag `-b` to indicate the name of the dataset and flag `-i` to provide the name of the artifact, as given by the dataset. The flag `-a` is used to run analyzer on the existing reproduced logs. For example, the following command will run log analyzer on the artifact `bugs-dot-jar_MATH-776_b9ca51f0` from Bugs.jar. [Estimated runtime: ~1 sec].

    ``` sh
    python scan4r.py -b bugs.jar -i bugs-dot-jar_MATH-776_b9ca51f0 -a
    ```

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-13 12:55:22 INFO     Reproducing Bugs.jar bugs-dot-jar_MATH-776_b9ca51f0
    2022-08-13 12:55:22 INFO     Reproducibility (Existence, NumMatch, NameMatch): False False False
    ```
    </details>


- To run log analyzer on *all* artifacts from the Bugs.jar dataset, simply use the flag `-a` after specifying the name of the dataset as follows. [Estimated runtime: ~5 mins].

    ``` sh
    python scan4r.py -b bugs.jar -a
    ```

    

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-13 12:55:57 INFO     Reproducing all bugs in bugs.jar
    2022-08-13 12:55:57 INFO     Reproducing 1158 Bugs.jar bugs
    2022-08-13 12:55:57 INFO     Reproducing Bugs.jar bugs-dot-jar_MATH-776_b9ca51f0
    2022-08-13 12:55:57 INFO     Reproducibility (Existence, NumMatch, NameMatch): False False False
    2022-08-13 12:55:57 INFO     Reproducing Bugs.jar bugs-dot-jar_CAMEL-6889_cd40b712
    2022-08-13 12:55:57 INFO     Reproducibility (Existence, NumMatch, NameMatch): False False False
    ...
    2022-08-13 12:57:26 INFO     Reproducing Bugs.jar bugs-dot-jar_OAK-3763_ab1a0cc2
    2022-08-13 12:57:26 INFO     Reproducibility (Existence, NumMatch, NameMatch): False False False
    2022-08-13 12:57:26 INFO     Overall reproducibility for 1158 Bugs.jar artifacts
    2022-08-13 12:57:26 INFO     {'Existence': 308, 'NumMatch': 303, 'NameMatch': 303}
    ```
    </details>


##### BugSwarm

- To run log analyzer on *one* artifact from the BugSwarm dataset, use the flag `-b` to indicate the name of the dataset and flag `-i` to provide the name of the artifact, as given by the dataset. The flag `-a` is used to run analyzer on the existing reproduced logs. For example, the following command will run log analyzer on the artifact `languagetool-org-languagetool-393031702` from BugSwarm. [Estimated runtime: ~1 sec].

    ``` sh
    python scan4r.py -b bugswarm -i languagetool-org-languagetool-393031702 -a
    ```

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-13 12:58:15 INFO     Reproducing BugSwarm languagetool-org-languagetool-393031702
    2022-08-13 12:58:16 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    ```
    </details>


- To run log analyzer on *all* artifacts from the BugSwarm dataset, simply use the flag `-a` after specifying the name of the dataset as follows. [Estimated runtime: ~20 mins].

    ``` sh
    python scan4r.py -b bugswarm -a
    ```

    

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-13 13:00:17 INFO     Reproducing all bugs in bugswarm
    2022-08-13 13:00:17 INFO     Reproducing 1795 BugSwarm bugs
    2022-08-13 13:00:17 INFO     Reproducing BugSwarm languagetool-org-languagetool-393031702
    2022-08-13 13:00:18 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    2022-08-13 13:00:18 INFO     Reproducing BugSwarm square-okio-140452393
    2022-08-13 13:00:18 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    ...
    2022-08-13 13:16:15 INFO     Reproducing BugSwarm fayder-restcountries-152161308
    2022-08-13 13:16:15 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    2022-08-13 13:16:15 INFO     Reproducing BugSwarm checkstyle-checkstyle-131729458
    2022-08-13 13:16:16 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    2022-08-13 13:16:16 INFO     Overall reproducibility for 1795 BugSwarm artifacts
    2022-08-13 13:16:16 INFO     {'Existence': 1392, 'NumMatch': 1388, 'NameMatch': 1387}
    ```
    </details>



##### Bears

- To run log analyzer on *one* artifact from the Bears dataset, use the flag `-b` to indicate the name of the dataset and flag `-i` to provide the name of the artifact, as given by the dataset. The flag `-a` is used to run analyzer on the existing reproduced logs. For example, the following command will run log analyzer on the artifact `Bears-1` from Bears. [Estimated runtime: ~1 sec].

    ``` sh
    python scan4r.py -b bears -i Bears-1 -a
    ```

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-13 12:58:47 INFO     Reproducing Bears Bears-1
    2022-08-13 12:58:47 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    ```
    </details>


- To run log analyzer on *all* artifacts from the Bears dataset, simply use the flag `-a` after specifying the name of the dataset as follows. [Estimated runtime: ~1 min].

    ``` sh
    python scan4r.py -b bears -a
    ```

    

    <details>
    <summary>Click to see sample output</summary>

    ```
    2022-08-13 12:59:12 INFO     Reproducing all bugs in bears
    2022-08-13 12:59:12 INFO     Reproducing 251 Bears bugs
    2022-08-13 12:59:12 INFO     Reproducing Bears Bears-1
    2022-08-13 12:59:12 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    2022-08-13 12:59:12 INFO     Reproducing Bears Bears-2
    2022-08-13 12:59:12 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    ...
    2022-08-13 12:59:20 INFO     Reproducing Bears Bears-250
    2022-08-13 12:59:20 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    2022-08-13 12:59:20 INFO     Reproducing Bears Bears-251
    2022-08-13 12:59:20 INFO     Reproducibility (Existence, NumMatch, NameMatch): True True True
    2022-08-13 12:59:20 INFO     Overall reproducibility for 251 Bears artifacts
    2022-08-13 12:59:20 INFO     {'Existence': 137, 'NumMatch': 134, 'NameMatch': 134}
    ```
    </details>


#### 2.2.2 [Optional] Run reproducer to generate reproduced logs from scratch

This section provides commands to run the log analyzer on *one* artifact and in *all* artifacts from each given dataset by producing the reproduced logs from scratch. Please refer to section 2.2.1 for sample outputs.

##### Defects4J

- To run, generate the reproduced log and compute the reproducibility of a designated artifact, use flag `-i` to specify the artifact name. For example, for `Chart-1`, type the following command and hit enter. [Estimated runtime: ~1 mins].

    ``` sh
    python scan4r.py -b defects4j -i Chart-1
    ```

- To run, generate the reproduced log, and compute the reproducibility of *all* Defects4J artifacts, type the following command and hit enter. [Estimated runtime: ~10 hours].

    ``` sh
    python scan4r.py -b defects4j
    ```

##### GrowingBugs

- To run, generate the reproduced log and compute the reproducibility of a designated artifact, use flag `-i` to specify the artifact name. For example, for `Mshared_archiver-1`, type the following command and hit enter. [Estimated runtime: ~5 mins].

    ``` sh
    python scan4r.py -b growingbugs -i Mshared_archiver-1
    ```

- To run, generate the reproduced log, and compute the reproducibility of *all* GrowingBugs artifacts, type the following command and hit enter. [Estimated runtime: ~10 hours].

    ``` sh
    python scan4r.py -b growingbugs
    ```

##### Bugs.jar

- To run, generate the reproduced log and compute the reproducibility of a designated artifact, use flag `-i` to specify the artifact name. For example, for `bugs-dot-jar_MATH-776_b9ca51f0`, type the following command and hit enter. [Estimated runtime: ~30 mins].

    ``` sh
    python scan4r.py -b bugs.jar -i bugs-dot-jar_MATH-776_b9ca51f0
    ```

- To run, generate the reproduced log, and compute the reproducibility of *all* Bugs.jar artifacts, type the following command and hit enter. [Estimated runtime: ~7 days].

    ``` sh
    python scan4r.py -b bugs.jar
    ```

##### Bugswarm

- To run, generate the reproduced log and compute the reproducibility of a designated artifact, use flag `-i` to specify the artifact name. For example, for `languagetool-org-languagetool-393031702`, type the following command and hit enter. [Estimated runtime: ~30 mins].

    ``` sh
    python scan4r.py -b bugswarm -i languagetool-org-languagetool-393031702
    ```

- To run, generate the reproduced log, and compute the reproducibility of *all* BugSwarm artifacts, type the following command and hit enter. [Estimated runtime: ~7 days].

    ``` sh
    python scan4r.py -b bugswarm
    ```

##### Bears

- To run, generate the reproduced log and compute the reproducibility of a designated artifact, use flag `-i` to specify the artifact name. For example, for `Bears-1`, type the following command and hit enter. [Estimated runtime: ~5 mins].

    ``` sh
    python scan4r.py -b bears -i Bears-1
    ```

- To run, generate the reproduced log, and compute the reproducibility of *all* Bears artifacts, type the following command and hit enter. [Estimated runtime: ~5 hours].

    ``` sh
    python scan4r.py -b bears
    ```


### 2.3 Reproduce the case study on BugSwarm (Section 3)


Change directory to `section-3`

``` sh
cd /On-the-Reproducibility/section-3
```

Type the following command and hit enter to generate the raw data for Figures 1, 2 and 4 [Estimated runtime: ~1 min].

``` sh
python run_replicate_section_3.py
```

This script generates all data for section 3.1, including the number of artifacts that break at least once, number of breakage instances, average newly reproducible and newly broken, as well as median newly reproducible and broken. The raw data for Figures 1, 2 and 4 will also be printed.

The script can be found [here](section-3). The output of the above script should be as follows:


<details>
<summary>Click to see sample outputs</summary>
  
```
Reproducing Statistical Data for Section 3: RQ3, RQ4 and RQ5

========== RQ3 ==========
Test suite in study range: 36 suites loaded.
╔═══════════════════╗
║ Data for Figure 2 ║
╚═══════════════════╝
Processing suite-2.csv: 7 newly reproducible, 11 newly broken
Processing suite-3.csv: 8 newly reproducible, 6 newly broken
Processing suite-4.csv: 7 newly reproducible, 16 newly broken
Processing suite-5.csv: 16 newly reproducible, 6 newly broken
Processing suite-6.csv: 10 newly reproducible, 6 newly broken
Processing suite-7.csv: 6 newly reproducible, 7 newly broken
Processing suite-8.csv: 23 newly reproducible, 8 newly broken
Processing suite-9.csv: 8 newly reproducible, 6 newly broken
Processing suite-10.csv: 26 newly reproducible, 13 newly broken
Processing suite-11.csv: 32 newly reproducible, 3 newly broken
Processing suite-12.csv: 4 newly reproducible, 69 newly broken
Processing suite-13.csv: 60 newly reproducible, 22 newly broken
Processing suite-14.csv: 23 newly reproducible, 10 newly broken
Processing suite-15.csv: 8 newly reproducible, 7 newly broken
Processing suite-16.csv: 11 newly reproducible, 24 newly broken
Processing suite-17.csv: 12 newly reproducible, 15 newly broken
Processing suite-18.csv: 16 newly reproducible, 3 newly broken
Processing suite-19.csv: 1 newly reproducible, 22 newly broken
Processing suite-20.csv: 19 newly reproducible, 12 newly broken
Processing suite-21.csv: 16 newly reproducible, 8 newly broken
Processing suite-22.csv: 10 newly reproducible, 13 newly broken
Processing suite-23.csv: 9 newly reproducible, 32 newly broken
Processing suite-24.csv: 15 newly reproducible, 18 newly broken
Processing suite-25.csv: 6 newly reproducible, 10 newly broken
Processing suite-26.csv: 6 newly reproducible, 14 newly broken
Processing suite-27.csv: 20 newly reproducible, 27 newly broken
Processing suite-28.csv: 25 newly reproducible, 9 newly broken
Processing suite-29.csv: 92 newly reproducible, 22 newly broken
Processing suite-30.csv: 14 newly reproducible, 90 newly broken
Processing suite-31.csv: 162 newly reproducible, 70 newly broken
Processing suite-32.csv: 157 newly reproducible, 34 newly broken
Processing suite-33.csv: 40 newly reproducible, 53 newly broken
Processing suite-34.csv: 43 newly reproducible, 29 newly broken
Processing suite-35.csv: 62 newly reproducible, 379 newly broken
Processing suite-36.csv: 383 newly reproducible, 49 newly broken
╔══════════════════════════╗
║ Statistical Data for RQ3 ║
╚══════════════════════════╝
Number of artifacts that break at least once: 1124
Number of breakage instances: 1606
Average newly broken: 32.08571428571429
Median newly broken: 14.0
Average newly reproducible: 38.77142857142857
Median newly reproducible: 16.0
╔═══════════════════╗
║ Data for Figure 1 ║
╚═══════════════════╝
             Image Tag
Break Times           
1                  849
2                  156
3                   70
4                   32
5                    5
6                    7
7                    2
8                    1
9                    2
Average breakages in each test suite: 430.75

========== RQ4 ==========
╔═══════════════════╗
║ Data for Figure 3 ║
╚═══════════════════╝
             Image Tag
Num Patches           
0                   69
1                  187
2                  295
3                  203
4                  289
5                   80
6                    1

========== RQ5 ==========
╔═════════════════════════════════════╗
║ Data for Figure 4                   ║
║ Reproducibility of Cached Artifacts ║
╚═════════════════════════════════════╝
1700 artifacts are successfully cached.
20 test suites are read for evaluation.
suite-1.csv: 1700 cached non-flaky java artifacts; 1476 reproducible. Reproducibility: 0.8682352941176471
suite-2.csv: 1700 cached non-flaky java artifacts; 1453 reproducible. Reproducibility: 0.8547058823529412
suite-3.csv: 1700 cached non-flaky java artifacts; 1443 reproducible. Reproducibility: 0.8488235294117648
suite-4.csv: 1700 cached non-flaky java artifacts; 1452 reproducible. Reproducibility: 0.8541176470588235
suite-5.csv: 1700 cached non-flaky java artifacts; 1472 reproducible. Reproducibility: 0.8658823529411764
suite-6.csv: 1700 cached non-flaky java artifacts; 1392 reproducible. Reproducibility: 0.8188235294117647
suite-7.csv: 1700 cached non-flaky java artifacts; 1396 reproducible. Reproducibility: 0.8211764705882353
suite-8.csv: 1700 cached non-flaky java artifacts; 1403 reproducible. Reproducibility: 0.8252941176470588
suite-9.csv: 1700 cached non-flaky java artifacts; 1417 reproducible. Reproducibility: 0.8335294117647059
suite-10.csv: 1700 cached non-flaky java artifacts; 1410 reproducible. Reproducibility: 0.8294117647058824
suite-11.csv: 1700 cached non-flaky java artifacts; 1406 reproducible. Reproducibility: 0.8270588235294117
suite-12.csv: 1700 cached non-flaky java artifacts; 1410 reproducible. Reproducibility: 0.8294117647058824
suite-13.csv: 1700 cached non-flaky java artifacts; 1411 reproducible. Reproducibility: 0.83
suite-14.csv: 1700 cached non-flaky java artifacts; 1410 reproducible. Reproducibility: 0.8294117647058824
suite-15.csv: 1700 cached non-flaky java artifacts; 1456 reproducible. Reproducibility: 0.8564705882352941
suite-16.csv: 1700 cached non-flaky java artifacts; 1447 reproducible. Reproducibility: 0.8511764705882353
suite-17.csv: 1700 cached non-flaky java artifacts; 1452 reproducible. Reproducibility: 0.8541176470588235
suite-18.csv: 1700 cached non-flaky java artifacts; 1420 reproducible. Reproducibility: 0.8352941176470589
suite-19.csv: 1700 cached non-flaky java artifacts; 1455 reproducible. Reproducibility: 0.8558823529411764
suite-20.csv: 1700 cached non-flaky java artifacts; 1450 reproducible. Reproducibility: 0.8529411764705882

╔═══════════════════════════════════════╗
║ Data for Figure 4                     ║
║ Reproducibility of Isolated Artifacts ║
╚═══════════════════════════════════════╝
1257 artifacts are fully isolated.
20 test suites are read for evaluation.
suite-1.csv: 1257 cached isolated java artifacts; 1242 reproducible. Reproducibility: 0.9880668257756563
suite-2.csv: 1257 cached isolated java artifacts; 1229 reproducible. Reproducibility: 0.9777247414478918
suite-3.csv: 1257 cached isolated java artifacts; 1217 reproducible. Reproducibility: 0.9681782020684169
suite-4.csv: 1257 cached isolated java artifacts; 1222 reproducible. Reproducibility: 0.9721559268098647
suite-5.csv: 1257 cached isolated java artifacts; 1241 reproducible. Reproducibility: 0.9872712808273667
suite-6.csv: 1257 cached isolated java artifacts; 1195 reproducible. Reproducibility: 0.9506762132060461
suite-7.csv: 1257 cached isolated java artifacts; 1206 reproducible. Reproducibility: 0.9594272076372315
suite-8.csv: 1257 cached isolated java artifacts; 1203 reproducible. Reproducibility: 0.9570405727923628
suite-9.csv: 1257 cached isolated java artifacts; 1212 reproducible. Reproducibility: 0.964200477326969
suite-10.csv: 1257 cached isolated java artifacts; 1215 reproducible. Reproducibility: 0.9665871121718377
suite-11.csv: 1257 cached isolated java artifacts; 1206 reproducible. Reproducibility: 0.9594272076372315
suite-12.csv: 1257 cached isolated java artifacts; 1206 reproducible. Reproducibility: 0.9594272076372315
suite-13.csv: 1257 cached isolated java artifacts; 1211 reproducible. Reproducibility: 0.9634049323786794
suite-14.csv: 1257 cached isolated java artifacts; 1213 reproducible. Reproducibility: 0.9649960222752586
suite-15.csv: 1257 cached isolated java artifacts; 1223 reproducible. Reproducibility: 0.9729514717581543
suite-16.csv: 1257 cached isolated java artifacts; 1217 reproducible. Reproducibility: 0.9681782020684169
suite-17.csv: 1257 cached isolated java artifacts; 1221 reproducible. Reproducibility: 0.9713603818615751
suite-18.csv: 1257 cached isolated java artifacts; 1197 reproducible. Reproducibility: 0.9522673031026253
suite-19.csv: 1257 cached isolated java artifacts; 1221 reproducible. Reproducibility: 0.9713603818615751
suite-20.csv: 1257 cached isolated java artifacts; 1217 reproducible. Reproducibility: 0.9681782020684169
```
</details>

Type the following command and hit enter to verify that data generated by the script above matches the the raw data on paper. [Estimated runtime: ~1 sec].

The script can be found [here](section-3/run_verify_data.py). It compares the data generated by the [script above](section-3/run_replicate_section_3.py) with the reference data [here](section-3/reference). The reference data is identical to the data presented on paper. If there are mismatches, the script will print the difference.

```bash
python run_verify_data.py
```
