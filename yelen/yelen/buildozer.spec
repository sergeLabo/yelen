[app]

title = Yelen

package.name = yelen
package.domain = org.test

source.dir = .

source.include_exts = py,png,jpg,kv,atlas

source.include_patterns = images/*.jpg,images/*.png

version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

requirements = python3,kivy,lxml,beautifulsoup4,certifi,openssl

orientation = all

fullscreen = 0

android.permissions = INTERNET

android.arch = armeabi-v7a

[buildozer]

log_level = 2

warn_on_root = 1
