call jupyter nbconvert readme.ipynb --to markdown --execute 
call jupyter nbconvert readme.ipynb --clear-output
for /F "tokens=*" %%a in ('git branch --show-current') do set BRANCH=%%a
call python str_replace.py ./readme.md -f ](readme_files/ -r ](https://raw.githubusercontent.com/austinorr/lsys/%BRANCH%/docs/_all_docs_source/readme/readme_files/