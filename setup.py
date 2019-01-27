from setuptools import setup


def fetch_version():
      '''
      Fetches version variable from version.py
      '''
      version = {}

      with open('scripting/version.py') as f:
            exec(f.read(), version)

      return version['__version__']


setup(name='wif',
      version=fetch_version(),
      description='Scripting Tools',
      url='http://github.com/UCLeuvenLimburg/scripting',
      author='Frederic Vogels',
      author_email='frederic.vogels@ucll.be',
      license='MIT',
      packages=['scripting'],
      entry_points = {
            'console_scripts': [ 'scripting=scripting.command_line:shell_entry_point']
      },
      zip_safe=False)