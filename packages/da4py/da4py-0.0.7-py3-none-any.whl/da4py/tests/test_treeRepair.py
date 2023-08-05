from unittest import TestCase
from pm4py.objects.petri.importer import importer as importer
from pm4py.objects.log.importer.xes import importer as xes_importer
import da4py.main.repair.treeRepair as treeRepair

from pm4py.visualization.petrinet import factory as vizu

class TestTreeRepair(TestCase):
    net, m0, mf = importer.apply("../../examples/tiny/A-B.pnml")
    log = xes_importer.apply("../../examples/tiny/4ABC_repair.xes")


    def testAddandCancelTransitionNotInBranch(self):
        '''
        Test function to add a transition not in a Branch
        '''
        placeBeforeTheNewTransition = list(self.m0.keys())[0]

        # add transition
        history = treeRepair.addTransition(self.net,self.m0,self.mf,("NEWT",placeBeforeTheNewTransition))
        self.assertIn("NEWT", [x.label for x in self.net.transitions])
        self.assertIn("NEWT", [outarc.source.label for outarc in placeBeforeTheNewTransition.in_arcs])

        # cancel action
        treeRepair.cancelAction(self.net, self.m0,self.mf,history)
        self.assertNotIn("NEWT", [x.label for x in self.net.transitions])


    def testRemoveCancelTransition(self):
        '''
        Test function to remove a transition not in a Branch/choice
        '''
        endPlace = list(self.mf.keys())[0]
        toRemove = list(endPlace.in_arcs)[0].source

        # remove transition
        history = treeRepair.removeTransition(self.net,self.m0,self.mf,toRemove)
        self.assertNotIn(toRemove, self.net.transitions)

        # cancel action
        treeRepair.cancelAction(self.net, self.m0,self.mf,history)
        self.assertIn(toRemove, self.net.transitions)

    def testAddandCancelTransitionInBranch(self):
        '''
        Test function to remove a transition in a new Branch
        '''
        placeBeforeTheNewTransition = list(self.m0.keys())[0]
        history = treeRepair.addInBranchTransition(self.net,self.m0,self.mf,("NEWT",placeBeforeTheNewTransition))
        self.assertIn("NEWT", [outarc.target.label for outarc in placeBeforeTheNewTransition.out_arcs])

        # cancel action
        treeRepair.cancelAction(self.net, self.m0,self.mf,history)
        self.assertNotIn("NEWT", [x.label for x in self.net.transitions])


    def testRemoveInBranch(self):
        placeBeforeTheNewTransition = list(self.m0.keys())[0]
        treeRepair.addInBranchTransition(self.net,self.m0,self.mf,("NEWT",placeBeforeTheNewTransition))
        transitionToRemove = [x for x in self.net.transitions if x.label=="NEWT"][0]
        treeRepair.removeTransition(self.net,self.m0,self.mf,transitionToRemove)
        vizu.apply(self.net,self.m0,self.mf).view()

