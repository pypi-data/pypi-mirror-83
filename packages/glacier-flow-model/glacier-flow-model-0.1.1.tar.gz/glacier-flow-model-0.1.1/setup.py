# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glacier_flow_model', 'glacier_flow_model.data']

package_data = \
{'': ['*']}

install_requires = \
['GDAL>=3.1.3,<4.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'numpy>=1.19.2,<2.0.0',
 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'glacier-flow-model',
    'version': '0.1.1',
    'description': 'Modeling glaciers flow, grounded on the glaciers mass balance and a digital elevation model (DEM).',
    'long_description': '.. image:: https://raw.githubusercontent.com/munterfinger/glacier-flow-model/master/docs/source/_static/logo.svg\n   :width: 120 px\n   :alt: https://github.com/munterfinger/glacier-flow-model\n   :align: right\n\n==================\nGlacier flow model\n==================\n\n.. image:: https://img.shields.io/pypi/v/glacier-flow-model.svg\n        :target: https://pypi.python.org/pypi/glacier-flow-model\n\n.. image:: https://github.com/munterfinger/glacier-flow-model/workflows/check/badge.svg\n        :target: https://github.com/munterfinger/glacier-flow-model/actions?query=workflow%3Acheck\n\n.. image:: https://readthedocs.org/projects/glacier-flow-model/badge/?version=latest\n        :target: https://glacier-flow-model.readthedocs.io/en/latest/\n        :alt: Documentation Status\n\n.. image:: https://codecov.io/gh/munterfinger/glacier-flow-model/branch/master/graph/badge.svg\n        :target: https://codecov.io/gh/munterfinger/glacier-flow-model\n\nModeling glaciers on a digital elevation model (DEM) based on the mass balance of the glaciers\nand the D8 flow algorithm applied to the ice.\n\nThe modeling is based on the linear relationship between altitude and mass balance, the so-called mass balance gradient.\nFor alpine glaciers this gradient is about 0.006 m/m. Continental glaciers tend to be at 0.003 and maritime glaciers\nat 0.01 m/m. The alpine gradient is set by default in the model.\nTo model the glaciers, annual steps are calculated. First the mass balance (accumulation and ablation) for the area\nis added to the glacier layer and in a second step the glacier flow is simulated by using the D8 technique,\nwhich is known for modeling surface water flows over the terrain. In order to avoid pure convergence of the flow,\na random impulse ("nudging") is added to the flow. Then the surface of the glaciers is slightly smoothed.\nThe simulation stops when the observed difference in mass balance for a smoothed curve (n=-100) is less than 0.0001 m.\n\nGetting started\n---------------\n\nThe **glacier-flow-model** package depends on GDAL, which needs to be installed on the system.\n\nGet the stable release of the package from pypi:\n\n.. code-block:: shell\n\n    pip install glacier-flow-model\n\nExample data\n____________\n\nThe package includes an example DEM from `swisstopo <https://www.swisstopo.admin.ch/en/home.html>`_.\nIt covers a smaller extent around the Aletsch glacial arena in Switzerland with a raster cell resolution of 200m.\n\n.. code-block:: python\n\n    from glacier_flow_model import PkgDataAccess\n    pkg = PkgDataAccess()\n    dem = pkg.load_dem()\n\nThe original DEM can be downloaded `here <https://shop.swisstopo.admin.ch/en/products/height_models/dhm25200>`_.\n\nUsage\n_____\n\nTo set up a glacier flow model, a path to a DEM in the GeoTiff (:code:`.tif` or :code:`.asc`)\nfile format has to passed to the model class constructor. By default the mass balance parameters for alpine glaciers\nin the year 2000 are set.  Keep the input file size small, otherwise the model may be slowed down remarkably:\n\n.. code-block:: python\n\n    from glacier_flow_model import GlacierFlowModel, PkgDataAccess\n    pkg = PkgDataAccess()\n    gfm = GlacierFlowModel(pkg.locate_dem())\n\nAfter initialization, the model needs to accumulate the initial ice mass until it reaches a steady state, call the\n:code:`reach_steady_state` method to do so:\n\n.. code-block:: python\n\n    gfm.reach_steady_state()\n\n.. image:: https://raw.githubusercontent.com/munterfinger/glacier-flow-model/master/docs/source/_static/steady_state_initial.png\n   :width: 120 px\n   :alt: https://github.com/munterfinger/glacier-flow-model\n   :align: center\n\nWhen the model is in a steady state, a temperature change of the climate can be simulated. Simply use\nthe :code:`simulate` method with a positive or negative temperature change in degrees.\nThe model changes the temperature gradually and simulates years until it reaches a steady state again.\n\nHeating 4.5°C after initial steady state:\n\n.. code-block:: python\n\n    gfm.simulate(4.5)\n\n.. image:: https://raw.githubusercontent.com/munterfinger/glacier-flow-model/master/docs/source/_static/steady_state_heating.png\n   :width: 120 px\n   :alt: https://github.com/munterfinger/glacier-flow-model\n   :align: center\n\nCooling -1°C after initial steady state:\n\n.. code-block:: python\n\n    gfm.simulate(-1)\n\n.. image:: https://raw.githubusercontent.com/munterfinger/glacier-flow-model/master/docs/source/_static/steady_state_cooling.png\n   :width: 120 px\n   :alt: https://github.com/munterfinger/glacier-flow-model\n   :align: center\n\nCheck out the `video <https://munterfinger.ch/media/film/gfm.mp4>`_ of the scenario simulation in the Aletsch\nglacial arena in Switzerland\n\nLimitations\n-----------\n\nThe model has some limitations that need to be considered:\n\n- The flow velocity of the ice per year is limited by the resolution of the grid cells. Therefore, a too high resolution should not be chosen for the simulation.\n- The modeling of ice flow is done with D8, a technique for modeling surface flow in hydrology. Water behaves fundamentally different from ice, which is neglected by the model (e.g. influence of crevasses).\n- No distinction is made between snow and ice. The density of the snow or ice mass is also neglected in the vertical column.\n\nLicense\n-------\n\nThis project is licensed under the MIT License - see the LICENSE file for details\n',
    'author': 'Merlin Unterfinger',
    'author_email': 'info@munterfinger.ch',
    'maintainer': 'Merlin Unterfinger',
    'maintainer_email': 'info@munterfinger.ch',
    'url': 'https://pypi.org/project/glacier-flow-model/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
