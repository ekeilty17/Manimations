from mpmath import mp, mpc, arg, cos, sin
mp.dps = 100  # Set number of decimal digits (you can raise this as needed)

class MobiusTransformation:

    def __init__(self, a, b, c, d):
        self.a = mpc(a)
        self.b = mpc(b)
        self.c = mpc(c)
        self.d = mpc(d)
    
    def inverse(self):
        det = self.a * self.d - self.b * self.c
        if det == 0:
            raise Exception("This Mobius Transformation is not invertible.")
        return MobiusTransformation(self.d / det, -self.b / det, -self.c / det, self.a / det)

    def __call__(self, z):
        x, y = z.real, z.imag
        z_precise = mpc(x, y)

        if self.c != 0 and round(abs(z_precise), 10) == round(abs(-self.d / self.c), 10):
            # we just truncate the magnitude but maintain the angle
            mod = 1_000_000
            angle = arg(self.a * z_precise + self.b) - arg(self.c * z_precise + self.d)
            return mpc(mod * cos(angle), mod * sin(angle))
        
        return (self.a * z_precise + self.b) / (self.c * z_precise + self.d)