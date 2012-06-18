package de.mypackage;

public class FailingProgram {

	public static void main(String[] args) {
		// run the thing
		MyClass myClass = new MyClass();
		myClass.getMin(4, null);
	}
}
