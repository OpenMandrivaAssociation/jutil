%define section         free
%define gcj_support     1

Name:           jutil
Version:        1.4
Release:        2
Epoch:          0
Summary:        Parameterized collections library for Java
License:        GPL
Group:          Development/Java
URL:            http://cscott.net/Projects/JUtil
Source0:        http://cscott.net/Projects/JUtil/jutil-latest/%{name}-%{version}.tar.gz
BuildRequires:  ant
BuildRequires:  java-rpmbuild >= 0:1.6
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif

%description
JUtil is a fully-parameterized (generic) collections library for
Java. It was originally part of the FLEX project.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__perl} -pi -e 's|<javac|<javac source="1.5" nowarn="true"|g' build*.xml
%{_bindir}/find . -type f -name '*.jar' | xargs -t %{__rm}

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} jar javadoc

%install
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr api/*  %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

#%{__perl} -pi -e 's/\r$//g' 

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.3-1.1.5mdv2011.0
+ Revision: 619872
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0:1.3-1.1.4mdv2010.0
+ Revision: 429653
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0:1.3-1.1.3mdv2009.0
+ Revision: 140829
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.3-1.1.3mdv2008.1
+ Revision: 120958
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.3-1.1.2mdv2008.0
+ Revision: 87454
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Jul 08 2007 David Walluck <walluck@mandriva.org> 0:1.3-1.1.1mdv2008.0
+ Revision: 49710
- Import jutil



* Sat Jul 07 2007 David Walluck <walluck@mandriva.org> 0:1.3-1.1.1mdv2008.0
- release

* Wed Mar 14 2007 David Walluck <walluck@mandriva.org> 0:1.3-1mdv2007.0
- 1.3

* Wed Mar 14 2007 David Walluck <walluck@mandriva.org> 0:1.1-2mdv2007.0
- enable gcj support
- use javadoc macro
- fix javadoc

* Mon Sep 18 2006 David Walluck <walluck@mandriva.org> 0:1.1-1mdv2007.0
- release

