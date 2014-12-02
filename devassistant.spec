%global shortname da

Name:           devassistant
Version:        0.10.0
Release:        2%{?dist}
Summary:        DevAssistant - Making life easier for developers

License:        GPLv2+ and CC-BY-SA
URL:            https://github.com/bkabrda/devassistant
Source0:        https://pypi.python.org/packages/source/d/%{name}/%{name}-%{version}.tar.gz
# to get desktop and appdata file:
# git clone https://github.com/bkabrda/devassistant.git && cd devassistant
# git checkout v0.10.0
# # devassistant.desktop, appdata/devassistant.appdata.xml
Source1:        %{name}.desktop
Source2:        %{name}.appdata.xml

Patch0:         %{name}-test.patch

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  python3-pytest
BuildRequires:  python3-devel
BuildRequires:  python3-dapp
BuildRequires:  python3-docker-py
BuildRequires:  python3-flexmock
BuildRequires:  python3-jinja2
BuildRequires:  python3-progress
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

BuildRequires:  python3-PyYAML

# it seems that other packages using bash-completion don't depend
# on it and rather just own the directory, so we will do the same
Requires:       git
# needed to create ssh key for GitHub access, not necessarily installed by default everywhere
Requires:       openssh-askpass
Requires:       polkit
Requires:       python3-gobject
Requires:       python3-dapp
Requires:       python3-docker-py
Requires:       python3-jinja2
Requires:       python3-progress
Requires:       python3-PyGithub
Requires:       python3-requests
Requires:       python3-setuptools
Requires:       python3-six
Requires:       python3-PyYAML

%global __requires_exclude ^\(/usr/bin/php\|/usr/bin/perl\|perl\\(\)

%description
DevAssistant can help you with creating and setting up basic projects
in various languages, installing dependencies, setting up environmens,
working with source control, etc.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
# remove bundled egg-info
rm -rf %{name}.egg-info

cp %{SOURCE1} .
sed -i '/Version/d' %{name}.desktop
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

# folder for assistants
mkdir -p %{buildroot}%{_datadir}/%{name}

# manpages
mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 644 manpages/%{shortname}.1 %{buildroot}%{_mandir}/man1
install -p -m 644 manpages/%{shortname}-gui.1 %{buildroot}%{_mandir}/man1
install -p -m 644 manpages/%{name}.1 %{buildroot}%{_mandir}/man1
install -p -m 644 manpages/%{name}-gui.1 %{buildroot}%{_mandir}/man1
# bash completion script
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -p -m 644 %{shortname}.bash %{buildroot}%{_sysconfdir}/bash_completion.d/
# icons
for SIZE in 16x16 22x22 24x24 32x32 48x48 256x256; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/$SIZE/apps
    install -p -m 644 icons/hicolor/$SIZE/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/$SIZE/apps/%{name}.png

    mkdir -p %{buildroot}%{_datadir}/icons/HighContrast/$SIZE/apps
    install -p -m 644 icons/HighContrast/$SIZE/%{name}.png %{buildroot}%{_datadir}/icons/HighContrast/$SIZE/apps/%{name}.png
done

# desktop and appdata
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{name}.desktop
mkdir -p %{buildroot}/%{_datadir}/appdata
cp -a %{SOURCE2} %{buildroot}/%{_datadir}/appdata

# polkit
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
install -p -m 644 polkit/devassistant_auth.policy %{buildroot}%{_datadir}/polkit-1/actions/
mkdir -p %{buildroot}%{_libexecdir}
install -p -m 755 polkit/da_auth %{buildroot}%{_libexecdir}

%check
%{__python3} setup.py test -t py.test-%{python3_version}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons/HighContrast &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /bin/touch --no-create %{_datadir}/icons/HighContrast &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/HighContrast &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc README.rst LICENSE
%{_bindir}/%{shortname}
%{_bindir}/%{shortname}-gui
%{_bindir}/%{name}
%{_bindir}/%{name}-gui
%{_datadir}/%{name}
%{_mandir}/man1/%{shortname}.1.gz
%{_mandir}/man1/%{shortname}-gui.1.gz
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/%{name}-gui.1.gz
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/HighContrast/*/apps/%{name}.png
%{_datadir}/polkit-1/actions/%{name}_auth.policy
%{_libexecdir}/da_auth
%{_sysconfdir}/bash_completion.d/
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py?.?.egg-info

%changelog
* Tue Dec 02 2014 Tomas Radej <tradej@redhat.com> - 0.10.0-2
- Converted to a Python 3-only package

* Tue Nov 18 2014 Tomas Radej <tradej@redhat.com> - 0.10.0-1
- Version 0.10.0

