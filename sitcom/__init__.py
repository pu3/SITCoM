import pkg_resources

readme_file = pkg_resources.resource_string(__name__, 'README.md')
print(readme_file.decode('utf-8'))
