from distutils.core import setup
setup(
    author='J Samuels',
    author_email='jeep123samuels@gmail.com',
    description='Base classes for users and authentications for Flask',
    download_url='https://github.com/Jeep123Samuels/auth_users/archive/main.zip',
    keywords=['Flask', 'users', 'authenticate'],
    license='MIT',
    name='auth_users',
    packages=['auth_users', 'auth_users.authentication'],
    version='0.1.5',
    url='https://github.com/Jeep123Samuels/auth_users',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
