\def\fileversion{0.28}
\def\filedate{2023/04/04}

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\typeout{^^J  ***  LaTeX class for IACR Communications in Cryptology v\fileversion\space ***^^J}
\ProvidesClass{iacrcc}[\filedate]

% IACR Communications in Cryptology DOCUMENT CLASS
% Authoritative source is github.com/IACR/latex/iacrcc
%
% To the extent possible under law, the author(s) have dedicated all
% copyright and related and neighboring rights to this software to the
% public domain worldwide. This software is distributed without any
% warranty.
%
% You should have received a copy of the CC0 Public Domain Dedication
% along with this software. If not, see
% <http://creativecommons.org/publicdomain/zero/1.0/>.
%
% Common definitions

% expl3: wrapper package for experimental LaTeX3
\RequirePackage{expl3} % used for text_purify on metadata.

% xkeyval: extension of the keyval package
%          This offers additional macros for setting keys and 
%          declaring and setting class or package options.
\RequirePackage{xkeyval}

\def\publname{IACR Communications in Cryptology}
\def\IACR@vol{0}
\def\IACR@no{0}
\def\IACR@fp{1}
\def\IACR@ISSN{XXXX-XXXX}
\def\IACR@DOI{XXXXXXXX}
\def\IACR@Received{20XX-XX-XX}
\def\IACR@Revised{20XX-XX-XX}
\def\IACR@Accepted{20XX-XX-XX}
\def\IACR@Published{20XX-XX-XX}
\newif\if@IACR@Received \@IACR@Receivedfalse
\newif\if@IACR@Revised \@IACR@Revisedfalse
\newif\if@IACR@Accepted \@IACR@Acceptedfalse
\newif\if@IACR@Published \@IACR@Publishedfalse

% etoolbox: is a toolbox of programming facilities geared primarily
%           towards LaTeX class and package authors.
\RequirePackage{etoolbox}

\newcommand{\setvolume}[1]{\def\IACR@vol{#1}}
\newcommand{\setnumber}[1]{\def\IACR@no{#1}}
\newcommand{\setISSN}[1]{\def\IACR@ISSN{#1}}
% See https://www.latex-project.org/news/latex2e-news/ltnews34.pdf
\tracinglostchars=3

% Options
% only required for old hyperxmp.
\newif\if@hyperxmp@doi
\@hyperxmp@doifalse
% doclicense added support for the macro \doclicenseLongTextForHyperref in version 3.1.0 (2022/04/27)
\newif\if@doclicense@LongTextForHyperref
\@doclicense@LongTextForHyperreffalse
% The jobname.iacrmetadata file will contain accepted \IACR@Received,  \IACR@Accepted,
% \IACR@Published, and \IACR@DOI.
\InputIfFileExists{\jobname.iacrmetadata}{
  \@IACR@Receivedtrue\@IACR@Acceptedtrue\@IACR@Publishedtrue\@hyperxmp@doitrue\typeout{Inserted DOI into PDF}%
}{}
\newif\if@optbiblatex
\@optbiblatexfalse
\define@key{IACR}{biblatex}[]{\@optbiblatextrue}
\newif\if@floatrow
\@floatrowfalse
\define@key{IACR}{floatrow}[]{\@floatrowtrue}
% version=submission will set anonymous to true, but it can be
% overridden with the notanonymous option for the class.
\newif\if@anonymous
\@anonymousfalse
% This maybe be used to override \@anonymous
\newif\if@notanonymous
\@notanonymousfalse
\define@key{IACR}{notanonymous}[]{\@notanonymoustrue}
\newcommand{\@IACRversion}{preprint}
\define@choicekey{IACR}{version}[\@IACRversion]{preprint,submission,final}[preprint]{}
\DeclareOptionX*{}
\ProcessOptionsX<IACR>\relax
\typeout{Compiling version=\@IACRversion}
\ifcsstring{@IACRversion}{submission}{
  \if@notanonymous\@anonymousfalse
  \typeout{Disabling anonymity}
  \else
  \@anonymoustrue
  \typeout{Setting to anonymous}
  \fi
}{}
\ifcsstring{@IACRversion}{final}{
  % This disabled boxes for overfull hboxes.
  \PassOptionsToClass{final}{article}
}{}

% xstring: provides macros for manipulating strings - testing a string’s 
%          contents, extracting substrings, substitution of substrings and
%          providing numbers such as string length, position of, or number
%          of recurrences of, a substring.
\RequirePackage{xstring} % Required for IfSubStr

% Options containing an equality sign are deleted from the original list by
% the xkeyval package from the \@classoptionslist macro.
% Remove allowed options and check if this macro is empty.
\ifx\@classoptionslist\@empty\else
  \edef\store@classoptionslist{\@classoptionslist}%
  \StrDel{\store@classoptionslist}{floatrow}[\store@classoptionslist]%
  \StrDel{\store@classoptionslist}{biblatex}[\store@classoptionslist]%
  \StrDel{\store@classoptionslist}{notanonymous}[\store@classoptionslist]%
  \StrDel{\store@classoptionslist}{,}[\store@classoptionslist]%
  \StrDel{\store@classoptionslist}{ }[\store@classoptionslist]%
  \ifx\store@classoptionslist\@empty\else
    \ClassError{iacrcc}{Invalid options passed to iacrcc: \store@classoptionslist}{}%
  \fi
\fi

% article class
\LoadClass[10pt,twoside]{article}[2007/10/19]

% iftex: am I running under pdfTEX, XETEX or LuaTEX?
\RequirePackage{iftex}

\ifluatex
  % lualatex-math: fixes for mathematics-related LuaLATEX issues
  \RequirePackage{lualatex-math}
  % Check for existence of luatex85.sty and load it if available.
  % This should ensure that it work also with newer versions of luatex.
  % luatex85: The package provides emulation of pdfTEX primitives for LuaTEX v0.85+.
  \IfFileExists{luatex85.sty}{\RequirePackage{luatex85}}{}
\fi

% xcolor: starts from the basic facilities of the color package, 
%         and provides easy driver-independent access to several kinds 
%         of color tints, shades, tones, and mixes of arbitrary colors. I
\RequirePackage{xcolor}

% The hyperref package is used to handle cross-referencing commands in 
% LaTeX to produce hypertext links in the document. 
% Hyperref must be loaded last, but before other AtEndPreamble hooks  
\AtEndPreamble{
  \@ifpackageloaded{hyperref}{}{\RequirePackage{hyperref}}
  \hypersetup{pdflang=en}
  \hypersetup{urlcolor=blue}
  \hypersetup{colorlinks=true,
    citecolor=black!70!green,
    linkcolor=black!70!red}
  % Disable latexdiff commands in PDF links
  \pdfstringdefDisableCommands{%
    \def\DIFadd#1{#1}%
    \def\DIFdel#1{}%
  }
  % Old versions of hyperxmp do not support DOI TODO: move to require newer version.
  \@ifpackagelater{hyperxmp}{2019/03/14}{\@hyperxmp@doitrue}{}
  % doclicense added support for the macro \doclicenseLongTextForHyperref in version 3.1.0 (2022/04/27)
  \@ifpackagelater{doclicense}{2022/04/25}{\@doclicense@LongTextForHyperreftrue}{}
  \@ifpackageloaded{biblatex}{}{\bibliographystyle{iacrcc}}
  % When pdflatex is used load T1 fonts using fontenc
  \ifpdftex
    % Prefer unicode encoding over T1 encoding. 
    % There are only a few glyphs that require falling back to T1, 
    % since most of our fonts should now be unicode-encoded (e.g., latin modern).
    \RequirePackage[TU,T1]{fontenc} 
  \fi
}

% XMP (eXtensible Metadata Platform) is a mechanism proposed by Adobe 
% for embedding document metadata within the document itself.
\RequirePackage{hyperxmp} % hyperxmp 5.x has issues with AtEndPreamble
\setcounter{tocdepth}{2}

% Geometry: flexible and complete interface to document dimensions
\RequirePackage[a4paper,hscale=0.65,vscale=0.75,marginratio=1:1,marginparwidth=2.7cm]{geometry}

% afterpage: execute command after the next page break
\RequirePackage{afterpage}

% secsty: control sectional headers
\RequirePackage{sectsty}
\allsectionsfont{\sffamily\boldmath}
\renewcommand*\descriptionlabel[1]{\hspace\labelsep
                                   \normalfont\bfseries\sffamily\boldmath #1}

% Make some counters robust that are made fragile by `calc` needed for orcidlink
\robustify\setcounter
\robustify\addtocounter
\robustify\setlength
\robustify\addtolength

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This provides a command to insert the ORCiD logo, which is hyperlinked to 
% the URL of the researcher whose iD was specified.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This copies over definition of the orcidlink from the orcidlink style file
% by by Leo C. Stein which in turn is a package around Milo's code on TeX.SE,
% see https://tex.stackexchange.com/a/445583/34063

% tikz: create PostScript and PDF graphics in TEX
\RequirePackage{tikz}
\ProcessOptions\relax
\usetikzlibrary{svg.path}

\definecolor{orcidlogocol}{HTML}{A6CE39}
\tikzset{%
  orcidlogo/.pic={%
    \fill[orcidlogocol] svg{M256,128c0,70.7-57.3,128-128,128C57.3,256,0,198.7,0,128C0,57.3,57.3,0,128,0C198.7,0,256,57.3,256,128z};
    \fill[white] svg{M86.3,186.2H70.9V79.1h15.4v48.4V186.2z}
                 svg{M108.9,79.1h41.6c39.6,0,57,28.3,57,53.6c0,27.5-21.5,53.6-56.8,53.6h-41.8V79.1z M124.3,172.4h24.5c34.9,0,42.9-26.5,42.9-39.7c0-21.5-13.7-39.7-43.7-39.7h-23.7V172.4z}
                 svg{M88.7,56.8c0,5.5-4.5,10.1-10.1,10.1c-5.6,0-10.1-4.6-10.1-10.1c0-5.6,4.5-10.1,10.1-10.1C84.2,46.7,88.7,51.3,88.7,56.8z};
  }%
}

% Reciprocal of the height of the svg whose source is above.  The
% original generates a 256pt high graphic; this macro holds 1/256.
\newcommand{\@OrigHeightRecip}{0.00390625}

% We will compute the current X height to make the logo the right height
\newlength{\@curXheight}

\DeclareRobustCommand\orcidlink[1]{%
  \texorpdfstring{%
    \setlength{\@curXheight}{\fontcharht\font`X}%
    \href{https://orcid.org/#1}{\XeTeXLinkBox{\mbox{%
    \begin{tikzpicture}[yscale=-\@OrigHeightRecip*\@curXheight,%
      xscale=\@OrigHeightRecip*\@curXheight,transform shape]%
      \pic{orcidlogo};
    \end{tikzpicture}%
}}}}{}}

% End of macros for orcidlink
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% pgfkeys: a flexible key management system
\RequirePackage{pgfkeys}

\pgfkeys{/IACR-author/entities/.cd,
  inst/.initial=\@empty,
  orcid/.initial=\@empty,
  footnote/.initial=\@empty,
  onclick/.initial=\@empty,
  email/.initial=\@empty,
  surname/.initial=\@empty,
}
\def\IACR@author@params@set@keys#1{%
  \pgfkeys{/IACR-author/entities/.cd,#1}}

\def\IACR@author@params@get#1{%
  \pgfkeysvalueof{/IACR-author/entities/#1}}

\newcommand\IACR@author@params@clearkeys{%
  \IACR@author@params@set@keys{inst=\@empty,orcid=\@empty,footnote=\@empty,onclick=\@empty,email=\@empty,surname=\@empty}%
}

\pgfkeys{/IACR-affiliation/entities/.cd,
  ror/.initial=\@empty,
  onclick/.initial=\@empty,
  department/.initial=\@empty,
  street/.initial=\@empty,
  city/.initial=\@empty,
  state/.initial=\@empty,
  postcode/.initial=\@empty,
  country/.initial=\@empty,
}
\def\IACR@affiliation@params@set@keys#1{%
  \pgfkeys{/IACR-affiliation/entities/.cd,#1}}

\def\IACR@affiliation@params@get#1{%%
  \pgfkeysvalueof{/IACR-affiliation/entities/#1}}

\newcommand\IACR@affiliation@params@clearkeys{%
 \IACR@affiliation@params@set@keys{ror=\@empty,onclick=\@empty,department=\@empty,street=\@empty,city=\@empty,state=\@empty,postcode=\@empty,country=\@empty}%
}

\pgfkeys{/IACR-title/entities/.cd,
  running/.initial=\@empty,
  onclick/.initial=\@empty,
  subtitle/.initial=\@empty,
  plaintext/.initial={},
}
\def\IACR@title@params@set@keys#1{%
  \pgfkeys{/IACR-title/entities/.cd,#1}}

\def\IACR@title@params@get#1{%
  \pgfkeysvalueof{/IACR-title/entities/#1}}

\pgfkeys{/IACR-funding/entities/.cd,
  country/.initial=\@empty,
  grantid/.initial=\@empty,
  fundref/.initial=\@empty,
  ror/.initial=\@empty,
}
\def\IACR@funding@params@set@keys#1{%
  \pgfkeys{/IACR-funding/entities/.cd,#1}}
\def\IACR@funding@params@get#1{%
  \pgfkeysvalueof{/IACR-funding/entities/#1}}
\newcommand\IACR@funding@params@clearkeys{%
  \IACR@funding@params@set@keys{country=\@empty,grantid=\@empty,fundref=\@empty,ror=\@empty}%
}

% Title/Author/affiliations
% Running author list for in the header
\global\let\IACR@runningauthors\@empty

% Full author list for the metadata in the pdf
\global\let\IACR@listofauthors\@empty

\global\let\@author\@empty
\global\let\@affiliation\@empty

% Bool to check if the user called the \authorrunning macro
\gdef\IACR@userdefinedrunningauthors{\@empty}%
\newcommand{\authorrunning}[1]{%
  \gdef\IACR@userdefinedrunningauthors{userdefined}%
  \gdef\IACR@runningauthors{#1}%
}

% Count the number of authors
\newcounter{IACR@author@cnt}

% Count the number of institutions
\newcounter{IACR@inst@cnt}

% Count the number of provided e-mail addresses
\newcounter{IACR@email@cnt}

% Meta information is written out in [jobname].meta
\newwrite\iacrmeta
\immediate\openout\iacrmeta=\jobname.meta

\AtEndDocument{%
  \immediate\closeout\iacrmeta%
  % Check if either \title, \addauthor or \affiliation macros were redefined
  % Also check if the font (\familydefault) or the margings (\paperwidth) were modified.
  % Throw an error if so, these are needed for meta-data collection
  \ifx\store@addauthor\addauthor\else
    \ClassError{iacrcc}{The \string\addauthor\space macro seems to be redefined}{}%
  \fi
  \ifx\store@title\title\else
    \ClassError{iacrcc}{The \string\title\space macro seems to be redefined}{}%
  \fi
  \ifx\store@affiliation\affiliation\else
    \ClassError{iacrcc}{The \string\affiliation\space macro seems to be redefined}{}%
  \fi
  \ifx\store@font\familydefault\else
    \ClassError{iacrcc}{The \string\familydefault\space macro seems to be redefined}{}%
  \fi
  \ifx\store@paperwidth\paperwidth\else
    \ClassError{iacrcc}{The \string\paperwidth\space macro seems to be redefined}{}%
  \fi
  % final version requires abstract.
  \ifcsstring{@IACRversion}{final}{%
    \IfFileExists{\jobname.abstract}{}{%
      \ClassError{iacrcc}{An abstract with abstract environment is required}{}%
    }%
  }{}%
}

\let\storeprotect\protect

% xpatch: Extending etoolbox patching commands
\RequirePackage{xpatch}

% create an immediate version of \protected@write
\let\protected@iwrite\protected@write
\xpatchcmd{\protected@iwrite}{\write}{\immediate\write}{}{}

\newcommand\@writemeta[1]{\protected@iwrite\iacrmeta{}{#1}}%

% alphalph: Convert numbers to letters, 
%           used for footnotes in addauthor
\RequirePackage{alphalph}

 \AtBeginDocument{%
  % Use this \maketitle command to first write out 
  % the necessary meta-information 
  \renewcommand\maketitle{\par
    \@writemeta{version: \@IACRversion}%
    \@writemeta{title: \@plaintitle}%
    \if\IACR@title@subtitle\@empty\else
      \@writemeta{\IACRSS subtitle: \IACR@title@subtitle}%
    \fi
    % Generic footnote and e-mails are displayed without markers
    \ifx\@genericfootnote\@empty\else
      \begingroup
        \renewcommand\thefootnote{}\footnotetext{\@genericfootnote}%
      \endgroup
    \fi
    \ifx\IACR@displayemails\@empty\else
      \begingroup
        \renewcommand\thefootnote{}\footnotetext{\IACR@displayemails}%
      \endgroup
    \fi
    \ifcsstring{@IACRversion}{final}{%
      % When we produce the final version we need at least one e-mail address  
      \ifnum\theIACR@email@cnt<1\relax
        \ClassError{iacrcc}{Provide at least one e-mail address for the final version}{}%
      \fi
    }{}%
    \begingroup
      \global\@topnum\z@   % Prevents figures from going at top of page.
      % Ensure we use alphabetical numbering for the author footnotes 
      \renewcommand*{\thefootnote}{\alphalph{\value{footnote}}}%
      \@maketitle
      \thispagestyle{title}\@thanks
    \endgroup
    \setcounter{footnote}{0}%
    \global\let\thanks\relax
    \global\let\maketitle\relax
    \global\let\@maketitle\relax
    \global\let\@thanks\@empty
    \global\let\@date\@empty
    \global\let\date\relax
    \global\let\and\relax
    % Adjust header size for title page
    \addtolength{\headheight}{\baselineskip}%
    \addtolength{\headsep}{-\baselineskip}%
    \afterpage{%
      \global\advance\headheight by -\baselineskip%
      \global\advance\headsep by \baselineskip%
    }%
  }%
}

% Add support to display the provided e-mail addresses 
% in the footnote of the front page
\global\let\IACR@displayemails\@empty

% Add support for a footnote without symbol on the front page
\global\let\@genericfootnote\@empty
\newcommand\genericfootnote[1]{%
  \gdef\@genericfootnote{#1}%
}

\def\@maketitle{%
  \newpage
  \null
  \vskip 2em%
  \begin{center}%
    % Insert the title and subtitle (if defined)
    {\def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
      {\LARGE \bfseries\sffamily\boldmath \@title\par}%
      \ifdefined\IACR@title@subtitle@defined\vskip .5em{\large\sffamily\bfseries\IACR@title@subtitle\par}\fi
    }%
    \vskip 1.5em%
    {\large
      \lineskip .5em%
        \if@anonymous
          Anonymous Submission
        \else
          \setcounter{footnote}{0}%
          \newcounter{IACR@cnt}
          \setcounter{IACR@cnt}{1}%
          % Make sure authors are separated by a comma except the last one where we use " and "
          \def\and{%
            \stepcounter{IACR@cnt}%
            \ifnum\theIACR@cnt=\theIACR@author@cnt\unskip\space and \ignorespaces\else\unskip, \ignorespaces\fi%
          }%
          % Display the list of authors
          % Note that affiliations and footnotes are picked up within 
          % the definition of \@author
          \@author%
          \vskip 1em\par
          \small
          \setcounter{IACR@cnt}{1}%        
          % When there is only one author with one or more affiliations
          % do not display the affiliation counter
          % Redefine \and to make sure we print the affiliation numbers
          \def\and{\par\ifnum\theIACR@author@cnt=1\relax\else\stepcounter{IACR@cnt}$^{\theIACR@cnt}$~\fi}
          % The above redefinition does not work for the first institute: fix that here
          \ifnum\theIACR@author@cnt=1\relax\else
            \ifnum\theIACR@inst@cnt>1$^1$~\fi\ignorespaces%
          \fi
          \@affiliation
        \fi%!anonymous
      }%
  \end{center}%
  \par
  \vskip 1.5em%
}

% This is for indentation in meta file.
\newcommand{\IACRSS}{\space\space}

% We do not support \author, use \addauthor instead
\renewcommand\author[2][]{%
  \ClassError{iacrcc}{Do not use the \string\author\space macro: use the \string\addauthor\space macro instead}{}%
}

\newcommand\addauthor[2][]{%
  \MathAllowedInCheckStringfalse
  \checkstring{#2}{author names should not contain macros or math}%
  % Some additional checks on the if addauthor is used correctly
  % Check if the name contains an ","
  \noexpandarg\IfSubStr{\detokenize{#2}}{,}{%
    \ClassError{iacrcc}{Do not put several authors in the same \string\addauthor\space macro}{}%
  }{}%
  % Affiliations should be defined *after* addauthor
  \ifnum\theIACR@inst@cnt>0\relax
    \ClassError{iacrcc}{Affiliations must follow authors}%
  \fi
  % Do not use " and " in your author name: this might indicate incorrect usage
  \noexpandarg\IfSubStr{#2}{ and }{%
    \ClassError{iacrcc}{Do not put several authors in the same \string\addauthor\space macro}{}%
  }{}%
  % No newline is allowed in addauthor
  \noexpandarg\IfSubStr{#2}{\\}{%
    \ClassError{iacrcc}{Do not put a newline in the \string\addauthor\space macro}{}%
  }{}% 
  %
  \stepcounter{IACR@author@cnt}%
  %
  % Write out the author in the meta file.
  \@writemeta{author:}%
  \IACR@author@params@set@keys{#1}%
  \pgfkeysgetvalue{/IACR-author/entities/footnote}{\IACRfootnote}%
  \expandafter\let\csname IACR@author@footnote\alphalph{\theIACR@author@cnt} \endcsname\IACRfootnote% Copy the pgf key
  \pgfkeysgetvalue{/IACR-author/entities/surname}{\IACR@surname}%
  \@writemeta{\IACRSS name: #2}%
  \if\relax\IACR@surname\relax\else
    % If a surname is provided does some basic sanity checking on the string
    \MathAllowedInCheckStringfalse
    \expandafter\checkstring\expandafter{\IACR@surname}{surname should not contain macros or math}%
    \@writemeta{\IACRSS surname: \IACR@surname}%
  \fi
  \@writemeta{\IACRSS affil: \IACR@author@params@get{inst}}%
  \edef\@IACRorcid{\IACR@author@params@get{orcid}}%
  \edef\@IACRonclick{\IACR@author@params@get{onclick}}%
  \edef\@IACRinst{\IACR@author@params@get{inst}}%
  \edef\@IACRemail{\IACR@author@params@get{email}}%
  % Create the unlabeled footnote consisting of:
  % First the provided footnote (if any) and next
  % the provided e-mail addresses
  \ifx\@IACRemail\@empty\else
    \ifx\IACR@displayemails\@empty
      \edef\IACR@displayemails{E-mail: \noexpand\url{\@IACRemail}~(\unexpanded{\mbox{#2}})}%
    \else
      \eappto\IACR@displayemails{, \noexpand\url{\@IACRemail}~(\unexpanded{\mbox{#2}})}%
    \fi
    \@writemeta{\IACRSS email: \@IACRemail}%
    \stepcounter{IACR@email@cnt}%
  \fi
  % Author name + optionally clickable
  \ifx\@author\@empty
    \ifx\@IACRonclick\@empty
      \def\@author{\unexpanded{\mbox{#2}}}%
    \else
      \edef\@author{\noexpand\href{\@IACRonclick}{\noexpand\color{black}{\unexpanded{\mbox{#2}}}}}%
    \fi
    \if\relax\IACR@userdefinedrunningauthors\relax
      \def\IACR@runningauthors{#2}%
    \fi
    \def\IACR@listofauthors{#2}%    
  \else
    \ifx\@IACRonclick\@empty
      \appto\@author{\and\unexpanded{\mbox{#2}}}%
    \else
      \eappto\@author{\noexpand\and\noexpand\href{\@IACRonclick}{\noexpand\color{black}{\unexpanded{\mbox{#2}}}}}%
    \fi
    \if\relax\IACR@userdefinedrunningauthors\relax
      \appto\IACR@runningauthors{,\space\unexpanded{#2}}%
    \fi
    \appto\IACR@listofauthors{,\space\unexpanded{#2}}%
  \fi
  % Add the footnote text if present
  % Define two seperate macros for the institute
  % \inst and \instwcomma where the latter inserts a comma
  % between the footnote and the institure marker
  \if\relax\IACRfootnote\relax
    \ifx\@IACRinst\@empty\else
      \eappto\@author{\noexpand\inst{\@IACRinst}}%
    \fi
  \else
    \eappto\@author{\noexpand\footnote{\expandafter\noexpand\csname IACR@author@footnote\alphalph{\theIACR@author@cnt} \endcsname}}%
    \ifx\@IACRinst\@empty\else
      \eappto\@author{\noexpand\instwcomma{\@IACRinst}}%
    \fi
  \fi
  \ifx\@IACRorcid\@empty\else
    \eappto\@author{~\noexpand\orcidlink{\@IACRorcid}}%
    \@writemeta{\IACRSS orcid: \@IACRorcid}%
  \fi
  \IACR@author@params@clearkeys%
}

\let\store@addauthor\addauthor% Save macro away

% Define the \addfunding macro to capture funding meta-data
\newcommand{\addfunding}[2][\@empty]{%
  \IACR@funding@params@set@keys{#1}%
  \edef\@IACR@funding@name{\unexpanded{#2}}%
  \edef\@IACR@funding@country{\IACR@funding@params@get{country}}%
  \edef\@IACR@funding@grantid{\IACR@funding@params@get{grantid}}%
  \edef\@IACR@funding@fundref{\IACR@funding@params@get{fundref}}%
  \edef\@IACR@funding@ror{\IACR@funding@params@get{ror}}%
  \@writemeta{funding:}%
  \@writemeta{\IACRSS name: \@IACR@funding@name}%
  \ifx\@IACR@funding@country\@empty\else
    \@writemeta{\IACRSS country: \@IACR@funding@country}%
  \fi
  \ifx\@IACR@funding@grantid\@empty\else
    \@writemeta{\IACRSS grantid: \@IACR@funding@grantid}%
  \fi
  \ifx\@IACR@funding@fundref\@empty\else
    \@writemeta{\IACRSS fundref: \@IACR@funding@fundref}%
  \fi  
  \ifx\@IACR@funding@ror\@empty\else
    \@writemeta{\IACRSS ror: \@IACR@funding@ror}%
  \fi  
  \IACR@funding@params@clearkeys%
}
 
% This is a complicated implementation to test whether a token list is
% appropriate to use as metadata. It is intended to make sure that
% \write will produce a string without macros, except that macros are
% allowed in math mode. In a previous implementation we compared the argument
% to \text_purify:n applied to the argument, but this did not allow accents
% to be applied. This implmentation is based on tokcycle, which
% provides handlers for four classes of tokens: character, group,
% macro, and space.
\RequirePackage{tokcycle}
\RequirePackage{listofitems}

% Just a shortcut
\newcommand\ClassErr[1]{%
  \ClassError{iacrcc}{#1}{}%
}

% TODO: Check if this is neccesary with new fixes.
% Check if a token macro (in pdflatex) is a UTF-8 char
\ExplSyntaxOn
\prg_new_conditional:Npnn \iacr_check_uitfeight:n #1 { T, F, TF }
{
  % Define a regular expression where the second argument
  % needs to be expanded.
  % Look if the meaning of the token contains UTFviii
  % In (pdf)latex UTF8 tokens look like:
  % * \UTFviii@invalid@err
  % * \UTFviii@two@octets (or three or four octets)
  \cs_generate_variant:Nn \regex_match:nnTF {nV}
  \regex_match:nVTF { UTFviii } { \token_to_meaning:N #1 }
  { \prg_return_true:  }
  { \prg_return_false: }
}
\cs_new_eq:NN \IfUITFEight \iacr_check_uitfeight:nTF
\ExplSyntaxOff

% Macro which specifies if math is allowed in the 
% first argument to \checkstring
\newif\ifMathAllowedInCheckString
\MathAllowedInCheckStringtrue

\newif\ifTokenNotFound
\newcommand\IsMacroAllowed[3]{%
  %\typeout{MACROCHECK: \meaning#1}%
  \TokenNotFoundtrue
  \setsepchar{,}% parsing-separator
  % List of macros which are allowed
  \readlist\phrase{\ ,\$,\#,\&,\%,\ss,\o,\O,\`,\',\^,\",\=,\~,\.,\u,\v,\H,\t,\c,\d,\b,\l,\L,\space,\{,\},\=,\\,\r}%
  \def\iacrtmp{#1}%
  \foreachitem\word\in\phrase{%
    \ifTokenNotFound
      \ifx\iacrtmp\word
        \TokenNotFoundfalse
      \fi
    \fi
  }%
  \ifTokenNotFound
    % Check if the macro is a UTF-8 character in pdflatex
    % If so, we do not complain
    \IfUITFEight{#1}{}{%
      \ClassErr{#3:^^Jmacro \iacrtmp not allowed in #2}%
    }{}%
  \fi
}

% #1 is a string to check as just text. No macros are allowed except accents
%    that are easily converted downstream and except in math mode. 
% #2 is an error message prefix.
\newcommand\checkstring[2]{%
  % Since tokcycle treats the math toggle character $ as just another character,
  % we keep track of whether we are in math mode using this if. This allows us
  % to allow macros and groups in math mode but not in text mode.
  \newif\ifInMathMode
  \tokcycle{% \typeout{CHARACTER: ##1} % character handler.
    \if##1$% Check if we see a math toggle catcode 3
      \ifMathAllowedInCheckString
        \ifInMathMode % toggle this
          \InMathModefalse
        \else
          \InMathModetrue
        \fi
      \else
        \ClassErr{#2:^^J math not allowed in ^^J #1}
      \fi
    \fi}% end of character handler
    {% \typeout{GROUP: ##1}%      group handler
    \ifInMathMode  % groups are allowed in math mode.
    \else
      % Recurse and check this group: this allows things like {\`e}
      \checkstring{##1}{#2}%
    \fi}% end of group handler
    {% \typeout{MACRO: \string##1}%  macro handler
    \ifInMathMode
      \ClassWarning{iacrcc}{^^JMacros are not recommended in the title^^J}
    \else
      \IsMacroAllowed{##1}{#1}{#2}%
    \fi
    }% end of macro handler
    {% spaces are just ok.
    }%
    {#1}% argument to be parsed by tokcycle
  % Reset the macro to check for math to the default (true) value
  \MathAllowedInCheckStringtrue
}

% Provide the title of the paper with its various options
\renewcommand\title[2][]{%
  \IACR@title@params@set@keys{#1}%
  \gdef\@plaintitle{#2}%
  \pgfkeysgetvalue{/IACR-title/entities/running}{\IACR@title@running}%
  \pgfkeysgetvalue{/IACR-title/entities/subtitle}{\IACR@title@subtitle}%
  \pgfkeysgetvalue{/IACR-title/entities/onclick}{\IACR@title@onclick}%
  \pgfkeysgetvalue{/IACR-title/entities/plaintext}{\IACR@title@plaintext}%
  \renewcommand\thanks[1]{\ClassError{iacrcc}{The \string\thanks\space macro is not supported. Please see the documentation how to use footnotes.}{}}%
  \ifx\IACR@title@plaintext\@empty
    \checkstring{#2}{error in title}
  \else
     \gdef\@plaintitle{\IACR@title@plaintext}%
     \expandafter\checkstring\expandafter{\IACR@title@plaintext}{plaintext argument to title must be plain text}%
  \fi
  \if\relax\IACR@title@onclick\relax
    \gdef\@title{#2}%
  \else
    \gdef\@title{\href{\IACR@title@onclick}{\color{black}{#2}}}%
  \fi
  \if\relax\IACR@title@running\relax
    \gdef\IACR@title@running{\@plaintitle}%
  \fi
  \if\IACR@title@subtitle\@empty\else
    \gdef\IACR@title@subtitle@defined{}%
  \fi
}

\let\store@title\title% Save macro away

\newcommand\affiliation[2][]{%
  \stepcounter{IACR@inst@cnt}%  
  % If a affiliation name is provided does some basic sanity checking on the string
  \MathAllowedInCheckStringfalse
  \checkstring{#2}{Affiliation name should not contain macros or math}% 
  \@writemeta{affiliation:}%
  \@writemeta{\IACRSS name: #2}%
  \IACR@affiliation@params@set@keys{#1}%
  \edef\@IACRror{\IACR@affiliation@params@get{ror}}%
  \edef\@IACRonclick{\IACR@affiliation@params@get{onclick}}%
  \edef\@IACRdepartment{\IACR@affiliation@params@get{department}}%
  \edef\@IACRstreet{\IACR@affiliation@params@get{street}}%
  \edef\@IACRcity{\IACR@affiliation@params@get{city}}%
  \edef\@IACRstate{\IACR@affiliation@params@get{state}}%
  \edef\@IACRpostcode{\IACR@affiliation@params@get{postcode}}%
  \edef\@IACRcountry{\IACR@affiliation@params@get{country}}%
  \ifx\@IACRror\@empty\else
    \@writemeta{\IACRSS ror: \@IACRror}%
  \fi  
  \ifx\@IACRdepartment\@empty\else
    \@writemeta{\IACRSS department: \@IACRdepartment}%
  \fi
  \ifx\@IACRstreet\@empty\else
    \@writemeta{\IACRSS street: \@IACRstreet}%
  \fi
  \ifx\@IACRcity\@empty\else
    \@writemeta{\IACRSS city: \@IACRcity}%
  \fi
  \ifx\@IACRstate\@empty\else
    \@writemeta{\IACRSS state: \@IACRstate}%
  \fi
  \ifx\@IACRpostcode\@empty\else
    \@writemeta{\IACRSS postcode: \@IACRpostcode}%
  \fi
  \ifx\@IACRcountry\@empty
    \ifcsstring{@IACRversion}{final}{%
      \ClassError{iacrcc}{Specify a country for each affiliation for the final version}{}%
    }{}
  \else
    \@writemeta{\IACRSS country: \@IACRcountry}%
  \fi
  \ifx\@IACRonclick\@empty
    \ifx\@affiliation\@empty
      \gdef\@affiliation{\unexpanded{#2}}%
    \else
      \appto\@affiliation{\and\unexpanded{#2}}%
    \fi
  \else
    \ifx\@affiliation\@empty
      \edef\@affiliation{\noexpand\href{\@IACRonclick}{\noexpand\color{black}{\unexpanded{#2}}}}%
    \else
      \eappto\@affiliation{\noexpand\and{\noexpand\href{\@IACRonclick}{\noexpand\color{black}{\unexpanded{#2}}}}}%
    \fi
  \fi
  \IACR@affiliation@params@clearkeys%
}

\let\store@affiliation\affiliation% Save macro away

\if@anonymous
  \gdef\@author{Anonymous Submission to \publname}%
  \gdef\IACR@runningauthors{}%
  \gdef\IACR@listofauthors{}%
  \renewcommand{\addauthor}[2][]{}%
  \renewcommand{\affiliation}[2][]{}%
\fi

\newcommand{\inst}[1]{%
  \ifnum\theIACR@author@cnt=1\relax\else
    \ifnum\theIACR@inst@cnt=1\relax\else
      \unskip$^{#1}$%
    \fi
  \fi
}

\newcommand{\instwcomma}[1]{%
  \ifnum\theIACR@author@cnt=1\relax\else
    \ifnum\theIACR@inst@cnt=1\relax\else
      \unskip$^{,\,#1}$%
    \fi
  \fi
}
  
% fancyhdr: extensive control of page headers and footers in LATEX2ε
\RequirePackage{fancyhdr}

% graphicx: enhanced support for graphics
\RequirePackage{graphicx}

% if the author decides to use biblatex, then we pass options for the style to enforce
% consistent look and feel.
\if@optbiblatex
  \typeout{biblatex options may not be changed with \@backslashchar usepackage}
  % csquotes: context sensitive quotation facilities
  \RequirePackage{csquotes} % to fix a conflict with biblatex and doclicense.
  % biblatex: sophisticated Bibliographies in LaTeX
  \RequirePackage[backend=biber,style=alphabetic,maxcitenames=4,maxbibnames=20]{biblatex}[2019/12/01]
  \DeclareNameFormat{author}{%
    \usebibmacro{name:given-family}{\namepartfamily}{\namepartgiven}{\namepartprefix}{\namepartsuffix}%
    \usebibmacro{name:andothers}%
    {\renewcommand{\bibnamedelima}{ }\renewcommand{\bibnamedelimi}{ }%
      \@writemeta{\IACRSS author: \expanded{\namepartgiven\ifdefvoid{\namepartprefix}{}{ \namepartprefix } \namepartfamily\ifdefvoid{\namepartsuffix}{}{, \namepartsuffix}}}%
      \@writemeta{\IACRSS surname:\ifdefvoid{\namepartprefix}{}{ \namepartprefix} \namepartfamily}}%
  }%
  % We use a sourcemap to copy certain fields to the side so we can
  % include them in the .meta file. biblatex makes it hard to recover
  % some fields intact such as AUTHOR, EDITOR, PUBLISHER, LOCATION, and
  % PAGES. biber is able to parse these, but they get rewritten in a way
  % that is inconvenient to copy them to the .meta file. There may
  % be a better way to do this, but biblatex is complicated.
  \DeclareSourcemap{%
    \maps[datatype=bibtex,overwrite=true]{%
      \map{% copy author to usera
        \step[fieldsource=author,]
        \step[fieldset=usera,origfieldval,append]
      }
      \map[overwrite]{% copy editor to userb
        \step[fieldsource=editor,]
        \step[fieldset=userb,origfieldval,append]
      }
      \map[overwrite]{% copy institution to userc
        \step[fieldsource=institution,]
        \step[fieldset=userc,origfieldval,append]
      }
      \map[overwrite]{% copy publisher to userd
        \step[fieldsource=publisher,]
        \step[fieldset=userd,origfieldval,append]
      }
      \map[overwrite]{% copy location to usere
        \step[fieldsource=location,]
        \step[fieldset=usere,origfieldval,append]
      }
      \map[overwrite]{% copy organization to userf
        \step[fieldsource=organization,]
        \step[fieldset=userf,origfieldval,append]
      }
      \map[overwrite]{% copy pages to verba
        \step[fieldsource=pages,]
        \step[fieldset=verba,origfieldval,append]
      }
      \map[overwrite]{% copy date to verbb
        \step[fieldsource=date,]
        \step[fieldset=verbb,origfieldval,append]
      }
    }
  }
  \AtEndPreamble{%
    % TODO: this does not handle ~ properly. Maybe other primitives?
    \newcommand{\@writemkv}[2]{%
      \ifstrempty{\@metaval}{}{\@writemeta{\IACRSS #1: #2}}}
    \AtEveryBibitem{%
      \@writemeta{citation: \strfield{entrytype} \strfield{entrykey}}
      \iffieldundef{title}{}{\@writemkv{title}{\strfield{title}}}
      \iffieldundef{subtitle}{}{\@writemkv{subtitle}{\strfield{subtitle}}}
      \iffieldundef{booktitle}{}{\@writemkv{booktitle}{\strfield{booktitle}}}
      \iffieldundef{journaltitle}{}{\@writemkv{journal}{\strfield{journaltitle}}}
      \iffieldundef{edition}{}{\@writemkv{edition}{\strfield{edition}}}
      \iffieldundef{volume}{}{\@writemkv{volume}{\strfield{volume}}}
      \iffieldundef{number}{}{\@writemkv{number}{\strfield{number}}}
      \iffieldundef{issue}{}{\@writemkv{issue}{\strfield{issue}}}
      \iffieldundef{series}{}{\@writemkv{series}{\strfield{series}}}
      \iffieldundef{chapter}{}{\@writemkv{chapter}{\strfield{chapter}}}
      \iffieldundef{year}{}{\@writemkv{year}{\strfield{year}}}
      \iffieldundef{month}{}{\@writemkv{month}{\strfield{month}}}
      \iffieldundef{note}{}{\@writemkv{note}{\strfield{note}}}
      \iffieldundef{usera}{}{\@writemkv{authors}{\strfield{usera}}}
      \iffieldundef{userb}{}{\@writemkv{editors}{\strfield{userb}}}
      \iffieldundef{userc}{}{\@writemkv{institution}{\strfield{userc}}}
      \iffieldundef{userd}{}{\@writemkv{publisher}{\strfield{userd}}}
      \iffieldundef{usere}{}{\@writemkv{address}{\strfield{usere}}}
      \iffieldundef{userf}{}{\@writemkv{organization}{\strfield{userf}}}
      \iffieldundef{verba}{}{\@writemkv{pages}{\strfield{verba}}}
      \iffieldundef{verbb}{}{\@writemkv{date}{\strfield{verbb}}}
      \iffieldundef{urlraw}{}{\@writemkv{url}{\strfield{urlraw}}}
      % unused. This escapes things like \
      % \iffieldundef{url}{}{\@writemeta{\IACRSS url: \strfield{url}}}
      \iffieldundef{doi}{}{\@writemkv{doi}{\strfield{doi}}}
      \iffieldundef{isbn}{}{\@writemkv{isbn}{\strfield{isbn}}}
      \iffieldundef{issn}{}{\@writemkv{issn}{\strfield{issn}}}
      \iffieldundef{keywords}{}{\@writemkv{keywords}{\strfield{keywords}}}
      \iffieldundef{howpublished}{}{\@writemkv{howpublished}{\strfield{howpublished}}}
      % TODO: maybe include eprint, eprintclass, eprinttype
    }
  }
\else % did not invoke \documentclass[biblatex]{iacrcc}
  \AtBeginDocument{%
    \@ifpackageloaded{biblatex}{%
      \ClassError{iacrcc}{biblatex should be loaded with \@backslashchar documentclass[biblatex]{iacrcc}}%
    }%
  }
\fi%!biblatex

\ifcsstring{@IACRversion}{final}{%
  % totpages: count pages in a document, and report last page number
  \RequirePackage{totpages}
  \def\IACR@lp{\pageref*{TotPages}}%
}{}

\global\let\@IACR@License\@empty%
\newcommand\license[1]{%
  \gdef\@IACR@License{#1}%
  \def\@IACR@CCby{CC-by}%
  \ifx\@IACR@License\@IACR@CCby%
    % doclicense: support for putting documents under a license.
    \RequirePackage[type={CC},modifier={by},version={4.0}]{doclicense}
  \else
    \ClassError{iacrcc}{Invalid license: must be one of { CC-by }}{}%
  \fi
}

\fancypagestyle{title}{%
  \fancyhf{} % clear all header and footer fields
  \ifcsstring{@IACRversion}{final}{%
      \ifx\@IACR@License\@empty
        \ClassError{iacrcc}{Please specify a license when using version=final}{}%
      \fi
      \fancyhead[L]{%
        \small%
        \publname{}\\
        ISSN~\IACR@ISSN, Vol.~\IACR@vol, No.~\IACR@no, pp.~\IACR@fp--\IACR@lp. \hfill{}%
        \href{https://doi.org/\IACR@DOI}{DOI:\IACR@DOI}%
      }
      \fancyfoot[L]{%
        \small%
        \doclicenseText%
        \hfill{}%
        \doclicenseImage[imagewidth=4em]\\[.1em]%
        \if@IACR@Received Received: \IACR@Received \hfill{}\fi%
        \if@IACR@Revised Revised: \IACR@Revised \hfill{}\fi%
        \if@IACR@Accepted Accepted: \IACR@Accepted \hfill{}\fi%
        \if@IACR@Published Published: \IACR@Published\fi%
      }%
      % doclicense added support for the macro \doclicenseLongTextForHyperref in version 3.1.0 (2022/04/27)
      \if@doclicense@LongTextForHyperref
        \hypersetup{pdfcopyright={\doclicenseLongTextForHyperref}}
      \else
        \hypersetup{pdfcopyright={This work is licensed under a \doclicenseLongName\space license.}}
      \fi
      \hypersetup{pdflicenseurl={\doclicenseURL}}
      \hypersetup{pdfsubject={\publname{}, DOI:\IACR@DOI}}
  }{} % final
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}%fancypagestyle

\fancyhf{}
\fancyhead[RO,LE]{\thepage}
\fancyhead[RE]{\IACR@title@running}%
\fancyhead[LO]{%
  \if@anonymous
    \def\thanks##1{}%
    \def\inst##1{}%
    \def\instwcomma##1{}%
    \def\\{}%
    \def\footnote##1{}%
    \setcounter{IACR@author@cnt}{1}%
    \@author%
  \else
    \ifnum\theIACR@author@cnt>4\relax
      \if\relax\IACR@userdefinedrunningauthors\relax
        \ClassError{iacrcc}{When using more than 4 authors please define the running authors using the  \string\authorrunning\space macro}{}%
      \fi
    \fi
    \IACR@runningauthors%
  \fi%!anonymous
}

\renewcommand{\markboth}[2]{}
\pagestyle{fancy}

% Abstract style, keywords
\global\let\IACR@text@keywords\@empty
\global\let\IACR@keywords\@empty
% \IACR@keywords may contain mathematics for display in LaTeX.
% \IACR@text@keywords is the plain text version used for PDF and metadata.

\newcommand{\keywords}[2][\@empty]{%
  \gdef\IACR@keywords{#2}%
  \ifx#1\@empty
    \checkstring{#2}{Keywords should be free of macros. Use optional argument to \string\keywords}
    \gdef\IACR@text@keywords{#2}%
  \else
    \checkstring{#1}{optional argument to keywords may not contain macros.}
    \gdef\IACR@text@keywords{#1}%
  \fi
}

% fancyvrb: sophisticated verbatim text
\RequirePackage{fancyvrb} % used to write the abstract into \jobname.abstract

\renewenvironment{abstract}{%
  \ifx\IACR@text@keywords\@empty\else
    \@writemeta{keywords: \IACR@text@keywords}%
  \fi
  \small\quotation\setlength{\parindent}{0pt}\noindent
  \textbf{\textsf{Abstract.}}
  \VerbatimOut{\jobname.abstract}%
}%
{%
  \endVerbatimOut
  \input{\jobname.abstract}
  \ifx\IACR@keywords\@empty\else
    \smallskip\par\textbf{\textsf{Keywords:}}
    % Replace comma by a centered period.
    \expandarg\StrSubstitute{\IACR@keywords}{,}{\unskip\space\textperiodcentered\space\ignorespaces}
  \fi
  \endquotation%
  %% PDF keywords
  \ifx\IACR@text@keywords\@empty\else
    \hypersetup{pdfkeywords={\IACR@text@keywords}}
  \fi
  %% PDF author
  \if@anonymous
    \hypersetup{pdfauthor={hidden for submission}}
  \else
    \hypersetup{pdfauthor={\IACR@listofauthors}}
  \fi%!anonymous
  %% PDF title
  \hypersetup{pdftitle={\@plaintitle}}
  % PDF metadata
  \ifcsstring{@IACRversion}{final}{%
    \if@hyperxmp@doi
      \hypersetup{%
        pdfdoi=\IACR@DOI,%
        pdfissn=\IACR@ISSN,%
        pdfpubtype=journal,%
        pdfpublication={\publname},%
        pdfvolumenum={\IACR@vol},%
        pdfissuenum={\IACR@no},%
        pdfpagerange={\IACR@fp-\IACR@lp},%
      }
    \fi%hyperxmp@doi
  }{}% final
}

% autoref: capitals for Sections, and adding Algorithm
\def\equationautorefname{Equation}%
\def\footnoteautorefname{footnote}%
\def\itemautorefname{item}%
\def\figureautorefname{Figure}%
\def\tableautorefname{Table}%
\def\partautorefname{Part}%
\def\appendixautorefname{Appendix}%
\def\chapterautorefname{Chapter}%
\def\sectionautorefname{Section}%
\def\subsectionautorefname{Subsection}%
\def\subsubsectionautorefname{Subsubsection}%
\def\paragraphautorefname{paragraph}%
\def\subparagraphautorefname{subparagraph}%
\def\FancyVerbLineautorefname{line}%
\def\theoremautorefname{Theorem}%
\def\pageautorefname{page}%

\def\algorithmautorefname{Algorithm}%
\def\definitionautorefname{Definition}%
\def\exampleautorefname{Example}%
\def\exerciseautorefname{Exercise}%
\def\propertyautorefname{Property}%
\def\questionautorefname{Question}%
\def\solutionautorefname{Solution}%
\def\propositionautorefname{Proposition}%
\def\problemautorefname{Problem}%
\def\lemmaautorefname{Lemma}%
\def\conjectureautorefname{Conjecture}%
\def\corollaryautorefname{Corollary}%
\def\claimautorefname{Claim}%
\def\remarkautorefname{Remark}%
\def\noteautorefname{Note}%
\def\caseautorefname{Case}%

% amsmath: AMS mathematical facilities for LATEX
% amssymb: defines all the symbols found in the AMS symbol fonts
% amsthm: typesetting theorems (AMS style)
\RequirePackage{amsmath,amssymb,amsthm}
% mathtools: mathematical tools to use with amsmath
\RequirePackage{mathtools}
\theoremstyle{definition}%
\newtheorem{definition}{Definition}%
\newtheorem{example}{Example}%
\newtheorem{exercise}{Exercise}%
\newtheorem{property}{Property}%
\newtheorem{question}{Question}%
\newtheorem{solution}{Solution}%

\theoremstyle{plain}%
\newtheorem{theorem}{Theorem}%
\newtheorem{proposition}{Proposition}%
\newtheorem{problem}{Problem}%
\newtheorem{lemma}{Lemma}%
\newtheorem{conjecture}{Conjecture}%
\newtheorem{corollary}{Corollary}%
\newtheorem*{claim}{Claim}%

\theoremstyle{remark}%
\newtheorem{remark}{Remark}%
\newtheorem{note}{Note}%
\newtheorem{case}{Case}%

\theoremstyle{plain}%

% Floats and captions
\if@floatrow
  % floatrow: modifying the layout of floats
  \RequirePackage{floatrow}
  \floatsetup[table]{style=Plaintop}
  % caption: customising captions in floating environments
  \RequirePackage{caption}
  \captionsetup{labelfont={sf,bf}}
\else
  % float: improved interface for floating objects
  \RequirePackage{float}
  \newcommand\fs@iacrabove{%
    % Swap \abovecaptionskip and \belowcaptionskip
    \addtolength\abovecaptionskip{-\belowcaptionskip}
    \addtolength\belowcaptionskip{\abovecaptionskip}
    \addtolength\abovecaptionskip{-\belowcaptionskip}
    \setlength\abovecaptionskip{-\abovecaptionskip}
    \fs@plaintop%
    \def\@fs@cfont{\sffamily\bfseries}}
  \newcommand\fs@iacrbelow{%
    \fs@plain%
    \def\@fs@cfont{\sffamily\bfseries}
  }
  \floatstyle{iacrabove}
  \restylefloat{table}
  \floatstyle{iacrbelow}
  \restylefloat{figure}
\fi

% Line # for submission
\newcommand\linenomathWithnumbersforAMS{%
  \ifLineNumbers
    \ifnum\interlinepenalty>-\linenopenaltypar
      \global\holdinginserts\thr@@
      \advance\interlinepenalty \linenopenalty
      \ifhmode                                   % v4.3
        \advance\predisplaypenalty \linenopenalty
      \fi
      \advance\interdisplaylinepenalty \linenopenalty
    \fi
  \fi
  \ignorespaces
}

\newcommand\IACR@linenumbers{%
  % lineno: line numbers on paragraphs
  \RequirePackage[mathlines]{lineno}
  \linenumbers
  \def\linenumberfont{\normalfont\tiny\sffamily\color{gray}}
  % Taken from http://phaseportrait.blogspot.fr/2007/08/lineno-and-amsmath-compatibility.html
  \newcommand*\patchAmsMathEnvironmentForLineno[1]{%
    \expandafter\let\csname old##1\expandafter\endcsname\csname ##1\endcsname
    \expandafter\let\csname oldend##1\expandafter\endcsname\csname end##1\endcsname
    \renewenvironment{##1}%
    {\linenomathWithnumbersforAMS\csname old##1\endcsname}%
    {\csname oldend##1\endcsname\endlinenomath}%
  }%
  \newcommand*\patchBothAmsMathEnvironmentsForLineno[1]{%
    \patchAmsMathEnvironmentForLineno{##1}%
    \patchAmsMathEnvironmentForLineno{##1*}%
  }%
  \AtBeginDocument{%
    \patchAmsMathEnvironmentForLineno{equation*}%
    \patchBothAmsMathEnvironmentsForLineno{align}%
    \patchBothAmsMathEnvironmentsForLineno{flalign}%
    \patchBothAmsMathEnvironmentsForLineno{alignat}%
    \patchBothAmsMathEnvironmentsForLineno{gather}%
    \patchBothAmsMathEnvironmentsForLineno{multline}%
  }
}
\ifcsstring{@IACRversion}{submission}{\IACR@linenumbers}{}
\ifcsstring{@IACRversion}{final}{%
  \InputIfFileExists{\jobname.copyedit}{% turn on linenumbers and
    % input any additional commands for copy editing.
    \typeout{^^JCopy editing enabled^^J}\IACR@linenumbers}{}
}{}
% microtype: subliminal refinements towards typographical perfection
\RequirePackage{microtype}

% We load lmodern to get latin modern fonts but only in pdflatex.
% Lualatex already uses latin modern for text and cm for math.
\ifpdftex
  \RequirePackage{lmodern}
\fi

% Store the default font family used
\let\store@font\familydefault%

% Store the paper width
\let\store@paperwidth\paperwidth%

\endinput
%end of file iacrcc.cls
