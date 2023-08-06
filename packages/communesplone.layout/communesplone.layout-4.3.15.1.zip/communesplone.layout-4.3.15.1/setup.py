from setuptools import setup, find_packages

version = '4.3.15.1'

long_description = (
    open('README.txt').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='communesplone.layout',
      version=version,
      description="General layout adaptations",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Programming Language :: Python",
      ],
      keywords='',
      author='CommunesPlone.org',
      author_email='support@communesplone.be',
      url='http://svn.communesplone.org/svn/communesplone/communesplone.layout',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['communesplone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.captcha'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
