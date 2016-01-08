  Project Title:       Human Brain Project
  -------------------- ------------------------------------
  Sub-Project Title:   Medical Informatics Platform (SP8)
  Task no:             8.4.2
  
  Document Title:    **User Guidelines : Algorithm Factory &gt; Pushing new algorithms into Algorithm pipeline**
  ------------------ --------------------------------------------------------------------------------------------------------
  Authors:   *Ludovic Claude, CHUV*
  ---------- ------------------------

  Summary:   *Steps of how new R algorithms may be tested and pushed into Algorithm Factory pipeline, for deployment into production.*
  ---------- -------------------------------------------------------------------------------------------------------------------------

<span id="_Overview_of_the" class="anchor"><span id="_Toc439876557" class="anchor"></span></span>Purpose of Guidelines
======================================================================================================================

Step-by-step guide to “R” algorithm developers on how to push new
algorithms developed in R into the MIP Algorithm Factory pipeline. Once
code is committed, the algorithm will be planned to be deployed into
MIP.

Guidelines for the other technologies (Matlab, Java etc) will be similar
and will be developed soon.

***Definitions:***

*Algorithm Pipeline = algorithms waiting to be deployed into production*

*Algorithm Catalogue = all algorithms of MIP - live, waiting to be
released into production (in pipeline), retired.*

*(SP8 will be applying ITIL service management standards for managing
algorithm services -*
[*http://www.itil.org.uk/what.htm*](http://www.itil.org.uk/what.htm)*)*


Step-by-Step Guidelines
=======================

1.  **Go to** GitHub

2.  **Clone** the *functions-repository* folder -
    <https://github.com/LREN-CHUV/functions-repository>

3.  In your clone, **go to** *mip\_node*

4.  **Make a copy** of *r-summary-stats* directory and rename it into
    the name of your algorithm (r-…)

5.  In your copy of r-summary-stats directory, **adapt** a few files :

    a.  *Dockerfile *:

      Line 14: **replace** this line to install your packages. There are 3
      possibilities:

i.  If your package is available in R-CRAN, use the syntax :

    RUN install.r &lt;package1&gt; &lt;package2&gt; &lt;package3&gt;…

ii. If your package is available on GitHub, use:

    RUN installGithub.r &lt;github coordinates&gt; where the Github
    coordinates look like username/projectname, and optionally add a @
    sign followed by the Git version to use, for example
    LREN-CHUV/hbpsummarystats@6f6a42e

iii. If the package is only available as a local file, copy the package
    into the same directory with the Dockerfile, and add the following
    two lines :

    COPY mypackage\_linux64.tar.gz /tmp/

    RUN install.r /tmp/mypackage\_linux64.tar.gz

b\. All files: **rename** *r-summary-stats* into the name of your
function (r-…)

c\. *main.R:*

> This file contains the main script used to adapt the R function to the
> MIP environment. It should work like that:

-   Parameters are coming from system environment variables. There are a
    few well known environment variables that you may need :

    -   *PARAM\_query* : contains the SQL query to execute against the
        local database

    -   *JOB\_ID* : ID of the current job

    -   *NODE* : name of the current node (don’t worry about it)

    -   *IN\_JDBC\_xxx* and *OUT\_JDBC\_xxx* define how to connect to
        the input and output database. You probably don’t need that
        except when you test your script.

-   Your function **may need more parameters**. In this case, use new
    environment variables, for example *PARAM\_nb\_iterations*. Use
    *Sys.env()* to read the values and maybe some conversions as those
    values are always read as strings.

-   **Call** fetchData function to query the database. It implicitly
    uses *PARAM\_query* to know what SQL query to send to the database.

-   **Perform the computation** using the result from *fetchData* and
    the additional parameters used by your function

-   **Transform the results into Json**. The library *jsonlite* from
    R-CRAN is available and good for this task. *If the results are a
    dataset or a matrix, you should not need to do anything.*

-   **Save the results** in the database using *saveResults* function.
    It can take as parameter a JSON string, a dataset or a matrix.

d\. *dev.sh:* **update this to test** **your main.R script**. This script
is launching R (from Docker) with some libraries installed and an input
and output database ready to use.

You can change the SQL query here, and from R you can call *fetchData()*
to get the results of the query. Paste the code from main.R into the R
console to test that it works as expected.

6.  Nice to have:

    Update *tests/test.sh* and *tests/testthat.R* to test your function.

    You can change the SQL query to select other datasets. If you need
    new datasets, go to */tests/dummy-ldsm/sql/create.sql* and adapt the
    table creation scripts written in SQL, then launch again *./dev.sh*
    to test that it works.

    The tests can be executed by running the command *‘captain test’*

7.  Commit the results and make a pull request in GitHub

If want to see the test data, go to */tests/dummy-ldsm/sql/create.sql *

Contact:
=======

**For any questions or problems, contact Ludovic Claude (CHUV),
<ludovic.claude54@gmail.com>**
