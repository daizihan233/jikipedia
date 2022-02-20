del .\dist\*.* /Q
python setup.py sdist bdist_wheel
python -m twine upload  dist/*
pip install jikipedia-api -U -i https://pypi.org/simple/