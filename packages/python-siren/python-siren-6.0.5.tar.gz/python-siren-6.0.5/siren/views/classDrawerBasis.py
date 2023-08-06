import wx, numpy, re
# The recommended way to use wx with mpl is with the WXAgg backend. 
import matplotlib
matplotlib.use('WXAgg')

import matplotlib.pyplot as plt
import scipy.spatial.distance

import matplotlib.colors
from matplotlib.text import Text
from matplotlib.patches import Ellipse
from matplotlib.patches import Polygon

from ..clired.classData import Data
from ..clired.classQuery import SYM, Query
from ..clired.classRedescription import Redescription
from ..clired.classSParts import SSetts
from .classInterObjects import MaskCreator

import pdb

# SPECIAL_BINS = [3, 5, 7, 10, 13]
# SPECIAL_LBLS = ["[3, 4]", "[5, 6]", "[7, 9]", "[10, 12]", "[13, 17]"]
# SPECIAL_BINS = range(3,18) #[3, 5, 7, 10, 13]
# SPECIAL_LBLS = ["%s" % v for v in SPECIAL_BINS]

# SPECIAL_CMAP = "jet"

SPECIAL_BINS, SPECIAL_LBLS, SPECIAL_CMAP = None, None, None

class DrawerBasis(object):

    zorder_sideplot = 5
    wait_delay = 300
    ann_to_right = True
    ann_xy = (-10, 15)
    info_dets = {"px": 0, "py":0, "dx": 10, "dy":10, "va":"bottom", "ha": "left", "ec": "#111111", "alpha": .6}
    
    NBBINS = 20
    ltids_map = {1: "PiYG", 2: "nipy_spectral", 3: "viridis"}
    cmap_name = None
    cmap_default = "jet"

    CMAP_DEF_COLOR = "#aaaaaa"
    
    @classmethod
    def getNamesTids(tcl):
        return Data.getNamesTids()
    @classmethod
    def getTidForName(tcl, name):
        return Data.getTidForName(name)
    @classmethod
    def isTypeId(tcl, tid, name, default_accept=False):
        return Data.isTypeId(tid, name, default_accept)

    
    @classmethod
    def getCMap(tcl, ltid=0, name_over=None):
        if name_over is not None:
            if isinstance(name_over, matplotlib.colors.Colormap):
                return name_over
            return plt.get_cmap(name_over)
        if tcl.cmap_name is not None:
            return plt.get_cmap(tcl.cmap_name)
        return plt.get_cmap(tcl.ltids_map.get(ltid, tcl.cmap_default))

    @classmethod
    def prepMapper(tcl, vmin=0, vmax=1, ltid=0, name_over=None):
        cmap = tcl.getCMap(ltid, name_over)            
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
        return matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    def __init__(self, view):
        self.view = view
        self.call_wait = None
        self.elements = {"active_info": False, "act_butt": [1]}
        self.initPlot()
        self.plot_void()
        
    def initPlot(self):
        self.setAxe(self.getFigure().add_subplot( 111 ))
        
    def draw(self):
        self.getLayH().draw()
    def setFocus(self):
        self.getLayH().setFocus()

    def getVecAndDets(self, inter_params=None):
        vec = self.getPltDtH().getVec()
        vec_dets = self.getPltDtH().getVecDets(inter_params)
        return vec, vec_dets
        
    def update(self, more=None):
        if self.view.wasKilled():
            return

        if self.readyPlot():
            
            self.clearPlot()
            self.makeBackground()
            inter_params = self.getParamsInter()
            vec, vec_dets = self.getVecAndDets(inter_params)
            draw_settings = self.getDrawSettings()
            selected = self.getPltDtH().getUnvizRows()


            self.dots_draw, mapper = self.prepareDotsDraw(vec, vec_dets, draw_settings)
            if len(selected) > 0 and "fc_dots" in self.dots_draw:
                selp = inter_params.get("slide_opac", 50)/100.
                self.dots_draw["fc_dots"][numpy.array(list(selected)), -1] *= selp
                self.dots_draw["ec_dots"][numpy.array(list(selected)), -1] *= selp

            if "draw_dots" in self.dots_draw:
                draw_indices = numpy.where(self.dots_draw["draw_dots"])[0]
            else:
                draw_indices = []
            if self.plotSimple(): ##  #### NO PICKER, FASTER PLOTTING.
                self.plotDotsSimple(self.getAxe(), self.dots_draw, draw_indices, draw_settings)
            else:
                self.plotDotsPoly(self.getAxe(), self.dots_draw, draw_indices, draw_settings)

            corners = self.getAxisCorners()
            if mapper is not None:
                corners = self.plotMapperHist(self.axe, vec, vec_dets, mapper, self.NBBINS, corners, draw_settings)

            self.makeFinish(corners)
            self.updateEmphasize(review=False)
            self.draw()
            self.setFocus()
        else:
            self.plot_void()      

    def prepareDotsDraw(self, vec, vec_dets, draw_settings):
        if self.getPltDtH().isSingleVar():
            dots_draw, mapper = self.prepareDotsDrawOther(vec, vec_dets, draw_settings)
        else:
            dots_draw = self.prepareDotsDrawSupp(vec, vec_dets, draw_settings)
            mapper = None
        return dots_draw, mapper
            
    ### IMPLEMENT
    def isEntitiesPlt(self):
        return False
    def isRedPlt(self):
        return False

    def inCapture(self, event):
        return event.inaxes == self.getAxe()   
    def readyPlot(self):
        return True
    def readyCoords(self):
        return self.readyPlot()        
    def getAxisCorners(self):
        return (0,1,0,1)
    def setAxisLims(self, xylims, bxys=None):
        self.axe.axis([xylims[0], xylims[1], xylims[2], xylims[3]])

    def drawPoly(self):
        return False
    def plotSimple(self):
        return not self.drawPoly()
    def adjust(self):
        pass

    def makeBackground(self):   
        pass
    def makeFinish(self, xylims=(0,1,0,1), bxys=None):
        self.setAxisLims(xylims, bxys)
    def updateEmphasize(self, review=True):
        if self.hasParent() and self.isEntitiesPlt():
            lids = self.getParentViewsm().getEmphasizedR(vkey=self.getId())
            self.emphasizeOnOff(turn_on=lids, turn_off=None, review=review)
    def emphasizeOnOff(self, turn_on=set(), turn_off=set(), hover=False, review=True):
        pass
        
    def clearPlot(self):
        axxs = self.getFigure().get_axes()
        for ax in axxs:
            ax.cla()
            if ax != self.getAxe():
                self.getFigure().delaxes(ax)
        self.clearHighlighted()
        self.clearInfoText()
    def clearHighlighted(self):
        ### IMPLEMENT
        pass
        
    def getId(self):
        return self.view.getId()
    def hasParent(self):
        return self.view.hasParent()
    def getParent(self):
        return self.view.getParent()
    def getLayH(self):
        return self.view.getLayH()
    def getPltDtH(self):
        return self.view.getPltDtH()
    def getParentData(self):
        return self.view.getParentData()
    def getParentViewsm(self):
        return self.view.getParentViewsm()
    def getDrawSettDef(self):
        return self.view.getDrawSettDef()
    def getDrawSettings(self):
        return self.view.getDrawSettings()
    def getVec(self, more=None):
        return self.getPltDtH().getVec(more)
    
    def getFigure(self):
        return self.getLayH().getFigure()
    def getAxe(self):
        return self.axe
    def setAxe(self, value):
        self.axe = value

    def delElement(self, key):
        if key in self.elements:
            del self.elements[key]
    def setElement(self, key, value):
        self.elements[key] = value
    def getElement(self, key):
        return self.elements[key]
    def hasElement(self, key):
        return key in self.elements
        
    def getSettV(self, key, default=False):
        return self.view.getSettV(key, default)    

    def makeAdditionalElements(self, panel=None):
        return []

    #### SEC: INTERACTIVE ELEMENTS
    ###########################################

    def prepareInteractive(self, panel=None):
        self.setElement("buttons", [])
        self.setElement("inter_elems", {})
        boxes = self.makeAdditionalElements(panel)
        self.interBind()
        self.setElement("ellipse", Ellipse((2, -1), 0.5, 0.5))
        for act, meth in self.getCanvasConnections():
            if act == "MASK":
                self.setElement("mask_creator", MaskCreator(self.getAxe(), None, buttons_t=[], callback_change=self.view.makeMenu))
            else:
                self.getFigure().canvas.mpl_connect(act, meth)
        self.prepareActions()
        self.setKeys()
        return boxes
    def getCanvasConnections(self):
        return []
    def interBind(self):
        for button in self.getElement("buttons"):
            button["element"].Bind(wx.EVT_BUTTON, button["function"])
        for name, elem in self.getElement("inter_elems").items():
            if re.match("slide", name):
                elem.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSlide)
            if re.match("choice", name):
                elem.Bind(wx.EVT_CHOICE, self.OnChoice)
                
    def getParamsInter(self):
        inter_params = {} 
        for name, elem in self.getElement("inter_elems").items():        
            if re.match("slide", name):
                inter_params[name] = elem.GetValue()
            if re.match("choice", name):
                inter_params[name] = elem.GetSelection()
        return inter_params

    def getInterElements(self):
        return self.getElement("inter_elems")
        
    def OnSlide(self, event):
        self.update()
    def OnChoice(self, event):
        self.update()
                
    #### SEC: ACTIONS
    ###########################################
    def hasToolbActive(self):
        return self.getLayH().getToolbar().has_active_button()

    def getActionsDetails(self):
        details = []
        for action, dtl in self.actions_map.items():        
            details.append({"label": "%s[%s]" % (dtl["label"].ljust(30), dtl["key"]),
                            "legend": dtl["legend"], "active": dtl["active_q"](),
                            "key": dtl["key"], "order": dtl["order"], "type": dtl["type"]})
        if self.hasElement("mask_creator"):
            details.extend(self.getElement("mask_creator").getActionsDetails(6))
        return details
    def prepareActions(self):
        self.actions_map = {}
    def OnMenuAction(self, event):
        if event.GetId() in self.menu_map_act:
            self.doActionForKey(self.menu_map_act[event.GetId()])
    def OnMenuMCAction(self, event):
        if self.hasElement("mask_creator") and event.GetId() in self.menu_map_act:
            self.getElement("mask_creator").doActionForKey(self.menu_map_act[event.GetId()])
    def makeActionsMenu(self, frame, menuAct=None):
        self.menu_map_act = {}
        if menuAct is None:
            menuAct = wx.Menu()
        for action in sorted(self.getActionsDetails(), key=lambda x:(x["order"],x["key"])):
            ID_ACT = wx.NewId()
            if action["type"] == "check":
                m_act = menuAct.AppendCheckItem(ID_ACT, action["label"], action["legend"])
                frame.Bind(wx.EVT_MENU, self.OnMenuAction, m_act)
                self.menu_map_act[ID_ACT] = action["key"]
                if action["active"]:
                    m_act.Check()
            else:
                m_act = menuAct.Append(ID_ACT, action["label"], action["legend"])
                if action["active"]:
                    if action["type"] == "mc":
                        frame.Bind(wx.EVT_MENU, self.OnMenuMCAction, m_act)
                    else:
                        frame.Bind(wx.EVT_MENU, self.OnMenuAction, m_act)
                    self.menu_map_act[ID_ACT] = action["key"]
                else:
                    menuAct.Enable(ID_ACT, False)
        if menuAct.GetMenuItemCount() == 0:
            self.getParent().appendEmptyMenuEntry(menuAct, "No Actions", "There are no edit actions.")
        return menuAct

    ################ HANDLING KEY ACTIONS
    def setKeys(self, keys=None):
        self.keys_map = {}
        if keys is None:
            for action, details in self.actions_map.items():
                details["key"] = action[0]
                self.keys_map[details["key"]] = action
        else:
            for action, details in self.actions_map.items():
                details["key"] = None
            for key, action in keys.items():
                if action in self.actions_map:
                    self.actions_map[action]["key"] = key
                    self.keys_map[key] = action
    def doActionForKey(self, key):
        if self.keys_map.get(key, None in self.actions_map):
            act = self.actions_map[self.keys_map[key]]
            if act["type"] == "check" or act["active_q"]():
                self.actions_map[self.keys_map[key]]["method"](self.actions_map[self.keys_map[key]]["more"])
                return True
        return False
    def key_press_callback(self, event):
        self.doActionForKey(event.key)
    def mkey_press_callback(self, event):
        self.doActionForKey(chr(event.GetKeyCode()).lower())

    ################ ACTIONS QUERIES
    def q_has_poly(self):
        return self.hasElement("mask_creator") and self.getElement("mask_creator").q_has_poly()

    def q_active_poly(self):
        return self.hasElement("mask_creator") and self.getElement("mask_creator").isActive()

    def q_active_info(self):
        return self.getElement("active_info")

    def q_true(self):
        return True

    def q_not_svar(self):
        return not self.getPltDtH().isSingleVar()
    def q_not_basis(self):
        if self.getPltDtH().isSingleVar():
            if self.getPltDtH().getRed() is not None:
                return self.getPltDtH().getRed().isXpr()
            return True
        return False
    def q_has_clusters(self):
        return self.getPltDtH().hasClusters()
    def q_has_selected(self):
        return len(self.getHighlightedIds()) > 0

    ################ ACTIONS FUNCTIONS
    def do_toggle_info(self, event):
        self.setElement("active_info", not self.getElement("active_info"))
    def do_toggle_poly(self, event):
        self.togglePoly()
    def togglePoly(self):
        if self.hasElement("mask_creator"):
             if self.getElement("mask_creator").isActive():
                 self.getElement("mask_creator").setButtons([])
                 self.setElement("act_butt", [1])
             else:
                 self.getElement("mask_creator").setButtons([1])
                 self.setElement("act_butt", [])
             self.view.makeMenu()
             self.getLayH().getToolbar().mouse_move()

    def apply_mask(self, path, radius=0.0):
        if path is not None and self.getCoords() is not None:
            points = numpy.transpose((self.getCoords(0), self.getCoords(1)))
            return [i for i,point in enumerate(points) if path.contains_point(point, radius=radius)]
        return []

    def do_deselect_all(self, more=None):
        if self.isEntitiesPlt():
            self.sendEmphasize(None)

    def do_set_select(self, setp):
        if self.isEntitiesPlt():
            points = [i for (i,p) in enumerate(self.getVec()) if p in setp]
            self.sendEmphasize(points)
                
    def do_select_poly(self, more=None):
        if self.isEntitiesPlt():
            points = self.apply_mask(self.getElement("mask_creator").get_path())
            self.getElement("mask_creator").clear()
            if points != set():
                self.sendEmphasize(points)

    def do_flip_emphasized(self, more=None):
        if self.isEntitiesPlt():
            self.sendFlipEmphasizedR()
    def saveSelVar(self, side=1):
        if self.hasParent() and self.isEntitiesPlt():
            lids = set(self.getParentViewsm().getEmphasizedR(vkey=self.getId()))
            self.getParent().OnSaveVecAsVar(lids, "%s_selection" % self.getParentViewsm().getItemId(self.getId()), side)
    def save_sel_varLHS(self, more=None):
        self.saveSelVar(side=0)
    def save_sel_varRHS(self, more=None):
        self.saveSelVar(side=1)

    def saveClusVar(self, side=1):
        if self.hasParent() and self.isEntitiesPlt():
            if self.getPltDtH().hasQueries() and self.getPltDtH().isSingleVar():
                r = self.getPltDtH().getRed()
                if r is not None and r.isXpr():
                    t = r.getXprTerm()
                    vname = t.getName()
                    if vname is None:
                        vname = "v%d:dyn" % self.getParentData().nbCols(side)
                    col = t.getCol()
                    self.getParent().OnSaveVecAsVar(col, vname, side, "values")
            elif self.getPltDtH().hasClusters():
                vec = self.getPltDtH().getVec()
                if self.getPltDtH().hasQueries():
                    self.getParent().OnSaveVecAsVar(vec, "%s_support" % self.getParentViewsm().getItemId(self.getId()), side, "support")
                else:
                    self.getParent().OnSaveVecAsVar(vec, "%s_clusters" % self.getParentViewsm().getItemId(self.getId()), side, "clusters")
    def save_clus_varLHS(self, more=None):
        self.saveClusVar(side=0)
    def save_clus_varRHS(self, more=None):
        self.saveClusVar(side=1)

    #### SEC: FILL and WAIT PLOTTING
    ###########################################
    def plot_void(self):
        if self.view.wasKilled():
            return
        self.clearPlot()
        self.axe.plot([r/10.0+0.3 for r in [0,2,4]], [0.5 for r in [0,2,4]], 's', markersize=10, mfc="#DDDDDD", mec="#DDDDDD")
        self.axe.axis([0,1,0,1])
        self.draw()

    def init_wait(self):
        self.call_wait = wx.CallLater(1, self.plot_wait)
        self.cp = 0

    def kill_wait(self):
        if self.call_wait is not None:
            self.call_wait.Stop()
        if self.view.wasKilled():
            return
        self.clearPlot()
        self.axe.plot([r/10.0+0.3 for r in [1,3]], [0.5, 0.5], 's', markersize=10, mfc="#DDDDDD", mec="#DDDDDD")
        self.axe.plot([r/10.0+0.3 for r in [0,2,4]], [0.5, 0.5, 0.5], 'ks', markersize=10)
        self.axe.axis([0,1,0,1])
        self.draw()

    def plot_wait(self):
        if self.view.wasKilled():
            return
        self.clearPlot()
        self.axe.plot([r/10.0+0.3 for r in range(5)], [0.5 for r in range(5)], 'ks', markersize=10, mfc="#DDDDDD", mec="#DDDDDD")
        self.axe.plot(((self.cp)%5)/10.0+0.3, 0.5, 'ks', markersize=10)
        self.axe.axis([0,1,0,1])
        self.draw()
        self.cp += 1
        self.call_wait.Restart(self.wait_delay)

    def setInfoText(self, text_str):
        if not self.hasElement("info_text"):
            info_text = {}
            ax = self.getAxe()
            dets = self.getInfoDets()
            xlims = ax.get_xlim()
            lx = xlims[0] + dets["px"]*(xlims[1]-xlims[0])
            ylims = ax.get_ylim()
            ly = ylims[0] + dets["py"]*(ylims[1]-ylims[0])
            info_text["text"] = ax.annotate(text_str, xy=(lx, ly), 
                                       xycoords='data', xytext=(dets["dx"], dets["dy"]), textcoords='offset points',
                                       color=dets["ec"], va=dets["va"], ha=dets["ha"], backgroundcolor="#FFFFFF",
                                       bbox=dict(boxstyle="round", facecolor="#FFFFFF", ec=dets["ec"], alpha=dets["alpha"]),
                                       zorder=8, **self.view.getFontProps())
            self.setElement("info_text", info_text)
        else:
            self.getElement("info_text")["text"].set_text(text_str)
        self.draw()

    def clearInfoText(self):
        self.delElement("info_text")
        
    def delInfoText(self):
        if self.hasElement("info_text"):
            self.getElement("info_text")["text"].remove()
            self.delElement("info_text")
        self.draw()
            
    def addStamp(self, pref="", force=False):
        if not self.getPltDtH().hasQueries() or (not force and not self.getSettV("add_stamp")):
            return
        
        if not self.hasElement("red_stamp"):
            old_pos = self.getAxe().get_position()
            new_pos = [old_pos.x0, old_pos.y0,  old_pos.width, 7./8*old_pos.height]
            # # pos2 = [0., 0.,  1., 1.0]
            self.getAxe().set_position(new_pos)
            # pos1 = self.axe.get_position()

        qrs = self.getPltDtH().getQueries()

        red = Redescription.fromQueriesPair(qrs, self.getParentData())
        tex_fields = ["LHS:query:", "RHS:query:", ":acc:", ":perc:Exx"]
        headers = ["qL=", "qR=", "J=", "%supp="]
        if self.getParentData().hasLT():            
            tex_fields.extend(["acc_ratioTL", "len_I_ratioTA"])
            headers.extend(["J$_{I/O}$=", "supp$_{I/A}$="])
        rr = pref
        tex_str = red.disp(self.getParentData().getNames(), list_fields=tex_fields, with_fname=headers, sep=" ", delim="", nblines=3, style="T", fmts=self.getParentData().getFmts()) #, rid=rr)
        if not self.hasElement("red_stamp"):
            red_stamp = {"old_pos": old_pos}
            red_stamp["text"] = self.getAxe().text(0.5, 1.01, tex_str, transform=self.getAxe().transAxes, ha="center", va="bottom", **self.view.getFontProps())
            self.setElement("red_stamp", red_stamp)
        else:
            self.getElement("red_stamp")["text"].set_text(tex_str)
            self.getElement("red_stamp")["text"].update(self.view.getFontProps())
        self.draw()

    def delStamp(self):
        if self.hasElement("red_stamp"):
            red_stamp = self.getElement("red_stamp")
            self.axe.set_position(red_stamp["old_pos"])
            red_stamp["text"].remove()
            self.delElement("red_stamp")
            self.draw()


    
class DrawerEntitiesTD(DrawerBasis):
    
    NBBINS = 20
    MAP_POLY = False
    map_select_supp = [("l", "|E"+SSetts.sym_sparts[SSetts.Exo]+"|", [SSetts.Exo]),
                       ("r", "|E"+SSetts.sym_sparts[SSetts.Eox]+"|", [SSetts.Eox]),
                       ("i", "|E"+SSetts.sym_sparts[SSetts.Exx]+"|", [SSetts.Exx]),
                       ("o", "|E"+SSetts.sym_sparts[SSetts.Eoo]+"|", [SSetts.Eoo])]

    
    def __init__(self, view):
        DrawerBasis.__init__(self, view)
        self.dots_draw = None
    
    def isEntitiesPlt(self):
        return True

    def drawPoly(self):
        return self.getPltDtH().hasPolyCoords() & self.getSettV("map_poly", self.MAP_POLY)
    
    def getAxisCorners(self):
        return self.getPltDtH().getCoordsExtrema()

    
    #### SEC: ACTIONS
    ######################################
    def makeAdditionalElements(self, panel=None):
        if panel is None:
            panel = self.getLayH().getPanel()
        flags = wx.ALIGN_CENTER | wx.ALL # | wx.EXPAND

        buttons = []
        buttons.append({"element": wx.Button(panel, size=(self.getLayH().butt_w,-1), label="Expand"),
                        "function": self.view.OnExpandSimp})
        buttons[-1]["element"].SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        inter_elems = {}
        inter_elems["slide_opac"] = wx.Slider(panel, -1, 10, 0, 100, wx.DefaultPosition, (self.getLayH().sld_w, -1), wx.SL_HORIZONTAL)

        ##############################################
        add_boxB = wx.BoxSizer(wx.HORIZONTAL)
        add_boxB.AddSpacer(self.getLayH().getSpacerWn()/2)

        v_box = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(panel, wx.ID_ANY,u"- opac. disabled +")
        label.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        v_box.Add(label, 0, border=1, flag=flags) #, userData={"where": "*"})
        v_box.Add(inter_elems["slide_opac"], 0, border=1, flag=flags) #, userData={"where":"*"})
        add_boxB.Add(v_box, 0, border=1, flag=flags)

        add_boxB.AddSpacer(self.getLayH().getSpacerWn())
        add_boxB.Add(buttons[-1]["element"], 0, border=1, flag=flags)

        add_boxB.AddSpacer(self.getLayH().getSpacerWn()/2)

        self.setElement("buttons", buttons)
        self.setElement("inter_elems", inter_elems)        
        return [add_boxB]

    def getCanvasConnections(self):
        return [("MASK", None),
                ("key_press_event", self.key_press_callback),
                ("button_release_event", self.on_click),
                ("motion_notify_event", self.on_motion)]
        
    def hoverActive(self):
        return self.getSettV('hover_entities') and not self.hasToolbActive()
    def hoverCoordsActive(self):
        return self.getSettV('hover_coords') and not self.hasToolbActive()    
    def clickActive(self):
        return self.getSettV('click_entities') and not self.hasToolbActive() and not self.q_active_poly()

    def getLidAt(self, x, y):
        if self.drawPoly():
            return self.getLidAtPoly(x, y)
        return self.getLidAtSimple(x, y)
    
    def getLidAtPoly(self, x, y):
        ids_drawn = numpy.where(self.dots_draw["draw_dots"])[0]
        d = scipy.spatial.distance.cdist(self.getCoordsXY(ids_drawn).T, [(x,y)])
        cands = [ids_drawn[i[0]] for i in numpy.argsort(d, axis=0)[:5]]
        i = 0
        while i < len(cands):
            path = Polygon(self.getPltDtH().getCoordsP(cands[i]), closed=True)
            if path.contains_point((x,y), radius=0.0):
                return cands[i]
            i += 1
    
    def getLidAtSimple(self, x, y):
        ids_drawn = numpy.where(self.dots_draw["draw_dots"])[0]
        sz = self.getPlotProp(0, "sz")
        size_dots = self.getLayH().getFigure().get_dpi()*self.getLayH().getFigure().get_size_inches()
        xlims = self.getAxe().get_xlim()
        ylims = self.getAxe().get_ylim()
        ### resolution: value delta per figure dot
        res = ((xlims[1]-xlims[0])/size_dots[0], (ylims[1]-ylims[0])/size_dots[1])

        coords = self.getCoordsXY(ids_drawn)
        for ss in range(3):
            sc = sz*(ss+1)
            tX = numpy.where((coords[0]-sc*res[0] <= x) & (x <= coords[0]+sc*res[0]) & (coords[1]-sc*res[1] <= y) & (y <= coords[1]+sc*res[1]))[0]
            if len(tX) > 0:
                return ids_drawn[tX[0]]
        return None
    
    def on_motion(self, event):
        if self.inCapture(event):
            if self.hoverActive():
                lid = self.getLidAt(event.xdata, event.ydata)
                if lid is None:
                    self.emphasizeOnOff(turn_off=None, hover=True, review=True)
                elif not self.isHovered(lid):
                    self.emphasizeOnOff(turn_on=[lid], turn_off=None, hover=True, review=True)
            elif self.hoverCoordsActive():
                txt = self.getPosInfoTxt(event.xdata, event.ydata)
                if txt is not None:
                    self.setInfoText(txt)
                else:
                    self.delInfoText()
        elif self.hoverCoordsActive():
            self.delInfoText()

    def getPosInfo(self, x, y):
        return (x, y)
    def getPosInfoTxt(self, x, y):
        return "x=% 8.4f, y=% 8.4f" % self.getPosInfo(x, y)

    
    def on_click(self, event):        
        if self.clickActive() and self.inCapture(event):
            lid = self.getLidAt(event.xdata, event.ydata)
            if lid is not None:
                self.sendEmphasize([lid])

    def prepareActions(self):
        ### First letter of action is the key, should be unique
        self.actions_map = {"deselect_all": {"method": self.do_deselect_all, "label": "&Deselect all",
                                             "legend": "Deselect all dots", "more": None, "type": "main",
                                             "order":1, "active_q":self.q_has_selected},
                            "flip_able": {"method": self.do_flip_emphasized, "label": "(Dis)able selected",
                                             "legend": "(Dis)able selected dots", "more": None, "type": "main",
                                             "order":0, "active_q":self.q_has_selected},
                            "noggle_info": {"method": self.do_toggle_info, "label": "Toggle i&nfo",
                                               "legend": "Toggle info", "more": None,  "type": "check",
                                               "order":101, "active_q":self.q_active_info},
                            "vave_sel_varLHS": {"method": self.save_sel_varLHS, "label": "Save selection as LHS variable",
                                               "legend": "Save the selection as a new left-hand side data variable",
                                               "more": None,  "type": "main",
                                               "order":10, "active_q":self.q_has_selected},
                            "wave_sel_varRHS": {"method": self.save_sel_varRHS, "label": "Save selection as RHS variable",
                                               "legend": "Save the selection as a new right-hand side data variable",
                                               "more": None,  "type": "main",
                                               "order":10, "active_q":self.q_has_selected}
                            }


        if self.getPltDtH().hasQueries():
            for setk, setl, setp in self.map_select_supp:
                self.actions_map[setk+"_set"] = {"method": self.do_set_select, "label": "(De)select "+setl,
                                                 "legend": "(De)select dots in "+setl, "more": setp, "type": "main",
                                                 "order":2, "active_q": self.q_not_svar}
                
        if self.getPltDtH().hasClusters():
            w = "clusters"
            if self.getPltDtH().hasQueries():
                w = "supports"

            self.actions_map.update({
                            "xave_clus_varLHS": {"method": self.save_clus_varLHS, "label": "Save %s as LHS variable" % w,
                                               "legend": "Save the %s as a new left-hand side data variable" % w,
                                               "more": None,  "type": "main",
                                               "order":11, "active_q": self.q_has_clusters},
                            "yave_clus_varRHS": {"method": self.save_clus_varRHS, "label": "Save %s as RHS variable" % w,
                                               "legend": "Save the %s as a new right-hand side data variable" % w,
                                               "more": None,  "type": "main",
                                               "order":11, "active_q": self.q_has_clusters}
                })
                
        if self.hasElement("mask_creator"):
            self.actions_map["poly_set"] = {"method": self.do_select_poly, "label": "(De)select &polygon",
                                               "legend": "Select dots inside the polygon", "more": None,  "type": "main",
                                               "order":3, "active_q":self.q_has_poly}
            self.actions_map["toggle_draw"] = {"method": self.do_toggle_poly, "label": "&Toggle polygon",
                                               "legend": "Toggle polygon drawing", "more": None,  "type": "check",
                                               "order":100, "active_q":self.q_active_poly}

        
    #### SEC: HANDLING HIGHLIGHTS
    ###########################################
    def getCoordsXYA(self, idp):
        return self.getPltDtH().getCoordsXYA(idp)
    def getCoordsXY(self, idp):
        return self.getPltDtH().getCoordsXY(idp)
    def getCoords(self, axi=None, ids=None):
        return self.getPltDtH().getCoords(axi, ids)

    def makeEmphTag(self, lid):
        # print(self.getParentData().getRName(lid), ">", self.getPltDtH().pltdt.get("coords")[0][:,lid,0])
        return self.getParentData().getRName(lid)
    
    def emphasizeOn(self, lids, hover=False):
        dsetts = self.getDrawSettings()
        if not self.hasDotsReady():
            return

        hgs = {}
        for lid in self.needingHighlight(lids):
            hg = self.drawEntity(lid, dsetts["colhigh"], self.getPlotColor(lid, "ec"), self.getPlotProp(lid, "sz"), self.getPlotProp(lid, "zord"), dsetts["default"])
            if lid not in hgs:
                hgs[lid] = []
            hgs[lid].extend(hg)
            
        for lid in self.needingHighLbl(lids):
            tag = self.makeEmphTag(lid)
            hg = self.drawAnnotation(self.getCoordsXYA(lid), self.getPlotColor(lid, "ec"), tag, self.getAnnXY())
            if lid not in hgs:
                hgs[lid] = []
            hgs[lid].extend(hg)

        self.addHighlighted(hgs, hover)

    

    def emphasizeOnOff(self, turn_on=set(), turn_off=set(), hover=False, review=True):
        self.emphasizeOff(turn_off, hover)
        self.emphasizeOn(turn_on, hover)
        self.emphasizeSpecial(turn_on, turn_off, hover)
        # if hover:
        self.draw()
        if not hover:
            self.view.makeMenu()
            
    def emphasizeSpecial(self, turn_on=set(), turn_off=set(), hover=False):
        pass
    
    def emphasizeOff(self, lids=None, hover=False):
        self.removeHighlighted(lids, hover)
        
    def sendEmphasize(self, lids):
        return self.getParentViewsm().setEmphasizedR(vkey=self.getId(), lids=lids, show_info=self.q_active_info())

    def sendFlipEmphasizedR(self):        
        return self.getParentViewsm().doFlipEmphasizedR(vkey=self.getId())        

    def initHighlighted(self):
        self.highl = {}
        self.high_lbl = set()
        self.current_hover = {}
    def clearHighlighted(self):
        self.initHighlighted()
    def isHovered(self, iid):
        return iid in self.current_hover
    def isHighlighted(self, iid):
        return iid in self.highl
    def isHighLbl(self, iid):
        return iid in self.high_lbl
    def needingHighLbl(self, iids):
        max_emphlbl = self.getSettV('max_emphlbl', 5)
        if max_emphlbl < 0 or len(iids) <= max_emphlbl:
            return [iid for iid in iids if not self.isHighLbl(iid)]
        return []
    def needingHighlight(self, iids):
        return [iid for iid in iids if not self.isHighlighted(iid)]
    def getHighlightedIds(self):
        return self.highl.keys()
    def addHighlighted(self, hgs, hover=False):
        where = self.highl
        if hover:
            where = self.current_hover

        for iid, high in hgs.items():
            if iid not in where:
                where[iid] = []
            if type(high) is list:
                has_lbl = any([isinstance(t, Text) for t in high])
                where[iid].extend(high)
            else:
                has_lbl = isinstance(high, Text)
                where[iid].append(high)
            if has_lbl and not hover:
                self.high_lbl.add(iid)
                
    def removeHighlighted1(self, iid):
        if iid in self.highl:
            while len(self.highl[iid]) > 0:
                t = self.highl[iid].pop()
                t.remove()
            del self.highl[iid]
            self.high_lbl.discard(iid)
    def removeHover1(self, iid):
        if iid in self.current_hover:
            while len(self.current_hover[iid]) > 0:
                t = self.current_hover[iid].pop()
                t.remove()
            del self.current_hover[iid]
    def removeHighlighted(self, iid=None, hover=False):
        if iid is None:
            if hover:
                iids = self.current_hover.keys()
            else:
                iids = self.highl.keys()
        elif type(iid) is list or type(iid) is set:
            iids = iid
        else:
            iids = [iid]
        for iid in iids:
            if hover:
                self.removeHover1(iid)
            else:
                self.removeHighlighted1(iid)

    #### SEC: PLOTTING
    ###########################################
    def hasDotsReady(self):
        return self.dots_draw is not None

    def getPlotColor(self, idp, prop):
        return tuple(self.dots_draw[prop+"_dots"][idp])
    def getPlotProp(self, idp, prop):
        return self.dots_draw[prop+"_dots"][idp]
    
    def prepareDotsDrawSupp(self,  vec, vec_dets, draw_settings):
        delta_on = draw_settings.get("delta_on", True)
        u, indices = numpy.unique(vec, return_inverse=True)

        styles = []
        for i in u:
            if draw_settings[i]["shape"] in [".",",","*","+","x"]:
                #### point-wise shape -> same color face and edge
                styles.append(draw_settings[i]["color_e"])
            else:
                #### otherwise -> possibly different colors face and edge
                styles.append(draw_settings[i]["color_f"])
        fc_clusts = numpy.array(styles)
        # fc_clusts = numpy.array([draw_settings[i]["color_f"] for i in u])
        fc_dots = fc_clusts[indices]
        ec_clusts = numpy.array([draw_settings[i]["color_e"] for i in u])
        ec_dots = ec_clusts[indices]
        zord_clusts = numpy.array([draw_settings[i]["zord"] for i in u])
        zord_dots = zord_clusts[indices]
            
        delta_dots = vec==SSetts.Eoo
        
        sz_dots = numpy.ones(vec.shape)*draw_settings["default"]["size"]
        sz_dots[~ delta_dots] *= 0.5

        if delta_on:
            draw_dots = numpy.ones(vec.shape, dtype=bool)
        else:
            draw_dots = ~ delta_dots
        return {"fc_dots": fc_dots, "ec_dots": ec_dots, "sz_dots": sz_dots, "zord_dots": zord_dots, "draw_dots": draw_dots}

    
    def prepareDotsDrawOther(self, vec, vec_dets, draw_settings):
        delta_on = draw_settings.get("delta_on", True)

        if SPECIAL_BINS is not None:
            re_vec, re_vec_dets = vec, vec_dets
            vec_dets = {'typeId': 2, 'single': True, 'binVals': None, 'binLbls': None}
            vec = numpy.zeros(re_vec.shape[0], dtype=int)
            for b in SPECIAL_BINS[1:]:
                vec += 1*(re_vec >= b)

        name_over = None
        vmin, vmax = (numpy.nanmin(vec), numpy.nanmax(vec))
        if vec_dets.get("min_max") is not None:
            vmin, vmax = vec_dets["min_max"]

        if draw_settings.get("custom_ccmap") is not None: #### CUSTOM CMAP
            custom_ccmap = draw_settings.get("custom_ccmap")
            if type(custom_ccmap) is str: ### name of color map
                name_over = custom_ccmap
            elif vec_dets.get("binLbls") is not None: ### dict of colors
                ord_vals = [custom_ccmap[i] for i in sorted([k for k in custom_ccmap.keys() if type(k) is int])]
                if len(ord_vals) == 0:
                    ord_vals = [self.CMAP_DEF_COLOR]
                lbls = [l.split()[0] for l in vec_dets.get("binLbls")]
                kys = [k for k in custom_ccmap.keys() if not type(k) is int]
                common_ks = set(lbls).intersection(kys)
                if len(kys) > 0 and len(common_ks) > 0:
                    vls = sorted(zip(vec_dets.get("binVals"), lbls))
                    idx_val = 0
                    colors_list = []
                    for v,c in vls:
                        if c in custom_ccmap:
                            colors_list.append(custom_ccmap[c])
                        else:
                            colors_list.append(ord_vals[idx_val % len(ord_vals)])
                            idx_val += 1
                    vmin, vmax = vls[0][0], vls[-1][0]
                    name_over = matplotlib.colors.ListedColormap(colors_list)
                # else:
                #     print("No custom ccmap key common with clusters...")
                #     print(lbls, kys)

        mapper = self.prepMapper(vmin, vmax, vec_dets["typeId"], name_over)
        
        # if min_max is not None:
        #     mmp = dict([(v, mapper.to_rgba(v, alpha=draw_settings["default"]["color_e"][-1])) for v in numpy.arange(vmin, vmax+1)])
        #     ec_dots = numpy.array([mmp[v] for v in vec])
        # elif vec_dets["typeId"] == 3 or (vmin !=0 and min_max is None):
        if vec_dets["typeId"] == 3 or (vmin !=0 and vec_dets.get("min_max") is None):
            ec_dots = numpy.array([mapper.to_rgba(v, alpha=draw_settings["default"]["color_e"][-1]) for v in vec])
        else:
            mmp = numpy.array([mapper.to_rgba(v, alpha=draw_settings["default"]["color_e"][-1]) for v in numpy.arange(vmin, vmax+1)]+[draw_settings["default"]["color_f"]])
            ec_dots = mmp[vec]
        
        fc_dots = numpy.copy(ec_dots)
        fc_dots[:,-1] = draw_settings["default"]["color_f"][-1]
                                
        dots_draw = {"fc_dots": fc_dots, "ec_dots": ec_dots,
                      "sz_dots": numpy.ones(vec.shape)*draw_settings["default"]["size"],
                      "zord_dots": numpy.ones(vec.shape)*draw_settings["default"]["zord"],
                      "draw_dots": numpy.ones(vec.shape, dtype=bool)}
        mapper.set_array(vec)
        return dots_draw, mapper

    def plotMapperHist(self, axe, vec, vec_dets, mapper, nb_bins, corners, draw_settings):
        if SPECIAL_BINS is not None:
            re_vec, re_vec_dets = vec, vec_dets
            vec_dets = {'typeId': 2, 'single': True, 'binVals': range(len(SPECIAL_BINS)), 'binLbls': SPECIAL_LBLS}
            # vec_dets = {'typeId': 2, 'single': True, 'binVals': None, 'binLbls': None}
            vec = numpy.zeros(re_vec.shape[0], dtype=int)
            for b in SPECIAL_BINS[1:]:
                vec += 1*(re_vec >= b)

        x0, x1, y0, y1 = corners
        bx = (x1-x0)/100. if x0 != x1 else 0.1
        fracts = [.1, .03] ## width of hist, ratio bars adjusted/fixed
        hspan = 0.95 ## height of hist (also used in proj to decide axis lims)
        nb = nb_bins
        idsan = numpy.where(~numpy.isnan(vec))[0]
        uniq = numpy.unique(vec[idsan])
        nb_distinct = len(uniq)
        if vec_dets["binLbls"] is not None:
            if vec_dets.get("binHist") is not None:
                nb = vec_dets["binHist"]
            else:
                if len(vec_dets["binVals"]) > 1:
                    df = max(numpy.diff(vec_dets["binVals"]))
                    nb = [vec_dets["binVals"][0]]+[(vec_dets["binVals"][i]+vec_dets["binVals"][i+1])/2. for i in range(len(vec_dets["binVals"])-1)]+[vec_dets["binVals"][-1]]
                    nb[0] -= df/2.
                    nb[-1] += df/2.
                else:
                    nb = 1
        # else: vec_dets["typeId"] == 2: ### Categorical
        #     nb = [b-0.5 for b in numpy.unique(vec[idsan])]
        #     nb.append(nb[-1]+1)
        #     bins_ticks = numpy.unique(vec[idsan])
        #     bins_lbl = vec_dets["binLbls"]
        elif nb_distinct-1 < nb and len(set(numpy.diff(uniq))) == 1:
            nb = nb_distinct-1

        n, bins, patches = plt.hist(vec[idsan], bins=nb)
        
        sum_h = numpy.max(n)
        norm_h = [ni*fracts[0]*float(x1-x0)/sum_h+fracts[1]*float(x1-x0) for ni in n]
        if vec_dets["binLbls"] is not None:            
            bins_ticks = numpy.arange(len(vec_dets["binLbls"]))
            tmpb = [b-0.5 for b in bins_ticks]
            tmpb.append(tmpb[-1]+1)

            norm_bins_ticks = [(bi-tmpb[0])/float(tmpb[-1]-tmpb[0]) * hspan*float(y1-y0) + y0 + (.5-hspan/2.)*float(y1-y0) for bi in bins_ticks]
            norm_bins = [(bi-tmpb[0])/float(tmpb[-1]-tmpb[0]) * hspan*float(y1-y0) + y0 + (.5-hspan/2.)*float(y1-y0) for bi in tmpb]
            bins_lbl = vec_dets["binLbls"]
            colors = [mapper.to_rgba(i) for i in vec_dets["binVals"]]
        else:
            # norm_bins = [(bi-bins[0])/float(bins[-1]-bins[0]) * hspan*float(y1-y0) + y0  + (.5-hspan/2.)*float(y1-y0) for bi in bins]
            norm_bins = [(bi-bins[0])/float(bins[-1]-bins[0]) * hspan*float(y1-y0) + y0  + (.5-hspan/2.)*float(y1-y0) for bi in bins]            
            norm_bins_ticks = [(bi-bins[0])/float(bins[-1]-bins[0]) * hspan*float(y1-y0) + y0  + (.5-hspan/2.)*float(y1-y0) for bi in bins]
            bins_lbl = bins
            colors = [mapper.to_rgba(numpy.mean(bins[i:i+2])) for i in range(len(n))]
        # left = [norm_bins[i]+(norm_bins[i+1]-norm_bins[i])/2 for i in range(len(n))]
        left = [norm_bins[i] for i in range(len(n))]
        width = [norm_bins[i+1]-norm_bins[i] for i in range(len(n))]        
        
        bckc = "white" 
        axe.barh(y0, -((fracts[0]+fracts[1])*(x1-x0)+bx), y1-y0, x1+(fracts[0]+fracts[1])*(x1-x0)+2*bx, color=bckc, edgecolor=bckc, align="edge", zorder=self.zorder_sideplot)
        axe.barh(left, -numpy.array(norm_h), width, x1+(fracts[0]+fracts[1])*(x1-x0)+2*bx, color=colors, edgecolor=bckc, linewidth=2, align="edge", zorder=self.zorder_sideplot)
        axe.plot([x1+2*bx+fracts[0]*(x1-x0), x1+2*bx+fracts[0]*(x1-x0)], [norm_bins[0], norm_bins[-1]], color=bckc, linewidth=2, zorder=self.zorder_sideplot)
        x1 += (fracts[0]+fracts[1])*(x1-x0)+2*bx
        axe.set_yticks(norm_bins_ticks)        
        axe.set_yticklabels(bins_lbl, **self.view.getFontProps())
        # self.axe.yaxis.tick_right()
        axe.tick_params(direction="inout", left="off", right="on",
                            labelleft="off", labelright="on", labelsize=self.view.getFontSizeProp())
        return (x0, x1, y0, y1)
        
    def plotDotsSimple(self, axe, dots_draw, draw_indices, draw_settings):
        ku, kindices = numpy.unique(dots_draw["zord_dots"][draw_indices], return_inverse=True)
        for vi, vv in enumerate(ku):
            if vv != -1:
                axe.scatter(self.getCoords(0,draw_indices[kindices==vi]),
                            self.getCoords(1,draw_indices[kindices==vi]),
                            c=dots_draw["fc_dots"][draw_indices[kindices==vi],:],
                            edgecolors=dots_draw["ec_dots"][draw_indices[kindices==vi],:],
                            s=5*dots_draw["sz_dots"][draw_indices[kindices==vi]], marker=draw_settings["default"]["shape"],
                            zorder=vv)
                
    def plotDotsPoly(self, axe, dots_draw, draw_indices, draw_settings):
        for idp in draw_indices:
            vv = self.getPlotProp(idp, "zord")
            if vv != 1:
                self.drawEntity(idp, self.getPlotColor(idp, "fc"), self.getPlotColor(idp, "ec"),
                              self.getPlotProp(idp, "sz"), vv, draw_settings["default"])
                
    def drawEntity(self, idp, fc, ec, sz=1, zo=4, dsetts={}):
        ### SAMPLE ###
        if self.drawPoly():
            return [self.axe.add_patch(Polygon(self.getPltDtH().getCoordsP(idp), closed=True, fill=True, fc=fc, ec=ec, zorder=zo))]
        else:
            # print(idp, fc, ec)
            x, y = self.getCoordsXY(idp)
            # return self.axe.plot(x, y, mfc=fc, mec=ec, marker=dsetts["shape"], markersize=sz, linestyle='None', zorder=zo)
            return [self.axe.scatter([x], [y], c=fc, edgecolors=ec, s=5*sz, marker=dsetts["shape"], zorder=zo)]
            
    def getAnnXY(self):
        if self.ann_to_right:
            return self.ann_xy
        else:
            return (-1*self.ann_xy[0], self.ann_xy[1])
    def getAnnAlign(self):
        if self.ann_to_right:
            return "left"
        else:
            return "right"

    def getInfoDets(self):
        return self.info_dets
    
    def drawAnnotation(self, xy, ec, tag, xytext=None):
        if xytext is None:
            xytext = self.getAnnXY()
        bckgc = numpy.around(numpy.max((1-ec[0], 1-ec[1], 1-ec[2])))
        if len(ec) > 3 and ec[3] < 0.3:
            whitec = (bckgc, bckgc, bckgc, ec[3])
        else:
            ec = (ec[0], ec[1], ec[2])
            whitec = (bckgc, bckgc, bckgc)
        return [self.axe.annotate(tag, xy=xy, zorder=8,
                                xycoords='data', xytext=xytext, textcoords='offset points',
                                color=ec, va="center", backgroundcolor=whitec, ha=self.getAnnAlign(),
                                bbox=dict(boxstyle="round", facecolor=whitec, ec=ec),
                                arrowprops=dict(arrowstyle="wedge,tail_width=1.", fc=whitec, ec=ec,
                                                    patchA=None, patchB=self.getElement("ellipse"), relpos=(0.2, 0.5)),**self.view.getFontProps())]

