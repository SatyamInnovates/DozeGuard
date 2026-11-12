pkgname=dozeguard
pkgver=1.0.0
pkgrel=1
pkgdesc='Per-user Linux sleep inhibitor'
arch=('any')
url='https://github.com/SatyamInnovates/DozeGuard'
license=('MIT')
depends=('python' 'python-psutil' 'python-dbus-next')
optdepends=('pyside6: optional system tray frontend')
makedepends=('python-setuptools' 'python-wheel' 'python-build' 'python-installer')
source=("$pkgname::git+https://github.com/SatyamInnovates/DozeGuard.git#commit=94bd28761a2d094453271ce083e8474c8c8a4474")
sha256sums=('SKIP')

build() {
  cd "$srcdir/$pkgname"
  python -m build --wheel --no-isolation
}

package() {
  cd "$srcdir/$pkgname"
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 dozeguard-tray.desktop "$pkgdir/usr/share/applications/dozeguard-tray.desktop"
}
