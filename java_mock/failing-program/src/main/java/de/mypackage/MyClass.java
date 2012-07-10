package de.mypackage;

public class MyClass {

	public int getMin(Integer x, Integer y) {
		doSomething();
		
		try {
			int c = potentialFailure(x, y);
		} catch (Exception e) {
			// oops, oh well.
		}
		
		if (x < y) {
			return x;
		}
		return y;
	}
	
	public void doSomething() {
		// this method is quite useless.
		int a = 1;
		while (a < 500) {
			a = 3*a;
			double b = a / 9.1d;
			a += b;
		}
	}
	
	public int potentialFailure(int a, int b) throws Exception {
		// just because I can
		if (a > b) {
			throw new Exception("So nicht!");
		} else
			return a+b;
	}
}
