import llk
from llk import Grammar, LLParser


def first(k, grammar, right):
    res = set()
    if k == 0:
        return res
    if right == '':
        return res
    w = right[0]

    if w.lower() == w and llk.Terminal(w) in grammar.terms:
        if len(right) == 1:
            res.add(w)
        aaa = first(k - 1, grammar, right[1:])
        for el in aaa:
            res.add(w + el)
        if k == 1:
            res.add(w)

    elif w.upper() == w and llk.Nonterminal(w) in grammar.nonterms:
        for pr in grammar.prod_by_nonterminal[llk.Nonterminal(w)]:
            res |= first(k, grammar, str(pr).split('->')[-1].strip() + right[1:])

    return res


def follow(k, grammar):
    follow = {}
    for nonterm in grammar.nonterms:
        follow[str(nonterm)] = set()
    changed = True
    while changed:
        changed = False
        for prod in grammar.prods:
            #print(prod)
            pr = str(prod).split('->')[-1].strip()
            for i in range(len(pr)):
                if pr[i].upper() == pr[i] and llk.Nonterminal(pr[i]) in grammar.nonterms:
                    last = follow[pr[i]].copy()
                    if pr[i+1:] != '':
                        follow[pr[i]] |= first(k, grammar, pr[i+1:])
                    else:
                        follow[pr[i]] |= follow[str(prod).split('->')[0].strip()]
                    if last != follow[pr[i]]:
                        changed = True
    return follow


def phi(grammar):
    for prod in grammar.prods:
        # print(prod)
        pr = str(prod).split('->')[-1].strip()


def main():
    grammar = Grammar.read('simple1.txt')   
    print(grammar)

    k = int(input("k: "))

    for nonterm in grammar.nonterms:
        print(f'FIRST({str(nonterm)}) = ', first(k, grammar, str(nonterm)))

    for nonterm, fol in follow(k, grammar).items():
        print(f'FOLLOW({nonterm}) = ', fol)


main()


# print(f"Grammar is in LL({parser.k})")
# print(f"Look-aheads: {parser.look_up}")
# print(parser.print_firsts())
# print(parser._first(3, ('S')))
# # word = 'ab'
# #
# # print(f"Word '{word}' is accepted: {parser.parse(word)}")