"""
This approach makes use of Natural Language Processing with a bit of Machine Learning (if I had chosen to implement this to generate the Rules).
"""
import sys

cases = []
if (1):
    # 
    cases.append(tuple(["([}{])", False]))
    cases.append(tuple(["([{}])", True]))
    cases.append(tuple(["[()]", True]))
    cases.append(tuple(["[(])", False]))
#else:

    cases.append(tuple(["()", True]))
    cases.append(tuple(["(", False]))
    cases.append(tuple([")", False]))

    cases.append(tuple(["[]", True]))
    cases.append(tuple(["[", False]))
    cases.append(tuple(["]", False]))

    cases.append(tuple(["{}", True]))
    cases.append(tuple(["{", False]))
    cases.append(tuple(["}", False]))

    cases.append(tuple(["[(]", False]))
    cases.append(tuple(["[()", False]))
    cases.append(tuple(["[)]", False]))
    cases.append(tuple(["[()", False]))
    cases.append(tuple(["()]", False]))
    cases.append(tuple(["[(", False]))
    cases.append(tuple([")]", False]))

    cases.append(tuple(["[({})]", True]))
    cases.append(tuple(["[({", False]))
    cases.append(tuple(["})]", False]))

    cases.append(tuple(["[({})({})({})({})]", True]))

    cases.append(tuple(["[({}{}{}{})({})({})({})]()", True]))

__rules__ = {
    '(' : ')',
    '[' : ']',
    '{' : '}'
}

def invert_dict(d):
    new_d = {}
    for k,v in d.items():
        new_d[v] = k
    return new_d

class Balancer():
    def __count_it__(self, c,d, is_o=False, is_c=False, toks1=[], toks2=[]):
        count_one = lambda c,d : 1 if (not (c in d.keys())) else d[c]+1
        d[c]=count_one(c,d)
        if (is_o):
            toks1.append(c)
        elif (is_c):
            toks2.append(c)
        return c
    
    def __analysis__(self):
        self.tokens = []
        self.tokens2 = []
        for c in self.s:
            is_opener = (c in self.rules.keys())
            is_closer = (c in self.rules.values())
            self.__count_it__(c,self.d, is_o=is_opener, is_c=is_closer, toks1=self.tokens, toks2=self.tokens2)
    
    def __is_balanced__(self, the_str):
        self.d = {}
        self.s = the_str
        if (self.method == 0):
            # This method has two loops...
            self.tokens = [self.__count_it__(c,self.d) for c in self.s if (c in self.rules.keys())]     # this contains the unbalanced tokens for openers
            self.tokens2 = [self.__count_it__(c,self.d) for c in self.s if (c in self.rules.values())]  # this contains the unbalanced tokens for closers
        else:
            # This method has one loop.
            self.__analysis__()
        self.__count__ = 0
        self.num1 = 0
        for k,v in self.rules.items():
            if (k in self.d.keys()):
                self.num1 += 1
            try:
                if (self.d[k] == self.d[v]):
                    self.__count__ += 1
            except KeyError:
                self.__count__ += 0
        return (self.num1 > 0) and (self.__count__ == self.num1) and (len(self.tokens) == len(self.tokens2))

    def __init__(self, the_str, the_rules={}, the_method=0):
        self.the_str = the_str
        self.__unmatched__ = []
        self.rules = the_rules
        self.method = the_method
        self.other_rules = invert_dict(the_rules)
        self._is_balanced = self.__is_balanced__(the_str)
        
    @property
    def is_balanced(self): 
        return self._is_balanced and self.isvalid

    @property
    def unmatched(self): 
        for k,v in self.d.items():
            if (k in self.rules.keys()):
                closer = self.rules[k]
                if (closer not in self.d.keys()):
                    self.__unmatched__.append(closer)
            elif (k in self.other_rules.keys()):
                opener = self.other_rules[k]
                if (opener not in self.d.keys()):
                    self.__unmatched__.append(opener)
        return list(set(self.__unmatched__))


    @property
    def is_matched(self):
        """
        Finds out how balanced an expression is.
        With a string containing only brackets.

        >>> is_matched('[]()()(((([])))')
        False
        >>> is_matched('[](){{{[]}}}')
        True
        """
        expression = self.the_str
        opening = tuple('({[')
        closing = tuple(')}]')
        mapping = dict(zip(opening, closing))
        queue = []

        for letter in expression:
            if letter in opening:
                queue.append(mapping[letter])
            elif letter in closing:
                if not queue or letter != queue.pop():
                    return False
        return not queue


    @property
    def isvalid(self):
        s = self.the_str
        brackets = ['{}{}'.format(k, self.rules.get(k)) for k in self.rules]
        while any(x in s for x in brackets):
            for br in brackets:
                s = s.replace(br, '')
        self.__notvalid__ = s
        return not s    

    @property
    def invalid_items(self):
        return self.__notvalid__

    @property
    def string(self):
        return self.the_str

if (__name__ == '__main__'):
    print('BEGIN: Analysis of Methods')
    results1 = []
    for c in cases:
        o0 = Balancer(c[0], the_rules=__rules__, the_method=0)
        o1 = Balancer(c[0], the_rules=__rules__, the_method=1)
        
        if (not o0.isvalid):
            print('*** the string -> {}'.format(o0.string))
            print('*** is_balanced ({}) -> {}, unmatched -> {}'.format(o0.method, o0.is_balanced, o0.unmatched))
            print('*** is_balanced ({}) -> {}, unmatched -> {}'.format(o1.method, o1.is_balanced, o1.unmatched))
            print('*** is_matched -> {} {}'.format(o0.is_matched, o1.is_matched))
            print('*** invalid_items -> {}'.format(o0.invalid_items))
            assert o0.isvalid == c[-1], 'isvalid Fails.'
            print('')
    print('END: Analysis of Methods')


    if (0):
        print('BEGIN: Method #1')
        results1 = []
        for c in cases:
            o = Balancer(c[0], the_rules=__rules__, the_method=0)
            oo = Balancer(c[0], the_rules=__rules__, the_method=1)
            __is__ = o.is_balanced
            is_b = __is__ == c[-1]
            reasons = []
            the_reason = 'Balanced.'
            if (not __is__):
                if (len(o.unmatched) > 0):
                    reasons.append('Unmatched %s' % (o.unmatched))
                the_reason = "%s" % (', '.join(reasons) if (len(reasons) > 0) else '')
            results1.append('is_balanced("%s") --> %s :: %s :: %s :: %s' % (c[0], __is__, is_b, the_reason, '' if (is_b) else "*** ERROR, Will Robinson."))
            print('*** is_balanced -> {} {}, unmatched -> {}'.format(o.is_balanced, oo.is_balanced, oo.unmatched))
            print('*** is_matched -> {}'.format(o.is_matched))
            assert o.is_matched == c[-1], 'isvalid Fails.'
            print('*** isvalid -> {}'.format(o.isvalid))
            assert o.isvalid == c[-1], 'isvalid Fails.'
            print('')
        print('END: Method #1')

        print('BEGIN: Method #2')
        results2 = []
        for c in cases:
            o = Balancer(c[0], the_rules=__rules__, the_method=1)
            __is__ = o.is_balanced
            is_b = __is__ == c[-1]
            reasons = []
            the_reason = 'Balanced.'
            if (not __is__):
                if (len(o.unmatched) > 0):
                    reasons.append('Unmatched %s' % (o.unmatched))
                the_reason = "%s" % (', '.join(reasons) if (len(reasons) > 0) else '')
            results2.append('is_balanced("%s") --> %s :: %s :: %s :: %s' % (c[0], __is__, is_b, the_reason, '' if (is_b) else "*** ERROR, Will Robinson."))
        print('END: Method #2')

        print('Perform Comparison of Methods.')
        if (len(results1) == len(results2)):
            print('Both methods produced the same number of results.')
        else:
            print('WARNING 1: Results differ for both methods.')

        warnings = 0
        for i in range(len(results1)):
            if (results1[i] != results2[i]):
                print('WARNING 2: Results differ for Line No. %s' % (i))
                warnings += 1
                
        print('There were %s warnings.%s' % (warnings, ' So both methods are identical.' if (warnings == 0) else ' Which means both methods are NOT identical.'))
        lineno = 1
        for r in results1:
            print('%s --> %s' % (lineno, r))
            lineno += 1
            
        print('Run Analysis Complete.')
