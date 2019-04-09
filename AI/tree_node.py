# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:55:37 2019
@author: KemyPeti
"""

class tree_node():
  
    def __init__(self, parent_node, prior_p):
        self.parent = parent_node; #tree_node
        self.P = prior_p;
        self.children = dict(); #dict of tree_nodes
        self.visits = 0;
        self.Q = 0;
        self.u = 0;
        
    def get_parent(self):
        return self.parent
      
    def get_children(self):
        return self.children
      
    def is_leaf(self):
        return (self.children == dict())

    def is_root(self):
        return (self.parent is None)
    
    def get_value(self, c_puct):
      
        self.u = (c_puct * self.P * np.sqrt(self.parent.visits) /
                  (1 + self.visits))
        
        return self.Q + self.u
      
    def SELECT(self, c_puct):
        """
        Selecting—is process is used to select a node on the tree that has the 
        highest possibility of winning.
        """
        return max(self.children.items(),
                   key=lambda child: child[1].get_value(c_puct))
      
      
    def EXPAND(self, action_priors):
        """
        Expanding — After selecting the right node. Expanding is used to increase
        the options further in the game by expanding the selected node and 
        creating many children nodes. These children nodes are the future moves 
        that can be played in the game.

        The nodes that are not expanded further for the time being are known 
        are leaves.
        """
        for action, prob in action_priors:
            if(action not in self.children):
                self.children[action] = TreeNode(self, prob)
                
    def EXPLORE(self, leaf_value):
        """
        Since nobody knows which node is the best children/ leave from the 
        group. The move which will perform best and lead to the correct answer 
        down the tree. 
        """
        self.visits += 1
        self.Q += 1.0*(leaf_value - self.Q) / self.visits
    
    def UPDATE(self, leaf_value):
        if self.parent:
            self.parent.UPDATE(-leaf_value)
        self.EXPLORE(leaf_value)
      