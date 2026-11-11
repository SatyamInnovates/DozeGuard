Name:           dozeguard
Version:        0.1.0
Release:        1%{?dist}
Summary:        Per-user Linux sleep inhibitor
License:        MIT
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-psutil
Requires:       python3-dbus-next
Suggests:       python3-pyside6
Source0:        https://github.com/SatyamInnovates/DozeGuard/archive/refs/tags/v%{version}.tar.gz
Source1:        dozeguard-tray.desktop

%description
DozeGuard temporarily inhibits system sleep while a user session is active.
Sleep inhibition currently requires systemd-logind.

%prep
%autosetup -n DozeGuard-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files backends core main daemon controller paths tray
install -Dpm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/dozeguard-tray.desktop

%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_datadir}/applications/dozeguard-tray.desktop
