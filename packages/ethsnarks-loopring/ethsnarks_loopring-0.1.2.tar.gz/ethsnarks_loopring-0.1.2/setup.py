from distutils.core import setup
setup(
  name = 'ethsnarks_loopring',
  packages = ['ethsnarks_loopring'],
  version = '0.1.2',
  license='MIT',
  description = 'A toolkit for zkSNARKS signing specific to loopring',
  author = 'LinqLiquidityNetwork',
  author_email = 'michael@linq.network', 
  url = 'https://github.com/Linq-Liquidity-Network/ethsnarks-loopring',
  download_url = 'https://github.com/Linq-Liquidity-Network/ethsnarks-loopring/archive/v0.1.2.tar.gz',
  keywords = ['crypto', 'loopring', 'SNARKS', 'zero-knowledge', 'ethereum'],
  install_requires=[
            'bitstring',
            'pysha3',
            'pyblake2'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)