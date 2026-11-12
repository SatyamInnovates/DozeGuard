pkgbase=dozeguard
pkgname=('dozeguard' 'dozeguard-tray')
pkgver=1.0.0
pkgrel=1
arch=('any')
url='https://github.com/SatyamInnovates/DozeGuard'
license=('MIT')
pkgdesc='Per-user Linux sleep inhibitor (CLI and daemon)'
depends=('python' 'python-psutil' 'python-dbus-next')
makedepends=('python-setuptools' 'python-wheel' 'python-build' 'python-installer')
source=("$pkgbase::git+https://github.com/SatyamInnovates/DozeGuard.git#commit=94bd28761a2d094453271ce083e8474c8c8a4474")
sha256sums=('SKIP')

build() {
  cd "$srcdir/$pkgbase"
  python -m build --wheel --no-isolation
}

package_dozeguard() {
  cd "$srcdir/$pkgbase"
  python -m installer --destdir="$pkgdir" dist/*.whl
  rm "$pkgdir/usr/bin/dozeguard-tray"
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

package_dozeguard-tray() {
  pkgdesc='Optional desktop tray and login autostart for DozeGuard'
  depends=('dozeguard' 'pyside6')
  cd "$srcdir/$pkgbase"
  local tray_stage="$srcdir/tray-stage"
  rm -rf "$tray_stage"
  python -m installer --destdir="$tray_stage" dist/*.whl
  install -Dm755 "$tray_stage/usr/bin/dozeguard-tray" "$pkgdir/usr/bin/dozeguard-tray"
  install -Dm644 dozeguard-tray.desktop "$pkgdir/usr/share/applications/dozeguard-tray.desktop"
  install -Dm644 dozeguard-tray-autostart.desktop "$pkgdir/etc/xdg/autostart/dozeguard-tray.desktop"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/dozeguard-tray/LICENSE"
}
