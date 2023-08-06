from setuptools import setup

setup(
    name='midi_viewer',
    version='0.0.1',
    author='Marco Bolt',
    email='marco.r.bolt@gmail.com',
    description = 'Basic midi keyboard display tool for use as a teaching aid.',
    install_requires=['PyQt5', 'pygame==2.0.0.dev18'],
    py_modules=['midi_viewer_live'],
    entry_points={
        'console_scripts': ['midi_viewer=midi_viewer_live:main']
    },
    classifiers = [
        "Programming Language :: Python :: 3.8"
    ]
)
