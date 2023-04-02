This is a pretty ugly test to make sure that we know what \protected@write
produces. Some things like \mathrm become "\protect \mathrm " with a space after
\mathrm, but other things like \! become "\protect \!" without a space after them.
Same for \( and \).