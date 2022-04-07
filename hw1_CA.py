#!/usr/bin/env python
# coding: utf-8

# In[74]:


import random
import numpy as np #only using for base 3 conversion
from matplotlib import pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


def page_printer(data, start=0, screen_lines=0, pager_cmd=None):
    if isinstance(data, dict):
        data = data['text/plain']
    print(data)

import IPython.core.page
IPython.core.page.page = page_printer


# In[284]:


rule_number = 10
length = 100
time = 100 

# make the initial condition
initial_condition = []
for i in range(length):
    initial_condition.append(random.randint(0,1))

# create list of neighborhood tuples in lex. order
neighborhoods = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]

# convert the rule number to binary and padd with 0s as needed
in_binary = bin(rule_number)[2:][::-1]
binary_length = len(in_binary)
if binary_length != 8:
    padding = 8 - binary_length
    in_binary = in_binary + '0'*padding

# create the lookup table dictionary
lookup_table = {}
for i in range(8):
    key = neighborhoods[i]
    val = in_binary[i]
    lookup_table.update({key:val})
    
# initialize spacetime field and current configuration
spacetime_field = [initial_condition]
current_configuration = initial_condition.copy()

# apply the lookup table to evolve the CA for the given number of time steps
for t in range(time):
    new_configuration = []
    for i in range(len(current_configuration)):
        
        neighborhood = (current_configuration[(i-1)], 
                        current_configuration[i], 
                        current_configuration[(i+1)%length])
        
        new_configuration.append(int(lookup_table[neighborhood]))
        
    current_configuration = new_configuration
    spacetime_field.append(new_configuration)
    
# plot the spacetime field diagram
plt.figure(figsize=(12,12))
plt.imshow(spacetime_field, cmap=plt.cm.Greys, interpolation='nearest')
plt.show()


# # No functions

# In[343]:


#IC
length = 100
time = 100

initial_condition = []
for i in range(length):
    initial_condition.append(random.randint(0,2))


# create list of neighborhood tuples in lex. order
neighborhoods = [(0,0), (0,1), (0,2),
                 (1,0), (1,1), (1,2),
                 (2,0), (2,1), (2,2)]
 


# base3  idea to have rule number instead of type list explicitly 
# convert the rule number to base 3 and pad with 0s as needed
rule = 3**9 -3**4 +1  # decimal

if rule > 3**9:
    raise ValueError('rule must be less than 3^9')
    
ternary = np.base_repr(rule,base=3)
print(type(ternary))
ternary_length = len(ternary)
if ternary_length != 9:
    padding = 9 - ternary_length
    ternary = '0'*padding + ternary 
print(ternary)

rule_list = [x for x in ternary]
print('rule list')
print(rule_list)
    

lookup_table = {}
for i in range(9):
    key = neighborhoods[i]
    val = rule_list[i]
    lookup_table.update({key:val})
if 1: #print rule 
    print()
    print('rule table')
    for key, val in lookup_table.items():
        print(key, '-->', val)
    print()




# initialize spacetime field and current configuration
spacetime_field = [initial_condition]
current_configuration = initial_condition.copy()

print('current config =',current_configuration)

# apply the lookup table to evolve the CA for the given number of time steps
for t in range(time):
    new_configuration = []
    for i in range(len(current_configuration)):
        neighborhood = (current_configuration[(i-1)], #negative 1 inx is last value (periodic BC)
                        current_configuration[i])
        
        new_configuration.append(int(lookup_table[neighborhood]))
        
    current_configuration = new_configuration
    spacetime_field.append(new_configuration)


print(type(spacetime_field))
print()

# plot the spacetime field diagram
plt.figure(figsize=(12,12))
plt.imshow(spacetime_field, cmap=plt.cm.Greys, interpolation='nearest')
plt.show()


# ### With classes and functions

# In[378]:


class CA:
    def __init__(self, rule, size, ic = []):
        
        #Make sure all inputs are valid
        ###################################################
        if rule > 3**9 or rule <= 0:
            raise ValueError('rule must be between 0 and 3^9')
        elif not isinstance(rule, int):
            raise TypeError('rule must be an int')
        else:
            self._rule = rule
            
        if size < 0:
            raise ValueError('size must be < 0 ')
        elif not isinstance(size, int):
            raise TypeError('size must be an int')
        else:
            self._size = size
        
        if len(ic) != size and not len(ic) == 0:
            raise ValueError('ic must be length size')
        elif not isinstance(ic, list):
            raise TypeError('ic must be a list')
        else:
            self._ic = ic
        
        #if no ic, assign randomly
        if self._ic == []: 
            for i in range(length):
                self._ic.append(random.randint(0,2))
        ###################################################
        
        #init spacetime field
        self._spacetime_field = [self._ic]
        self._current_configuration = self._ic.copy()
        self._new_configuration = []
    
    def rule_to_ternary(self, rule):
        '''
        Returns 
        --------
        List
            Ternary representation of rule
        --------
        '''
        ternary = np.base_repr(rule,base=3)
        ternary_length = len(ternary)
        if ternary_length != 9:
            padding = 9 - ternary_length
            ternary = '0'*padding + ternary 
        return(ternary)
    
    
    def gen(self, timeSteps):
        _ternary = self.rule_to_ternary(300)
        _rule_list = [x for x in _ternary]
        # create list of neighborhood tuples in lex. order
        _neighborhoods = [(0,0), (0,1), (0,2),
                 (1,0), (1,1), (1,2),
                 (2,0), (2,1), (2,2)]
        _lookup_table = {}
        for i in range(9):
            _key = _neighborhoods[i]
            _val = _rule_list[i]
            _lookup_table.update({_key:_val})
        
        if 0: #print rule 
            print()
            print('rule table')
            for _key, _val in _lookup_table.items():
                print(_key, '-->', _val)
            print()
            
        for t in range(timeSteps):
            for i in range(len(self._current_configuration)):
                _neighborhood = (self._current_configuration[(i-1)], #negative 1 inx is last value (periodic BC)
                                self._current_configuration[i])
            self._new_configuration.append(int(_lookup_table[_neighborhood]))
            self._current_configuration = self._new_configuration
        print(type(self._spacetime_field.append(self._new_configuration)))
        return(self._spacetime_field.append(self._new_configuration))

    
    #getters and setters
    def get_rule(self):
        return self._rule
    
    def set_rule(self, r):
        if r > 3**9 or r <= 0:
            raise ValueError('rule must be between 0 and 3^9')
        elif not isinstance(r, int):
            raise TypeError('rule must be an int')
        else:
            self._rule = r

    def get_size(self):
        return self._size
    
    def set_size(self, s):
        if s <= 0:
            raise ValueError('size must be > 0')
        elif not isinstance(s, int):
            raise TypeError('size must be an int')
        else:
            self._size = s


# In[379]:


my_CA = CA(3, 4)


# In[376]:


print(type(my_CA.gen(5)))
      
plt.figure(figsize=(12,12))
plt.imshow(my_CA.gen(5), cmap=plt.cm.Greys, interpolation='nearest')
plt.show()


# In[224]:

 
my_CA.set_size(309)


# In[226]:


my_CA.get_size()


# In[ ]:



