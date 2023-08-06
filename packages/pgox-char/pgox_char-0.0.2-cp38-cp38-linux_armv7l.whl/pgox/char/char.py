class char:
    def __init__(self):
        pass
    def db(self, *combo):
        self.combo = combo
    def setter(self):
        self.BU = []
        self.BL = []
        self.N = []
        self.S = []
        
        for i in range(65, 91):
            self.BU.append(chr(i))
        for i in range(97, 123):
            self.BL.append(chr(i))
        for i in range(48, 58):
            self.N.append(chr(i))
        for i in range(33, 48):
            self.S.append(chr(i))
        for i in range(58, 65):
            self.S.append(chr(i))
        for i in range(91, 97):
            self.S.append(chr(i))
        for i in range(122, 127):
            self.S.append(chr(i))
        
    def combi(self):
        self.con = []
        combos = len(self.combo)
        if combos == 1:
            if self.combo[0] == 'BL':
                self.con += self.BL
            elif self.combo[0] == 'BU':
                self.con += self.BU
            elif self.combo[0] == 'N':
                self.con += self.N
            elif self.combo[0] == 'S':
                self.con += self.S
        elif combos == 2:
            if self.combo[0] == 'BL':
                self.con += self.BL
                if self.combo[1] == 'BL':
                    self.con += self.BL
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                elif self.combo[1] == 'N':
                    self.con += self.N
                elif self.combo[1] == 'S':
                    self.con += self.S
            elif self.combo[0] == 'BU':
                self.con += self.BU
                if self.combo[1] == 'BL':
                    self.con += self.BL
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                elif self.combo[1] == 'N':
                    self.con += self.N
                elif self.combo[1] == 'S':
                    self.con += self.S
            elif self.combo[0] == 'N':
                self.con += self.N
                if self.combo[1] == 'BL':
                    self.con += self.BL
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                elif self.combo[1] == 'N':
                    self.con += self.N
                elif self.combo[1] == 'S':
                    self.con += self.S
            elif self.combo[0] == 'S':
                self.con += self.S
                if self.combo[1] == 'BL':
                    self.con += self.BL
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                elif self.combo[1] == 'N':
                    self.con +=self.N
                elif self.combo[1] == 'S':
                    self.con += self.S
        elif combos == 3:
            if self.combo[0] == 'BL':
                self.con += self.BL
                if self.combo[1] == 'BL':
                    self.con += self.BL
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'N':
                    self.con = self.N
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'S':
                    self.con += self.S
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
            elif self.combo[0] == 'BU':
                self.con += self.BU
                if self.combo[1] == 'BL':
                    self.con += self.BL
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                    self.con += self.BU
                elif self.combo[1] == 'N':
                    self.con += self.N
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'S':
                    self.con += self.S
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
            elif self.combo[0] == 'N':
                self.con += self.N
                if self.combo[1] == 'BL':
                    self.con += self.BL
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                    self.con += self.BU
                elif self.combo[1] == 'N':
                    self.con += self.N
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'S':
                    self.con += self.S
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
            elif self.combo[0] == 'S':
                self.con += self.S
                if self.combo[1] == 'BL':
                    self.con += self.BL
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'N':
                    self.con += self.N
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
                elif self.combo[1] == 'S':
                    self.con += self.S
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                    elif self.combo[2] == 'N':
                        self.con += self.N
                    elif self.combo[2] == 'S':
                        self.con += self.S
        elif combos == 4:
            if self.combo[0] == 'BL':
                self.con += self.BL
                if self.combo[1] == 'BL':
                    self.con += self.BL
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'N':
                    self.con += self.N
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'S':
                    self.con += self.S
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
            elif self.combo[0] == 'BU':
                self.con += self.BU
                if self.combo[1] == 'BL':
                    self.con += self.BL
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'N':
                    self.con += self.N
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'S':
                    self.con += self.S
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
            elif self.combo[0] == 'N':
                self.con += self.N
                if self.combo[1] == 'BL':
                    self.con += self.BL
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'N':
                    self.con += self.N
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'S':
                    self.con += self.S
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
            elif self.combo[0] == 'S':
                self.con += self.S
                if self.combo[1] == 'BL':
                    self.con += self.BL
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'BU':
                    self.con += self.BU
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'N':
                    self.con += self.N
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                elif self.combo[1] == 'S':
                    self.con += self.S
                    if self.combo[2] == 'BL':
                        self.con += self.BL
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'BU':
                        self.con += self.BU
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'N':
                        self.con += self.N
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
                    elif self.combo[2] == 'S':
                        self.con += self.S
                        if self.combo[3] == 'BL':
                            self.con += self.BL
                        elif self.combo[3] == 'BU':
                            self.con += self.BU
                        elif self.combo[3] == 'N':
                            self.con += self.N
                        elif self.combo[3] == 'S':
                            self.con += self.S
    def output(self):
        return self.con