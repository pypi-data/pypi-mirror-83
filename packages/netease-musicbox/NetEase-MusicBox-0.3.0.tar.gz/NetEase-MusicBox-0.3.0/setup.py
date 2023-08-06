# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['NEMbox']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy>=0.18.0,<0.19.0',
 'importlib-metadata>=2.0.0,<3.0.0',
 'pycryptodomex>=3.9.8,<4.0.0',
 'python-Levenshtein>=0.12.0,<0.13.0',
 'requests-cache>=0.5.2,<0.6.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['musicbox = NEMbox.__main__:start']}

setup_kwargs = {
    'name': 'netease-musicbox',
    'version': '0.3.0',
    'description': 'A sexy command line interface musicbox',
    'long_description': '# NetEase-MusicBox\n\n**感谢为 MusicBox 的开发付出过努力的[每一个人](https://github.com/darknessomi/musicbox/graphs/contributors)！**\n\n高品质网易云音乐命令行版本，简洁优雅，丝般顺滑，基于Python编写。\n\n[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)\n[![versions](https://img.shields.io/pypi/v/NetEase-MusicBox.svg)](https://pypi.org/project/NetEase-MusicBox/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/NetEase-MusicBox.svg)](https://pypi.org/project/NetEase-MusicBox/)\n\n## Demo\n\n[![NetEase-MusicBox-GIF](https://qfile.aobeef.cn/3abba3b8a3994ee3d5cd.gif)](https://pypi.org/project/NetEase-MusicBox/)\n\n## 功能特性\n\n1. 320kbps的高品质音乐\n2. 歌曲，艺术家，专辑检索\n3. 网易22个歌曲排行榜\n4. 网易新碟推荐\n5. 网易精选歌单\n6. 网易主播电台\n7. 私人歌单，每日推荐\n8. 随心打碟\n9. 本地收藏，随时加❤\n10. 播放进度及播放模式显示\n11. 现在播放及桌面歌词显示\n12. 歌曲评论显示\n13. 一键进入歌曲专辑\n14. 定时退出\n15. Vimer式快捷键让操作丝般顺滑\n16. 可使用数字快捷键\n17. 可使用自定义全局快捷键\n18. 对当前歌单列表进行本地模糊搜索\n\n### 键盘快捷键\n\n有 num + 字样的快捷键可以用数字修饰，按键顺序为先输入数字再键入被修饰的键，即 num + 后的快捷键。\n\n| Key       | Effect          |                    |\n| --------- | --------------- | ------------------ |\n| <kbd>j</kbd>         | Down            | 下移               |\n| <kbd>k</kbd>         | Up              | 上移               |\n| num + <kbd>j</kbd>   | Quick Jump      | 快速向后跳转n首    |\n| num + <kbd>k</kbd>   | Quick Up        | 快速向前跳转n首    |\n| <kbd>h</kbd>         | Back            | 后退               |\n| <kbd>l</kbd>         | Forword         | 前进               |\n| <kbd>u</kbd>         | Prev Page       | 上一页             |\n| <kbd>d</kbd>         | Next Page       | 下一页             |\n| <kbd>f</kbd>         | Search          | 当前列表模糊搜索   |\n| <kbd>\\[</kbd>        | Prev Song       | 上一曲             |\n| <kbd>]</kbd>         | Next Song       | 下一曲             |\n| num + <kbd>\\[</kbd>  | Quick Prev Song | 快速前n首          |\n| num + <kbd>]</kbd>   | Quick Next Song | 快速后n首          |\n| num + <kbd>Shift</kbd> + <kbd>g</kbd>   | Index for Song  | 跳到第n首          |\n| <kbd>=</kbd>         | Volume +        | 音量增加           |\n| <kbd>-</kbd>         | Volume -        | 音量减少           |\n| <kbd>Space</kbd>     | Play/Pause      | 播放/暂停          |\n| <kbd>?</kbd>         | Shuffle         | 手气不错           |\n| <kbd>m</kbd>         | Menu            | 主菜单             |\n| <kbd>p</kbd>         | Present/History | 当前/历史播放列表  |\n| <kbd>i</kbd>         | Music Info      | 当前音乐信息       |\n| <kbd>Shift</kbd> + <kbd>p</kbd> | Playing Mode    | 播放模式切换       |\n| <kbd>a</kbd>         | Add             | 添加曲目到打碟     |\n| <kbd>Shift</kbd> + <kbd>a</kbd> | Enter Album     | 进入专辑           |\n| <kbd>g</kbd>         | To the First    | 跳至首项           |\n| <kbd>Shift</kbd> + <kbd>g</kbd> | To the End      | 跳至尾项           |\n| <kbd>z</kbd>         | DJ List         | 打碟列表           |\n| <kbd>s</kbd>         | Star            | 添加到收藏         |\n| <kbd>c</kbd>         | Collection      | 收藏列表           |\n| <kbd>r</kbd>         | Remove          | 删除当前条目       |\n| <kbd>Shift</kbd> + <kbd>j</kbd> | Move Down       | 向下移动当前项目   |\n| <kbd>Shift</kbd> + <kbd>k</kbd> | Move Up         | 向上移动当前项目   |\n| <kbd>Shift</kbd> + <kbd>c</kbd> | Cache           | 缓存歌曲到本地     |\n| <kbd>,</kbd>         | Like            | 喜爱               |\n| <kbd>.</kbd>         | Trash FM        | 删除 FM            |\n| <kbd>/</kbd>         | Next FM         | 下一FM             |\n| <kbd>q</kbd>         | Quit            | 退出               |\n| <kbd>t</kbd>         | Timing Exit     | 定时退出           |\n| <kbd>w</kbd>         | Quit & Clear    | 退出并清除用户信息 |\n\n## 安装\n\n### 必选依赖\n\n1. `mpg123` 用于播放歌曲，安装方法参见下面的说明\n2. `python-fuzzywuzzy` 用于模糊搜索\n\n### 可选依赖\n\n1. `aria2` 用于缓存歌曲\n2. `libnotify-bin` 用于支持消息提示（Linux平台）\n3. `pyqt python-dbus dbus qt` 用于支持桌面歌词\n   (Mac 用户需要 `brew install qt --with-dbus` 获取支持 DBus 的 Qt)\n4. `python-levenshtein` 用于模糊搜索\n\n### PyPi安装（*nix系统）\n\n```bash\n    pip3 install NetEase-MusicBox\n```\n\n### Git clone安装master分支（*nix系统）\n\n```bash\n    git clone https://github.com/darknessomi/musicbox.git && cd musicbox\n    poetry build && poetry install\n```\n\n### macOS安装\n\n```bash\n    pip3 install NetEase-MusicBox\n    brew install mpg123\n```\n\n### Linux安装\n\n**注意：通过以下方法安装可能仍然需要`pip3 install -U NetEase-MusicBox`更新到最新版**。\n\n#### Fedora\n\n首先添加[FZUG](https://github.com/FZUG/repo/wiki)源，然后`sudo dnf install musicbox`。\n\n#### Ubuntu/Debian\n\n```bash\n    pip3 install NetEase-MusicBox\n\n    sudo apt-get install mpg123\n```\n\n#### Arch Linux\n\n```bash\n    pacaur -S netease-musicbox-git # or $ yaourt musicbox\n```\n\n#### Centos/Red Hat\n\n```bash\n    pip3 install NetEase-MusicBox\n    wget http://mirror.centos.org/centos/7/os/x86_64/Packages/mpg123-1.25.6-1.el7.x86_64.rpm\n    sudo yum install -y mpg123-1.25.6-1.el7.x86_64.rpm\n```\n\n## 配置和错误处理\n\n配置文件地址: `~/.config/netease-musicbox/config.json`\n可配置缓存，快捷键，消息，桌面歌词。\n由于歌曲 API 只接受中国大陆地区访问，非中国大陆地区用户请自行设置代理（可用polipo将socks5代理转换成http代理）：\n\n```bash\nexport http_proxy=http://IP:PORT\nexport https_proxy=http://IP:PORT\ncurl -L ip.cn\n```\n\n显示IP属于中国大陆地区即可。\n\n### 已测试的系统兼容列表\n\n| OS       | Version               |\n| -------- | --------------------- |\n| Arch     | Rolling               |\n| macOS    | 10.15.7               |\n\n### 错误处理\n\n当某些歌曲不能播放时，总时长为 00:01 时，请检查是否为版权问题导致。\n\n如遇到在特定终端下不能播放问题，首先检查**此终端**下mpg123能否正常使用，其次检查**其他终端**下musicbox能否正常使用，报告issue的时候请告知以上使用情况以及出问题终端的报错信息。\n\n同时，您可以通过`tail -f ~/.local/share/netease-musicbox/musicbox.log`自行查看日志。\nmpg123 最新的版本可能会报找不到声音硬件的错误，测试了1.25.6版本可以正常使用。\n\n### 已知问题及解决方案\n\n- [#374](https://github.com/darknessomi/musicbox/issues/374) i3wm下播放杂音或快进问题，此问题常见于Arch Linux。尝试更改mpg123配置。\n- [#405](https://github.com/darknessomi/musicbox/issues/405) 32位Python下cookie时间戳超出了32位整数最大值。尝试使用64位版本的Python或者拷贝cookie文件到对应位置。\n- [#347](https://github.com/darknessomi/musicbox/issues/347) 暂停时间超过一定长度（数分钟）之后mpg123停止输出，导致切换到下一首歌。此问题是mpg123的bug，暂时无解决方案。\n- [#791](https://github.com/darknessomi/musicbox/issues/791) 版权问题，master分支已经修复\n\n## 使用\n\n```bash\n    musicbox\n```\n\nEnjoy it !\n\n## 更新日志\n\n2020-10-23 版本 0.3.0    接口更新，错误修复\n\n2018-11-28 版本 0.2.5.4    修复多处错误\n\n2018-06-21 版本 0.2.5.3    修复多处播放错误\n\n2018-06-07 版本 0.2.5.1    修复配置文件错误\n\n2018-06-05 版本 0.2.5.0    全部迁移到新版api，大量错误修复\n\n[更多>>](https://github.com/darknessomi/musicbox/blob/master/CHANGELOG.md)\n\n## LICENSE\n\n[MIT](LICENSE)\n',
    'author': 'omi',
    'author_email': '4399.omi@gmail.com',
    'maintainer': 'omi',
    'maintainer_email': '4399.omi@gmail.com',
    'url': 'https://github.com/darknessomi/musicbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
