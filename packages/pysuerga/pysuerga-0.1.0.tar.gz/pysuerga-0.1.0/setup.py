import setuptools


LONG_DESCRIPTION = '''
Pysuerga is a very simple static site generator. It was initially created
for [pandas](https://pandas.pydata.org), but is used in other projects.

To use Pysuerga you need to create the website structure for your project,
with markdown templates, and Pysuerga will generate the same structure after
rendering the files.

It is able to manage variables in a structure way, can use Jinja2 in the templates
and includes plugins for some common pages: team page with GitHub info, blog
aggregator, release information, etc.
'''

setuptools.setup(name='pysuerga',
                 description='Python simple static site generator for open source projects',
                 long_description=LONG_DESCRIPTION,
                 url='https://github.com/datapythonista/pysuerga',
                 version='0.1.0',
                 author='Marc Garcia',
                 author_email='garcia.marc@gmail.com',
                 license='BSD',
                 packages=setuptools.find_packages(),
                 package_data={'': ['templates/layout.html']},
                 install_requires=['markdown', 'jinja2', 'pyyaml'],
                 classifiers=['Development Status :: 4 - Beta',
                              'Environment :: Console',
                              'Operating System :: OS Independent',
                              'Intended Audience :: Developers',
                              'Programming Language :: Python :: 3',
                              'Programming Language :: Python :: 3.6',
                              'Programming Language :: Python :: 3.7',
                              'Programming Language :: Python :: 3.8',
                              'Topic :: Utilities'])
