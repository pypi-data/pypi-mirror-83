# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastflix',
 'fastflix.encoders',
 'fastflix.encoders.av1_aom',
 'fastflix.encoders.avc_x264',
 'fastflix.encoders.common',
 'fastflix.encoders.gif',
 'fastflix.encoders.hevc_x265',
 'fastflix.encoders.rav1e',
 'fastflix.encoders.svt_av1',
 'fastflix.encoders.vp9',
 'fastflix.encoders.webp',
 'fastflix.widgets',
 'fastflix.widgets.panels']

package_data = \
{'': ['*'], 'fastflix': ['data/*', 'data/encoders/*', 'data/rotations/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'coloredlogs>=14.0,<15.0',
 'mistune>=0.8.4,<0.9.0',
 'psutil>=5.7.2,<6.0.0',
 'pyside2>=5.15.0,<6.0.0',
 'python-box[all]>=5.1.1,<6.0.0',
 'qtpy>=1.9.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'reusables>=0.9.5,<0.10.0',
 'ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['fastflix = fastflix.__main__:start_fastflix']}

setup_kwargs = {
    'name': 'fastflix',
    'version': '3.3.1',
    'description': 'Easy to use video encoder GUI',
    'long_description': '# FastFlix\n\n![preview](./docs/gui_preview.png)\n\nFastFlix is a simple and friendly GUI for encoding videos.\n\nFastFlix keeps HDR10 metadata for x265, which will be expanded to AV1 libraries when available.\n\nIt needs `FFmpeg` (version 4.3 or greater) under the hood for the heavy lifting, and can work with a variety of encoders.\n\nCheck out [the FastFlix github wiki](https://github.com/cdgriffith/FastFlix/wiki) for help or more details!\n\n#  Encoders\n\n FastFlix supports the following encoders when their required libraries are found in FFmpeg:\n\n* HEVC (libx265) &nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_x265.png" height="30" alt="x265" >\n* AVC (libx264) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_x264.png" height="30" alt="x264" >\n* AV1 (librav1e) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_rav1e.png" height="30" alt="rav1e" >\n* AV1 (libaom-av1) &nbsp; <img src="./fastflix/data/encoders/icon_av1_aom.png" height="30" alt="av1_aom" >\n* AV1 (libsvtav1) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_svt_av1.png" height="30" alt="svt_av1" >\n* VP9 (libvpx) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_vp9.png" height="30" alt="vpg" >\n* WEBP (libwebp) &nbsp;&nbsp;&nbsp;<img src="./fastflix/data/encoders/icon_webp.png" height="30" alt="vpg" >\n* GIF (gif) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_gif.png" height="30" alt="gif" >\n\nMost builds do not have all these encoders available by default and may require custom compiling FFmpeg for a specific encoder.\n\n* [Window FFmpeg (and more) auto builder](https://github.com/m-ab-s/media-autobuild_suite)\n* [Windows cross compile FFmpeg (build on linux)](https://github.com/rdp/ffmpeg-windows-build-helpers)\n* [FFmpeg compilation guide](https://trac.ffmpeg.org/wiki/CompilationGuide)\n\n# Releases\n\n## Windows\n[![Build status](https://ci.appveyor.com/api/projects/status/208k29cvoq8xwf8j/branch/master?svg=true)](https://ci.appveyor.com/project/cdgriffith/fastflix/branch/master)\n\nView the [releases](https://github.com/cdgriffith/FastFlix/releases) for 64 bit Windows binaries (Generated via Appveyor and also [available there](https://ci.appveyor.com/project/cdgriffith/fastflix)).\n\n## MacOS and Linux\n\nDue to a recent library addition there have been unexpected dependencies on *nix systems that will try to be removed in future versions.\n\n**MacOS** You will need to have Xcode installed  \n**Linux** Please install `gcc` and python3 development files (`python3-dev` on Ubuntu, `python3-devel` on RedHat)\n\nThen please use [pipx](https://pipxproject.github.io/pipx/installation/) to install as a properly virtualized app\n\n```\npipx install fastflix\n```\n\nYou will need to have `ffmpeg` and `ffprobe` executables on your PATH and they must be executable. Version 4.3 or greater is required. The one in your in your package manager system may not support all encoders or options.\nCheck out the [FFmpeg download page for static builds](https://ffmpeg.org/download.html) for Linux and Mac.\n\n## Running from source code\n\n```\ngit clone https://github.com/cdgriffith/FastFlix.git\ncd FastFlix\npython3 -m venv venv\n. venv/bin/activate\npip install -r requirements.txt\npython -m fastflix\n```\n\n# HDR\n\nOn any 10-bit or higher video output, FastFlix will copy the input HDR colorspace (bt2020). Which is [different than HDR10 or HDR10+](https://codecalamity.com/hdr-hdr10-hdr10-hlg-and-dolby-vision/).\n\n## HDR10\n\nFastFlix was created to easily extract / copy HDR10 data, but as of sept 2020, only x265 supports copying that data through FFmpeg, no AV1 library does.\n\n* rav1e -  can set mastering data and CLL via their CLI but [not through ffmpeg](https://github.com/xiph/rav1e/issues/2554).\n* SVT AV1 - accepts a "--enable-hdr" flag that is [not well documented](https://github.com/AOMediaCodec/SVT-AV1/blob/master/Docs/svt-av1_encoder_user_guide.md), not supported through FFmpeg.\n* aomenc (libaom-av1) - does not look to support HDR10\n\n## HDR10+\n\nFastFlix does not currently support copying HDR10+ metadata, but is a planned feature for x265.\n\n## Dolby Vision\n\nFastFlix does not plan to support Dolby Visions proprietary format, as it requires royalties.\n\n\n# License\n\nCopyright (C) 2019-2020 Chris Griffith\n\nThe code itself is licensed under the MIT which you can read in the `LICENSE` file. <br>\nRead more about the release licensing in the [docs](docs/README.md) folder. <br>\nEncoder icons for [VP9](https://commons.wikimedia.org/wiki/File:Vp9-logo-for-mediawiki.svg) and [AOM AV1](https://commons.wikimedia.org/wiki/File:AV1_logo_2018.svg) are from Wikimedia Commons all others are self created.\n',
    'author': 'Chris Griffith',
    'author_email': 'chris@cdgriffith.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
