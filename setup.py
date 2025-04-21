from setuptools import setup, find_packages

setup(
    name='AcousticEmotions',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'librosa',
        'keras',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'acoustic-emotions=app:app',
        ],
    },
    description='A Flask app for Emotion Detection from Audio',
    author='Om Shirsat',  
    author_email='omshirsat77@gmail.com', 
    url='',  
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
