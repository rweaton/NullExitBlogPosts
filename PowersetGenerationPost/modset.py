class ModSet():
    
    # Instance constructor
    def __init__(self, setElement):
        self.val = setElement  # set arg saved in .val attribute
    
    # String eval representation of self instance 
    def __repr__(self):
        return self.val.__repr__() # Return string eval represent.
                                   # of string object in .val
    
    # Method to make a copy of self instance
    def __copy__(self):
        return ModSet(self.val)
    
    # Modify .val to contain the set of itself, of itself, ...
    # nesting .val "depth" number of levels.
    def pushDown(self, depth):
        while depth > 0:
            self.val = set([ModSet(self.val)])
            depth -= 1     
    
    # Remove one nesting level from set in self.val.
    # If un-nested, ignore.
    def pullUpOneLevel(self):
        listSet = list(self.val)
        if len(listSet) == 1:
            self.val = listSet[0].val
        else:
            pass
    
    # Remove "height" nesting levels from set in
    # self.val by repeatedly calling above method
    def pullUp(self, height):
        while height > 0:
            self.pullUpOneLevel()
            height -= 1
    
    # Within a single set, multiple ModSets with 
    # equivalent .val attributes can exist.  
    # This can occur because each instance of ModSet
    # allocated its own location in memory. For sets
    # to have unique members in terms of ModSet.val
    # values, we define the following filtering method.
    def removeDuplicates(self):
        uniqueSet = set()  # initialize as empty the unique set to be built
        for s in self.val:  # s is a member of the ModSet().val set
            inUniqueSet = False  # initialize match detection flag as false
            sTest = s  # default conditional testing value for s
            for us in uniqueSet: # us is a member of the uniqueSet set
                usTest = us  # default conditional testing value for us
                if isinstance(us, ModSet): # if member us is a ModSet
                    usTest = us.val        # change testing value to its attribute
                if isinstance(s, ModSet):  # if member s is a ModSet
                    sTest = s.val          # change testing value to its attribute
                if usTest == sTest:  # compare us and s testing values on this run
                    inUniqueSet = True  # if match, set existence flag to true
            if not inUniqueSet:    # only add member s to uniqueSet if
                uniqueSet.add(s)   # match is NOT detected
        self.val = uniqueSet    # set .val to the uniqueSet from above
    
    # union join multiple items, enforce that ModSet members be unique
    def union(self, *modSets):
        for modSet in modSets:
            self.val = self.val.union(modSet.val)  # this is union method from set class
            self.removeDuplicates()  # removes duplicate-valued instances of ModSet members
    
    # set intersect multiple items
    def intersection(self, *modSets):
        for modSet in modSets:
            self.val = self.val.intersection(modSet.val)
    
    # set difference multiple items. note: arg order matters here! 
    def difference(self, *modSets):
        for modSet in modSets:
            self.val = self.val.difference(modSet.val)
    
    # version of above method that returns a new instance,
    # only takes two arguments.
    def diffFunc(modSet1, modSet2):
        return ModSet(set.difference(modSet1.val, modSet2.val))
    
    # Generate powerset via direct, binary mask approach
    def powerSet_bin(self):
        
        ## Initialize local variables ##
        S = list(self.val)         # convert to list for indexing
        setSize = len(self.val)    # count number of members in source set
        psetSize = pow(2, setSize) # calculate the number of elements in the power set
        lastIndex = setSize - 1    # index value of last member
        setIndices = range(0, setSize)  # make indices list for source set
        psetIndices = range(0, psetSize) # make indices list for power set to be built
        bMasks = [[False for s in setIndices] for p in psetIndices] # Initialize binary mask       
        pSet = ModSet(set())  # initialize power set as empty ModSet() instance
        pSet.pushDown(1)  # and nest it down one level for later joining
        
        ## Populate powerset with each subset, one at a time ##
        for i in psetIndices: # loop through each member of power set
            
            ## Generate binary mask for subset i of power set ##
            val = i  # assign current pSet index as current "value" of mask 
            for j in setIndices: # loop through each bit-digit of mask
                
                if (val >= pow(2, lastIndex - j)):  # if mask value >= value of current bit,
                    bMasks[i][lastIndex - j] = True # then set corresp. mask bit to "true"
                    val -= pow(2, lastIndex - j)    # subtract value of current bit from
                                                    # mask value to determine next bit-digit
            ## Form subset i of power set ##
            # Use generator expression for compactness
            dummySet = ModSet(set([S[k] for k in setIndices if bMasks[i][k] == True]))
            dummySet.pushDown(1)  # nest ModSet instance down one level for union join
            pSet.union(dummySet)  # include new subset in power set
            
        return pSet, bMasks  # return complete power set and binary masks as output
    
    # Generate powerset recursively.
    def powerSet_rec(self):
        
        pSet = self.__copy__()      # Preserve self instance; its copy, pSet
                                    # will be altered
        pSet.pushDown(1)            # Nest pSet for later joining.
              
        if len(self.val) > 0:       # Recursion termination condition
            for elSet in self.val:  # Iterate through members of set self.val
                # Generate subset that remains after removing current
                # element, elSet, from set self.val
                dummySet = self.diffFunc(ModSet(set([elSet]))) 
                # To current powerset, append the powerset of the
                # subset from previous step
                pSet.union(dummySet.powerSet_rec())  # Self-call powerset method,
                                                     # union join powerset of 
                                                     # dummySet with pSet
            return pSet             # Return powerset at current 
                                    # level of recursion
        else:
            dummySet = ModSet(set())  # Generate instance of ModSet of empty set
            dummySet.pushDown(1)      # Nest empty set down one level so it can
            return dummySet           # be union joined in the recursion level
                                      # above that called this run-through.

    def powerSet_mix(self):  # self.val is a set with reg. elements
        
        if len(self.val) > 0:  # if self.val is not empty do the following

            el = list(self.val)[-1] # obtain last element of self.val set
            el = ModSet(set([el])) # insert element within a ModSet
            T = self.diffFunc(el) # get ModSet complement of self by set-subtracting el
            pSet = T.powerSet_mix() # self-call to obtain power set of ModSet complement
            # copy the power set of complement, need it kept unaltered from subsequent mods
            extSet = ModSet(set([i.__copy__() for i in pSet.val])) # element-by-element copy
            for s in extSet.val: # iterate through each subset in the power set of complement
                s.union(el) # union-join the stripped element to each member subset
            extSet.union(pSet) # union-join modified extSet to power set of complement
            return extSet # return result which is power set of self
        
        else:  # if self.val is empty
            dummySet = ModSet(set())  # construct ModSet of empty
            dummySet.pushDown(1) # nest down 1 level
            return dummySet # return power set (nested ModSet instance) that 
                            # includes only singleton subset as member