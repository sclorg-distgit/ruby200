%global scl_name_base ruby
%global scl_name_version 200

%global scl %{scl_name_base}%{scl_name_version}
%scl_package %scl

# Do not produce empty debuginfo package.
%global debug_package %{nil}

%global install_scl 1

Summary: Package that installs %scl
Name: %scl_name
Version: 1.1
Release: 7%{?dist}
License: GPLv2+
Source0: README
Source1: LICENSE
%if 0%{?install_scl}
Requires: %{scl_prefix}ruby
%endif
BuildRequires: help2man
BuildRequires: scl-utils-build

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package scldevel
Summary: Package shipping development files for %scl

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.

%prep
%setup -T -c

# Expand macros used in README file.
cat > README << EOF
%{expand:%(cat %{SOURCE0})}
EOF

cp %{SOURCE1} .

%build
# Generate a helper script that will be used by help2man.
cat > h2m_help << 'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_help

# Generate the man page from include.h2m and ./h2m_help --help output.
help2man -N --section 7 ./h2m_help -o %{scl_name}.7

%install
%scl_install

cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\$MANPATH
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
EOF

cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

# Install generated man page.
mkdir -p %{buildroot}%{_mandir}/man7/
install -p -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/

# Create directory for pkgconfig files, originally provided by pkgconfig
# package, but not for SCL.
mkdir -p %{buildroot}%{_libdir}/pkgconfig

%files

%files runtime
%doc README LICENSE
%scl_files
# Own the manual directories (rhbz#1073458, rhbz#1072319).
%dir %{_mandir}/man1
%dir %{_mandir}/man7
%dir %{_libdir}/pkgconfig
%{_mandir}/man7/%{scl_name}.*

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog
* Mon Mar 31 2014 Honza Horak <hhorak@redhat.com> - 1.1-7
- Fix path typo in README
  Related: #1061460

* Tue Mar 25 2014 Vít Ondruch <vondruch@redhat.com> - 1.1-6
- Own manual directories.
- Own pkgconfig directory.
  Resolves: rhbz#1073458

* Wed Feb 26 2014 Josef Stribny <jstribny@redhat.com> - 1.1-5
- Properly expand empty $PATH
  Resolves: rhbz#1069302

* Wed Feb 12 2014 Honza Horak <hhorak@redhat.com> - 1.1-4
- Fix grammar mistakes in README
  Related: #1061460

* Tue Feb 11 2014 Vít Ondruch <vondruch@redhat.com> - 1.1-3
- Do not produce empty debuginfo package.
  Related: rhbz#1061460

* Mon Feb 10 2014 Vít Ondruch <vondruch@redhat.com> - 1.1-2
- Install ruby when installing ruby200 metapackage.
  Related: rhbz#1039934

* Thu Feb 06 2014 Vít Ondruch <vondruch@redhat.com> - 1.1-1
- Bump version.
- Drop rails dependencies.
  Resolves: rhbz#1056022
- Add -build package dependency on scl-utils-build.
  Resolves: rhbz#1058616
- Add LICENSE, README and man page.
  Resolves: rhbz#1061460

* Tue Jan 21 2014 Vít Ondruch <vondruch@redhat.com> - 1-6
- Add -scldevel sub-package.
  Resolves: rhbz#1055548

* Wed Dec 11 2013 Josef Stribny <jstribny@redhat.com> - 1-4
- Allow sdoc since it's built already
  - Resolves: rhbz#1039934

* Wed Oct 30 2013 Josef Stribny <jstribny@redhat.com> - 1-3
- Add bcrypt-ruby, uglifier and jbuilder.

* Wed Oct 30 2013 Josef Stribny <jstribny@redhat.com> - 1-2
- Add packages that should install in this scl.

* Mon Apr 29 2013 Josef Stribny <jstribny@redhat.com> - 1-1
- Initial package.
