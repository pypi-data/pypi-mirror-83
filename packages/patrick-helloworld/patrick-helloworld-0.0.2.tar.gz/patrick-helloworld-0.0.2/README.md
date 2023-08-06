# Create Your Own Python Package

Based on the talk here: https://www.youtube.com/watch?v=GIF3LaRqgXo&ab_channel=CodingTech

<b>Setup Steps</b>

1. Create your Python module (in here it is helloworld.py)
2. Create setup.py file (see setup.py file)
3. Run "python setup.py bdist_wheel" (creates build, dist, and other folders/files)
4. Optional: Create .gitignore (just good practice, checkout gitignore.io)
5. Add the .egg-info file in the src directory to the .gitignore (it is unnecessary apparently).
6. Create README.md
7. Run "pip install -e ." to install this package locally (run frequently to check your work)
8. Add a license (checkout choosealicense.com). MIT License added here by default.
9. Optional: Run some tests (checkout a package called pytest, it is great)
10. Run "pip install check-manifest", then "check-manifest --create", then "git add MANIFEST.in" (this all helps the next step run properly)
11. Run "python setup.py sdist" to create a .tar.gz file with the source code for distribution
12. Run "python setup.py bdist_wheel sdist"
13. Run "pip install twine", then "twine upload dist/*" and woohoo! you have now uploaded it to pypi!
14. To test with different versions of Python, checkout the "tox" package
15. To get started, it is best to use the "cookiecutter" package! Run "pip install cookiecutter" then "cookiecutter gh: ionelmc/cookiecutter-pylibrary