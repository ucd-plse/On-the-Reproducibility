# Reproducibility Results by Project

- The reproducibility results by project for each dataset can be found [here](.). There is a CSV file per dataset.

- Defects4J and GrowingBugRepository have overlap on target projects. See the following table for the comparison on reproducibility of overlapping projects.


|                 |    Defects4J   |            |                 | GrowingBugRepository |            |                 |
|-----------------|:--------------:|:----------:|:---------------:|:--------------------:|:----------:|:---------------:|
|                 | # Reproducible | # Artifact | Reproducibility | # Reproducible       | # Artifact | Reproducibility |
| Cli             |             39 |         40 |          97.50% |                    0 |          2 |           0.00% |
| Codec           |             18 |         18 |         100.00% |                    1 |          1 |         100.00% |
| Collections     |              4 |         28 |          14.29% |                    3 |          4 |          75.00% |
| Compress        |             47 |         47 |         100.00% |                    2 |          4 |          50.00% |
| Csv             |             16 |         16 |         100.00% |                    1 |          1 |         100.00% |
| JacksonCore     |             26 |         26 |         100.00% |                    3 |          4 |          75.00% |
| JacksonDatabind |            112 |        112 |         100.00% |                   12 |         39 |          30.77% |
| Lang            |             64 |         65 |          98.46% |                    0 |          9 |           0.00% |


- BugSwarm and Bears have overlap on target projects. See the following table for the the comparison on reproducibility of overlapping projects.

|                                     |      Bears     |            |                 |                                     |   BugSwarm     |            |                 |
|:-----------------------------------:|:--------------:|:----------:|:---------------:|:-----------------------------------:|:--------------:|:----------:|:---------------:|
| Project                             | # Reproducible | # Artifact | Reproducibility | Project                             | # Reproducible | # Artifact | Reproducibility |
| spring-projects/spring-data-commons |              3 |         15 |          20.00% | spring-projects-spring-data-commons |              0 |          1 |           0.00% |
| spring-projects/spring-data-jpa     |              2 |          2 |         100.00% | spring-projects-spring-data-jpa     |              5 |         31 |          16.13% |
| brettwooldridge/HikariCP            |              0 |          1 |           0.00% | brettwooldridge-HikariCP            |              3 |          3 |         100.00% |
| vkostyukov/la4j                     |              1 |          1 |         100.00% | vkostyukov-la4j                     |              8 |          8 |         100.00% |
| square/javapoet                     |              1 |          1 |         100.00% | square-javapoet                     |              6 |         12 |          50.00% |
| raphw/byte-buddy                    |              0 |          5 |           0.00% | raphw-byte-buddy                    |            351 |        361 |          97.23% |
| HubSpot/Baragon                     |              0 |          1 |           0.00% | HubSpot-Baragon                     |             26 |         94 |          27.66% |
| apache/jackrabbit-oak               |              0 |          1 |           0.00% | apache-jackrabbit-oak               |              4 |          6 |          66.67% |

- Bugs.jar does not have projects overlapping with any other datasets.
