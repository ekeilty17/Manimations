from mpmath import mp, mpc, arg, cos, sin
mp.dps = 100  # Set number of decimal digits (you can raise this as needed)

class MobiusTransformation:

    ROUND_PRECISION = 50
    EPSILON = 0.00000000001

    def __init__(self, a, b, c, d, safe_evaluation=True):
        self.a = mpc(a)
        self.b = mpc(b)
        self.c = mpc(c)
        self.d = mpc(d)
        self.safe_evaluation = safe_evaluation
    
    def inverse(self):
        det = self.a * self.d - self.b * self.c
        if det == 0:
            raise Exception("This Mobius Transformation is not invertible.")
        return MobiusTransformation(self.d / det, -self.b / det, -self.c / det, self.a / det, safe_evaluation=self.safe_evaluation)

    def __call__(self, z):
        x, y = z.real, z.imag
        z_precise = mpc(x, y)

        if self.safe_evaluation:
            if self.c != 0 and round(abs(z_precise), self.ROUND_PRECISION) == round(abs(-self.d / self.c), self.ROUND_PRECISION):
                z_precise += self.EPSILON
        
        return (self.a * z_precise + self.b) / (self.c * z_precise + self.d)