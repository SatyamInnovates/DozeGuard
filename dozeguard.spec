Name:           dozeguard
Version:        1.0.0
Release:        1%{?dist}
%{!?sourcecommit:%global sourcecommit 94bd28761a2d094453271ce083e8474c8c8a4474}
Summary:        Per-user Linux sleep inhibitor
License:        MIT
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-psutil
Requires:       python3-dbus-next
Source0:        https://github.com/SatyamInnovates/DozeGuard/archive/%{sourcecommit}.tar.gz
Source1:        dozeguard-tray.desktop
Source2:        dozeguard-tray-autostart.desktop

%package tray
Summary:        Optional desktop tray and window for DozeGuard
Requires:       %{name} = %{version}-%{release}
Requires:       python3-pyside6

%description tray
DozeGuard tray controls sessions and displays their current status. This
package also enables background login startup by default.

%description
DozeGuard temporarily inhibits system sleep while a user session is active.
Sleep inhibition currently requires systemd-logind.

%prep
%autosetup -n DozeGuard-%{sourcecommit}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files backends core main daemon controller paths tray desktop_integration
install -Dpm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/dozeguard-tray.desktop
install -Dpm0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/xdg/autostart/dozeguard-tray.desktop

%files -f %{pyproject_files}
%{_bindir}/dozeguard
%exclude %{_bindir}/dozeguard-tray
%exclude %{python3_sitelib}/__pycache__
%exclude %{python3_sitelib}/*/__pycache__
%exclude %{python3_sitelib}/__pycache__/*
%exclude %{python3_sitelib}/*/__pycache__/*
%license LICENSE
%doc README.md

%files tray
%{_bindir}/dozeguard-tray
%{_datadir}/applications/dozeguard-tray.desktop
%{_sysconfdir}/xdg/autostart/dozeguard-tray.desktop

%changelog
* Thu Nov 12 2026 DozeGuard contributors <noreply@example.invalid> - 1.0.0-1
- Initial packaged release
