from setuptools import find_packages, setup

package_name = 'test_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gustaw',
    maintainer_email='gustaw@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
		"gpio_node = test_package.gpio_test_node:main",
		"pwm_node = test_package.gpio_pwm_test:main",
        "camera_node = test_package.camera_cv2_node:main"

        ],
    },
)
