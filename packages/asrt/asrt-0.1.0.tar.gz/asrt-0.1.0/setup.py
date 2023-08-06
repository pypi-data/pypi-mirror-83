try:
    from setuptools import setup #enables develop
except ImportError:
    from distutils.core import setup

from setuptools import find_packages

long_description = '''
ASRT is a high-level deep learning API for speech recognition,
written in Python and capable of running on top of
Keras, TensorFlow, or MxNet.
Use ASRT if you need a deep learning library that:
- Allows for easy and fast prototyping for speech recognition
  (through user friendliness, modularity, and extensibility).
- Supports both Keras and other Deep learning framework(on future).
- Runs seamlessly on CPU and GPU.
- Contains a api server module for developers to test models easily.
Read the documentation at: https://github.com/nl8590687/ASRT_SpeechRecognition/wiki
For a detailed overview of what makes ASRT special, see:
https://asrt.ailemon.me
ASRT is compatible with Python 3.0-3.7
and is distributed under the GPL v3.0 license.
'''

setup(name='asrt',
	version='0.1.0',
	description='A Deep-Learning-Based Auto Speech Recognition Toolkit',
	long_description=long_description,
	long_description_content_type = 'text/markdown',
	author='ailemon',
	author_email='ailemon@ailemon.me',
	license='GPL v3.0',
	url='https://asrt.ailemon.me',
	download_url = "https://pypi.python.org/pypi/asrt",
	project_urls={
		"Bug Tracker": "https://github.com/nl8590687/ASRT_SpeechRecognition/issues",
		"Documentation": "https://asrt.ailemon.me/docs/",
		"Source Code": "https://github.com/nl8590687/ASRT_SpeechRecognition",
	},
	python_requires='>=3.5',
	packages=find_packages(),
	package_data={
        '': ['LICENSE'], },
	zip_safe=False,
	install_requires=[
		'numpy',
		'scipy',
		'wave',
		'matplotlib',
		'python_speech_features',
	],
	extras_require={
		'visualize': ['pydot>=1.2.4'],
		'tests': ['pandas',
				'requests'],
	},
	
	classifiers=[
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
		('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
		"Operating System :: OS Independent",
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6'
	]
)