%global shortname da

Name:           devassistant
Version:        0.10.0
Release:        1%{?dist}
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

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  pytest
BuildRequires:  python2-devel
BuildRequires:  python-flexmock
BuildRequires:  python-jinja2
BuildRequires:  python-progress
BuildRequires:  python-requests
BuildRequires:  python-setuptools
BuildRequires:  python-six

BuildRequires:  PyYAML

# it seems that other packages using bash-completion don't depend
# on it and rather just own the directory, so we will do the same
Requires:       git
# needed to create ssh key for GitHub access, not necessarily installed by default everywhere
Requires:       openssh-askpass
Requires:       polkit
Requires:       pygobject3
Requires:       python-jinja2
Requires:       python-progress
Requires:       python-PyGithub
Requires:       python-requests
Requires:       python-setuptools
Requires:       python-six
Requires:       PyYAML

%global __requires_exclude ^\(/usr/bin/php\|/usr/bin/perl\|perl\\(\)

%description
DevAssistant can help you with creating and setting up basic projects
in various languages, installing dependencies, setting up environmens,
working with source control, etc.

%prep
%setup -q -n %{name}-%{version}
# remove bundled egg-info
rm -rf %{name}.egg-info

cp %{SOURCE1} .
sed -i '/Version/d' %{name}.desktop

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

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
%{__python} setup.py test -t py.test

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
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info

%changelog
* Tue Nov 18 2014 Tomas Radej <tradej@redhat.com> - 0.10.0
- Version 0.10.0

