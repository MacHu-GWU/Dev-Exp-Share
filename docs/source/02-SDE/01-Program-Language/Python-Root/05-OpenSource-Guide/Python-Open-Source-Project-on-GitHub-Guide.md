## Python Open Source Project on GitHub Guide

From author perspective, Open Source is not just writing the code and checking in to the GitHub. There are far more works to do to make an OpenS Source project successful. **Now let's think backward from the user's perspective, how usually people make decision to use an Open Source project as an user**:

1. I have a problem, which Open Source project can solve the problem?
2. Does the project have document to teach me how to use it?
    - I want to quick start in ten minutes.
    - If I have a use case, is there an example of how to do it?
    - If I am looking for details of an API, is there an input / output document?
3. Can I trust this project?
    - Are the features really working? Are the core features fully tested with many different good cases, edge cases?
    - How do I know non-feature code won't break my work? What is the percentage of the code base that covered by test?
    - How do I know my OS and Python version is fully supported?
4. How can I install this software?
5. Can I trust the author / maintainer team of this project?
    - do they have Continues Integration (CI) for code quality control?
    - does the code style shows that they are trustworthy developers?
6. If I have questions, need help, where can I get help?
7. If I have a very important use case which is similar to this open source but not supported yet, how can I contribute this project? So I can use it in the next version?

**Based on how user thinking, the following list is what we need to include in an Open Source project**. The more we missed, the users are less confident.

1. Define the problem this project is trying to solve, and your code should be able to solve that in a User-Friendly / Pythonic way.
2. Have lots of documentation, doc string for your ``module, Class, method, function``.
    - basic: the Readme file style
    - advanced: delegated doc website on www.readthedocs.org, with 10 minutes tutorial, doc by use case, doc by API
3. Have unit test to ensure the core features are working in different scenarios.
4. Have code coverage test to ensure non-feature code won't break. Better to have 95%+ for Open Source.
5. Have matrix test to ensure your project works consistently on Windows / MacOS / Linux, Python3.6, 3.7, 3.8, ...
6. Publish the project on PyPI, should be pip installable, and dependencies installation should also be automated.
7. Use Continues Integration (CI) for unit test, code coverage test, matrix test, doc build.
8. Have consistent code style to prove that the maintainer team are quality developers.
9. Have an Open Source community for this project, allow user to submit "bug report", "feature request", "ask for help"
    - basic: GitHub issue + Issue Template
    - advance: public Slack / Gitter channel, Stackoverflow Tag
10. Have many digital badges to display status of CI / doc status / latest version and other information on the home page.
11. Have a Contribution Guide, allow users to contribute code and run test with minimal setup. Open Source usually use GitHub folk workflow for this purpose.
12. Have release history docs, mark the API history, API change, backward incompatible change, etc ...
    - basic: one readme file
    - advanced: use ``.. versionadded::``, ``.. deprecated::`` everywhere in your code base.
