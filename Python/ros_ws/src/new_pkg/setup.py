from setuptools import find_packages, setup
from glob import glob
package_name = 'new_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='roberto',
    maintainer_email='roberto.gar.1748@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "publicador         = new_pkg.publicador:main",
            "suscriptor         = new_pkg.suscriptor:main",
            "servidor_servicio  = new_pkg.servidor_servicio:main",
            "cliente_servicio   = new_pkg.cliente_servicio:main",
            "servidor_accion    = new_pkg.servidor_accion:main",
            "cliente_accion     = new_pkg.cliente_accion:main"
        ],
    },
)
