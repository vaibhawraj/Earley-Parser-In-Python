# EARLEY PARSER : PARSING WITH CONTEXT-FREE GRAMMARS

	In computer science, the Earley parser is an algorithm for parsing strings that belong to a given context-free language, though (depending on the variant) it may suffer problems with certain nullable grammars.[1] The algorithm, named after its inventor, Jay Earley, is a chart parser that uses dynamic programming; it is mainly used for parsing in computational linguistics. It was first introduced in his dissertation[2] in 1968 (and later appeared in an abbreviated, more legible, form in a journal[3]).

Earley parsers are appealing because they can parse all context-free languages, unlike LR parsers and LL parsers, which are more typically used in compilers but which can only handle restricted classes of languages. The Earley parser executes in cubic time in the general case {\displaystyle {O}(n^{3})} {O}(n^{3}), where n is the length of the parsed string, quadratic time for unambiguous grammars {\displaystyle {O}(n^{2})} {O}(n^{2}),[4] and linear time for almost all LR(k) grammars. It performs particularly well when the rules are written left-recursively.


the Earley
algorithm (Earley, 1970) uses dynamic programming to implement a top-down search
The core of the Earley algorithm is a single
left-to-right pass that fills an array we’ll call a chart that has N + 1 entries. For each
word position in the sentence, the chart contains a list of states representing the partial
parse trees that have been generated so far.

About Earley Parser

Implementation Details

Usage

Input

Run Test

References