% IACR Journal document class. This can be used for
% CiC (replacing iacrj.cls)
% ToSC (replacing iacrtrans.cls)
% TCHES (replacing iacrtrans.cls)
%
% The authoritative source is github.com/IACR/latex/iacrj
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

\def\fileversion{0.90}
\def\filedate{2025/01/28}

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\typeout{^^J  ***  LaTeX class for IACR Communications in Cryptology v\fileversion\space ***^^J}
\ProvidesClass{iacrj}[\filedate]
  
% Common definitions

% This is used to make the latex log easier to parse and keep track of
% the current file for error reporting.
\RequirePackage[abspath=true]{currfile}
% \currfileabspath is sometimes empty when \RequirePackage is called
% from inside a package included with \RequirePackage under lualatex,
% but currfilepath is always present (but may not be unique).
\AtBeginOfFiles{\ifx\currfileabspath\empty%
  \wlog{---------------------------iacrj:opened as \currfilepath}%
  \else%
  \wlog{---------------------------iacrj:opened with \currfileabspath}%
  \fi}
\AtEndOfFiles{\ifx\currfileabspath\empty%
  \wlog{---------------------------iacrj:closed as \currfilepath}
  \else%
  \wlog{---------------------------iacrj:closed with \currfileabspath}%
  \fi}

% expl3: wrapper package for experimental LaTeX3
\RequirePackage{expl3}

% xkeyval: extension of the keyval package
%          This offers additional macros for setting keys and
%          declaring and setting class or package options.
\RequirePackage{xkeyval}

\def\IACR@vol{0}
\def\IACR@no{0}
\def\IACR@fp{1}
\def\IACR@DOI{}
\def\IACR@CROSSMARKURL{}
\global\let\IACR@Published\@empty
\global\let\IACR@Received\@empty
\global\let\IACR@Revised\@empty
\global\let\IACR@Accepted\@empty

% etoolbox: is a toolbox of programming facilities geared primarily
%           towards LaTeX class and package authors.
\RequirePackage{etoolbox}
% xstring: provides macros for manipulating strings - testing a string’s
%          contents, extracting substrings, substitution of substrings and
%          providing numbers such as string length, position of, or number
%          of recurrences of, a substring.
\RequirePackage{xstring} % Required for IfSubStr and IfStrEq

% See https://www.latex-project.org/news/latex2e-news/ltnews34.pdf
\tracinglostchars=3

\newif\if@optbiblatex
\@optbiblatexfalse
\DeclareOptionX<IACR>{biblatex}{\@optbiblatextrue}
\newif\if@floatrow
\@floatrowfalse
\DeclareOptionX<IACR>{floatrow}{\@floatrowtrue}
% version=submission will set anonymous to true, but it can be
% overridden with the notanonymous option for the class.
\newif\if@anonymous
\@anonymousfalse
% This maybe be used to override \@anonymous
\newif\if@notanonymous
\@notanonymousfalse
\DeclareOptionX<IACR>{notanonymous}{\@notanonymoustrue}
\define@choicekey{IACR}{version}[\@IACRversion]{preprint,submission,final}[preprint]{}
\define@choicekey{IACR}{journal}[\@IACRjournal]{cic,tosc,tches}{}
\DeclareOptionX*{}
\ProcessOptionsX<IACR>\relax
% The \jobname.iacrmetadata file can be used to set journal-imposed
% metadata including \IACR@Received, \IACR@Revised, \IACR@Accepted, \IACR@Published,
% \IACR@DOI, \IACR@fp, \IACR@no, and \IACR@vol

\ifx\@IACRversion\undefined\def\@IACRversion{preprint}\fi
\InputIfFileExists{\jobname.iacrmetadata}{
  \typeout{Read journal metadata}%
}{}
\IfStrEq{\@IACRjournal}{cic}{%
  \def\publname{IACR Communications in Cryptology}%
  \def\IACR@EISSN{3006-5496}
}{%
  \ifx\IACR@fp{1}\else\AtBeginDocument{\setcounter{page}{\IACR@fp}}\fi%
  \IfStrEq{\@IACRjournal}{tosc}{%
    \def\publname{IACR Transactions on Symmetric Cryptology}%
    \def\IACR@EISSN{2519-173X}%
  }{%
    \IfStrEq{\@IACRjournal}{tches}{%
      \def\publname{IACR Transactions on Cryptographic Hardware and Embedded Systems}%
      \def\IACR@EISSN{2569-2925}%
    }{%
      \ClassError{iacrj}{Invalid journal option \@IACRjournal}
    }
  }
}
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
    \ClassError{iacrj}{Invalid options passed to iacrj: \store@classoptionslist}{}%
  \fi
\fi

% article class
\LoadClass[10pt,twoside]{article}[2007/10/19]

% iftex: am I running under pdfTEX, XETEX or LuaTEX?
\RequirePackage{iftex}

\ifluatex
  % Check for existence of luatex85.sty and load it if available.
  % This should ensure that it work also with newer versions of luatex.
  % luatex85: The package provides emulation of pdfTEX primitives for LuaTEX v0.85+.
  \IfFileExists{luatex85.sty}{\RequirePackage{luatex85}}{}
\fi

\setcounter{tocdepth}{2}

\@ifpackageloaded{biblatex}{}{%
  \bibliographystyle{alphaurl}%
  \def\bibliographystyle#1{%
    \ClassError{iacrj}{The bibliography style is set by iacrj.cls and may not be changed by the author}{}%
  }}

\if@anonymous
  \RequirePackage[maketitle=iacrj,anonymous,notitlefootnote]{metacapture}
\else
\ifcsstring{@IACRversion}{final}{
  \RequirePackage[countryrequired,emailreq=one,maketitle=iacrj,notitlefootnote]{metacapture}
}{ 
  \RequirePackage[maketitle=iacrj,notitlefootnote]{metacapture}
}
\fi
\AtEndPreamble{%
  % hyperref: Extensive support for hypertext in LaTeX
  % bookmarksopen: If Acrobat bookmarks are requested,
  %                show them with all the subtrees expanded
  % bookmarksopenlevel: parameter level to which bookmarks are open
  \RequirePackage[hyperfootnotes=false,bookmarksopen=true,bookmarksopenlevel=2]{hyperref}
  \@ifpackageloaded{natbib}{%
    % TODO: Note that latex now has the \disable@package@load method. It's not clear if we
    % should use that instead.
    \ClassError{iacrj}{The natbib package is not supported}{}}{}
  \ifpdftex
    % TU encoding is only available with XeTeX and LuaTeX.
    % Defaulting to T1 encoding.
    % fontenc: Standard package for selecting font encodings
    \RequirePackage[T1]{fontenc}
  \fi
  %
  \if@anonymous
    \hypersetup{pdfauthor={hidden for submission}}
  \else
    \hypersetup{pdfauthor={\METAC@listofauthors}}
  \fi
  \ifcsstring{@IACRjournal}{cic}{%
    \hypersetup{pdflang=en,%
      urlcolor=blue,%
      colorlinks=true,%
      citecolor=black!70!green,%
      linkcolor=black!70!red}%
  }{%
    \hypersetup{pdflang=en,%
      colorlinks=true,%
      citecolor=black!70!green,%
      linkcolor=black!70!red%
    }}
  \ifcsstring{@IACRversion}{final}{%
    \ifx\IACR@DOI\@empty%
      \hypersetup{pdfsubject={\publname}}%
    \else%
      \hypersetup{pdfsubject={\publname{}, DOI:\IACR@DOI}}%
    \fi%
  }{}% final
  % Disable latexdiff commands in PDF links
  \pdfstringdefDisableCommands{%
    \def\DIFadd#1{#1}%
    \def\DIFdel#1{}%
  }
  % When the ulem package is loaded make sure to enable \normalem:
  % this makes sure ulem does not replace italics with underlining
  % in text emphasized by \emph, and to some extent by \em
  \@ifpackageloaded{ulem}{\normalem}{}%
  % The hyperref package is used to handle cross-referencing commands in
  % LaTeX to produce hypertext links in the document. hyperref is fussy about
  % the order in which it is loaded, and the official documentation recommends
  % loading last. In spite of this, there are some packages that must be
  % loaded after hyperref. (e.g., cleveref). In order to support this, the
  % author should create a file called after-hyperref.sty with
  % \RequirePackage{cleveref} in it.
  \IfFileExists{after-hyperref.sty}{%
    \RequirePackage{after-hyperref}
  }{}
  \ifcsstring{@IACRversion}{final}{%
    % When compiling the final version we need the last page number
    % totpages: count pages in a document, and report last page number
    % The documentation recommends to load this package last.
    \RequirePackage{totpages}
  }{}% final
  \@ifpackageloaded{savetrees}{\ClassError{iacrj}{The~savetrees~package~is~not~allowed}{}}
}

% The TotPages label is not defined until after the \begin{document}.
\AtBeginDocument{%
  \ifcsstring{@IACRversion}{final}{%
    \def\IACR@lp{\pageref*{TotPages}}%
  }{}% final
}

% Geometry: flexible and complete interface to document dimensions.
\RequirePackage[a4paper,hscale=0.65,vscale=0.75,marginratio=1:1,marginparwidth=2.7cm]{geometry}

% afterpage: execute command after the next page break
\RequirePackage{afterpage}

\RequirePackage{tikz}
\ProcessOptions\relax
\usetikzlibrary{svg.path}

% Macro for crossmark image.
\definecolor{c948f8f}{RGB}{148,143,143}
\definecolor{cd0d0d0}{RGB}{208,208,208}
\definecolor{ca0a0a0}{RGB}{192,192,192}
\definecolor{c535353}{RGB}{83,83,83}
\definecolor{cc72914}{RGB}{199,41,20}
\definecolor{cef3340}{RGB}{239,51,64}
\definecolor{c3eb1c8}{RGB}{62,177,200}
\definecolor{cffc72c}{RGB}{255,199,44}
\newcommand\crossmarkimage[1]{%
  \begin{tikzpicture}[scale=#1, every node/.append style={scale=#1}, inner sep=0pt, outer sep=0pt, x=1cm, y=1cm]
  \path[draw=c948f8f,shading=axis,top color=white,bottom color=ca0a0a0,fill=cd0d0d0,line width=0.0198cm,miter limit=10.0,rounded corners=0.0529cm] (0.1058, -0.1058) rectangle (7.0, -1.5875);
  \node[text=c535353,anchor=south west] (text235) at (1.8, -1.15){\fontfamily{phv}\selectfont \LARGE Check for updates};
  \path[fill=cc72914] (0.6599, -1.1044) -- (1.1393, -0.7848) -- (1.1393, -0.4011) -- (0.6599, -0.4011) -- (0.6599, -1.1044) -- (0.6599, -1.1044)-- cycle;
  \path[fill=cef3340] (1.1393, -1.1044) -- (0.6599, -0.7848) -- (0.6599, -0.4011) -- (1.1393, -0.4011) -- (1.1393, -1.1044) -- (1.1393, -1.1044)-- cycle;
  \path[fill=c3eb1c8] (0.8996, -0.3175)arc(90.0:360.0:0.5292)arc(0.0:90.0:0.5292) -- cycle(0.8996, -1.2462)arc(270.0:0.0:0.3995)arc(0.0:-90.0:0.3995) -- cycle;
  \path[fill=cffc72c] (1.193, -1.1173)arc(317.2441:158.1926:0.3993) -- (0.418, -0.6281)arc(155.807:319.67:0.5292) -- cycle;
\end{tikzpicture}}
% end of crossmark image

% pgfkeys: a flexible key management system
%\RequirePackage{pgfkeys}

\global\let\@author\@empty%
\global\let\@affiliation\@empty%

% Bool to check if the user called the \authorrunning macro
\newif\ifIACR@userdefinedrunningauthors
\IACR@userdefinedrunningauthorsfalse
\def\IACR@runningauthors{}%
\newcommand\authorrunning[1]{%
  \ifx\@onlypreamble\@notprerr\ClassError{iacrj}{\string\authorrunning\space may only be used before \string\begin{document}}{}%
  \else%
    \IACR@userdefinedrunningauthorstrue%
    \def\IACR@runningauthors{#1}%
  \fi
}

\AtEndDocument{%
  % Final version requires textabstract.
  \IfFileExists{\jobname.abstract}{}{%
    \ifcsstring{@IACRversion}{final}{%
      \ClassError{iacrj}{An abstract with textabstract environment is required}{}}{%
      \ClassWarningNoLine{iacrj}{^^JYour final version will need the textabstract environment.^^J}%
    }
  }{}
  \ifcsstring{@IACRversion}{final}{%
    \ifnum\theMETAC@affil@cnt<1\relax
      \ClassError{iacrj}{Specify at least one affiliation for the final version}{}%
    \fi%
  }{}% final
}
\let\storeprotect\protect

% xpatch: Extending etoolbox patching commands
\RequirePackage{xpatch}

% fancyhdr: extensive control of page headers and footers in LATEX2ε
\RequirePackage{fancyhdr}

% graphicx: enhanced support for graphics
\RequirePackage{graphicx}

\global\let\@IACR@docdate\@empty%
\newcommand{\documentdate}[1]{%
  \gdef\@IACR@docdate{#1}%
  \gdef\@IACR@docdate@defined{1}%
}

% Ensure the bookmark for the reference points to the section header
% Insert a PDF anchor into the beginning of \refname
\let\oldrefname\refname%
\def\refname{\leavevmode\texorpdfstring{\vbox to 0pt{\vss\pdfdest name{references}XYZ\vskip\baselineskip}\relax\oldrefname}{\oldrefname}}%

\apptocmd{\thebibliography}{%
  \def\@currentHref{references}\relax%
  \addcontentsline{toc}{section}{References}%
}{}{}

\AtEndPreamble{%
  \@ifpackageloaded{babel}{%
    % Ensure the bookmark for the reference points to the section header
    % Insert a PDF anchor into the beginning of \refname
    % Add this to captionsenglish to avoid problems when babel is used
    \addto\captionsenglish{%
      \gdef\refname{\leavevmode\texorpdfstring{\vbox to 0pt{\vss\pdfdest name{references}XYZ\vskip\baselineskip}\relax\oldrefname}{\oldrefname}}%
    }%
  }{}%
}

% for backwards compatibility with older iacrj.
\NewDocumentCommand{\keywords}{om}{\IfNoValueTF{#1}{\addkeywords{#2}}{\addkeywords[#1]{#2}}}

% if the author decides to use biblatex, then we pass options for the style to enforce
% consistent look and feel.
\if@optbiblatex
  \typeout{biblatex options may not be changed with \@backslashchar usepackage}
  % csquotes: context sensitive quotation facilities
  \RequirePackage{csquotes} % to fix a conflict with biblatex and doclicense.
  \RequirePackage{xifthen} % to make sure that biblatex does not define \TE@hook.
  % biblatex: sophisticated Bibliographies in LaTeX
  \RequirePackage[backend=biber,style=trad-alpha,minalphanames=3,maxalphanames=4,maxbibnames=20,useprefix=true]{biblatex}[2019/12/01]
  \DeclarePrintbibliographyDefaults{heading=bibintoc}%
  \DeclareLabelalphaTemplate{
    \labelelement{
      \field[strwidth=3,strside=left]{label}
      \field[strwidth=3,strside=left,ifnames=1]{labelname}
      \field[strwidth=1,strside=left]{labelname}
      \field[strwidth=3,strside=left]{citekey}
    }
    \labelelement{\field[strwidth=2,strside=right]{year}}
  }
  %% \DeclareNameFormat{author}{%
  %%   \usebibmacro{name:given-family}{\namepartfamily}{\namepartgiven}{\namepartprefix}{\namepartsuffix}%
  %% }%
\else % did not invoke \documentclass[biblatex]{iacrj}
  \AtBeginDocument{%
    \@ifpackageloaded{biblatex}{%
      \ClassError{iacrj}{biblatex should be loaded with \@backslashchar documentclass[biblatex]{iacrj}}%
    }%
  }
\fi%!biblatex

% xurl: Allow URL breaks at any alphanumerical character
% Load xurl *after* biblatex to ensure the same behavior
\RequirePackage{xurl}

\def\ymdtoday{\leavevmode\hbox{\the\year-\twodigits\month-\twodigits\day}}\def\twodigits#1{\ifnum#1<10 0\fi\the#1}

% We delay this to after begin{document} because it depends upon stuff
% from the license, which in turn depends on hyperref having been
% loaded.
\AtBeginDocument{
  \fancypagestyle{title}{%
  \fancyhf{} % clear all header and footer fields
  \ifcsstring{@IACRversion}{final}{%
    \ifx\METAC@license\@empty
       \ClassError{iacrj}{Please specify a license when using version=final: using for example \string\license{CC-BY-4.0}}{}%
    \fi
    \IfStrEq{\@IACRjournal}{cic}{%
      \fancyhead[L]{%
        \small%
        \publname{}\\
        \ifx\IACR@EISSN\@empty\else{ISSN~\IACR@EISSN, }\fi%
        Vol.~\IACR@vol, No.~\IACR@no, \IACR@lp\ pages.}
      \ifx\IACR@DOI\@empty\else\fancyhead[R]{\small%
        \begin{tabular}{r}\href{https://doi.org/\IACR@DOI}{https://doi.org/\IACR@DOI}\ifx\IACR@CROSSMARKURL\@empty\else\vspace{2px}\\%
          \href{\IACR@CROSSMARKURL}{\crossmarkimage{.35}}\fi\end{tabular}}\fi%
    }{% only CiC uses crossref.
    \fancyhead[L]{%
      \small%
      \publname{}\\
      ISSN~\IACR@EISSN, Vol.~\IACR@vol, No.~\IACR@no, pp.~\IACR@fp--\IACR@lp. \hfill{}%
      \href{https://doi.org/\IACR@DOI}{DOI:\IACR@DOI}
    }}%
  }{}% final
  \ifx\@METAC@license\@empty\else%
    % If \license is provided show this for preprint and final (not for submission)
    \ifcsstring{@IACRversion}{submission}{}{%
      \fancyfoot[L]{%
        \small%
        \ifx\METAC@license\@empty\else
        \doclicenseText%
        \hfill{}%
        % CiC uses a taller doclicense image.
        \IfStrEq{\@IACRjournal}{cic}{%
          \doclicenseImage[imagewidth=4em]%
        }{\doclicenseImage[imagewidth=4em,imagemodifier={-80x15}]}%
        \\[.1em]%
        \fi
        \ifcsstring{@IACRversion}{final}{% Only show this information on the final version
          \ifx\IACR@Received\@empty\else Received: \IACR@Received \hfill{}\fi%
          \ifx\IACR@Revised\@empty\else Revised: \IACR@Revised \hfill{}\fi%
          \ifx\IACR@Accepted\@empty\else Accepted: \IACR@Accepted\fi%
          \ifx\IACR@Published\@empty\else\IfStrEq{\@IACRjournal}{cic}{}{\hfill{}Published: \IACR@Published}\fi%
        }{%
          \ifdefined\@IACR@docdate@defined%
            \ifx\@IACR@docdate\@empty%
              % an empty string was passed \documentdate to
              % indicate to *not* display any date
            \else
              Date of this document: \@IACR@docdate.%
            \fi% !if \@IACR@docdate = \@empty
          \else%
            Date of this document: \ymdtoday.%
          \fi% !if \@IACR@docdate@defined is defined
        }%
      }%
    }% !if @IACRversion != submission
  \fi% !\@METAC@license
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
  }
}

\newbox\measurerunningauthors
\newdimen\@maxrunningwidth%
\ExplSyntaxOn
\AtBeginDocument{
  \fancyhf{}
  \fancyhead[RO,LE]{\thepage}
  \fancyhead[RE]{\g_metac_titlerunning_tl}%
  \fancyhead[LO]{%
    \if@anonymous
      \def\inst##1{}%
      \def\instwcomma##1{}%
      \def\\{}%
      \@author%
    \else%
      \IACR@runningauthors%
    \fi%!anonymous
  }
  \if@anonymous
    \gdef\@author{Anonymous Submission to \publname}%
    \def\IACR@runningauthors{}%
    \renewcommand{\addauthor}[2][]{}%
    \renewcommand{\addaffiliation}[2][]{}%
  \else
    \ifIACR@userdefinedrunningauthors\else\def\IACR@runningauthors{\METAC@listofauthors}\fi
  \fi
  % maxrunningwidth is the maximum width we can tolerate for authors and title.
  \@maxrunningwidth=\textwidth%
  \advance\@maxrunningwidth by -15pt% allow for the page number width
  \global\setbox\measurerunningauthors=\hbox{\IACR@runningauthors}
  \if@anonymous\else%
    \ifdim\wd\measurerunningauthors>2\@maxrunningwidth % more than two lines
      \ClassError{iacrj}{List of authors is too long for running head. Please use \string\authorrunning\space to fix this}{}%
    \fi
    \ifdim\wd\measurerunningauthors>\@maxrunningwidth
      \ClassWarning{iacrj}{List of authors is too long for running head. Please use \string\authorrunning\space to fix this}{}
    \fi
  \fi
  \thispagestyle{title}
  \renewcommand{\markboth}[2]{}
  \pagestyle{fancy}
  \def\pagestyle#1{\ClassError{iacrj}{The pagestyle is set by iacrj.cls and may not be changed by the author}{}}
  \def\pagenumbering#1{\ClassError{iacrj}{The page numbering is set by iacrj.cls and may not be changed by the author}{}}
}
\ExplSyntaxOff

% Add support for a footnote without symbol on the front page
\global\let\@genericfootnote\@empty

\newcommand\genericfootnote[1]{%
  \ifx\@onlypreamble\@notprerr% in the document.
    \@ifpackageloaded{hyperref}{\begin{NoHyper}}{}%
      \renewcommand\thefootnote{}\footnotetext{#1}%
    \@ifpackageloaded{hyperref}{\end{NoHyper}}{}
  \else% in the preamble, so save it for later.
    \gdef\@genericfootnote{#1}%
  \fi%
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
%\RequirePackage{amsmath,amssymb,amsthm}
\RequirePackage{amsthm}
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
    \linenumbers
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
  % lmodern: Latin modern fonts in outline formats
  \RequirePackage{lmodern}
\fi
\ExplSyntaxOn
\AddToHook{cmd/maketitle/before}{%
  % Generic footnote and e-mails are displayed without markers
  \ifx\@genericfootnote\@empty\else
    \begingroup
    \@ifpackageloaded{hyperref}{\begin{NoHyper}}{}%
      \renewcommand\thefootnote{}\footnotetext{\@genericfootnote}%
    \@ifpackageloaded{hyperref}{\end{NoHyper}}{}
    \endgroup
  \fi
  \if@anonymous\else%
    \begingroup
      \@ifpackageloaded{hyperref}{\begin{NoHyper}}{}%
      \renewcommand\thefootnote{}\footnotetext{\g_metac_displayemails_tl}%
      \@ifpackageloaded{hyperref}{\end{NoHyper}}{}
    \endgroup
  \fi%
}
\ExplSyntaxOff

% Store the default font family used
\let\store@font\familydefault%

% Store the paper width
\let\store@paperwidth\paperwidth%

% One might get an “Unused global options” warning for some of our options.
% This can be removed using the \XKV@useoption command provided by the xkeyval
% package but this does not seem to work in all LaTeX environments.
% Simply remove the options from \@unusedoptionlist ourselves.
\ifx\@unusedoptionlist\@empty\else
  \StrDel{\@unusedoptionlist}{journal=tosc}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{journal=cic}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{journal=tches}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{journal}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{version=final}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{version=preprint}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{version=submission}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{version}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{floatrow}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{notanonymous}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{biblatex}[\@unusedoptionlist]%
  \StrDel{\@unusedoptionlist}{,}[\@unusedoptionlist]%
\fi

%TODO abstract appears before title in some document classes, so this is dangerous.
\ExplSyntaxOn
\AddToHook{env/abstract/after}{%
  \clist_if_empty:NTF \g_metac_keywords_raw_clist {} {
    \smallskip\par\noindent\textbf{\noindent\textsf{Keywords:}}~\clist_use:Nnnn \g_metac_keywords_raw_clist {,~} {,~} {,~}
  }    
}
\ExplSyntaxOff

\endinput
%end of file iacrj.cls
