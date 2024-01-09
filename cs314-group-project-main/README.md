# Group Project for CS314 Elements of Software Engineering
Our data processing software contract for ChocAn.

## Development Setup
Some steps to get a nice environment on `ada.cs.pdx.edu` for working on the code.

### Clone the repo
After `ssh`-ing into `ada.cs.pdx.edu` and `cd`-ing to where you want the project directory to live, run:
```bash
git clone git@gitlab.cecs.pdx.edu:sjeobb/cs314-group-project.git
```

### Install [`hatch`](https://hatch.pypa.io)
Hatch is the package manager we'll use to help keep our python dependencies organized. This install step should only need to be done once per account.  
There's a script to install it, [`initialize.sh`](initialize.sh), so just `cd` to the project directory and run:
```bash
./initialize.sh
```

### Connect VS Code (optional)
You can just use `vim` if you want, but having an IDE can be nice.
With VS Code and the "Remote - SSH" extension installed, you can click the little section in the bottom left of the VS Code window and choose "Connect to Host", then enter info for `ada.cs.pdx.edu` and finally navigate to the directory for this project.

TODO: add some notes about integrating the testing, linting, and formatting tools with VS Code.

## Writing Code
After getting your development environment setup, You can start writing some code!  
> 📝 We can make this less elaborate if we would like, but here is an idea for a very "Software Engineering"-y style of contribution process. We are small enough of a team to not really *need* it but it might be a fun exercise. The simplest alternative would just be to push directly to the main branch.
  * Set the `main` branch as current, if it is not already:
    ```bash
    git checkout main
    ```
  * Pull any changes that may have been made to the GitLab respository since you last checked:
    ```bash
    git pull
    ```
  * Pick a name for the chunk of changes you intend to make, and create a new branch to hold them.
    ```bash
    git checkout -b descriptive_branch_name_here
    ```
  * Make some changes! Program code goes in [`src/cs314_group_project/`](src/cs314_group_project/), and test code goes in [`tests/`](tests/).
  * As you make changes, it can be nice to periodically run automatic formatting to keep the style consistent:
    ```bash
    hatch run lint:fmt
    ```
  * Check that your code is good:
    ```bash
    # This checks that the code is formatted, that the type annotations (if any) are correct, and also that a bunch of miscellaneous mistakes haven't been made.
    hatch run lint:all
    ```
    ```bash
    # This runs all the pytests in the `tests/` directory.
    hatch run test
    ```
  * Once you've made a "logical unit" of change you could describe in a few words, and the above checks all pass, it's a good idea to make a commit.
    ```bash
    git status  # to see what git notices as having changed
    ```
    ```bash
    git add file_path_here  # to add each changed file to the commit individually
    # or
    git add .  # to add changes in the current directory, i.e. everything
    ```
    ```bash
    git commit -m 'short description of unit of change'
    # if you leave off the `-m` message, git will open an editor for you to write the message.
    ```
  * After making all the commits needed for the chunk of change you set out to accomplish with this branch, you can push your branch to the online repository.
    ```bash
    # This longer command is for pushing a new branch for the first time, so that it gets created on GitLab. `-u` is short for `--set-upstream`.
    git push -u origin HEAD
    ```
  * "Merge Requests" will be how we organize our chunks of changes. They provide a dedicated place for us to all look at, discuss, and propose edits together for each big change. There is integrated tooling for commenting on specific lines, suggesting edits, signing your approval of the merge, etc.  
    GitLab should respond to your push of a new branch with a link in the terminal output to create a merge request for your branch. Follow that.
    Alternatively, there should be some way to initiate the merge request from the GitLab page somewhere, but I'm not sure where it is.  
    On the page for creating the merge request, give it a title and description if you want. You can also assign people to be reviewers if you want. Then just click the button to finish creating the request.  
    Then potentially some of us will review your code. If there are any suggested edits that you agree with, you can go and make them from VS Code, and then commit and push them again, which will show up in the merge request. (You won't need the longer form of `git push` this time since the branch already exists on GitLab)
  * Finally, once the merge request has been reviewed and approved, we can click the button to merge your changes into the main branch.  
  After that, you can go and delete the branch you made on your local repo:
    ```bash
    git branch --delete your_old_branch_name_here
    ```
    And start from the beginning again!