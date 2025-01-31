rm -rf htmlcov
coverage run -m unittest notepaper_test
coverage html
