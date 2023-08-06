from setuptools import setup

setup(
    name='waveshare-d2a-a2d-pigpio',
    version='1.0.0',
    packages=['waveshare', 'waveshare.ADS1256', 'waveshare.DAC8552', 'original-AD', 'original-DA', 'examples'],
    url='https://github.com/the-moog/waveshare_a2d_d2a_python',
    license='https://github.com/makahn64/waveshare_a2d_d2a_python',
    author='Jason Morgan, largely based on work by Mitch Kahn',
    author_email='pypy@cropwell.net',
    description='Python PiGPIO interface to Raspberry Pi Waveshare A2D/D2A Card',
    install_requires=['pigpio', 'blessings'],
    python_requires='>=3.7',
)

