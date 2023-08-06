from setuptools import setup, Extension


setup(
    name='mangoes',
    version='1.2.0',
    python_requires='>=3.6',
    packages=['mangoes', 'mangoes.evaluation', 'mangoes.utils'],
    ext_modules = [Extension("mangoes.utils.counting", ["mangoes/utils/counting.pyx"])],
    package_data={
        'mangoes': ['resources/en/similarity/*.txt', 'resources/fr/similarity/*.txt', 'resources/en/analogy/*/*/*.txt',
                    'resources/en/outlier_detection/*/*.txt', 'resources/en/outlier_detection/*.zip'],
    },
    include_package_data=True,
    url='https://gitlab.inria.fr/magnet/mangoes/',
    download_url='https://gitlab.inria.fr/magnet/mangoes/repository/1.2.0/archive.tar.gz',
    license='LGPL',
    author='Inria - Magnet',
    author_email='nathalie.vauquier@inria.fr',
    description='Mangoes 1.2 is a toolbox for constructing and evaluating word vector representations '
                '(aka word embeddings).',
    install_requires=['cython', 'nltk', 'numpy', 'scipy', 'sklearn', 'pandas'],
    extras_require={
        'visualize': ["matplotlib"],
        'generator': ["gensim"]
    },
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3.6',
    ],

)
