"""part3d generator

module to generat part3d 
"""


__all__ = ["Part3D"]

class Part3D:
    """create a part3d object"""
    def __init__(self):
        """startup class"""
        self.points = list()
        self.conn = list()
        
    def add_line(self, pos0, pos1, npts):
        """Add a line frop pos0 to pos1"""
        p_t = list(pos0)

        self.points.append(list(p_t))
        for i in range(0, npts-1):
            next_ptid = len(self.points)
            alpha = 1.*(i+1)/(npts-1)
            for j in range(3):
                p_t[j] = pos0[j] + (pos1[j]-pos0[j])*alpha
            
            self.points.append(list(p_t))
            self.conn.append([next_ptid-1, next_ptid])



