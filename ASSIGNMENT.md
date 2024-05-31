
# Cyber Security Base 2024 - Project 1 - assignment

In the first project, the participants will construct software with security flaws, point out the flaws in the project, and provide the steps to fix them.

The project has only 1 part.

## Project description

In the first course project, your task is to create a web application that has at least five different flaws from the OWASP [top ten list](https://owasp.org/www-project-top-ten/) as well as their fixes. The application should have a backend.

OWASP recently updated its list and there are now two lists: 2017 and 2021. You can use either list but specify which one you are using. Do not mix the lists. Note that CSRF is missing from both lists as it is more rare nowadays due to the more secure frameworks. However, due to its fundamental nature it is allowed as a flaw.

We recommend that you implement the website using Python & Django. If you did the previous course you should already Django libraries installed. See [installation guide](https://cybersecuritybase.mooc.fi/installation-guide) otherwise. To create a starter website, follow the instructions [here](https://docs.djangoproject.com/en/3.1/intro/tutorial01/).

You may do the project without using the starter template (in a language of your own choosing). In that case, however, you must also provide guidelines for installing and running the web application on Windows, Linux and Mac (including guidelines for installing any possible required dependencies).

The code must be stored in a public repository so that other students may review it. A standard option is to use [GitHub](https://github.com). If you are a student at Helsinki University, you can use [version.helsinki.fi](https://version.helsinki.fi/). Make sure that the project is public. The easiest way to check the visibility is to try the links in incognito mode. Do not remove the project until you have received the points.

Make sure that (these are the most common reasons for project being rejected)

- The flaws are real, and not just hypothetical, and the fixes are included in the code
- The fix actually fixes the problem, and not just hide it
- There is a backend, and the flaws/fixes occur in the backend. Remember that the user can manipulate the frontend as much as possible.

Note that assay is not accepted immediately as it needs to be approved by the course staff.

## Writing essay

You will then write a 1000 word report (hard limits: 800-1500) that pinpoints the flaws and describes how they can be fixed. The report must follow the following structure:

```
LINK: link to the repository
installation instructions if needed

FLAW 1:
exact source link pinpointing flaw 1...
description of flaw 1...
how to fix it...

FLAW 2:
exact source link pinpointing flaw 2...
description of flaw 2...
how to fix it...

...

FLAW 5:
exact source link pinpointing flaw 5...
description of flaw 5...
how to fix it...
```

Add source link to each flaw if appropriate. Ideally, the link should have the format https://urldomain/repo/file.py#L42 (Line 42 in file.py). The links can be easily obtained by clicking the line numbers in the Github repository file browser. If the flaw involves in omitting some code, then comment-out the code, and provide the link to the beginning of the commented block.

Be specific with your fix. If possible, provide a fix to the problem in the code. The fix can be commented out. If appropriate, add a source link to each fix as well.

We recommend not to write the essay directly to the browser. Instead write (and save) it using your favourite text editor, and then use copy-paste.

Please write the essay carefully and with thought. Other participants in the course will review them and give you feedback. Essays should be written individually and using your own words. Copy-pasting from other sources is not allowed. Copy-pasting text from other sources and pretending it to be your own counts as plagiarism. [Plagiarism](https://studies.helsinki.fi/instructions/article/what-cheating-and-plagiarism) is not allowed under any circumstances, and will have consequences when caught. See [here](https://cybersecuritybase.mooc.fi/rubric#heading-on-the-usage-of-llm) regarding the usage of LLMs.

## Peer reviewing essays

Peer reviewing consists of general comments and 5 grades, one for each flaw.

You should justify your grading in the general comments. Comment on each flaw. Be specific, constructive, and polite.

If the essay contains more than 5 flaws, select 5 flaws you would like to grade, for example, 5 first or, in your opinion, 5 best.

```
1. Failed: The flaw is missing, or otherwise inappropriate
2. Passable: The flaw is identified correctly, the fix partially corrects the problem. The underlying problem and the effect of the fix is somewhat misuderstood.
3. Average: The flaw described adequately and the fix fixes the problem. Minor misunderstanding of the underlying mechanism. The description is too vague but ultimately correct.
4. Good: The flaw and the fix are correctly done. Minor issues in descriptions.
5. Excellent: No issues or only cosmetic issues
```
