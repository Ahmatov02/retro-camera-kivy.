[app]
title = RetroCameraApp
package.name = retrocamera
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,opencv-python-headless,numpy
orientation = portrait
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.ndk = 25b
android.archs = arm64-v8a
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1
