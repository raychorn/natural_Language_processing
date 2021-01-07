"""
This approach makes use of Natural Language Processing with a bit of Machine Learning (if I had chosen to implement this to generate the Rules).
"""
import sys

cases = []
if (1):
    cases.append(tuple(["[(])", False]))
else:
    cases.append(tuple(["([}{])", False]))
    cases.append(tuple(["([{}])", True]))
    cases.append(tuple(["[()]", True]))

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
    def __init__(self, the_str, the_rules={}, the_method=0):
        self.the_str = the_str
        self.rules = the_rules
        self.other_rules = invert_dict(the_rules)

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

    @invalid_items.setter
    def invalid_items(self, v):
        self.__notvalid__ = v
        
    @property
    def string(self):
        return self.the_str
    
    @string.setter
    def string(self, v):
        self.the_str = v
    
    @property
    def autocorrect(self):
        o = Balancer(self.invalid_items, the_rules=self.rules)
        o.invalid_items = self.invalid_items
        i = 0
        n = len(o.invalid_items)
        corrections = []
        while (i < n):
            s = o.string
            revs = ['{}{}'.format(k,v) for k,v in dict(zip(self.other_rules.keys(), self.other_rules.values())).items()]
            while any(x in s for x in revs):
                for br in revs:
                    if (s.find(br) > -1):
                        corrections.append({'*': br})
                        s = s.replace(br, '')
            print('(1) {}'.format(o.string))
            ch = o.invalid_items[i]
            chR = self.other_rules.get(ch)
            if (not chR):
                chL = self.rules.get(ch)
                if (chL) and (o.invalid_items.find(chL) == -1):
                    corrections.append({ch:chL})
                    o.string = o.string + chL
                    print('(1.1) {} -> {}'.format(corrections[-1], o.string))
            elif (o.invalid_items.find(chR) == -1):
                corrections.append({ch:chR})
                o.string = chR + o.string
                print('(1.2) {} -> {}'.format(corrections[-1], o.string))
            i += 1
            if (o.isvalid):
                print('(3) {}'.format(o.string))
                print('(3.1) corrections -> {}'.format(corrections))
                print()
                break
            else:
                print('(2) {}'.format(o.string))
                print()
        print('*** corrections -> {}'.format(corrections))
        assert len(corrections) > 0, 'Failed to find any corrections for {}.'.format(o.string)
        return self.the_str
    
    

if (__name__ == '__main__'):
    print('BEGIN: Analysis')
    results1 = []
    for c in cases:
        o = Balancer(c[0], the_rules=__rules__)
        
        if (not o.isvalid):
            print('*** the string -> {}'.format(o.string))
            assert o.isvalid == c[-1], 'isvalid Fails.'
            print('*** invalid_items -> {}'.format(o.invalid_items))
            o.autocorrect
            print('')
    print('END: Analysis')
